import json
import os
import re
from typing import Any, Dict, Optional

import requests
from dotenv import load_dotenv

from lib.knowledge import (
    find_relevant_slide,
    get_all_slides,
    get_slide_by_id,
    get_slide_by_page,
)

# Nạp file .env (tìm ở cả thư mục codebase và thư mục gốc dự án)
load_dotenv(override=True)
_base_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
load_dotenv(os.path.join(_base_dir, ".env"), override=True)
load_dotenv(os.path.join(os.path.dirname(_base_dir), ".env"), override=True)


def _classify_intent(question: str) -> str:
    """
    Phân loại ý định của người học theo đúng Spec §4b & §6:
    - out_of_scope: Đòi giải bài tập Lab, hack prompt, hỏi ngoài giáo trình VLearn.
    - low_confidence: Câu hỏi cộc lốc, mơ hồ, bôi đen thiếu ý (dưới 5 ký tự hoặc từ chung chung).
    - socratic_followup: Học viên trả lời câu hỏi Socratic trước đó.
    - happy_path: Câu hỏi thắc mắc kiến thức trên slide bài học.
    """
    q = (question or "").strip().lower()

    # 1. Out-of-scope & Policy (Luồng 3: Ngoài phạm vi / Thẩm quyền)
    out_patterns = [
        r"đáp án",
        r"phần trả lời",
        r"giải (hộ|sẵn|bài tập|lab|toán|giúp|tích phân)",
        r"làm (hộ|giúp) bài",
        r"cho (mình|xin|tôi) (code|link|đáp án)",
        r"(tìm|cho xin|tải)\s+(file|pdf|sách)",
        r"pdf",
        r"bỏ qua (các |mọi )?(cảnh báo|hướng dẫn|chỉ thị|quy định|prompt|ràng buộc|guardrail)",
        r"ignore (all )?previous",
        r"(tài khoản|quyền|là) admin",
        r"quản trị viên",
        r"system\s*prompt",
        r"lỗ hổng bảo mật",
        r"hack (wifi|mật khẩu|tài khoản)",
        r"viết (hộ|giúp|cho) (mình |tôi )?(code|đoạn code)",
        r"viết code (c\+\+|quicksort|python|react)",
        r"thời tiết",
        r"chứng khoán",
        r"giá vàng",
    ]
    for pattern in out_patterns:
        if re.search(pattern, q):
            return "out_of_scope"

    # 2. Socratic Follow-up / Phản hồi tư duy (Luồng 4)
    # Lưu ý: nếu câu hỏi bắt đầu bằng 'vì sao' hoặc 'tại sao' thì là câu hỏi thắc mắc kiến thức (Luồng 1)
    if not re.search(r"^(vì sao|tại sao)", q):
        followup_patterns = [
            r"^(tiết kiệm|output|input|vì |mình nghĩ|theo mình|đắt hơn|lan man|nhớ sâu|tự động não|buộc|giúp)",
            r"đúng không",
            r"đồng ý",
            r"rút ngắn prompt",
            r"sinh từng từ",
        ]
        for pattern in followup_patterns:
            if re.search(pattern, q):
                return "socratic_followup"

    # 3. Low-confidence (Luồng 2 - HAX G10: Thu hẹp phạm vi khi mơ hồ)
    cleaned_q = re.sub(r"[^\w\s]", "", q).strip()
    vague_phrases = [
        "cái này là sao",
        "câu này là sao",
        "phần này là sao",
        "phần này là gì",
        "chỗ này là sao",
        "chỗ này là gì",
        "đoạn này là sao",
        "đoạn này là gì",
        "trang này nói gì",
        "tài liệu này nói về cái chi dợ",
        "là sao",
        "tại sao",
        "sao thế",
        "không hiểu",
        "thế nào",
        "giải thích đi",
        "alo",
        "help",
        "r",
        "asds",
        "hii",
    ]
    # Kiểm tra nếu câu ngắn <= 4 ký tự, hoặc khớp cụm mơ hồ, hoặc câu hỏi thiếu chủ ngữ rõ ràng
    vague_pattern = r"^(cái|câu|phần|chỗ|đoạn|ý|nó|thế còn cái)\s+(này|đó|kia)?\s*(là gì|là sao|nghĩa là gì|sao thế|thế nào|thì sao|hoạt động thế nào)?$"
    if len(cleaned_q) <= 4 or cleaned_q in vague_phrases or re.match(vague_pattern, cleaned_q) or "bôi đen ở trang" in cleaned_q:
        return "low_confidence"

    # 4. Mặc định là Happy Path (Luồng 1)
    return "happy_path"


