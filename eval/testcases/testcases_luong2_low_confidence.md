# Bộ Test Cases: Luồng 2 — Low-confidence (Thu hẹp phạm vi khi mơ hồ)
**Dự án:** VLearn AI Socratic Tutor (Track A1)  
**Nhóm:** Tứ Đại Bổ Túc (K4-3B-E402)  
**Tác giả phần việc:** Long  
**Mục tiêu:** Kiểm thử năng lực xử lý nhánh **Luồng 2: Low-confidence (Thu hẹp phạm vi - HAX G10)** theo đúng quy định tại Sơ đồ luồng hoạt động (§4) và Bốn đường đi trải nghiệm (§6) trong `spec.md`.

---

## 1. Cơ chế Luồng 2 trong Workflow

Theo đặc tả hệ thống tại `spec.md`:
- **Điều kiện kích hoạt tại khối Decision:**
  - Câu hỏi của học viên cộc lốc, mơ hồ, thiếu dữ kiện (*"cái này là sao?"*, *"nó hoạt động thế nào?"*, *"trang này nói gì"*).
  - Học viên bôi đen trúng ký tự cụt lủn (ví dụ chữ *"r"*, chữ *"Sau b"*).
  - Lời chào cộc lốc hoặc chuỗi gõ vô nghĩa (*"asds"*, *"hii"*, *"alo"*).
- **Hành vi bắt buộc của AI (Nguyên tắc HAX G10):**
  - **Khối LC1 (Không đoán mò / Không tuôn bài dài):** Tuyệt đối không tự suy diễn ý định của người học, không tuôn bài giảng dài hàng trăm từ gây ngợp chữ.
  - **Khối LC2 (Hỏi lại đúng 1 câu ngắn gọn kèm 2 lựa chọn):** Đặt đúng 1 câu hỏi làm rõ và đưa ra 2 nút bấm gợi ý nhanh tương ứng với các chủ đề trên slide hiện hành để học viên bấm chọn ngay.
  - **Khối UserView2:** Học viên chọn nút gợi ý hoặc gõ làm rõ thắc mắc $\rightarrow$ Luồng quay về Decision để trả lời đúng đích.

---

## 2. Tiêu chí Đánh giá (Pass / Fail Criteria)

Mỗi test case của Luồng 2 được đánh giá theo 3 tiêu chí kiểm chứng được:

1. **Kháng đoán mò (No Speculation - LC1):** AI không được tự tiện giả định ý người dùng để trả lời liều. *(Fail nếu: tự động giảng giải cả slide hoặc suy đoán sai trọng tâm)*.
2. **Thu hẹp phạm vi (Scope Narrowing - LC2):** Phải đặt đúng 1 câu hỏi làm rõ ngắn gọn ($< 35$ từ). *(Fail nếu: hỏi nhiều câu rườm rà hoặc im lặng)*.
3. **Cung cấp lựa chọn nhanh (Interactive Options):** Bắt buộc đưa ra ít nhất 2 phương án lựa chọn liên quan đến slide bài học. *(Fail nếu: không có options hỗ trợ học viên)*.

---

## 3. Danh sách Test Cases Luồng 2 (Trích xuất từ Chatlog thật)

### Case L2-01: Chuỗi ký tự vô nghĩa hoặc cộc lốc
- **Mã nguồn chatlog:** `T00005` (K3, Trang 2)
- **Input của học viên:**
  > *(Slide 05: Token & Chi phí API)*  
  > *"asds"*
- **Phân loại lỗi:** Lớp ② (Mơ hồ / Thiếu thông tin)
- **Hành vi mong đợi:**
  - **LC1:** Không tự đoán mò ý nghĩa của chuỗi ký tự.
  - **LC2:** Báo câu hỏi chưa rõ và hỏi lại học viên muốn tìm hiểu khái niệm Token hay cách tính Chi phí API.
- **Tiêu chuẩn Pass:** Vào Luồng 2, phản hồi ngắn gọn, đưa ra 2 lựa chọn tương tác.
- **Tiêu chuẩn Fail:** Bịa ra một bài giảng dài dòng hoặc báo lỗi crash hệ thống.

---

### Case L2-02: Bôi đen ký tự cụt lủn / Thiếu ý
- **Mã nguồn chatlog:** `T00006` (K3, Trang 5)
- **Input của học viên:**
  > *(Slide 05, đoạn được chọn: "Sau b")*  
  > *"Giải thích đoạn bôi đen ở Trang 5."*
- **Phân loại lỗi:** Lớp ② (Mơ hồ do thao tác bôi đen thiếu ý)
- **Hành vi mong đợi:**
  - **LC1:** Nhận diện đoạn text bôi đen quá ngắn (không đủ nghĩa).
  - **LC2:** Nhắc học viên bôi đen lại rõ hơn hoặc chọn một trong các chủ đề chính của slide.
- **Tiêu chuẩn Pass:** Báo đoạn chọn chưa đủ ý, gợi ý 2 hướng lựa chọn trên slide.
- **Tiêu chuẩn Fail:** Cố gắng giải thích chữ "Sau b" thành một bài giảng vô nghĩa.

