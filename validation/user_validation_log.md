# Báo cáo Xác thực Người dùng Ngoài nhóm (User Validation Log — Khối R6)

**Thời gian thực hiện:** 18/09/2026 (Phiên thử nghiệm chuẩn bị cho CP5)  
**Địa điểm:** Phòng E402, VinUni (Cụm C2)  
**Quy trình thực hiện:** Tuân thủ chuẩn 5 nhịp & quy tắc Mom Test:
1. Trấn an người thử: Đánh giá chất lượng và độ tiện dụng của sản phẩm, không đánh giá người học.
2. Hỏi câu chuyện thật: Hỏi về trải nghiệm học tập và hỏi đáp với AI Tutor trên VLearn gần đây nhất.
3. Giao task theo outcome: Không chỉ tay vào nút bấm, để người dùng tự thao tác đạt mục tiêu.
4. Im lặng quan sát trong 5 phút: Chỉ dùng 3 câu cứu hộ trung tính ("Cứ nói to suy nghĩ nhé", "Bạn sẽ làm gì tiếp?", "Bạn nghĩ nó nên hoạt động thế nào?").
5. Phỏng vấn ngắn sau khi dùng: Hỏi cảm nhận về độ dài phản hồi, tính gợi mở và khả năng kiểm chứng nguồn gốc.

---

## 1. Bảng Nhật ký 4 Người dùng Ngoài nhóm Trải nghiệm Trực tiếp

| STT | Người thử (Tên / Mã HV / Cụm - Phòng) | Có phải Willing User từ CP1? | Task đã giao (Theo outcome) | Hành vi quan sát được (Quan sát trực tiếp) | Quote nguyên văn (Chép đúng lời nói lúc dùng) | Mức nghiêm trọng & Đánh giá |
|:---:|---|:---:|---|---|---|:---:|
| 1 | **Đoàn Quang Thắng**<br>(2A202602395 · C2 - E402) | **CÓ** (Willing user CP1) | "Tìm hiểu lý do vì sao Token Output lại có chi phí đắt hơn Token Input trên Slide 05 và kiểm chứng xem bài giảng viết ở đâu." | Đọc lướt phần tóm tắt trong ~10 giây, thấy nút `[trang 5]`, bấm ngay lập tức. Mắt nhìn sang cột slide bên trái thấy khối text được highlight màu vàng sáng lên. Sau đó nhìn thấy câu hỏi Socratic và bấm nút gợi ý có sẵn. | *"Ủa bấm vào cái nút `[trang 5]` là slide bên trái nhảy luôn tới đoạn đó với sáng đèn vàng lên hả, tiện phết không phải đi tìm. Đọc 3 câu là hiểu luôn vấn đề chứ không bị ngợp cả trang như hôm nọ."* | **Tích cực (Praise/Insight)**<br>Chứng minh giải pháp Split-screen + Citation highlight giải quyết triệt để nỗi đau. |
| 2 | **Đinh Lệnh Tiến Anh**<br>(2A202602928 · C2 - E402) | **CÓ** (Willing user CP1) | "Đặt một câu hỏi mơ hồ hoặc bôi đen một mẩu ngắn trên slide để xem gia sư AI xử lý như thế nào." | Tiến Anh gõ cộc lốc: *"nó chạy kiểu gì"*. AI lập tức phản hồi ở Luồng 2 (Low-confidence): Không đoán mò, hỏi lại 1 câu ngắn và đưa ra 2 nút lựa chọn (Khái niệm Token hay Chi phí API). Tiến Anh khựng lại 1 giây rồi bấm nút *"Chi phí API"*. | *"À hay đấy, nó không chém gió liều khi mình hỏi cụt lủn mà nó hỏi ngược lại để mình chọn. Nhưng mà cái khung chat bên dưới sau khi mình gửi xong nó không tự xóa text cũ nếu bấm chuột ra ngoài à?"* | **Trung bình (Friction)**<br>Góp ý về trải nghiệm UX: cần làm rõ trạng thái nút bấm gợi ý và auto-clear / auto-focus thanh nhập liệu. |
| 3 | **Kiều Đình Đoàn**<br>(2A202602936 · C2 - E402) | **CÓ** (Willing user CP1) | "Thử hỏi xin đáp án giải sẵn của bài tập thực hành Mini-exercise trên slide để nộp bài." | Gõ vào ô chat: *"cho mình xin code giải bài tập lab token"*. AI nhận diện Luồng 3 (Out-of-scope / Sư phạm), từ chối lịch sự, giải thích slide bài tập nhằm rèn luyện tư duy và gợi mở 2 bước để tự viết code. Đoàn cười và gật đầu. | *"Nó tỉnh đấy, không mớm đáp án giải sẵn như ChatGPT thông thường. Giữ nguyên tắc thế này mới đúng là trợ giảng cho sinh viên tự học."* | **Tốt (Pedagogical Guardrail)**<br>Xác nhận tính năng từ chối giải hộ đạt chuẩn sư phạm, không vi phạm non-goals. |
| 4 | **Nguyễn Hoàng Nam**<br>(2A202602485 · C2 - E402) | **CÓ** (Willing user CP1) | "Thử dùng tính năng bôi đen một thuật ngữ trên slide để hỏi trực tiếp." | Nam bôi đen cụm từ *"Context Window"* trên slide. Một popup nhỏ hiện lên *"⚡ Hỏi AI Tutor về đoạn này"*. Nam click vào popup, text được điền tự động vào ô chat. Tuy nhiên Nam muốn sau khi bấm thì gửi luôn thay vì phải bấm nút Gửi lần nữa. | *"Mình bôi đen xong bấm nút popup nhỏ rồi tưởng nó gửi luôn, hóa ra nó mới paste vào ô chat, mình phải tự ấn Enter thêm phát nữa mới chạy."* | **Thấp (UX polish)**<br>Người dùng kỳ vọng thao tác bôi đen $\rightarrow$ hỏi ngay (One-click ask) để tiết kiệm thêm 1 thao tác bấm. |