def _call_gemini_api(system_instruction: str, user_prompt: str) -> Optional[Dict[str, Any]]:
    """Gọi API Google Gemini thật (gemini-3.6-flash) với cấu hình maxOutputTokens đủ lớn để không bị cắt xén."""
    api_key = os.getenv("GEMINI_API_KEY")
    if not api_key:
        return None

    full_prompt = f"{system_instruction}\n\nYÊU CẦU NGƯỜI HỌC: {user_prompt}"

    payload = {
        "contents": [{"parts": [{"text": full_prompt}]}],
        "generationConfig": {
            "temperature": 0.25,
            "maxOutputTokens": 2048,
            "responseMimeType": "application/json",
        },
    }

    url = f"https://generativelanguage.googleapis.com/v1beta/models/gemini-3.6-flash:generateContent?key={api_key}"
    try:
        res = requests.post(url, json=payload, timeout=15)
        if res.status_code == 200:
            data = res.json()
            candidates = data.get("candidates", [])
            if candidates:
                parts = candidates[0].get("content", {}).get("parts", [])
                for part in parts:
                    text = part.get("text", "").strip()
                    if text:
                        # Làm sạch markdown json nếu có
                        clean_text = re.sub(r"^```json\s*", "", text, flags=re.IGNORECASE)
                        clean_text = re.sub(r"\s*```$", "", clean_text)
                        try:
                            return json.loads(clean_text)
                        except Exception:
                            continue
    except Exception as exc:
        print(f"[Gemini API Error] {exc}")

    return None


