#!/usr/bin/env python3
"""
Script chạy kiểm thử tự động toàn diện cho VLearn AI Socratic Tutor.
Chạy toàn bộ bộ Golden Set (20 test cases) thuộc 4 luồng trải nghiệm:
- Luồng 1: Happy Path (Socratic & Đúng cỡ)
- Luồng 2: Low-confidence (Thu hẹp phạm vi - HAX G10)
- Luồng 3: Out-of-scope (Từ chối lịch sự - Bảo vệ nguyên tắc sư phạm)
- Luồng 4: Socratic Loop (Phản hồi & Đính chính ngộ nhận)

Kết quả đo lường và log chi tiết sẽ được tự động xuất ra:
- eval/eval_results.json (Bản ghi JSON đầy đủ để lưu vết và phân tích)
- eval/eval_report.md (Báo cáo Markdown bảng % pass/fail cho slide demo và spec §7)
"""

import datetime
import json
import os
import sys

# Đảm bảo import được codebase
CURRENT_DIR = os.path.dirname(os.path.abspath(__file__))
PROJECT_ROOT = os.path.dirname(CURRENT_DIR)
CODEBASE_DIR = os.path.join(PROJECT_ROOT, "codebase")
sys.path.insert(0, CODEBASE_DIR)

from lib.answer_builder import generate_socratic_answer


def evaluate_case(case: dict) -> dict:
    case_id = case["id"]
    flow_expected = case["flow"]
    user_q = case["input"]["student_question"]
    context = case["input"].get("context", "")

    # Thực thi qua AI Tutor
    res = generate_socratic_answer(user_q)
    actual_type = res.get("type")
    actual_source = res.get("source", "unknown")
    summary = res.get("summary", "")
    citations = res.get("citations", [])
    probing_question = res.get("probing_question", "")

    passed = True
    failure_reasons = []

    # 1. Kiểm tra luồng (Flow Route)
    if "Luồng 1" in flow_expected and actual_type != "happy_path":
        passed = False
        failure_reasons.append(f"Sai luồng: Mong đợi Happy Path nhưng ra '{actual_type}'")
    elif "Luồng 2" in flow_expected and actual_type != "low_confidence":
        passed = False
        failure_reasons.append(f"Sai luồng: Mong đợi Low-confidence nhưng ra '{actual_type}'")
    elif "Luồng 3" in flow_expected and actual_type != "out_of_scope":
        passed = False
        failure_reasons.append(f"Sai luồng: Mong đợi Out-of-scope nhưng ra '{actual_type}'")
    elif "Luồng 4" in flow_expected and actual_type != "socratic_followup":
        passed = False
        failure_reasons.append(f"Sai luồng: Mong đợi Socratic Loop nhưng ra '{actual_type}'")

    # 2. Kiểm tra quy tắc phản hồi cho Luồng 1
    if actual_type == "happy_path":
        # Không được dài quá 4 câu
        sentences = [s for s in summary.replace("?", ".").replace("!", ".").split(".") if len(s.strip()) > 5]
        if len(sentences) > 4:
            passed = False
            failure_reasons.append(f"Quá dài: {len(sentences)} câu (mong đợi <= 3 câu)")
        # Phải có trích dẫn trang
        if not citations or not citations[0].get("page"):
            passed = False
            failure_reasons.append("Thiếu thẻ trích dẫn trang slide [trang N]")
        # Phải có câu hỏi gợi mở Socratic
        if not probing_question:
            passed = False
            failure_reasons.append("Thiếu câu hỏi gợi mở Socratic")

    # 3. Kiểm tra Luồng 3: Tuyệt đối không cho chép bài / bịa link
    if actual_type == "out_of_scope":
        bad_words = ["đây là đáp án", "lời giải chi tiết", "http://", "https://"]
        for bw in bad_words:
            if bw in summary.lower():
                passed = False
                failure_reasons.append(f"Vi phạm nguyên tắc: Chứa từ cấm '{bw}'")

    return {
        "id": case_id,
        "turn_id": case.get("turn_id", ""),
        "flow": flow_expected,
        "input_question": user_q,
        "actual_type": actual_type,
        "passed": passed,
        "failure_reasons": failure_reasons,
        "source": actual_source,
        "summary": summary,
        "probing_question": probing_question,
        "citations": citations,
    }


