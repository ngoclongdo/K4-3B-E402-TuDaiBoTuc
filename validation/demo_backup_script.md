# Kịch Bản Demo Dự Phòng Buổi Thuyết Trình (Pitch Backup Script — CP5)

**Sản phẩm:** VLearn Socratic AI Tutor (Phản hồi đúng cỡ & Gợi mở tư duy)  
**Nhóm:** TuDaiBoTuc · **Lớp:** 3B · **Phòng:** E402 · **Cụm:** C2  
**Thời lượng demo:** 2 phút (Trong tổng 7 phút thuyết trình)  
**Thành viên thực hiện demo:** Cao Đức Anh (Tech Lead) & Đỗ Nguyễn Ngọc Long (Lead)

---

## 1. Mục Đích & Nguyên Tắc An Toàn Của Kịch Bản

- **Mục đích:** Đảm bảo buổi thuyết trình diễn ra trọn vẹn, không bị động trước bất kỳ sự cố mạng wifi, API rate limit hoặc treo máy nào tại hội trường E402.
- **Quy tắc dự phòng (Fallback):**
  1. *Nếu mạng tốt:* Thực hiện live trực tiếp trên trình duyệt tại `http://localhost:5000`.
  2. *Nếu mạng chập chờn / mất kết nối API:* Chuyển ngay sang video quay sẵn màn hình demo (`demo_backup_video.mp4` lưu sẵn trên desktop máy trình chiếu). Ban tổ chức sẽ chiếu video này và không trừ điểm theo đúng quy chế CP5.
  3. *Thời gian chuyển đổi:* Dưới 5 giây, người trình bày tiếp tục nói theo nhịp mà không xin lỗi hay ngắt mạch.

---

## 2. Kịch Bản Chi Tiết Từng Giây (2 Phút Live Demo)

### Phút 0:00 – 0:25: Giới thiệu giao diện Split-Screen & Thiết lập bối cảnh
- **Người nói (Long):**
  > *"Kính thưa ban giám khảo, đây là giao diện học tập thực tế trên VLearn với màn hình chia đôi. Bên trái là Slide bài giảng số 05 về Token & Chi phí, bên phải là Trợ giảng Socratic. Khi gặp điểm chưa hiểu, thay vì nhận cả trang bài giảng dài 1.052 ký tự gây ngợp, hãy xem trợ giảng phản hồi thế nào."*
- **Thao tác (Đức Anh):**
  - Mở trình duyệt hiển thị màn hình chia đôi (Slide Viewer bên trái và Chat dock bên phải).
  - Trỏ chuột vào nhãn HAX G1 trên thanh tiêu đề: *"HAX G1: Hỗ trợ giải thích Slide 05 · Token & Chi phí"*.

### Phút 0:25 – 1:05: DEMO CASE 1 — Case Chuẩn (Luồng 1 · Happy Path)
- **Người nói (Long):**
  > *"Em đóng vai một học viên đang đọc Slide 05 và thắc mắc: 'Tại sao số lượng token lại ảnh hưởng đến chi phí API?'"*
- **Thao tác (Đức Anh):**
  - Bấm vào nút chip gợi ý màu xanh: `🟢 Luồng 1: Tại sao token ảnh hưởng chi phí?` (hoặc gõ và bấm `Enter`).
- **Hành vi AI quan sát được trên màn hình:**
  - AI phản hồi sau 1.2 giây với 3 đặc điểm chuẩn thiết kế:
    1. **Tóm tắt đúng cỡ:** Đúng 2 câu (chưa đầy 45 từ), nêu rõ token là đơn vị tính tiền và Token Output đắt gấp 3-4 lần Token Input.
    2. **Grounding có nguồn:** Xuất hiện nhãn `📖 [trang 5] Token và chi phí gọi API`.
    3. **Socratic probing:** Đặt câu hỏi gợi mở: *"Theo bạn, giữa việc rút ngắn câu lệnh Prompt và giới hạn độ dài phản hồi (max_tokens), cách nào giúp tiết kiệm chi phí hiệu quả hơn?"* kèm 2 nút bấm tương tác.