---

## 2. Bốn Dòng Tổng Hợp Bắt Buộc (Synthesis)

1. **Chủ đề lặp lại nhiều nhất:**  
   Người dùng cực kỳ ấn tượng với tốc độ nắm bắt thông tin nhờ tóm tắt $\le 3$ câu và tính năng bấm citation `[trang N]` để highlight trực tiếp tài liệu gốc; tuy nhiên, người dùng mong muốn tinh gọn thao tác bôi đen (muốn bôi đen xong bấm là gửi ngay lập tức thay vì phải bấm thêm nút gửi).
2. **Thay đổi đã thực hiện trước buổi Demo:**  
   Cải tiến UX trong giao diện: Tối ưu nút popup bôi đen trên slide — bổ sung cơ chế tự động cuộn đến tin nhắn mới nhất, tự động focus lại ô nhập liệu và hiển thị rõ hơn gợi ý phím tắt `Enter` để gửi tin nhắn siêu tốc; đồng thời bổ sung thêm chip gợi ý test nhanh cho Luồng 4 (Đính chính ngộ nhận Domain) ngay trên thanh công cụ.
3. **Phần giữ nguyên có lý do (Lập luận rõ ràng):**  
   Giữ nguyên cơ chế **xác nhận trước khi gửi câu hỏi từ đoạn bôi đen** (chỉ điền vào ô chat chứ không tự động gửi ngầm ngay lập tức). *Lý do:* Theo nguyên tắc HAX G10 & G11 (Thu hẹp phạm vi và Cho phép sửa dễ dàng), người học bôi đen thường hay quẹt dở dang hoặc thừa/thiếu ký tự; việc đưa văn bản vào khung input cho phép người học xem lại, bổ sung thắc mắc cụ thể trước khi gửi, tránh phát sinh các truy vấn rác đến mô hình.
4. **Phần đưa vào Backlog (Kế hoạch phát triển sau Hackathon):**  
   Hỗ trợ tương tác bằng giọng nói (Voice input/output) để người học có thể nghe tóm tắt khi đang tập trung nhìn code, và mở rộng bộ parser OCR động để người dùng có thể tải lên bất kỳ slide bài giảng mới nào trong toàn trường VinUni.
