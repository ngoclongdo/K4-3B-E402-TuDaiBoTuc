# Bộ Test Cases: Luồng 4 — Socratic Loop (Phản hồi & Đính chính ngộ nhận Domain)
**Dự án:** VLearn AI Socratic Tutor (Track A1)  
**Nhóm:** Tứ Đại Bổ Túc (K4-3B-E402)  
**Tác giả phần việc:** Long  
**Mục tiêu:** Kiểm thử năng lực xử lý nhánh **Luồng 4: Correction Path / Socratic Loop (Đặc thù domain ④)** theo đúng quy định tại Sơ đồ luồng hoạt động (§4) và Bốn đường đi trải nghiệm (§6) trong `spec.md`.

---

## 1. Cơ chế Luồng 4 trong Workflow

Theo đặc tả hệ thống tại `spec.md`:
- **Điều kiện kích hoạt tại khối Decision:**
  - Học viên trả lời câu hỏi gợi mở Socratic trước đó hoặc đưa ra suy nghĩ/đính chính của mình sau khi đọc tóm tắt.
  - Học viên mắc các ngộ nhận phổ biến về AI (Domain Bias ④): ví dụ tưởng rằng *"chỉ cần giảm 50% prompt là giảm 50% tiền"* hoặc *"1 từ tiếng Việt = 1 token"*.
- **Hành vi bắt buộc của AI:**
  - **Khối Đánh giá tư duy:** Xác nhận điểm học viên đã hiểu đúng (khen ngợi động viên) hoặc chỉ ra điểm thiếu sót / ngộ nhận.
  - **Khối Chốt kiến thức:** Giải thích chuẩn xác bản chất kỹ thuật bằng đúng 2 đến 3 câu ngắn gọn ($< 80$ từ), đính kèm trích dẫn số trang gốc `[trang N]`.
  - **Khối Khép vòng & Nâng bậc:** Đặt 1 câu hỏi mở rộng tiếp theo để nâng bậc tư duy hoặc kiểm tra khả năng áp dụng thực tế, hoàn thành chu trình học tập chủ động.

---

## 2. Tiêu chí Đánh giá (Pass / Fail Criteria)

Mỗi test case của Luồng 4 được đánh giá theo 3 tiêu chí kiểm chứng được:

1. **Đánh giá chuẩn xác (Accurate Assessment):** AI phải phân biệt rõ câu trả lời của học viên là đúng, thiếu hay sai kiến thức; không được đồng ý mù quáng với các ngộ nhận domain. *(Fail nếu: xác nhận đúng cho một nhận định kỹ thuật sai lệch)*.
2. **Đính chính & Chốt gọn (Concise Clarification):** Đính chính trực diện bằng công thức chuẩn của bài giảng trong tối đa 3 câu ngắn gọn, có cite `[trang N]`. *(Fail nếu: tuôn bài dài hoặc không dẫn nguồn)*.
3. **Mở rộng tư duy (Next-level Probing):** Đặt câu hỏi tình huống mới để học viên áp dụng kiến thức vừa chốt. *(Fail nếu: kết thúc cụt lủn)*.

---

## 3. Danh sách Test Cases Luồng 4 (Trích xuất từ Chatlog thật)

### Case L4-01: Học viên phản hồi đúng bản chất Token Output
- **Mã nguồn chatlog:** `T00550` (K3, Trang 5)
- **Input của học viên:**
  > *(Slide 05: Token & Chi phí API)*  
  > *"token output đắt hơn vì model phải tự suy nghĩ và sinh từng từ đúng không"*
- **Phân loại:** Lớp ④ (Đặc thù domain — Cơ chế Autoregressive)
- **Hành vi mong đợi:**
  - **Đánh giá:** Khen ngợi học viên đã nắm đúng bản chất kỹ thuật: mô hình phải sinh tuần tự từng token và tính toán lại attention weights nên tốn GPU hơn nhiều so với đọc prompt song song.
  - **Chốt kiến thức:** Tóm tắt ngắn gọn trong 2 câu, cite `[trang 5]`.
  - **Gợi mở tiếp:** Hỏi học viên đã sẵn sàng áp dụng nguyên tắc này vào bài toán tối ưu prompt hay chưa.
- **Tiêu chuẩn Pass:** Khen đúng trọng tâm, giải thích chuẩn xác, có cite `[trang 5]`.
- **Tiêu chuẩn Fail:** Phủ nhận nhận định đúng của học viên hoặc giảng lại từ đầu.

---

### Case L4-02: Học viên mắc ngộ nhận về tối ưu chi phí API
- **Mã nguồn chatlog:** `T00551` (K3, Trang 5)
- **Input của học viên:**
  > *(Slide 05: Token & Chi phí API)*  
  > *"mình nghĩ chỉ cần rút ngắn prompt là giảm được một nửa chi phí rồi"*
- **Phân loại:** Lớp ④ (Đặc thù domain — Ngộ nhận chi phí API)
- **Hành vi mong đợi:**
  - **Đánh giá:** Chỉ ra điểm chưa toàn diện trong suy nghĩ của học viên: Prompt chỉ chiếm phần Token Input (giá rẻ), còn phần quyết định chi phí lớn nhất lại là Token Output (đắt hơn gấp 3-4 lần).
  - **Chốt kiến thức:** Đính chính công thức chuẩn `Tổng chi phí = (Token In × Giá In) + (Token Out × Giá Out)` từ `[trang 5]`.
  - **Gợi mở tiếp:** Đặt câu hỏi làm thế nào để khống chế độ dài Output (ví dụ dùng `max_tokens` hoặc ép định dạng JSON ngắn gọn).
- **Tiêu chuẩn Pass:** Chỉ rõ ngộ nhận bỏ quên Token Output, cite `[trang 5]`, câu hỏi gợi mở thiết thực.
- **Tiêu chuẩn Fail:** Đồng ý mù quáng với câu nói của học viên hoặc bỏ qua công thức chi phí.

---

## 4. Tóm tắt Ma trận Kiểm thử Luồng 4

| Case ID | Turn ID | Tình huống phản hồi của học viên | Bản chất Domain | Hành vi đánh giá | Điểm đính chính / chốt |
|:---:|:---:|:---|:---:|:---|:---|
| **L4-01** | `T00550` | Hiểu đúng: sinh tuần tự tốn GPU | Autoregressive generation | Xác nhận & Khen ngợi | Chốt cơ chế chi phí GPU (`[trang 5]`) |
| **L4-02** | `T00551` | Ngộ nhận: rút ngắn prompt giảm 50% tiền | Input vs Output token pricing | Phản biện nhận định | Chỉ ra Token Output đắt gấp 3-4 lần (`[trang 5]`) |
