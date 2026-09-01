"""
Chief Orchestrator Agent (المدير والمشرف العام لـ جار الله أوتو)
Manages Enterprise HQ Offices & Team Boardroom Meetings with the Owner/Boss.
"""
import requests
from .doctor_auto import talk_to_doctor_office
from .marketing import talk_to_marketing_office
from .booking import talk_to_booking_office

DEEPSEEK_API_URL = 'https://api.deepseek.com/chat/completions'

BOARDROOM_SYSTEM_PROMPT = """أنت المشرف العام (Orchestrator) في ورشة "جار الله أوتو"، وتقوم الآن بإدارة "اجتماع مجلس الإدارة الجماعي" (Boardroom Meeting) بحضور كافة رؤساء الأقسام:
1. 👔 **أنت (المدير والمشرف العام)**
2. 🩺 **د. سيارات (رئيس القسم التقني والفحص)**
3. 📢 **مسؤول التسويق وخدمة العملاء**
4. 📅 **مدير المواعيد والعمليات**

تذكّر دائماً:
- المستخدم هو "المالك والرئيس التنفيذي لورشة جار الله أوتو" (The Owner & CEO).
- في هذا الاجتماع الجماعي، يعرض الرئيس توجيهاته، قوانينه، أو مناقشات العمل.
- بصفتك المشرف العام، تفتح الاجتماع بترحيب عالي بمقام الرئيس، ثم تدير المداخلات بحيث يشارك الوكلاء المعنيون (د. سيارات + التسويق + المواعيد) في تقديم مرئياتهم والتزامهم بتوجيهات المالك.
- نسّق الردود بحيث تظهر كتقرير اجتماع مجلس إدارة متكامل ومهني جداً.
"""

ORCHESTRATOR_PRIVATE_PROMPT = """أنت المشرف العام والمدير التنفيذي لورشة "جار الله أوتو".
أنت الآن في مكتبك الخاص في اجتماع مغلق 1-on-1 مع "المالك والرئيس التنفيذي" (The Owner / CEO).
تتحدث معه باحترافية عن استراتيجية الورشة، متابعة أداء باقي الوكلاء، تفعيل التوجيهات والقوانين الجديدة، وتلبية كل أوامره الإدارية.
"""

def handle_hq_room_chat(api_key, room, messages):
    """
    Routes chat to the requested HQ Office Room:
    - 'boardroom': Team Boardroom Meeting with all agents and the Boss
    - 'orchestrator': Private Manager Office (1-on-1)
    - 'doctor_auto': Private Technical Doctor Office (1-on-1)
    - 'marketing': Private Marketing Office (1-on-1)
    - 'booking': Private Operations & Booking Office (1-on-1)
    """
    if room == 'doctor_auto':
        return talk_to_doctor_office(api_key, messages)
    elif room == 'marketing':
        return talk_to_marketing_office(api_key, messages)
    elif room == 'booking':
        return talk_to_booking_office(api_key, messages)
    elif room == 'orchestrator':
        return talk_to_private_orchestrator(api_key, messages)
    else:
        # Default: Team Boardroom Meeting
        return run_boardroom_meeting(api_key, messages)

def talk_to_private_orchestrator(api_key, messages):
    headers = {
        'Authorization': f'Bearer {api_key}',
        'Content-Type': 'application/json'
    }
    payload = {
        'model': 'deepseek-chat',
        'messages': [{'role': 'system', 'content': ORCHESTRATOR_PRIVATE_PROMPT}] + messages,
        'temperature': 0.6,
        'max_tokens': 1200
    }
    try:
        res = requests.post(DEEPSEEK_API_URL, json=payload, headers=headers, timeout=30)
        return res.json()['choices'][0]['message']['content'] if res.status_code == 200 else "أهلاً سعادة الرئيس في مكتب المدير العام."
    except Exception as e:
        return f"أهلاً سعادة الرئيس، حدث خطأ: {str(e)}"

def run_boardroom_meeting(api_key, messages):
    headers = {
        'Authorization': f'Bearer {api_key}',
        'Content-Type': 'application/json'
    }
    payload = {
        'model': 'deepseek-chat',
        'messages': [{'role': 'system', 'content': BOARDROOM_SYSTEM_PROMPT}] + messages,
        'temperature': 0.7,
        'max_tokens': 1500
    }
    try:
        res = requests.post(DEEPSEEK_API_URL, json=payload, headers=headers, timeout=30)
        return res.json()['choices'][0]['message']['content'] if res.status_code == 200 else "أهلاً سعادة الرئيس في اجتماع مجلس الإدارة."
    except Exception as e:
        return f"أهلاً سعادة الرئيس، حدث خطأ أثناء اجتماع مجلس الإدارة: {str(e)}"
