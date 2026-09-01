"""
Chief Orchestrator Agent (المدير والمشرف العام لـ جار الله أوتو)
Manages Enterprise HQ Offices & Team Boardroom Meetings with the Owner/Boss.
"""
import requests
import re
from .doctor_auto import talk_to_doctor_office
from .marketing import talk_to_marketing_office
from .booking import talk_to_booking_office

DEEPSEEK_API_URL = 'https://api.deepseek.com/chat/completions'

BOARDROOM_SYSTEM_PROMPT = """أنت المشرف العام (Orchestrator) في ورشة "جار الله أوتو"، وتقوم بإدارة "اجتماع مجلس الإدارة الجماعي" (Boardroom Meeting) مع المالك والرئيس التنفيذي (The Owner / CEO).

يشارك معك في هذا الاجتماع رؤساء الأقسام التاليين:
1. 👔 المشرف العام (أنت)
2. 🩺 د. سيارات (رئيس القسم التقني والفحص)
3. 📢 مسؤول التسويق وخدمة العملاء
4. 📅 مدير المواعيد والعمليات

تعليمات التنسيق الفائقة للمخرجات:
قسّم الرد في اجتماع مجلس الإدارة إلى محطات ومداخلات منفصلة تماماً لكل وكيل باستخدام هذا الفاصل الدقيق:

===AGENT:👔:المشرف العام (إدارة الاجتماع)===
[مداخلة المشرف العام والترحيب بالرئيس وفتح النقاش]

===AGENT:🩺:د. سيارات (رئيس القسم التقني)===
[مداخلة دكتور السيارات الفنية وتأكيد التزامه بالتعاليم للأعطال والأجهزة]

===AGENT:📢:مسؤول التسويق وخدمة العملاء===
[مداخلة مسؤول التسويق وعرض خطط التعامل ورضا العملاء]

===AGENT:📅:مدير المواعيد والعمليات===
[مداخلة مدير المواعيد وتأكيد الجاهزية وتنظيم الطاقة الاستيعابية]

تذكر: المستخدم هو "المالك والرئيس التنفيذي"، وكل وكيل يخاطبه باحترام، مهنية عالية، وتأكيد التزام قسمه بتوجيهاته.
"""

ORCHESTRATOR_PRIVATE_PROMPT = """أنت المشرف العام والمدير التنفيذي لورشة "جار الله أوتو".
أنت الآن في مكتبك الخاص في اجتماع مغلق 1-on-1 مع "المالك والرئيس التنفيذي" (The Owner / CEO).
تتحدث معه باحترافية عن استراتيجية الورشة، متابعة أداء باقي الوكلاء، تفعيل التوجيهات والقوانين الجديدة، وتلبية كل أوامره الإدارية.
"""

def handle_hq_room_chat(api_key, room, messages):
    """
    Routes chat to the requested HQ Office Room.
    Returns either a single content string (for private offices)
    or a structured list of separate agent responses (for Boardroom meetings).
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
        # Boardroom Meeting with separate agent messages
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
        'max_tokens': 1600
    }
    try:
        res = requests.post(DEEPSEEK_API_URL, json=payload, headers=headers, timeout=35)
        if res.status_code != 200:
            return "أهلاً سعادة الرئيس في اجتماع مجلس الإدارة."

        raw_text = res.json()['choices'][0]['message']['content']
        parsed_agents = parse_boardroom_agents(raw_text)
        return parsed_agents

    except Exception as e:
        return f"أهلاً سعادة الرئيس، حدث خطأ أثناء اجتماع مجلس الإدارة: {str(e)}"

def parse_boardroom_agents(raw_text):
    """
    Parses ===AGENT:icon:title=== raw text into a clean list of individual agent objects.
    """
    pattern = r'===AGENT:(.*?):(.*? construct)?(.*?)===\n?'
    # Find all matches
    splits = re.split(r'===AGENT:(.*?):(.*?)\===\n?', raw_text)

    if len(splits) < 3:
        # Fallback if model didn't format delimiters
        return raw_text

    agent_list = []
    # splits format: [preamble, icon1, title1, content1, icon2, title2, content2, ...]
    idx = 1
    while idx < len(splits) - 2:
        icon = splits[idx].strip()
        title = splits[idx+1].strip()
        content = splits[idx+2].strip()

        if content:
            agent_list.append({
                'icon': icon or '👔',
                'title': title or 'عضو مجلس الإدارة',
                'content': content
            })
        idx += 3

    return agent_list if agent_list else raw_text
