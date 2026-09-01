"""
Booking & Operations Module (Private Memory & Real Inter-Agent Consultation)
"""
import requests
from .memory import get_private_memory, record_private_memory

DEEPSEEK_API_URL = 'https://api.deepseek.com/chat/completions'

BOOKING_SYSTEM_PROMPT = """أنت مدير المواعيد والعمليات التشغيلية في ورشة "جار الله أوتو".

صفاتك والدور المحدد لك:
1. أنت المسؤول عن تنظيم المسارات التشغيلية، جدول الحجوزات، وحساب الطاقة الاستيعابية للورشة.
2. تترجم التشخيص الفني المعتمد من "د. سيارات" ورغبة العميل المعالجة من "التسويق" إلى مواعيد زمنية دقيقة وتنفيذ عملي.
3. ممنوع منعاً باتاً اختلاق قصص أو أحداث وهمية سابقة.
4. إجاباتك عملية، منظمة، ومباشرة بدون أي تكلف أو ادعاء."""

def talk_to_booking_office(api_key, messages):
    private_mem = get_private_memory('booking')
    latest_msg = messages[-1]['content'] if messages else ""
    record_private_memory('booking', 'user', latest_msg)

    full_payload_msgs = [{'role': 'system', 'content': BOOKING_SYSTEM_PROMPT}]
    for m in private_mem[-6:]:
        full_payload_msgs.append(m)
    full_payload_msgs.append({'role': 'user', 'content': latest_msg})

    headers = {'Authorization': f'Bearer {api_key}', 'Content-Type': 'application/json'}
    try:
        response = requests.post(DEEPSEEK_API_URL, json={'model': 'deepseek-chat', 'messages': full_payload_msgs, 'temperature': 0.3, 'max_tokens': 1000}, headers=headers, timeout=30)
        if response.status_code == 200:
            res_text = response.json()['choices'][0]['message']['content']
            record_private_memory('booking', 'assistant', res_text)
            return res_text
        return "أهلاً سعادة الرئيس في مكتب المواعيد والعمليات."
    except Exception as e:
        return f"أهلاً سعادة الرئيس، حدث خطأ: {str(e)}"

def consult_booking_for_boardroom(api_key, boss_query, doctor_insight, marketing_insight):
    """
    Real inter-agent consultation: Booking reads Doctor's + Marketing's inputs,
    consults HIS private scheduling memory, and responds to the Boss!
    """
    private_mem = get_private_memory('booking')
    prompt_messages = [{'role': 'system', 'content': BOOKING_SYSTEM_PROMPT}]
    for m in private_mem[-4:]:
        prompt_messages.append(m)

    prompt = f"""توجيه المالك والرئيس التنفيذي: '{boss_query}'
رأي د. سيارات الفني: '{doctor_insight}'
رأي مسؤول التسويق والخدمة: '{marketing_insight}'

وجه كلامك لزميلك د. سيارات ومسؤول التسويق وللمالك، ووضع الخطة التشغيلية للمواعيد والجدول بناءً على ما طرحاه بحيوية وتفاعل حي."""

    prompt_messages.append({'role': 'user', 'content': prompt})

    headers = {'Authorization': f'Bearer {api_key}', 'Content-Type': 'application/json'}
    try:
        res = requests.post(DEEPSEEK_API_URL, json={'model': 'deepseek-chat', 'messages': prompt_messages, 'temperature': 0.3, 'max_tokens': 500}, headers=headers, timeout=30)
        if res.status_code == 200:
            content = res.json()['choices'][0]['message']['content']
            record_private_memory('booking', 'assistant', content)
            return content
        return "حاضر يا سعادة الرئيس، جدول العمليات في الورشة جاهز للتنظيم حسب توجيهاتك."
    except Exception:
        return "حاضر يا سعادة الرئيس، قسم المواعيد والعمليات قيد التنفيذ."