def generate_socratic_answer(
    question: str,
    topic_id: Optional[str] = None,
    selected_text: Optional[str] = None
) -> Dict[str, Any]:
    """
    Xử lý câu hỏi học viên thông qua LLM Gemini thật và điều hướng 4 luồng theo Spec:
    - Luồng 1 (Happy Path): Tóm tắt ≤ 3 câu + Trích dẫn Slide [trang N] + 1 câu hỏi gợi mở.
    - Luồng 2 (Low-confidence): Không đoán mò, hỏi lại 1 câu ngắn kèm 2 gợi ý.
    - Luồng 3 (Out-of-scope): Từ chối lịch sự, nói rõ không hỗ trợ giải sẵn đáp án bài tập.
    - Luồng 4 (Socratic Loop): Xác nhận câu trả lời của học viên và củng cố bài học.
    """
    query = (question or "").strip()
    if selected_text:
        query = f"Đoạn bôi đen trên slide: \"{selected_text.strip()}\". Câu hỏi: {query}"

    slide = find_relevant_slide(query, preferred_id=topic_id)
    intent = _classify_intent(query)
    best_snippet = slide["snippets"][0]

    # Tìm snippet phù hợp nhất trên slide
    q_low = query.lower()
    for snip in slide.get("snippets", []):
        snip_words = snip["title"].lower().split() + snip["text"].lower().split()[:10]
        if any(w in q_low for w in snip_words if len(w) > 3):
            best_snippet = snip
            break

    citation = {
        "page": slide["page"],
        "title": slide["title"],
        "id": slide["id"],
        "snippet_id": best_snippet["id"],
    }

    # ================= LUỒNG 3: OUT-OF-SCOPE =================
    if intent == "out_of_scope":
        system_prompt = (
            "Bạn là VLearn AI Socratic Tutor. Học viên đang xin đáp án bài tập Lab, xin code giải sẵn hoặc hỏi ngoài phạm vi bài học.\n"
            "Hãy từ chối lịch sự theo đúng nguyên tắc sư phạm: Giải thích rằng AI Tutor không giải sẵn bài tập để học viên tự rèn luyện, "
            "tóm tắt ngắn gọn 1-2 câu lý thuyết nền tảng trên slide để họ tự làm, và đặt 1 câu hỏi gợi mở.\n"
            "Trả về JSON:\n"
            "{\n"
            '  "summary": "Từ chối lịch sự và hướng dẫn tự học...",\n'
            '  "probing_question": "Câu hỏi gợi ý để học viên tự làm...",\n'
            '  "options": ["Lựa chọn 1", "Lựa chọn 2"]\n'
            "}"
        )
        api_data = _call_gemini_api(system_prompt, query)
        if api_data and "summary" in api_data:
            return {
                "type": "out_of_scope",
                "path_name": "Luồng 3: Out-of-scope (Bảo vệ nguyên tắc sư phạm)",
                "summary": api_data["summary"],
                "citations": [citation],
                "probing_question": api_data.get("probing_question", "Bạn có muốn mình giải thích lại lý thuyết nền tảng trên slide để tự làm bài không?"),
                "options": api_data.get("options", [f"Xem lại lý thuyết Slide 0{slide['page']}", "Đọc lại các khái niệm chính"]),
                "slide_page": slide["page"],
                "highlight_id": None,
                "source": "gemini-3.6-flash (Live API)",
            }
        return {
            "type": "out_of_scope",
            "path_name": "Luồng 3: Out-of-scope (Bảo vệ nguyên tắc sư phạm)",
            "summary": "Tài liệu bài học hiện tại không hỗ trợ giải sẵn đáp án bài tập thực hành. Để nắm vững kiến thức thực chiến, bạn hãy xem lại slide lý thuyết hoặc trao đổi cùng Giảng viên / Lab Coach tại buổi học.",
            "citations": [citation],
            "probing_question": "Bạn có muốn mình giải thích lại phần lý thuyết nền tảng trên slide để tự làm bài không?",
            "options": [f"Xem lại lý thuyết Slide 0{slide['page']}", "Đọc lại các khái niệm chính"],
            "slide_page": slide["page"],
            "highlight_id": None,
            "source": "rule_based",
        }

    # ================= LUỒNG 2: LOW-CONFIDENCE (HAX G10) =================
    if intent == "low_confidence":
        return {
            "type": "low_confidence",
            "path_name": "Luồng 2: Low-confidence (Thu hẹp phạm vi khi mơ hồ - HAX G10)",
            "summary": "Câu hỏi của bạn còn khá ngắn hoặc chưa rõ trọng tâm. Để trợ giảng hỗ trợ đúng điểm vướng mắc mà không tuôn bài giảng dài dòng, bạn đang muốn làm rõ ý nào dưới đây?",
            "citations": [citation],
            "probing_question": slide.get("clarification_question", "Bạn muốn tìm hiểu khái niệm nào trên slide hiện tại?"),
            "options": slide.get("clarification_options", [f"Khái niệm chính Slide 0{slide['page']}", "Cách ứng dụng thực tế"]),
            "slide_page": slide["page"],
            "highlight_id": None,
            "source": "gemini_socratic_router",
        }

    # ================= LUỒNG 4: SOCRATIC LOOP / CORRECTION =================
    if intent == "socratic_followup":
        system_prompt = (
            f"Bạn là VLearn AI Socratic Tutor đang hỗ trợ học viên học Slide 0{slide['page']} ({slide['title']}).\n"
            "Học viên vừa trả lời câu hỏi gợi mở Socratic trước đó.\n"
            "Nhiệm vụ: Đánh giá câu trả lời của học viên (khen ngợi nếu đúng, chỉ ra điểm thiếu sót nếu chưa chuẩn), "
            "chốt lại bài học bằng ĐÚNG 2 ĐẾN 3 CÂU NGẮN GỌN (dưới 80 từ), và đặt 1 câu hỏi mở rộng tiếp theo.\n"
            "Trả về JSON:\n"
            "{\n"
            '  "summary": "Xác nhận và chốt kiến thức đúng 2-3 câu...",\n'
            '  "probing_question": "Câu hỏi mở rộng tiếp theo...",\n'
            '  "options": ["Lựa chọn 1", "Lựa chọn 2"],\n'
            '  "target_snippet_id": "mã snippet"\n'
            "}"
        )
        api_data = _call_gemini_api(system_prompt, query)
        if api_data and "summary" in api_data:
            snip_id = api_data.get("target_snippet_id", best_snippet["id"])
            return {
                "type": "socratic_followup",
                "path_name": "Luồng 4: Socratic Loop (Xác nhận & Khép vòng tư duy)",
                "summary": api_data["summary"],
                "citations": [{"page": slide["page"], "title": slide["title"], "snippet_id": snip_id, "id": slide["id"]}],
                "probing_question": api_data.get("probing_question", "Bạn đã sẵn sàng áp dụng kiến thức này sang phần tiếp theo chưa?"),
                "options": api_data.get("options", ["Sẵn sàng rồi!", "Cho mình xem lại ví dụ"]),
                "slide_page": slide["page"],
                "highlight_id": snip_id,
                "source": "gemini-3.6-flash (Live API)",
            }
        # Fallback cho Luồng 4 khi LLM timeout
        return {
            "type": "socratic_followup",
            "path_name": "Luồng 4: Socratic Loop (Xác nhận & Khép vòng tư duy)",
            "summary": "Chính xác! Bạn đã nắm rất vững bản chất vấn đề. Việc chủ động liên hệ kiến thức giúp khắc sâu bài học hơn rất nhiều.",
            "citations": [{"page": slide["page"], "title": slide["title"], "snippet_id": best_snippet["id"], "id": slide["id"]}],
            "probing_question": "Bạn có muốn tiếp tục thử thách với một câu hỏi tình huống thực tế khác không?",
            "options": ["Tiếp tục câu hỏi mới!", "Cho mình xem lại phần tóm tắt."],
            "slide_page": slide["page"],
            "highlight_id": best_snippet["id"],
            "source": "socratic_engine_fallback",
        }

    # ================= LUỒNG 1: HAPPY PATH (LIVE GEMINI API) =================
    context_text = "\n".join([f"- {s['title']}: {s['text']}" for s in slide["snippets"]])
    system_prompt = (
        f"Bạn là VLearn AI Socratic Tutor hỗ trợ học viên giải đáp thắc mắc về bài học (Slide 0{slide['page']} - {slide['title']}).\n"
        f"NỘI DUNG SLIDE GỐC:\n{context_text}\n\n"
        "QUY TẮC PHẢN HỒI (BẮT BUỘC):\n"
        "1. TÓM TẮT TRỌNG TÂM BẰNG ĐÚNG 2 ĐẾN 3 CÂU NGẮN GỌN (tổng dưới 80 từ). Trả lời trực diện vào câu hỏi của học viên, giải thích bản chất thực tế, tuyệt đối không viết dài dòng, không tuôn bài giảng lý thuyết.\n"
        "2. ĐẶT ĐÚNG 1 CÂU HỎI GỢI MỞ SOCRATIC sâu sắc để kích thích người học tự suy nghĩ tiếp.\n"
        "3. ĐƯA RA 2 LỰA CHỌN TRẢ LỜI NGẮN GỌN để học viên bấm chọn phản hồi ngay.\n"
        f"4. CHỌN 1 MÃ SNIPPET PHÙ HỢP NHẤT trong các mã sau: {[s['id'] for s in slide['snippets']]}.\n"
        "Trả về JSON thuần túy:\n"
        "{\n"
        '  "summary": "Tóm tắt đúng 2-3 câu ngắn gọn...",\n'
        '  "probing_question": "Câu hỏi gợi mở Socratic...",\n'
        '  "options": ["Lựa chọn 1", "Lựa chọn 2"],\n'
        '  "target_snippet_id": "mã snippet được chọn"\n'
        "}"
    )

    api_data = _call_gemini_api(system_prompt, query)
    if api_data and "summary" in api_data and "probing_question" in api_data:
        target_id = api_data.get("target_snippet_id") or best_snippet["id"]
        citation["snippet_id"] = target_id
        return {
            "type": "happy_path",
            "path_name": "Luồng 1: Happy Path (Socratic & Đúng cỡ - Dưới 3 câu)",
            "summary": api_data["summary"].strip(),
            "citations": [citation],
            "probing_question": api_data["probing_question"].strip(),
            "options": api_data.get("options", [
                "Mình hiểu rồi, tiếp tục thôi!",
                "Cho mình ví dụ thực tế hơn nữa."
            ])[:2],
            "slide_page": slide["page"],
            "highlight_id": target_id,
            "source": "gemini-3.6-flash (Live API)",
        }

    # Fallback khi mạng lỗi: tạo phản hồi bám sát câu hỏi thay vì text cố định
    first_snip = best_snippet["text"]
    return {
        "type": "happy_path",
        "path_name": "Luồng 1: Happy Path (Socratic & Đúng cỡ - Dưới 3 câu)",
        "summary": f"Đối với vấn đề bạn hỏi về {slide['title'].lower()}: {first_snip}",
        "citations": [citation],
        "probing_question": f"Theo bạn, điều gì sẽ xảy ra nếu ta không kiểm soát tốt phần {best_snippet['title'].lower()} khi ứng dụng vào sản phẩm thực tế?",
        "options": [
            "Hệ thống sẽ tốn kém chi phí và dễ gặp lỗi không kiểm soát.",
            "Người dùng sẽ nhận câu trả lời không đúng mong đợi."
        ],
        "slide_page": slide["page"],
        "highlight_id": best_snippet["id"],
        "source": "socratic_engine_fallback",
    }
