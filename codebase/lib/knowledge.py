"""
Kho tri thức bài giảng VLearn phục vụ Socratic AI Tutor.
Bao gồm các slide cốt lõi của khóa học AI Thực chiến (Day 1 / Day 2).
Mỗi slide gồm các đoạn snippet có định danh độc nhất để hỗ trợ đối chiếu nguồn và highlight (HAX G2).
"""

from typing import Any, Dict, List, Optional

SLIDES: List[Dict[str, Any]] = [
    {
        "id": "token-chi-phi",
        "page": 5,
        "title": "Token & Chi phí API",
        "subtitle": "Hiểu đơn vị đo lường và cơ chế tính giá trong LLM",
        "keywords": ["token", "chi phí", "giá", "api", "tính tiền", "tiền", "chi phi", "đầu vào", "đầu ra", "input", "output", "tối ưu"],
        "snippets": [
            {
                "id": "s5-def",
                "title": "1. Khái niệm Token",
                "text": "Token là đơn vị cơ bản mà mô hình ngôn ngữ (LLM) dùng để xử lý văn bản. Một token không tương đương chính xác 1 từ (1 token ≈ 0.75 từ tiếng Anh, với tiếng Việt có thể là 1 đến 2 token cho mỗi từ do dấu thanh).",
                "badge": "Định nghĩa"
            },
            {
                "id": "s5-calc",
                "title": "2. Cơ chế tính phí API",
                "text": "Chi phí gọi API được tính theo công thức: Tổng chi phí = (Token Input × Đơn giá Input) + (Token Output × Đơn giá Output). Token Output thường có giá đắt hơn gấp 3 đến 4 lần so với Token Input.",
                "formula": "Tổng chi phí = (Token In × Giá In) + (Token Out × Giá Out)",
                "badge": "Công thức tính"
            },
            {
                "id": "s5-opt",
                "title": "3. Nguyên tắc tối ưu",
                "text": "Prompt càng dài và phản hồi càng lan man thì số token tiêu thụ càng lớn. Rút gọn prompt và khống chế phản hồi đúng trọng tâm giúp giảm từ 40% - 60% chi phí vận hành hệ thống mà vẫn giữ nguyên chất lượng thông tin.",
                "badge": "Thực hành"
            }
        ],
        "clarification_question": "Bạn đang muốn làm rõ khái niệm Token là gì, hay cách tính Chi phí API theo số lượng token?",
        "clarification_options": [
            "Khái niệm Token là gì?",
            "Cách tính Chi phí API từ Token?"
        ]
    },
    {
        "id": "prompt-engineering",
        "page": 6,
        "title": "Prompt Engineering căn bản",
        "subtitle": "Kỹ thuật giao tiếp chính xác với mô hình ngôn ngữ",
        "keywords": ["prompt", "engineering", "cấu trúc", "hướng dẫn", "ngữ cảnh", "vai trò", "định dạng", "few-shot"],
        "snippets": [
            {
                "id": "s6-struct",
                "title": "1. Khung cấu trúc 4 phần",
                "text": "Một prompt chuẩn gồm 4 thành phần: Vai trò (Role) - Ngữ cảnh (Context) - Nhiệm vụ (Instruction) - Định dạng đầu ra (Output Format).",
                "badge": "Khung chuẩn"
            },
            {
                "id": "s6-concise",
                "title": "2. Nguyên tắc Tinh gọn",
                "text": "Prompt dài không đồng nghĩa với prompt tốt. Loại bỏ các từ ngữ thừa thãi, tập trung vào ràng buộc rõ ràng giúp mô hình bám sát yêu cầu và giảm ảo giác.",
                "badge": "Nguyên tắc"
            },
            {
                "id": "s6-fewshot",
                "title": "3. Kỹ thuật Few-shot Prompting",
                "text": "Cung cấp từ 1 đến 2 ví dụ mẫu (input - output) trong prompt giúp mô hình hiểu chính xác định dạng mong muốn mà không cần giải thích dài dòng.",
                "badge": "Kỹ thuật"
            }
        ],
        "clarification_question": "Bạn muốn tìm hiểu về cấu trúc của một prompt chuẩn, hay kỹ thuật Few-shot prompting?",
        "clarification_options": [
            "Cấu trúc 4 phần của Prompt?",
            "Kỹ thuật Few-shot Prompting?"
        ]
    },
    {
        "id": "socratic-learning",
        "page": 9,
        "title": "Phương pháp Socratic trong AI Tutor",
        "subtitle": "Chuyển từ độc thoại lý thuyết sang đối thoại gợi mở",
        "keywords": ["socratic", "gợi mở", "tư duy", "chủ động", "hỏi", "gia sư", "tutor", "ngợp chữ"],
        "snippets": [
            {
                "id": "s9-core",
                "title": "1. Triết lý Socratic",
                "text": "Thay vì đưa ngay bài giảng dài dòng, người dạy đặt câu hỏi dẫn dắt để người học tự kết nối tri thức và tìm ra bản chất vấn đề.",
                "badge": "Triết lý"
            },
            {
                "id": "s9-rule",
                "title": "2. Quy tắc phản hồi đúng cỡ",
                "text": "Phản hồi của AI Tutor cần ngắn gọn (≤ 3 câu), có trích dẫn nguồn cụ thể [trang N], và luôn kết thúc bằng 1 câu hỏi thăm dò mức hiểu.",
                "badge": "Quy tắc 3 câu"
            },
            {
                "id": "s9-loop",
                "title": "3. Vòng lặp học tập chủ động",
                "text": "Học viên đọc nhanh trong 15 giây, kiểm chứng nguồn tài liệu gốc, rồi trả lời câu hỏi gợi mở để khắc sâu bài học mà không bị quá tải nhận thức.",
                "badge": "Vòng lặp tương tác"
            }
        ],
        "clarification_question": "Bạn muốn tìm hiểu về lợi ích phương pháp Socratic hay quy tắc phản hồi ≤ 3 câu của AI Tutor?",
        "clarification_options": [
            "Lợi ích phương pháp Socratic?",
            "Quy tắc phản hồi ≤ 3 câu?"
        ]
    },
    {
        "id": "rag-knowledge",
        "page": 11,
        "title": "RAG & Nguồn sự thật",
        "subtitle": "Hạn chế ảo giác (Hallucination) bằng tri thức bài giảng",
        "keywords": ["rag", "tri thức", "nguồn", "retrieval", "hallucination", "ảo giác", "bài giảng", "chân lý"],
        "snippets": [
            {
                "id": "s11-rag",
                "title": "1. Cơ chế RAG",
                "text": "Retrieval-Augmented Generation kết hợp tìm kiếm dữ liệu thực tế từ bài giảng trước khi đưa vào ngữ cảnh để AI tổng hợp phản hồi.",
                "badge": "Cơ chế"
            },
            {
                "id": "s11-cite",
                "title": "2. Tính minh bạch & Trích dẫn",
                "text": "Mỗi phát biểu của AI đều phải gắn kèm số trang slide gốc để người học có thể kiểm chứng ngay lập tức, ngăn ngừa sai lệch kiến thức.",
                "badge": "Minh bạch"
            },
            {
                "id": "s11-hallucination",
                "title": "3. Kiểm soát Hallucination",
                "text": "Khi câu hỏi vượt ngoài phạm vi tài liệu đã học, hệ thống an toàn phải từ chối lịch sự thay vì tự suy diễn và bịa đặt thông tin sai lệch.",
                "badge": "An toàn"
            }
        ],
        "clarification_question": "Bạn muốn tìm hiểu RAG ngăn ảo giác như thế nào, hay cơ chế trích dẫn nguồn gốc?",
        "clarification_options": [
            "RAG ngăn ảo giác thế nào?",
            "Cách gắn trích dẫn nguồn?"
        ]
    }
]


def get_all_slides() -> List[Dict[str, Any]]:
    """Trả về danh sách tất cả slide bài giảng."""
    return SLIDES


def get_slide_by_id(slide_id: str) -> Optional[Dict[str, Any]]:
    """Tìm slide theo ID."""
    for s in SLIDES:
        if s["id"] == slide_id:
            return s
    return None


def get_slide_by_page(page: int) -> Optional[Dict[str, Any]]:
    """Tìm slide theo số trang."""
    for s in SLIDES:
        if s["page"] == page:
            return s
    return None


def find_relevant_slide(query: str, preferred_id: Optional[str] = None) -> Dict[str, Any]:
    """Tìm slide phù hợp nhất với câu hỏi học viên."""
    if preferred_id:
        slide = get_slide_by_id(preferred_id)
        if slide:
            return slide

    q = (query or "").lower()
    best_slide = SLIDES[0]
    max_score = -1

    for s in SLIDES:
        score = 0
        for kw in s["keywords"]:
            if kw.lower() in q:
                score += 2
        if s["title"].lower() in q:
            score += 4
        if score > max_score:
            max_score = score
            best_slide = s

    return best_slide
