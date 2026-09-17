# Canvas 7 dòng — Checkpoint 1 (CP1)

**Lớp:** 3B · **Phòng:** E402 · **Cụm:** C2 · **Nhóm:** TuDaiBoTuc  
**Đội trưởng:** Đỗ Nguyễn Ngọc Long (Mã HV: 2A202602390)  
**Link repo:** `https://github.com/VinUni-AI20k/K4-3B-E402-TuDaiBoTuc`  

---

## Bảng Canvas 7 dòng

| # | Dòng | Nội dung |
|---|---|---|
| **1** | **Track + đề** | **Track A · VLearn Tutor** — Đề **A1**: Tối ưu AI Tutor hiện có (Khắc phục phản hồi dài dòng, chuyển sang mô hình gia sư Socratic ngắn gọn & gợi mở). |
| **2** | **Job executor** | Học viên khoá AI Thực chiến đang học trên VLearn, vừa bôi đen hoặc gõ câu hỏi thắc mắc về một khái niệm/slide bài giảng. |
| **3** | **Pain một câu** *(ai – đang làm gì – vướng đâu – hậu quả)* | Học viên khi hỏi làm rõ một ý nhỏ trên slide thì bị AI Tutor trả lời đang bị dài (500 - 1.000 ký tự) và độc thoại lý thuyết một chiều, khiến học viên bị ngợp chữ, lười đọc, không nắm được trọng tâm và bỏ dở việc học. |
| **4** | **1–2 bằng chứng đầu** *(số + cách đếm + mã hội thoại / khảo sát)* | **1. Mining chatlog thật (`tutor_turns.csv`):**<br>• **89.3%** câu trả lời ở K4 là `review_concept` (2.767 / 3.097 lượt).<br>• Chiều dài trung bình phản hồi là **1.052 ký tự** (>50.8% câu dài trên 1.000 ký tự).<br>• Chỉ vỏn vẹn **6 / 3.097 lượt** (0.19%) Tutor có hỏi ngược học viên (`ask_probing_question`).<br>• *Mã hội thoại minh hoạ:* `T10317`, `T10502`, `T10728`.<br><br>**2. Khảo sát nhanh học viên trong lớp:**<br>• **5/5 (100%)** xác nhận từng bị ngợp hoặc lười đọc khi nhìn thấy độ dài câu trả lời của Tutor.<br>• **4/5 (80%)** chỉ đọc lướt vài dòng đầu hoặc cuộn xuống tìm từ khóa.<br>• *Quote nguyên văn:* "Giảng giải lại cả một đoạn lý thuyết dài từ đầu", "Không giống người". |
| **5** | **Lát cắt MỘT CÂU** *(1 user · 1 việc · 1 quyết định AI · 1 kết quả)* | **Một học viên đang đọc slide bài học** · **hỏi giải thích một khái niệm chưa hiểu** · **AI Tutor quyết định tóm lược trọng tâm dưới 3 câu có trích dẫn trang slide và đặt 1 câu hỏi gợi mở (Socratic)** · **học viên nắm được ý chính ngay và chủ động tương tác tiếp mà không bị ngợp chữ.** |
| **6** | **AI tự làm đến đâu + lý do · Willing users** | • **Tự làm (Augment / Socratic):** Trích xuất ý chính từ slide, trả lời ngắn gọn (≤3 câu), trích dẫn đúng số trang `[trang N]` và đặt 1 câu hỏi gợi mở để người học tự tư duy.<br>• **Không tự làm:** Không tự tuôn ra toàn bộ bài giảng lý thuyết dài dòng; không tự giải đáp án bài tập khi chưa thăm dò mức hiểu của học viên.<br>• **Lý do (Cost-of-error):** Trả lời quá dài gây quá tải nhận thức (cognitive overload), triệt tiêu sự chủ động học tập; giải thích dài dễ kèm hallucination sai lệch định nghĩa của giảng viên.<br>• **Willing users (≥2 người ngoài nhóm đồng ý test ở CP5):**<br>  1. Đoàn Quang Thắng - 2A202602395 (C2 - E402)<br>  2. Đinh Lệnh Tiến Anh - 2A202602928 (C2 - E402)<br>  3. Kiều Đình Đoàn - 2A202602936 (C2 - E402)<br>  4. Nguyễn Hoàng Nam - 2A202602485 (C2 - E402) |
| **7** | **Phân công có tên** | • **Đỗ Nguyễn Ngọc Long** (Lead): Chốt Canvas, cấu trúc Spec, điều phối chung.<br>• **Nguyễn Tuấn Anh**: Tạo form khảo sát, phân tích số liệu.<br>• **Cao Đức Anh**: Trực tiếp đi khảo sát các bạn trong lớp, thu thập dữ liệu, phỏng vấn người dùng (user interview). |

---

## Chi tiết phục vụ đối chiếu tiêu chí chấm (Rubric Check)

- **Đúng format lát cắt 1 câu**: Đầy đủ 4 thành tố: 1 user (học viên đọc slide) · 1 việc (hỏi giải thích khái niệm) · 1 quyết định AI (tóm lược ≤3 câu + cite trang + hỏi 1 câu Socratic) · 1 kết quả (nắm ý chính ngay, chủ động học).
- **Đạt chuẩn Bằng chứng (Evidence)**: Kết hợp cả Mining data thật (có số đếm %, mã turn `T#####`) và Khảo sát thật tại phòng học E402 (có tỷ lệ xác nhận, quote nguyên văn).
- **Khai báo Willing Users**: Đã xác nhận trước để phục vụ nghiệm thu vòng validation R6 tại CP5.
