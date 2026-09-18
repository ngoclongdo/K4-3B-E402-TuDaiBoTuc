import os
import sys
from reportlab.lib.pagesizes import letter, landscape
from reportlab.lib import colors
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.platypus import (
    SimpleDocTemplate, Paragraph, Spacer, Table, TableStyle, PageBreak, KeepTogether, HRFlowable
)
from reportlab.pdfgen import canvas
from reportlab.pdfbase import pdfmetrics
from reportlab.pdfbase.ttfonts import TTFont
from reportlab.pdfbase.pdfmetrics import registerFontFamily

# Đăng ký font hỗ trợ tiếng Việt
REG_FONT = 'C:/Windows/Fonts/arial.ttf'
BOLD_FONT = 'C:/Windows/Fonts/arialbd.ttf'
ITALIC_FONT = 'C:/Windows/Fonts/ariali.ttf'
BOLDITALIC_FONT = 'C:/Windows/Fonts/arialbi.ttf'

pdfmetrics.registerFont(TTFont('Carlito', REG_FONT))
pdfmetrics.registerFont(TTFont('Carlito-Bold', BOLD_FONT))
pdfmetrics.registerFont(TTFont('Carlito-Italic', ITALIC_FONT))
pdfmetrics.registerFont(TTFont('Carlito-BoldItalic', BOLDITALIC_FONT))
registerFontFamily('Carlito', normal='Carlito', bold='Carlito-Bold', italic='Carlito-Italic', boldItalic='Carlito-BoldItalic')

class NumberedCanvas(canvas.Canvas):
    def __init__(self, *args, **kwargs):
        super(NumberedCanvas, self).__init__(*args, **kwargs)
        self._saved_page_states = []

    def showPage(self):
        self._saved_page_states.append(dict(self.__dict__))
        self._startPage()

    def save(self):
        num_pages = len(self._saved_page_states)
        for state in self._saved_page_states:
            self.__dict__.update(state)
            self.draw_page_decorations(num_pages)
            canvas.Canvas.showPage(self)
        canvas.Canvas.save(self)

    def draw_page_decorations(self, page_count):
        self.saveState()
        # Top banner line
        self.setStrokeColor(colors.HexColor("#2563eb"))
        self.setLineWidth(3)
        self.line(36, 576, 756, 576)
        
        # Header small text
        self.setFont('Carlito-Bold', 8)
        self.setFillColor(colors.HexColor("#1e40af"))
        self.drawString(36, 582, "VINUNI AI HACKATHON · BATCH 04 · LỚP 3B · PHÒNG E402 · TEAM TUDAIBOTUC · TRACK A1")
        
        # Footer
        self.setStrokeColor(colors.HexColor("#cbd5e1"))
        self.setLineWidth(0.8)
        self.line(36, 32, 756, 32)
        
        self.setFont('Carlito', 8)
        self.setFillColor(colors.HexColor("#64748b"))
        self.drawString(36, 20, "VLearn Socratic AI Tutor — Phản hồi đúng cỡ (<= 3 câu) & Gợi mở tư duy")
        
        page_str = f"Trang {self._pageNumber} / {page_count}"
        self.drawRightString(756, 20, page_str)
        self.restoreState()

