import sys
import os

pdf_path = os.path.abspath("AutoOne_Technical_Architecture_Report.pdf")

try:
    from reportlab.lib.pagesizes import A4
    from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer, HRFlowable, Preformatted
    from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
    from reportlab.lib import colors
    import arabic_reshaper
    from bidi.algorithm import get_display

    def ar(text):
        if not text:
            return ""
        lines = text.split('\n')
        reshaped_lines = []
        for line in lines:
            has_arabic = any('\u0600' <= char <= '\u06FF' for char in line)
            if has_arabic:
                reshaped = arabic_reshaper.reshape(line)
                reshaped_lines.append(get_display(reshaped))
            else:
                reshaped_lines.append(line)
        return '\n'.join(reshaped_lines)

    doc = SimpleDocTemplate(pdf_path, pagesize=A4, rightMargin=25, leftMargin=25, topMargin=25, bottomMargin=25)
    story = []

    from reportlab.pdfbase import pdfmetrics
    from reportlab.pdfbase.ttfonts import TTFont

    win_font = "C:\\Windows\\Fonts\\arial.ttf"
    if os.path.exists(win_font):
        pdfmetrics.registerFont(TTFont('ArabicFont', win_font))
        font_name = 'ArabicFont'
    else:
        font_name = 'Helvetica'

    styles = getSampleStyleSheet()

    title_style = ParagraphStyle(
        'TitleStyle', parent=styles['Normal'],
        fontName=font_name, fontSize=18, leading=22,
        textColor=colors.HexColor("#1A365D"), alignment=1, spaceAfter=12
    )

    h1_style = ParagraphStyle(
        'H1Style', parent=styles['Normal'],
        fontName=font_name, fontSize=13, leading=17,
        textColor=colors.HexColor("#2B6CB0"), alignment=2, spaceBefore=10, spaceAfter=6
    )

    body_style = ParagraphStyle(
        'BodyStyle', parent=styles['Normal'],
        fontName=font_name, fontSize=9.5, leading=13.5,
        textColor=colors.HexColor("#2D3748"), alignment=2, spaceAfter=4
    )

    prompt_style = ParagraphStyle(
        'PromptStyle', parent=styles['Normal'],
        fontName=font_name, fontSize=8.5, leading=12,
        textColor=colors.HexColor("#1A202C"), alignment=2,
        backColor=colors.HexColor("#EDF2F7"), borderColor=colors.HexColor("#CBD5E0"),
        borderWidth=1, borderPadding=8, spaceBefore=4, spaceAfter=8
    )

    story.append(Paragraph(ar("تقرير الشرح التقني الشامل لبنية مشروع AutoOne (مركز برق الجزيرة)"), title_style))
    story.append(HRFlowable(width="100%", thickness=2, color=colors.HexColor("#3182CE"), spaceAfter=10))

    # Read system prompts from agents
    from agents.marketing import MARKETING_SYSTEM_PROMPT
    from agents.doctor_auto import DOCTOR_AUTO_SYSTEM_PROMPT
    from agents.booking import BOOKING_SYSTEM_PROMPT
    from agents.orchestrator import ORCHESTRATOR_SYSTEM_PROMPT

    sections = [
        ("1. قائمة الوكلاء (Agents) وأماكن الكود في المشروع", [
            "• المشرف العام والمدير التنفيذي (Chief Orchestrator): agents/orchestrator.py",
            "• د. سيارات (Technical Diagnostic Expert): agents/doctor_auto.py",
            "• مسؤول التسويق وخدمة العملاء (Customer Relations Agent): agents/marketing.py",
            "• مدير المواعيد والعمليات (Booking Agent): agents/booking.py",
            "• نظام الذاكرة المستقلة (Isolated Private Memory System): agents/memory.py",
            "• خادم السيرفر السحابي (Flask Web Application Server): app.py"
        ]),
        ("2. آلية التواصل المباشر بين الوكلاء (Inter-Agent Communication)", [
            "السؤال: هل يوجد دالة حقيقية (Tool/Function) يستدعيها وكيل التسويق للاستشارة؟",
            "الجواب: نعم! توجد دالة بايثون تنفيذية حقيقية 100% وليست مجرد نص بالـ Prompt.",
            "اسم الدالة: consult_doctor_for_boardroom(api_key, query) في agents/doctor_auto.py",
            "طريقة الاستدعاء داخل agents/marketing.py:",
            "  doctor_tech_input = consult_doctor_for_boardroom(api_key, customer_msg)",
            "شكل الـ API Call: يتم إرسال طلب HTTP POST أول مستقل إلى DeepSeek API بـ Prompt د. سيارات، ثم تُمرر النتيجة كـ Context في طلب HTTP POST ثانٍ مستقل لوكيل التسويق."
        ]),
        ("3. مصادر البيانات والتخزين (Data Persistence & Knowledge Base)", [
            "• ملف البيانات التراكمية: agents_private_memory.json يقع في الجذر الرئيسي للمشروع.",
            "• الأمان التزامني: محمي بواسطة threading.Lock() لمنع التداخل والتعارض بين استدعاءات السيرفر المتزامنة.",
            "• تقييد الحجم: يتم تقييد حفظ الذاكرة تلقائياً عند آخر 50 محادثة لكل وكيل لضمان الأمان والسرعة.",
            "• لائحة الأسعار: معرّفة ومبوبة في قاعدة المعرفة الصارمة داخل MARKETING_SYSTEM_PROMPT (DOD = 300 ريال، فحص كمبيوتر = 100 ريال، مراوح = 250 ريال، وتفاوض حتى 150 ريال كحد أدنى)."
        ]),
        ("4. المشرف العام وكود التوجيه المركزي (Chief Orchestrator)", [
            "• ملف الكود: agents/orchestrator.py",
            "• الدالة التنفيذية للإدارة: run_real_inter_agent_boardroom(api_key, messages)",
            "• آلية العمل: تدير خط أنابيب تسلسلي حقيقي (Sequential Inter-Agent Pipeline): المشرف العام 👈 د. سيارات 👈 التسويق 👈 المواعيد، وتجمع الردود في مصفوفة JSON لعرضها في واجهة القيادة للمالك."
        ]),
        ("5. مواصفات الموديل والإعدادات (Model Specifications & Hyperparameters)", [
            "• اسم الموديل المحدد: deepseek-chat (DeepSeek-V3 Engine)",
            "• رابط الـ API Endpoint: https://api.deepseek.com/chat/completions",
            "• درجات الحرارة (Temperature): 0.3 لدكتور سيارات والمواعيد والمشرف العام، و 0.3 - 0.4 لوكيل التسويق.",
            "• الحد الأقصى للتوكنز (Max Tokens): 500 إلى 1000 توكن حسب نوع الاستدعاء."
        ])
    ]

    for title, items in sections:
        story.append(Paragraph(ar(title), h1_style))
        for item in items:
            story.append(Paragraph(ar(item), body_style))
        story.append(Spacer(1, 4))

    # Prompts Section
    prompts_data = [
        ("System Prompt وكيل التسويق (MARKETING_SYSTEM_PROMPT)", MARKETING_SYSTEM_PROMPT),
        ("System Prompt وكيل خبير السيارات (DOCTOR_AUTO_SYSTEM_PROMPT)", DOCTOR_AUTO_SYSTEM_PROMPT),
        ("System Prompt مدير المواعيد (BOOKING_SYSTEM_PROMPT)", BOOKING_SYSTEM_PROMPT),
        ("System Prompt المشرف العام (ORCHESTRATOR_SYSTEM_PROMPT)", ORCHESTRATOR_SYSTEM_PROMPT),
    ]

    story.append(Paragraph(ar("6. الـ System Prompts الكاملة لجميع الوكلاء (Full System Prompts)"), h1_style))
    for p_title, p_content in prompts_data:
        story.append(Paragraph(ar(p_title), h1_style))
        story.append(Paragraph(ar(p_content), prompt_style))
        story.append(Spacer(1, 4))

    doc.build(story)
    print("PDF Generated successfully with all full System Prompts at:", pdf_path)

except Exception as e:
    print("Error generating PDF:", str(e))
    sys.exit(1)