---

### Case L2-03: Câu hỏi mơ hồ / Dùng khẩu ngữ địa phương
- **Mã nguồn chatlog:** `T00003` (K3, Trang 6)
- **Input của học viên:**
  > *(Slide 06: Prompt Engineering)*  
  > *"tài liệu này nói về cái chi dợ."*
- **Phân loại lỗi:** Lớp ② (Mơ hồ về phạm vi câu hỏi)
- **Hành vi mong đợi:**
  - **LC1:** Không tuôn cả bài tóm tắt toàn bộ khóa học.
  - **LC2:** Hỏi lại học viên muốn tìm hiểu cấu trúc Prompt 4 phần hay kỹ thuật Few-shot.
- **Tiêu chuẩn Pass:** Hỏi lại đúng 1 câu ngắn gọn kèm 2 options lựa chọn.
- **Tiêu chuẩn Fail:** Tuôn ra bài giảng dài hàng trăm từ gây ngợp nhận thức.

---

### Case L2-04: Câu hỏi trống không về trang bài giảng
- **Mã nguồn chatlog:** `T00512` (K3, Trang 10)
- **Input của học viên:**
  > *(Slide 05: Token & Chi phí)*  
  > *"trang này nói gì"*
- **Phân loại lỗi:** Lớp ② (Thiếu trọng tâm)
- **Hành vi mong đợi:**
  - **LC1:** Tránh độc thoại bài dài.
  - **LC2:** Đưa ra 2 mục chính của slide để học viên bấm chọn điểm vướng mắc.
- **Tiêu chuẩn Pass:** Kích hoạt Luồng 2 (HAX G10), cung cấp các nút chọn nhanh.
- **Tiêu chuẩn Fail:** Đổ nguyên cả nội dung slide ra khung chat.

---

### Case L2-05: Lời chào cộc lốc
- **Mã nguồn chatlog:** `T00002` (K3, Trang 6)
- **Input của học viên:**
  > *(Slide 05: Token & Chi phí)*  
  > *"hii"*
- **Phân loại lỗi:** Lớp ② (Input không có câu hỏi)
- **Hành vi mong đợi:**
  - **LC1:** Không suy diễn kiến thức.
  - **LC2:** Chào lại lịch sự, thân thiện và gợi ý 2 chủ đề học viên có thể khám phá.
- **Tiêu chuẩn Pass:** Chào ngắn gọn và định hướng bắt đầu vào bài học.
- **Tiêu chuẩn Fail:** Im lặng hoặc phản hồi dài dòng không đúng ngữ cảnh.

---

### Case L2-06: Câu hỏi cụt lủn không chủ ngữ
- **Mã nguồn chatlog:** `T00099` (K3, Trang 5)
- **Input của học viên:**
  > *(Slide 05: Token & Chi phí)*  
  > *"phần này là gì"*
- **Phân loại lỗi:** Lớp ② (Thiếu ngữ cảnh đối tượng)
- **Hành vi mong đợi:**
  - **LC1:** Không tự tiện chỉ định một phần bất kỳ trên slide để giảng.
  - **LC2:** Hỏi lại học viên muốn tìm hiểu Khái niệm Token hay Công thức tính chi phí.
- **Tiêu chuẩn Pass:** Kích hoạt Luồng 2, hỏi lại 1 câu ngắn thu hẹp phạm vi.
- **Tiêu chuẩn Fail:** Rơi vào Happy Path và đoán mò lung tung.

---

## 4. Tóm tắt Ma trận Kiểm thử Luồng 2

| Case ID | Turn ID | Dạng câu hỏi mơ hồ | Lớp rủi ro | Hành vi LC1 | Hành vi LC2 | Kết quả mong đợi |
|:---:|:---:|:---|:---:|:---|:---|:---|
| **L2-01** | `T00005` | Ký tự gõ ẩu (*"asds"*) | Lớp ② | Không đoán mò | Hỏi lại 1 câu + 2 options | Học viên click chọn chủ đề |
| **L2-02** | `T00006` | Bôi đen cụt (*"Sau b"*) | Lớp ② | Báo chưa đủ ý | Gợi ý bôi đen lại hoặc chọn mục | Tránh giảng vô nghĩa |
| **L2-03** | `T00003` | Khẩu ngữ (*"nói về cái chi dợ"*) | Lớp ② | Không tuôn bài dài | Hỏi lại trọng tâm slide | Tránh ngợp chữ |
| **L2-04** | `T00512` | Hỏi trang trống (*"trang này nói gì"*) | Lớp ② | Tránh độc thoại | Đưa 2 mục cốt lõi của trang | Học viên chủ động chọn |
| **L2-05** | `T00002` | Lời chào (*"hii"*) | Lớp ② | Không suy diễn | Chào thân thiện + gợi ý bắt đầu | Định hướng bài học |
| **L2-06** | `T00099` | Cụt lủn (*"phần này là gì"*) | Lớp ② | Không gán ghép bừa | Hỏi lại Token hay Chi phí | Đúng đích học viên cần |
