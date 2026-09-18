# Bộ Test Cases: Luồng 1 — Happy Path (Socratic & Đúng cỡ)
**Dự án:** VLearn AI Socratic Tutor (Track A1)  
**Nhóm:** Tứ Đại Bổ Túc (K4-3B-E402)  
**Tác giả phần việc:** Đức Anh  
**Mục tiêu:** Kiểm thử năng lực xử lý nhánh **Luồng 1: Happy Path (Socratic & Đúng cỡ)** theo đúng quy định tại Sơ đồ luồng hoạt động (§4) và Bốn đường đi trải nghiệm (§6) trong `spec.md`.

---

## 1. Cơ chế Luồng 1 trong Workflow

Theo đặc tả hệ thống tại `spec.md`:
- **Điều kiện kích hoạt tại khối Decision:**
  - Câu hỏi học viên rõ ràng, có căn cứ đầy đủ trong các trang slide bài giảng hiện hành (Slide 03, Slide 05, Slide 06, Slide 09, Slide 11).
- **Hành vi bắt buộc của AI:**
  - **Khối HP1 (Tóm tắt trọng tâm $\le 3$ câu):** Trả lời trực diện, súc tích (tổng dưới 80 từ), tuyệt đối không tuôn bài giảng dài dòng gây quá tải nhận thức.
  - **Khối HP2 (Gắn thẻ trích dẫn nguồn):** Bắt buộc kèm badge `[trang N]` để khi click vào sẽ tự động highlight đoạn tài liệu gốc trên Slide Viewer bên trái.
  - **Khối HP3 (Tạo 1 câu hỏi gợi mở Socratic):** Luôn kết thúc bằng 1 câu hỏi dẫn dắt và 2 nút lựa chọn nhanh để học viên tiếp tục suy nghĩ và tương tác chủ động.
  - **Khối UserView1 & Loop:** Học viên đọc nhanh trong 15 giây, kiểm chứng nguồn tài liệu gốc, rồi chủ động tương tác tiếp.

---

## 2. Tiêu chí Đánh giá (Pass / Fail Criteria)

Mỗi test case của Luồng 1 được đánh giá theo 3 tiêu chí kiểm chứng được:

1. **Đúng cỡ & Trọng tâm (Conciseness - HP1):** Phản hồi tối đa 3 câu ngắn gọn, giải thích đúng bản chất kỹ thuật. *(Fail nếu: dài quá 4 câu hoặc tuôn bài giảng lý thuyết lan man)*.
2. **Minh bạch nguồn (Factuality & Citation - HP2):** Bắt buộc có trích dẫn `[trang N]` chính xác với bài giảng. *(Fail nếu: không trích dẫn trang hoặc cite sai số trang)*.
3. **Đối thoại gợi mở (Socratic Probing - HP3):** Bắt buộc có câu hỏi gợi mở và ít nhất 2 options gợi ý nhanh. *(Fail nếu: chỉ trả lời cụt lủn không gợi mở tiếp)*.

---

## 3. Danh sách Test Cases Luồng 1 (Trích xuất từ Chatlog thật)

### Case L1-01: Mối quan hệ giữa Token và Chi phí API
- **Mã nguồn chatlog:** `T00123` (K3, Trang 3)
- **Input của học viên:**
  > *(Slide 05: Token & Chi phí API)*  
  > *"Tại sao số lượng token lại ảnh hưởng đến chi phí API?"*
- **Phân loại:** Happy Path — Kiến thức trọng tâm
- **Hành vi mong đợi:**
  - **HP1:** Tóm tắt $\le 3$ câu giải thích giá tính trên tổng Token In và Token Out.
  - **HP2:** Gắn nhãn `[trang 5]`.
  - **HP3:** Đặt câu hỏi Socratic về lý do Token Output lại đắt hơn Token Input.
- **Tiêu chuẩn Pass:** Tóm tắt $\le 3$ câu, cite `[trang 5]`, có câu hỏi gợi mở.
- **Tiêu chuẩn Fail:** Dài dòng trên 4 câu, không có trích dẫn trang.

---

### Case L1-02: Khái niệm Token và quy tắc Token tiếng Việt
- **Mã nguồn chatlog:** `T00092` (K3, Trang 26)
- **Input của học viên:**
  > *(Slide 05, đoạn bôi đen: Khái niệm Token)*  
  > *"Token là gì và 1 từ tiếng Việt thì bằng bao nhiêu token?"*
- **Phân loại:** Happy Path — Khái niệm cốt lõi & Domain
- **Hành vi mong đợi:**
  - **HP1:** Giải thích 1 token không tương đương 1 từ; tiếng Việt mất 1-2 token/từ do dấu thanh.
  - **HP2:** Gắn nhãn `[trang 5]`.
  - **HP3:** Đặt câu hỏi gợi mở về tác động của độ dài câu chữ tiếng Việt tới chi phí.
- **Tiêu chuẩn Pass:** Nêu đúng quy tắc token tiếng Việt, có trích dẫn trang 5.
- **Tiêu chuẩn Fail:** Khẳng định sai 1 từ = 1 token hoặc không dẫn nguồn.

---

### Case L1-03: Cấu trúc 4 phần của một Prompt chuẩn
- **Mã nguồn chatlog:** `T00119` (K3, Trang 27)
- **Input của học viên:**
  > *(Slide 06: Prompt Engineering căn bản)*  
  > *"Một prompt chuẩn gồm những thành phần nào?"*