def main():
    golden_file = os.path.join(CURRENT_DIR, "golden_set_20cases.json")
    if not os.path.exists(golden_file):
        print(f"[Error] Không tìm thấy file {golden_file}")
        return

    with open(golden_file, "r", encoding="utf-8") as f:
        cases = json.load(f)

    print(f"🚀 Bắt đầu chạy đo lường trên {len(cases)} test cases của Golden Set...")
    print("-" * 65)

    results = []
    flow_stats = {
        "Luồng 1 (Happy Path)": {"total": 0, "pass": 0},
        "Luồng 2 (Low-confidence)": {"total": 0, "pass": 0},
        "Luồng 3 (Out-of-scope)": {"total": 0, "pass": 0},
        "Luồng 4 (Socratic Loop)": {"total": 0, "pass": 0},
    }

    for idx, case in enumerate(cases, 1):
        r = evaluate_case(case)
        results.append(r)

        # Thống kê
        for flow_key in flow_stats.keys():
            if flow_key.split()[1] in r["flow"]:
                flow_stats[flow_key]["total"] += 1
                if r["passed"]:
                    flow_stats[flow_key]["pass"] += 1

        status_str = "✅ PASS" if r["passed"] else "❌ FAIL"
        print(f"[{idx:02d}/20] {r['id']} ({r.get('turn_id')}) | {r['flow'][:20]}... -> {status_str}")
        if not r["passed"]:
            for err in r["failure_reasons"]:
                print(f"       ⚠️ {err}")

    # Tính tổng quan
    total_cases = len(results)
    total_passed = sum(1 for r in results if r["passed"])
    pass_rate = (total_passed / total_cases) * 100

    print("-" * 65)
    print(f"📊 TỔNG KẾT: {total_passed}/{total_cases} passed ({pass_rate:.1f}%)")
    for f_name, stat in flow_stats.items():
        sub_rate = (stat["pass"] / stat["total"] * 100) if stat["total"] > 0 else 0
        print(f"   • {f_name}: {stat['pass']}/{stat['total']} ({sub_rate:.1f}%)")

    # Lưu log chi tiết JSON
    now = datetime.datetime.now()
    timestamp_str = now.strftime("%Y-%m-%d %H:%M:%S")
    file_timestamp = now.strftime("%Y%m%d_%H%M%S")

    log_data = {
        "timestamp": timestamp_str,
        "total_cases": total_cases,
        "total_passed": total_passed,
        "pass_rate_pct": round(pass_rate, 2),
        "flow_stats": flow_stats,
        "details": results,
    }

    # Đảm bảo thư mục history tồn tại
    history_dir = os.path.join(CURRENT_DIR, "history")
    os.makedirs(history_dir, exist_ok=True)

    # 1. File mới nhất (Latest)
    results_json_path = os.path.join(CURRENT_DIR, "eval_results.json")
    with open(results_json_path, "w", encoding="utf-8") as f:
        json.dump(log_data, f, ensure_ascii=False, indent=2)

    # 2. File lưu vết lịch sử (History Run)
    hist_json_path = os.path.join(history_dir, f"run_{file_timestamp}_{int(pass_rate)}pct.json")
    with open(hist_json_path, "w", encoding="utf-8") as f:
        json.dump(log_data, f, ensure_ascii=False, indent=2)

    # Báo cáo Markdown
    report_content = f"# Báo cáo Kết quả Đo lường Golden Set (20 Cases)\n\n"
    report_content += f"- **Thời điểm chạy:** {timestamp_str}\n"
    report_content += f"- **Tỷ lệ vượt qua (Quality Pass Rate):** **{total_passed}/{total_cases} ({pass_rate:.1f}%)**\n\n"
    report_content += f"## 1. Kết quả theo từng Luồng Trải Nghiệm\n\n"
    report_content += f"| Luồng hoạt động | Số case | Đạt (Pass) | Tỷ lệ (%) | Nhận xét chất lượng |\n"
    report_content += f"|---|:---:|:---:|:---:|---|\n"
    for f_name, stat in flow_stats.items():
        sub_rate = (stat["pass"] / stat["total"] * 100) if stat["total"] > 0 else 0
        note = "Đạt chuẩn" if sub_rate >= 80 else "Cần cải thiện prompt / regex"
        report_content += f"| **{f_name}** | {stat['total']} | {stat['pass']} | {sub_rate:.1f}% | {note} |\n"

    report_content += f"\n## 2. Chi tiết từng Ca Kiểm Thử (Log)\n\n"
    report_content += f"| Case ID | Turn ID | Câu hỏi học viên | Luồng mong đợi | Luồng thực tế | Trạng thái | Ghi chú lỗi |\n"
    report_content += f"|:---:|:---:|---|---|---|:---:|---|\n"
    for r in results:
        stat_icon = "✅ Pass" if r["passed"] else "❌ Fail"
        reason_str = "; ".join(r["failure_reasons"]) if r["failure_reasons"] else "—"
        q_short = r["input_question"].replace("\n", " ")[:45]
        report_content += f"| {r['id']} | {r['turn_id']} | `{q_short}` | {r['flow'].split(':')[0]} | `{r['actual_type']}` | {stat_icon} | {reason_str} |\n"

    # Lưu Markdown mới nhất và bản lưu lịch sử
    report_md_path = os.path.join(CURRENT_DIR, "eval_report.md")
    with open(report_md_path, "w", encoding="utf-8") as f:
        f.write(report_content)

    hist_md_path = os.path.join(history_dir, f"run_{file_timestamp}_{int(pass_rate)}pct.md")
    with open(hist_md_path, "w", encoding="utf-8") as f:
        f.write(report_content)

    print(f"\n✅ Đã lưu kết quả tại:")
    print(f"   - Mới nhất: {results_json_path}")
    print(f"   - Lịch sử:  {hist_json_path}")


if __name__ == "__main__":
    main()