- **Thao tác tương tác (Đức Anh):**
  - Bấm chuột vào nút `[trang 5]`: Cột Slide bên trái lập tức cuộn mượt và **tô sáng (highlight) viền vàng** vào đúng đoạn văn bản gốc nói về chi phí token.
- **Người nói (Long):**
  > *"Chỉ mất đúng 10 giây để học viên nắm trọn ý chính, bấm xem ngay vị trí bài giảng gốc mà không phải tự lật trang tìm lại."*

### Phút 1:05 – 1:45: DEMO CASE 2 — Case Chỗ Khó (Luồng 2 & Luồng 3 · HAX G10 & Sư Phạm)
- **Người nói (Long):**
  > *"Bây giờ đến phần thử thách mô hình với 2 kịch bản khó nhất trong Taxonomy rủi ro."*
- **Tình huống 2A (Mơ hồ / Thiếu thông tin - Luồng 2):**
  - **Thao tác (Đức Anh):** Gõ câu hỏi cộc lốc: `cái này là sao?` rồi bấm `Enter`.
  - **Hành vi AI:** AI không đoán mò, không tuôn bài dài; lập tức vào Luồng 2 (Low-confidence), hỏi lại đúng 1 câu: *"Bạn đang muốn làm rõ khái niệm Token hay cách tính Chi phí API trên slide này?"* kèm 2 nút bấm chọn nhanh.
  - **Người nói:** *"Tuân thủ nghiêm ngặt nguyên tắc HAX G10: Thu hẹp phạm vi khi mơ hồ thay vì suy diễn liều."*
- **Tình huống 2B (Đòi đáp án bài tập - Luồng 3 & Nguyên tắc Sư phạm):**
  - **Thao tác (Đức Anh):** Gõ: `cho mình xin đáp án bài tập mini exercise để nộp bài` rồi bấm `Enter`.
  - **Hành vi AI:** AI nhận diện Luồng 3 (Out-of-scope), từ chối lịch sự: *"Tài liệu bài học không cung cấp sẵn đáp án bài tập thực hành nhằm giúp học viên tự rèn luyện tư duy. Bạn hãy xem lại Slide 05 về công thức tính token và thử tự ước tính trước nhé!"*.
  - **Người nói:** *"Khác biệt hoàn toàn với ChatGPT thông thường: Hệ thống giữ vững nguyên tắc sư phạm, từ chối mớm bài giải và hướng dẫn người học tự tư duy."*

### Phút 1:45 – 2:00: Chốt & Chuyển Sang Bằng Chứng Đo Lường
- **Người nói (Long):**
  > *"Cả 2 kịch bản chuẩn và khó đều được kiểm chứng tự động qua bộ Golden Set 20 cases với tỷ lệ đạt 100%. Xin mời ban giám khảo cùng nhìn vào các con số đo lường thực tế trên slide tiếp theo."*
- **Thao tác (Đức Anh):** Chuyển màn hình về file slide `demo-slides.pdf` tại Trang 4 (Kết quả đo).

---

## 3. Checklist Chuẩn Bị File Cho Buổi Pitch Thực Tế

1. [x] Xuất bản file `demo-slides.pdf` 6 trang chuẩn đặt tại thư mục gốc của repo.
2. [x] Khởi chạy sẵn local server: `python codebase/server.py` tại cổng `5000` (đã nạp sẵn key và kho tri thức offline dự phòng).
3. [x] Chuẩn bị sẵn tab trình duyệt mở tại `http://localhost:5000` với chế độ zoom 110% để khán trường nhìn rõ.
4. [x] Video demo dự phòng sẵn sàng trên máy để phát ngay khi ban tổ chức yêu cầu nếu mạng hội trường E402 gặp sự cố.