- **Phân loại:** Happy Path — Cấu trúc kỹ thuật
- **Hành vi mong đợi:**
  - **HP1:** Tóm tắt đủ 4 thành phần: Role - Context - Instruction - Output Format trong 2-3 câu.
  - **HP2:** Gắn nhãn `[trang 6]`.
  - **HP3:** Hỏi xem thành phần nào học viên thường hay bỏ sót nhất khi viết prompt.
- **Tiêu chuẩn Pass:** Nêu đúng 4 thành phần, cite `[trang 6]`.
- **Tiêu chuẩn Fail:** Kể thiếu thành phần hoặc dài dòng quá 80 từ.

---

### Case L1-04: Triết lý Socratic giúp người học tránh ngợp chữ
- **Mã nguồn chatlog:** `T00007` (K3, Trang 5)
- **Input của học viên:**
  > *(Slide 09: Phương pháp Socratic trong AI Tutor)*  
  > *"Phương pháp Socratic giúp người học tránh ngợp chữ như thế nào?"*
- **Phân loại:** Happy Path — Phương pháp Socratic
- **Hành vi mong đợi:**
  - **HP1:** Nêu rõ AI thay bài giảng dài bằng tóm tắt $\le 3$ câu và câu hỏi dẫn dắt từng bước.
  - **HP2:** Gắn nhãn `[trang 9]`.
  - **HP3:** Hỏi học viên đánh giá sự khác biệt giữa tự suy nghĩ và đọc thụ động.
- **Tiêu chuẩn Pass:** Đúng bản chất phương pháp, cite `[trang 9]`, phong cách đối thoại.
- **Tiêu chuẩn Fail:** Viết một bài giảng dài dòng mâu thuẫn với chính triết lý tóm tắt.

---

### Case L1-05: Kỹ thuật Few-shot Prompting
- **Mã nguồn chatlog:** `T00030` (K3, Trang 3)
- **Input của học viên:**
  > *(Slide 06: Prompt Engineering căn bản)*  
  > *"Few-shot prompting là gì và khi nào nên dùng?"*
- **Phân loại:** Happy Path — Kỹ thuật nâng cao
- **Hành vi mong đợi:**
  - **HP1:** Giải thích việc cung cấp 1-2 ví dụ mẫu để định hình format cho LLM.
  - **HP2:** Gắn nhãn `[trang 6]`.
  - **HP3:** Đặt câu hỏi về việc cân đối giữa chất lượng format và chi phí token mẫu.
- **Tiêu chuẩn Pass:** Tóm tắt chính xác trong $\le 3$ câu, cite `[trang 6]`.
- **Tiêu chuẩn Fail:** Giải thích sai lệch hoặc dài dòng trên 100 từ.

---

### Case L1-06: Lý do Token Output đắt hơn Token Input
- **Mã nguồn chatlog:** `T00106` (K3, Trang 38)
- **Input của học viên:**
  > *(Slide 05: Token & Chi phí API)*  
  > *"Vì sao token đầu ra (output) lại đắt hơn gấp 3 đến 4 lần token đầu vào?"*
- **Phân loại:** Happy Path — Cơ chế kỹ thuật sâu
- **Hành vi mong đợi:**
  - **HP1:** Giải thích chi phí GPU tính toán sinh token tuần tự (autoregressive) tốn tài nguyên hơn đọc song song.
  - **HP2:** Gắn nhãn `[trang 5]`.
  - **HP3:** Đặt câu hỏi về cách khống chế độ dài phản hồi để tối ưu ngân sách API.
- **Tiêu chuẩn Pass:** Trả lời đúng bản chất kỹ thuật, cite `[trang 5]`, có câu hỏi gợi mở.
- **Tiêu chuẩn Fail:** Không giải thích được hoặc bịa thông tin ngoài tài liệu.

---

## 4. Tóm tắt Ma trận Kiểm thử Luồng 1

| Case ID | Turn ID | Chủ đề kiểm thử | Trang Slide | Yêu cầu số câu | Yêu cầu Citation | Yêu cầu Socratic |
|:---:|:---:|:---|:---:|:---:|:---:|:---:|
| **L1-01** | `T00123` | Token & Chi phí API | Slide 05 | $\le 3$ câu | `[trang 5]` | 1 câu + 2 options |
| **L1-02** | `T00092` | Khái niệm Token tiếng Việt | Slide 05 | $\le 3$ câu | `[trang 5]` | 1 câu + 2 options |
| **L1-03** | `T00119` | Khung Prompt chuẩn 4 phần | Slide 06 | $\le 3$ câu | `[trang 6]` | 1 câu + 2 options |
| **L1-04** | `T00007` | Triết lý Socratic tránh ngợp chữ | Slide 09 | $\le 3$ câu | `[trang 9]` | 1 câu + 2 options |
| **L1-05** | `T00030` | Kỹ thuật Few-shot Prompting | Slide 06 | $\le 3$ câu | `[trang 6]` | 1 câu + 2 options |
| **L1-06** | `T00106` | Chi phí Token Output vs Input | Slide 05 | $\le 3$ câu | `[trang 5]` | 1 câu + 2 options |