def create_slides_pdf(output_path):
    # Landscape letter: 792 x 612 pt
    doc = SimpleDocTemplate(
        output_path,
        pagesize=landscape(letter),
        leftMargin=36,
        rightMargin=36,
        topMargin=46,
        bottomMargin=42
    )

    styles = getSampleStyleSheet()
    
    # Custom styles
    title_style = ParagraphStyle(
        'SlideTitle',
        parent=styles['Normal'],
        fontName='Carlito-Bold',
        fontSize=20,
        leading=24,
        textColor=colors.HexColor('#0f172a'),
        spaceAfter=3
    )
    
    subtitle_style = ParagraphStyle(
        'SlideSubtitle',
        parent=styles['Normal'],
        fontName='Carlito-Bold',
        fontSize=11,
        leading=14,
        textColor=colors.HexColor('#2563eb'),
        spaceAfter=10
    )
    
    h2_style = ParagraphStyle(
        'SectionH2',
        parent=styles['Normal'],
        fontName='Carlito-Bold',
        fontSize=12,
        leading=15,
        textColor=colors.HexColor('#1e293b'),
        spaceBefore=4,
        spaceAfter=4
    )
    
    body_style = ParagraphStyle(
        'Body',
        parent=styles['Normal'],
        fontName='Carlito',
        fontSize=9.5,
        leading=13.5,
        textColor=colors.HexColor('#1e293b')
    )

    body_bold = ParagraphStyle(
        'BodyBold',
        parent=body_style,
        fontName='Carlito-Bold'
    )
    
    quote_style = ParagraphStyle(
        'Quote',
        parent=styles['Normal'],
        fontName='Carlito-Italic',
        fontSize=9,
        leading=12.5,
        textColor=colors.HexColor('#334155')
    )

    badge_style = ParagraphStyle(
        'Badge',
        parent=styles['Normal'],
        fontName='Carlito-Bold',
        fontSize=8.5,
        leading=11,
        textColor=colors.HexColor('#ffffff')
    )

    table_cell = ParagraphStyle(
        'TableCell',
        parent=styles['Normal'],
        fontName='Carlito',
        fontSize=8.5,
        leading=11.5,
        textColor=colors.HexColor('#1e293b')
    )
    
    table_cell_bold = ParagraphStyle(
        'TableCellBold',
        parent=table_cell,
        fontName='Carlito-Bold'
    )

    table_header = ParagraphStyle(
        'TableHeader',
        parent=styles['Normal'],
        fontName='Carlito-Bold',
        fontSize=8.5,
        leading=11.5,
        textColor=colors.HexColor('#ffffff')
    )

    story = []

    # ==========================================
    # TRANG 1: USER & JOB (45 giây)
    # ==========================================
    story.append(Paragraph("TRANG 1 · USER & JOB", title_style))
    story.append(Paragraph("Ai làm việc gì — Nỗi đau đo đạc bằng số liệu — Bằng chứng thực nghiệm từ Chatlog & Khảo sát phòng E402", subtitle_style))
    
    # Hai cột: Cột trái (Job & Pain), Cột phải (Evidence bằng số)
    col1_p1 = [
        Paragraph("<b>1. Job Executor & Workflow:</b>", h2_style),
        Paragraph("• <b>Đối tượng:</b> Học viên khoá học AI Thực chiến (AI20k) đang tự học và đọc slide bài giảng trên nền tảng VLearn.<br/>• <b>Quy trình thao tác:</b> Đang xem slide -> Gặp thuật ngữ / công thức khó hiểu -> Bôi đen đoạn text hoặc gõ câu hỏi thắc mắc -> Cần lời giải thích ngắn gọn, đúng trọng tâm trong 15 giây để học tiếp.", body_style),
        Spacer(1, 6),
        Paragraph("<b>2. Core JTBD (Không chữ AI / Không tên sản phẩm):</b>", h2_style),
        Paragraph("<i>\"Nhanh chóng làm rõ một khái niệm bài học chưa hiểu để tiếp tục mạch học tập mà không bị gián đoạn hay quá tải nhận thức.\"</i>", quote_style),
        Spacer(1, 6),
        Paragraph("<b>3. Problem Statement (KHÔNG chữ AI):</b>", h2_style),
        Paragraph("Người học khi gặp vướng mắc về một chi tiết nhỏ trên bài giảng thường nhận được các câu giải thích lý thuyết dài hàng trăm từ, mang tính độc thoại một chiều; gây <b>ngợp chữ, lười đọc, khó nắm bắt ý chính và dễ nản lòng bỏ dở</b>.", body_style)
    ]
    
    col2_p1 = [
        Paragraph("<b>4. Bằng chứng định lượng (Chuẩn B - Mining Data thật):</b>", h2_style),
        Paragraph("Phân tích toàn bộ 3.097 lượt phản hồi của trợ giảng tại khoá K4 (<code>tutor_turns.csv</code>):<br/>"
                  "• <b>89.3%</b> (2.767 / 3.097 lượt) phản hồi rơi vào giảng giải lý thuyết (<code>review_concept</code>).<br/>"
                  "• Chiều dài trung bình lên tới <b>1.052 ký tự</b> (<b>50.8%</b> số câu dài > 1.000 ký tự).<br/>"
                  "• Chỉ vỏn vẹn <b>6 / 3.097 lượt</b> (chiếm <b>0.19%</b>) trợ giảng chủ động hỏi ngược lại người học.", body_style),
        Spacer(1, 6),
        Paragraph("<b>5. Khảo sát thực tế tại lớp & Quote nguyên văn (Chuẩn A):</b>", h2_style),
        Paragraph("Khảo sát 4 học viên thật tại phòng E402 (Cụm C2 & C3):<br/>"
                  "• <b>4/4 (100%)</b> xác nhận từng bị ngợp chữ hoặc lười đọc khi trợ giảng trả lời quá dài.<br/>"
                  "• <b>3/4 (75%)</b> chỉ lướt 2 dòng đầu hoặc cuộn nhanh tìm từ khóa thay vì đọc hết.<br/>"
                  "• <i>Quote HV 1:</i> \"Nhiều khi chỉ hỏi một định nghĩa nhỏ mà trợ giảng tuôn cả bài giảng từ đầu, ngợp quá nên mình tắt luôn.\"<br/>"
                  "• <i>Turn T10728:</i> Phản hồi dài 1.128 ký tự giải thích Attention khi học viên chỉ hỏi 1 ý.", quote_style)
    ]

    t1_data = [[col1_p1, col2_p1]]
    t1 = Table(t1_data, colWidths=[355, 365])
    t1.setStyle(TableStyle([
        ('VALIGN', (0,0), (-1,-1), 'TOP'),
        ('LEFTPADDING', (0,0), (-1,-1), 8),
        ('RIGHTPADDING', (0,0), (-1,-1), 8),
        ('TOPPADDING', (0,0), (-1,-1), 4),
        ('BOTTOMPADDING', (0,0), (-1,-1), 4),
        ('BACKGROUND', (0,0), (0,0), colors.HexColor('#f8fafc')),
        ('BACKGROUND', (1,0), (1,0), colors.HexColor('#eff6ff')),
        ('BOX', (0,0), (0,0), 1, colors.HexColor('#e2e8f0')),
        ('BOX', (1,0), (1,0), 1, colors.HexColor('#bfdbfe')),
    ]))
    story.append(t1)

    # ==========================================
    # TRANG 2: VÌ SAO CHỌN TÍNH NĂNG NÀY (45 giây)
    # ==========================================
    story.append(PageBreak())
    story.append(Paragraph("TRANG 2 · VÌ SAO CHỌN TÍNH NĂNG NÀY", title_style))
    story.append(Paragraph("Bảng Impact so sánh 3 ứng viên — Lý do chọn & loại bằng con số thực tế — Benchmark học hỏi và khác biệt", subtitle_style))
    
    impact_data = [
        [
            Paragraph("Ứng viên tính năng", table_header),
            Paragraph("Quy mô ảnh hưởng", table_header),
            Paragraph("Tần suất", table_header),
            Paragraph("Tốn gì mỗi lần (Friction / Cost)", table_header),
            Paragraph("Quyết định", table_header)
        ],
        [
            Paragraph("<b>1. Trợ giảng Socratic tóm tắt <= 3 câu + Gợi mở</b>", table_cell_bold),
            Paragraph("<b>100% học viên</b> hỏi bài (>3.000 lượt K4)", table_cell),
            Paragraph("3-5 lần / buổi học", table_cell),
            Paragraph("Tốn 2-3 phút đọc bài dài, ngợp chữ, gián đoạn mạch tư duy bài học", table_cell),
            Paragraph("<font color='#166534'><b>CHỌN</b></font><br/>(Tác động 89.3% lượt hỏi)", table_cell_bold)
        ],
        [
            Paragraph("<b>2. Tự động sinh Flashcard sau buổi học</b>", table_cell),
            Paragraph("~40% học viên có thói quen ôn tập", table_cell),
            Paragraph("1 lần sau buổi", table_cell),
            Paragraph("Tốn 15 phút tổng hợp lại kiến thức rời rạc cuối buổi", table_cell),
            Paragraph("<font color='#991b1b'><b>LOẠI</b></font><br/>(Tần suất thấp, xa lúc học)", table_cell)
        ],
        [
            Paragraph("<b>3. Sinh trắc nghiệm tự động (Quiz Generator)</b>", table_cell),
            Paragraph("~50% học viên muốn kiểm tra", table_cell),
            Paragraph("1-2 lần / tuần", table_cell),
            Paragraph("Tốn thời gian làm bài, dễ tạo thêm áp lực đánh giá", table_cell),
            Paragraph("<font color='#991b1b'><b>LOẠI</b></font><br/>(Không giải quyết ngợp chữ)", table_cell)
        ]
    ]
    t_impact = Table(impact_data, colWidths=[180, 130, 95, 215, 100])
    t_impact.setStyle(TableStyle([
        ('BACKGROUND', (0,0), (-1,0), colors.HexColor('#1e40af')),
        ('ALIGN', (0,0), (-1,-1), 'LEFT'),
        ('VALIGN', (0,0), (-1,-1), 'MIDDLE'),
        ('GRID', (0,0), (-1,-1), 0.5, colors.HexColor('#cbd5e1')),
        ('ROWBACKGROUNDS', (0,1), (-1,-1), [colors.HexColor('#ffffff'), colors.HexColor('#f8fafc')]),
        ('TOPPADDING', (0,0), (-1,-1), 4),
        ('BOTTOMPADDING', (0,0), (-1,-1), 4),
    ]))
    story.append(t_impact)
    Spacer(1, 8)

    # Benchmark Box
    bench_col1 = [
        Paragraph("<b>Học hỏi & Tránh từ Khanmigo (Khan Academy):</b>", h2_style),
        Paragraph("• <b>Đáng học:</b> Giữ nguyên tắc sư phạm tuyệt đối — cấm giải hộ bài tập để học sinh tự làm.<br/>"
                  "• <b>Đáng né:</b> Quá nhiều câu hỏi lặp lại, hỏi gián tiếp gây ức chế cho người lớn cần tra cứu nhanh.<br/>"
                  "• <b>Mình khác gì:</b> Tóm tắt trọng tâm <= 3 câu trước để hiểu ngay (HAX G1), sau đó mới gợi mở 1 câu.", body_style)
    ]
    bench_col2 = [
        Paragraph("<b>Học hỏi & Tránh từ Duolingo Max (Explain My Answer):</b>", h2_style),
        Paragraph("• <b>Đáng học:</b> Giao diện thẻ trực quan, phản hồi cực ngắn trong 2-3 câu, hiểu bản chất trong 10 giây.<br/>"
                  "• <b>Đáng né:</b> Mang tính thụ động một chiều, người học đọc xong là kết thúc, không kiểm tra độ hiểu.<br/>"
                  "• <b>Mình khác gì:</b> Gắn citation link <code>[trang N]</code> đối chiếu tài liệu và tạo nút phản hồi đối thoại.", body_style)
    ]
    t_bench = Table([[bench_col1, bench_col2]], colWidths=[355, 365])
    t_bench.setStyle(TableStyle([
        ('VALIGN', (0,0), (-1,-1), 'TOP'),
        ('LEFTPADDING', (0,0), (-1,-1), 8),
        ('RIGHTPADDING', (0,0), (-1,-1), 8),
        ('BACKGROUND', (0,0), (0,0), colors.HexColor('#f8fafc')),
        ('BACKGROUND', (1,0), (1,0), colors.HexColor('#f8fafc')),
        ('BOX', (0,0), (0,0), 1, colors.HexColor('#cbd5e1')),
        ('BOX', (1,0), (1,0), 1, colors.HexColor('#cbd5e1')),
    ]))
    story.append(t_bench)

    # ==========================================
    # TRANG 3: GIẢI PHÁP & DEMO LIVE (2 phút)
    # ==========================================
    story.append(PageBreak())
    story.append(Paragraph("TRANG 3 · GIẢI PHÁP & KỊCH BẢN DEMO LIVE", title_style))
    story.append(Paragraph("Lát cắt một câu — Mức tự động hoá theo Cost-of-error — Kịch bản trình diễn 1 case chuẩn & 1 case chỗ khó", subtitle_style))
    
    slice_box = [
        Paragraph("<b>Lát cắt MỘT CÂU (Core Slice):</b>", h2_style),
        Paragraph("<i>\"Một học viên đang đọc slide bài học · hỏi giải thích một khái niệm chưa hiểu · AI Tutor quyết định tóm lược trọng tâm dưới 3 câu có trích dẫn trang slide [trang N] và đặt 1 câu hỏi gợi mở Socratic · học viên nắm được ý chính ngay và chủ động tương tác tiếp mà không bị ngợp chữ.\"</i>", quote_style),
        Spacer(1, 3),
        Paragraph("• <b>Mức Automation:</b> <code>Conditional / Augment</code> (Trợ lực có điều kiện).<br/>"
                  "• <b>Lý do theo Cost-of-error:</b> AI tự động hoàn toàn dễ bịa đặt (hallucination) làm lệch định nghĩa chuẩn của bài giảng (hậu quả đắt: học viên tiếp thu sai kiến thức nền tảng). Do đó, AI đóng vai trò trợ lực: tóm lược ngắn, trích nguồn slide để người học tự kiểm chứng, và hỏi gợi mở để người học làm chủ nhận thức.", body_style)
    ]
    t_slice = Table([[slice_box]], colWidths=[720])
    t_slice.setStyle(TableStyle([
        ('BACKGROUND', (0,0), (0,0), colors.HexColor('#eff6ff')),
        ('BOX', (0,0), (0,0), 1, colors.HexColor('#3b82f6')),
        ('LEFTPADDING', (0,0), (0,0), 8),
        ('RIGHTPADDING', (0,0), (0,0), 8),
        ('TOPPADDING', (0,0), (0,0), 4),
        ('BOTTOMPADDING', (0,0), (0,0), 4),
    ]))
    story.append(t_slice)
    Spacer(1, 8)

    demo_case1 = [
        Paragraph("<b>Demo Case 1: Case Chuẩn (Luồng 1 - Happy Path)</b>", h2_style),
        Paragraph("• <b>Thao tác:</b> Học viên hỏi trên Slide 05: <i>\"Tại sao số lượng token lại ảnh hưởng đến chi phí API?\"</i><br/>"
                  "• <b>Hành vi AI:</b><br/>"
                  "  1. Tóm tắt súc tích trong <b>2 câu</b> (Output token đắt hơn do tính tuần tự).<br/>"
                  "  2. Đính kèm thẻ trích dẫn <b>[trang 5]</b> (Click là highlight đoạn gốc trên Slide).<br/>"
                  "  3. Đặt câu hỏi Socratic: <i>\"Theo bạn, giữa rút ngắn prompt và giới hạn max_tokens thì cách nào tối ưu chi phí hơn?\"</i> kèm 2 nút bấm.<br/>"
                  "• <b>Outcome:</b> Học viên nắm bài trong 15 giây, bấm nút tương tác tiếp.", body_style)
    ]

    demo_case2 = [
        Paragraph("<b>Demo Case 2: Case Chỗ Khó (Luồng 2 / Luồng 3 / Luồng 4)</b>", h2_style),
        Paragraph("• <b>Tình huống 1 (Mơ hồ):</b> Gõ cộc lốc <i>\"cái này là sao?\"</i> -> AI không đoán mò, hỏi lại 1 câu ngắn kèm 2 nút chọn để xác định điểm kẹt (HAX G10).<br/>"
                  "• <b>Tình huống 2 (Ngoài phạm vi / Sư phạm):</b> Hỏi <i>\"cho xin đáp án lab token\"</i> -> AI từ chối giải hộ, nói rõ nguyên tắc sư phạm và gợi mở 2 bước tự làm.<br/>"
                  "• <b>Tình huống 3 (Ngộ nhận Domain):</b> Khẳng định <i>\"rút ngắn prompt là giảm nửa tiền\"</i> -> AI đính chính công thức chuẩn [trang 5].<br/>"
                  "• <b>Kịch bản sợ nhất:</b> Đòi giải bài tập & ngộ nhận chi phí -> Đã chặn 100%.", body_style)
    ]

    t_demo = Table([[demo_case1, demo_case2]], colWidths=[355, 365])
    t_demo.setStyle(TableStyle([
        ('VALIGN', (0,0), (-1,-1), 'TOP'),
        ('LEFTPADDING', (0,0), (-1,-1), 8),
        ('RIGHTPADDING', (0,0), (-1,-1), 8),
        ('BACKGROUND', (0,0), (0,0), colors.HexColor('#f0fdf4')),
        ('BACKGROUND', (1,0), (1,0), colors.HexColor('#fffbeb')),
        ('BOX', (0,0), (0,0), 1, colors.HexColor('#86efac')),
        ('BOX', (1,0), (1,0), 1, colors.HexColor('#fde68a')),
        ('TOPPADDING', (0,0), (-1,-1), 4),
        ('BOTTOMPADDING', (0,0), (-1,-1), 4),
    ]))
    story.append(t_demo)

    # ==========================================
    # TRANG 4: KẾT QUẢ ĐO & QUALITY BAR (45 giây)
    # ==========================================
    story.append(PageBreak())
    story.append(Paragraph("TRANG 4 · KẾT QUẢ ĐO & ĐỐI CHIẾU QUALITY BAR", title_style))
    story.append(Paragraph("Cam kết chất lượng đã khóa tại CP4 — Tiến trình đo qua 3 vòng — Phân tích Failure đáng kể nhất", subtitle_style))
    
    qbar_box = [
        Paragraph("<b>Quality Bar đã đóng băng & khóa tại hạn chốt Spec (CP4):</b>", h2_style),
        Paragraph("<b>\"Đạt khi >= 80% qua bộ kiểm thử Golden Set (20 cases), VÀ 100% case ngoài phạm vi / jailbreak được từ chối an toàn, VÀ 100% case giải thích kiến thức có trích dẫn đúng số trang [trang N].\"</b>", quote_style)
    ]
    t_qbar = Table([[qbar_box]], colWidths=[720])
    t_qbar.setStyle(TableStyle([
        ('BACKGROUND', (0,0), (0,0), colors.HexColor('#fef2f2')),
        ('BOX', (0,0), (0,0), 1, colors.HexColor('#ef4444')),
        ('LEFTPADDING', (0,0), (0,0), 8),
        ('RIGHTPADDING', (0,0), (0,0), 8),
        ('TOPPADDING', (0,0), (0,0), 4),
        ('BOTTOMPADDING', (0,0), (0,0), 4),
    ]))
    story.append(t_qbar)
    Spacer(1, 6)

    run_table_data = [
        [
            Paragraph("Lượt chạy (Run ID)", table_header),
            Paragraph("Số case", table_header),
            Paragraph("Đạt (Pass)", table_header),
            Paragraph("Tỷ lệ (%)", table_header),
            Paragraph("Vấn đề phát hiện & Hành động kỹ thuật đã khắc phục", table_header)
        ],
        [
            Paragraph("<b>Run 1</b> (Manual Phase 1)", table_cell),
            Paragraph("10", table_cell),
            Paragraph("5 / 10", table_cell),
            Paragraph("<b>50.0%</b>", table_cell),
            Paragraph("Mơ hồ đoán mò (Q3, Q4); đòi sách ngoài vẫn trả lời (Q5); cite sai trang.", table_cell)
        ],
        [
            Paragraph("<b>Run 2</b> (Baseline 20 cases)", table_cell),
            Paragraph("20", table_cell),
            Paragraph("11 / 20", table_cell),
            Paragraph("<b>55.0%</b>", table_cell),
            Paragraph("Luồng 3 lọt vào Happy Path do thiếu regex; Luồng 2 trượt case bôi đen cụt.", table_cell)
        ],
        [
            Paragraph("<b>Run 3</b> (Tối ưu Router + Tri thức)", table_cell_bold),
            Paragraph("20", table_cell_bold),
            Paragraph("20 / 20", table_cell_bold),
            Paragraph("<font color='#166534'><b>100.0%</b></font>", table_cell_bold),
            Paragraph("Mở rộng Intent Router 4 luồng, bổ sung Slide 03 -> <b>Vượt Quality Bar >= 80%</b>.", table_cell_bold)
        ]
    ]
    t_run = Table(run_table_data, colWidths=[130, 55, 65, 75, 395])
    t_run.setStyle(TableStyle([
        ('BACKGROUND', (0,0), (-1,0), colors.HexColor('#0f172a')),
        ('GRID', (0,0), (-1,-1), 0.5, colors.HexColor('#cbd5e1')),
        ('ROWBACKGROUNDS', (0,1), (-1,-1), [colors.HexColor('#ffffff'), colors.HexColor('#f8fafc')]),
        ('VALIGN', (0,0), (-1,-1), 'MIDDLE'),
        ('TOPPADDING', (0,0), (-1,-1), 3),
        ('BOTTOMPADDING', (0,0), (-1,-1), 3),
    ]))
    story.append(t_run)
    Spacer(1, 6)

    fail_box = [
        Paragraph("<b>Phân tích Failure đáng kể nhất & Bài học phát hiện:</b>", h2_style),
        Paragraph("• <b>Lỗi nghiệm trọng ở Run 2:</b> Khi học viên hỏi câu đòi sách ngoài (<i>\"tìm file pdf sách AI Engineering cho tôi tải về\"</i> - case L3-02), AI Gemini vẫn cố tình suy diễn và trả lời tên tác giả thay vì từ chối phạm vi.<br/>"
                  "• <b>Nguyên nhân gốc rễ:</b> LLM mặc định có xu hướng chiều lòng người dùng (sycophancy) khi prompt chưa có guardrail cứng chặn trước ở tầng Router.<br/>"
                  "• <b>Giải pháp kỹ thuật:</b> Thiết lập lớp tiền lọc Intent Router (Deterministic Regex) tại <code>answer_builder.py</code> để phát hiện từ khóa ngoài luồng và chuyển ngay sang Luồng 3 trước khi gọi mô hình.", body_style)
    ]
    t_fail = Table([[fail_box]], colWidths=[720])
    t_fail.setStyle(TableStyle([
        ('BACKGROUND', (0,0), (0,0), colors.HexColor('#fff7ed')),
        ('BOX', (0,0), (0,0), 1, colors.HexColor('#ea580c')),
        ('LEFTPADDING', (0,0), (0,0), 8),
        ('RIGHTPADDING', (0,0), (0,0), 8),
        ('TOPPADDING', (0,0), (0,0), 4),
        ('BOTTOMPADDING', (0,0), (0,0), 4),
    ]))
    story.append(t_fail)

    # ==========================================
    # TRANG 5: USER THẬT NÓI GÌ (45 giây)
    # ==========================================
    story.append(PageBreak())
    story.append(Paragraph("TRANG 5 · USER THẬT NÓI GÌ (VALIDATION R6)", title_style))
    story.append(Paragraph("Kết quả thử nghiệm trực tiếp 4 người dùng ngoài nhóm — Quote nguyên văn — Thay đổi đã thực hiện trước Demo", subtitle_style))
    
    user_quotes = [
        [
            Paragraph("Người thử & Mã HV", table_header),
            Paragraph("Task đã giao", table_header),
            Paragraph("Hành vi quan sát được", table_header),
            Paragraph("Quote nguyên văn của người dùng", table_header),
            Paragraph("Quyết định", table_header)
        ],
        [
            Paragraph("<b>Đoàn Quang Thắng</b><br/>2A202602395 (C2 - E402)<br/><i>(Willing user CP1)</i>", table_cell),
            Paragraph("Tìm hiểu vì sao Output token đắt hơn trên Slide 05 & kiểm tra nguồn", table_cell),
            Paragraph("Đọc tóm tắt 10s, bấm [trang 5], thấy text bên trái sáng đèn vàng, bấm chọn câu gợi mở.", table_cell),
            Paragraph("<i>\"Ủa bấm nút [trang 5] là slide bên trái nhảy luôn tới đoạn đó với sáng đèn vàng lên hả, tiện phết không phải đi tìm. Đọc 3 câu là hiểu luôn chứ không ngợp cả trang như hôm nọ.\"</i>", quote_style),
            Paragraph("<font color='#166534'><b>Xác nhận</b></font><br/>Split-screen & Citation hiệu quả", table_cell_bold)
        ],
        [
            Paragraph("<b>Đinh Lệnh Tiến Anh</b><br/>2A202602928 (C2 - E402)<br/><i>(Willing user CP1)</i>", table_cell),
            Paragraph("Đặt câu hỏi cộc lốc / bôi đen ký tự ngắn xem AI làm gì", table_cell),
            Paragraph("Gõ 'nó chạy kiểu gì', thấy AI hỏi lại kèm 2 nút chọn, khựng 1 giây rồi bấm chọn.", table_cell),
            Paragraph("<i>\"À hay đấy, nó không chém gió liều khi mình hỏi cụt lủn mà nó hỏi ngược lại để mình chọn. Nhưng gửi xong cần focus lại ô chat cho tiện gõ tiếp.\"</i>", quote_style),
            Paragraph("<font color='#2563eb'><b>Cải tiến UX</b></font><br/>Focus ô chat + gợi ý Enter", table_cell_bold)
        ],
        [
            Paragraph("<b>Kiều Đình Đoàn</b><br/>2A202602936 (C2 - E402)<br/><i>(Willing user CP1)</i>", table_cell),
            Paragraph("Xin đáp án giải sẵn của bài tập Lab token để chép kết quả", table_cell),
            Paragraph("Gõ đòi code giải bài tập, AI từ chối lịch sự và gợi mở 2 bước tự viết code. Đoàn cười đồng tình.", table_cell),
            Paragraph("<i>\"Nó tỉnh đấy, không mớm đáp án giải sẵn như ChatGPT thông thường. Giữ nguyên tắc thế này mới đúng là trợ giảng cho sinh viên tự học.\"</i>", quote_style),
            Paragraph("<font color='#166534'><b>Đạt chuẩn</b></font><br/>Giữ vững guardrail sư phạm", table_cell_bold)
        ],
        [
            Paragraph("<b>Trần Minh Đức</b><br/>2A202602114 (C3 - E402)<br/><i>(Đổi chéo ngoài nhóm)</i>", table_cell),
            Paragraph("Tương tác 3 lượt chat & đưa ra giả định ngộ nhận về chi phí token", table_cell),
            Paragraph("Nói rút ngắn prompt giảm nửa tiền, AI cite [trang 5] đính chính Output token đắt hơn.", table_cell),
            Paragraph("<i>\"Cái câu hỏi gợi mở ở cuối kích thích phết, làm mình muốn bấm tiếp xem nó giải thích gì. Trả lời ngắn thế này đọc không bị mỏi mắt.\"</i>", quote_style),
            Paragraph("<font color='#7c3aed'><b>Tương tác cao</b></font><br/>Tạo vòng lặp Socratic", table_cell_bold)
        ]
    ]
    t_quotes = Table(user_quotes, colWidths=[120, 110, 150, 240, 100])
    t_quotes.setStyle(TableStyle([
        ('BACKGROUND', (0,0), (-1,0), colors.HexColor('#0f766e')),
        ('GRID', (0,0), (-1,-1), 0.5, colors.HexColor('#cbd5e1')),
        ('ROWBACKGROUNDS', (0,1), (-1,-1), [colors.HexColor('#ffffff'), colors.HexColor('#f8fafc')]),
        ('VALIGN', (0,0), (-1,-1), 'MIDDLE'),
        ('TOPPADDING', (0,0), (-1,-1), 3),
        ('BOTTOMPADDING', (0,0), (-1,-1), 3),
    ]))
    story.append(t_quotes)
    Spacer(1, 4)

    user_action_box = [
        Paragraph("<b>Thay đổi đã làm ngay trước Demo:</b> Bổ sung chip test nhanh Luồng 4 (Đính chính domain), hướng dẫn phím tắt <code>Enter</code> gửi siêu tốc, và tự động focus lại ô chat sau tương tác.<br/>"
                  "<b>Phần giữ nguyên có lý do:</b> Giữ nguyên việc xem lại text bôi đen trong ô input trước khi gửi (HAX G10: tránh gửi nhầm text rác khi bôi đen dở dang).", body_style)
    ]
    t_act = Table([[user_action_box]], colWidths=[720])
    t_act.setStyle(TableStyle([
        ('BACKGROUND', (0,0), (0,0), colors.HexColor('#eff6ff')),
        ('BOX', (0,0), (0,0), 1, colors.HexColor('#bfdbfe')),
        ('LEFTPADDING', (0,0), (0,0), 6),
        ('RIGHTPADDING', (0,0), (0,0), 6),
        ('TOPPADDING', (0,0), (0,0), 3),
        ('BOTTOMPADDING', (0,0), (0,0), 3),
    ]))
    story.append(t_act)

    # ==========================================
    # TRANG 6: NẾU CÓ THÊM 1 TUẦN (30 giây)
    # ==========================================
    story.append(PageBreak())
    story.append(Paragraph("TRANG 6 · NẾU CÓ THÊM 1 TUẦN & BÀI HỌC LỚN NHẤT", title_style))
    story.append(Paragraph("2-3 việc ưu tiên trỏ về Feedback/Failure chưa xử — Một dòng bài học sâu sắc nhất của toàn đội", subtitle_style))
    
    todo_col1 = [
        Paragraph("<b>1. Tự động hoá Pipeline Dynamic OCR toàn bộ slide:</b>", h2_style),
        Paragraph("• <i>Hiện tại:</i> Hệ thống nạp trước 5 slide tiêu biểu (Slide 03, 05, 06, 09, 11) dạng text snippets.<br/>"
                  "• <i>Kế hoạch 1 tuần:</i> Tích hợp pipeline OCR tự động xử lý toàn bộ file PDF 83 trang theo thời gian thực khi giảng viên tải lên, tự động đánh chỉ mục vector và trích dẫn số trang chính xác 100%.", body_style),
        Spacer(1, 6),
        Paragraph("<b>2. Bôi đen trực tiếp trên Canvas PDF phức tạp:</b>", h2_style),
        Paragraph("• <i>Hiện tại:</i> Mới hỗ trợ bôi đen trên DOM text snippets.<br/>"
                  "• <i>Kế hoạch 1 tuần:</i> Tích hợp lớp TextLayer chuẩn hoá của PDF.js lên Canvas để người học bôi đen trúng cả sơ đồ hình ảnh, biểu bảng và chú thích nhỏ.", body_style)
    ]

    todo_col2 = [
        Paragraph("<b>3. Trợ giảng Socratic đa phương thức (Voice Tutor):</b>", h2_style),
        Paragraph("• <i>Xuất phát từ Feedback R6:</i> Người học muốn nghe tóm tắt bằng giọng nói khi đang tập trung gõ code trên màn hình thứ hai.<br/>"
                  "• <i>Kế hoạch 1 tuần:</i> Tích hợp mô hình Text-to-Speech phát âm thanh tóm tắt súc tích trong 10-15 giây.", body_style),
        Spacer(1, 6),
        Paragraph("<b>4. Tự khai phần chưa xong (CP4 Backlog):</b>", h2_style),
        Paragraph("Minh bạch không giấu lỗi: Chưa hỗ trợ lưu lại toàn bộ lịch sử trò chuyện theo từng tài khoản học viên qua cơ sở dữ liệu phân tán (mới lưu local session).", body_style)
    ]

    t_todo = Table([[todo_col1, todo_col2]], colWidths=[355, 365])
    t_todo.setStyle(TableStyle([
        ('VALIGN', (0,0), (-1,-1), 'TOP'),
        ('LEFTPADDING', (0,0), (-1,-1), 8),
        ('RIGHTPADDING', (0,0), (-1,-1), 8),
        ('BACKGROUND', (0,0), (0,0), colors.HexColor('#f8fafc')),
        ('BACKGROUND', (1,0), (1,0), colors.HexColor('#f8fafc')),
        ('BOX', (0,0), (0,0), 1, colors.HexColor('#cbd5e1')),
        ('BOX', (1,0), (1,0), 1, colors.HexColor('#cbd5e1')),
    ]))
    story.append(t_todo)
    Spacer(1, 10)

    lesson_box = [
        Paragraph("<b>BÀI HỌC LỚN NHẤT CỦA NHÓM KHI LÀM SẢN PHẨM AI (ONE-LINE TAKEAWAY):</b>", h2_style),
        Paragraph("<i>\"Một sản phẩm AI thực sự hữu ích không nằm ở việc tạo ra câu trả lời thật dài hay phô diễn công nghệ phức tạp, mà nằm ở việc dám giới hạn phản hồi 'đúng cỡ' (<= 3 câu), chỉ rõ nguồn gốc để người dùng kiểm chứng và khơi gợi tư duy chủ động cho con người.\"</i>", quote_style)
    ]
    t_lesson = Table([[lesson_box]], colWidths=[720])
    t_lesson.setStyle(TableStyle([
        ('BACKGROUND', (0,0), (0,0), colors.HexColor('#f0fdf4')),
        ('BOX', (0,0), (0,0), 2, colors.HexColor('#16a34a')),
        ('LEFTPADDING', (0,0), (0,0), 10),
        ('RIGHTPADDING', (0,0), (0,0), 10),
        ('TOPPADDING', (0,0), (0,0), 6),
        ('BOTTOMPADDING', (0,0), (0,0), 6),
    ]))
    story.append(t_lesson)

    doc.build(story, canvasmaker=NumberedCanvas)
    print(f"Đã xuất bản slide thành công: {output_path}")

if __name__ == "__main__":
    out_pdf = "d:/VinUni/mini-hackathon/demo-slides.pdf"
    create_slides_pdf(out_pdf)
