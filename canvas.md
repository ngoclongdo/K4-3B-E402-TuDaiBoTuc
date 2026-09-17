# CP1 Canvas — TuDaiBoTuc

| Mục | Nội dung |
|---|---|
| **Hướng** | A — VLearn (A1: Tối ưu AI Tutor hiện có) |
| **Job executor** | Học viên khoá AI Thực chiến đang học trên VLearn, bôi đen hoặc gõ câu hỏi thắc mắc về một khái niệm/slide bài giảng. |
| **Pain 1 câu** | Khi học viên hỏi làm rõ một ý nhỏ, AI Tutor trả lời quá dài (>1.000 ký tự) và độc thoại một chiều; học viên bị ngợp chữ, lười đọc và bỏ dở việc học. |
| **Evidence ban đầu** | Data K4: 89.3% là `review_concept`, độ dài TB 1.052 ký tự, chỉ 0.19% hỏi ngược (`T10317`, `T10502`). Khảo sát lớp: 5/5 bạn xác nhận bị ngợp chữ, 80% chỉ đọc lướt. |
| **Lát cắt 1 câu** | Một học viên hỏi giải thích khái niệm; AI Tutor quyết định tóm lược dưới 3 câu kèm trích dẫn `[trang N]` và đặt 1 câu hỏi gợi mở Socratic; học viên nắm ý chính ngay và chủ động tương tác tiếp. |
| **Automation** | Augment / Conditional: AI tự tóm tắt ngắn gọn và trích dẫn trang khi có căn cứ; hỏi lại khi câu hỏi mơ hồ; không tự tuôn bài giảng dài khi chưa thăm dò mức hiểu. |
| **Willing users dự kiến** | 3 bạn ngoài nhóm tại phòng E402 (bàn 2, bàn 3) đã hẹn test CP5. |
| **Phân công** | Long: spec + prompt; Tuấn Anh: evidence mining + eval/golden set; Đức Anh: prototype + AI call. |
