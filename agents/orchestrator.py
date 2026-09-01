"""
Chief Orchestrator Agent (المدير والمشرف العام لـ جار الله أوتو)
Real human-like, realistic, direct conversation with the Owner/Boss.
NO FAKE STATS, NO INVENTED NUMBERS, NO CORPORATE FANTASY.
"""
import requests
import re
from .doctor_auto import talk_to_doctor_office
from .marketing import talk_to_marketing_office
from .booking import talk_to_booking_office

DEEPSEEK_API_URL = 'https://api.deepseek.com/chat/completions'

BOARDROOM_SYSTEM_PROMPT = """أنت المشرف العام في ورشة "جار الله أوتو"، وتدير اجتماع مجلس الإدارة مع المالك والرئيس التنفيذي (The Owner / CEO).

قوانين الصدق والواقعية المشددة:
1. 🚫 **يمنع منعاً باتاً اختراع أو تأليف أرقام ونسب مئوية وهمية** (مثل: 78%، 30%، 4.5/5، أو اختراع أعداد سيارات وشكاوى من رأسك).
2. 👥 **التحدث كبشر حقيقيين واقعيين 100%**: ينصت الفريق لتوجيهات المالك مباشرة، يناقش خطوات العمل الحقيقية، يطلب البيانات الحقيقية من المالك إن لزم الأمر، ويتفاعل بأسلوب صادق وواقعي دون أي كلام إنشائي أو دراما أو أرقام مفبركة.

يشارك في هذا الاجتماع رؤساء الأقسام التاليين:
1. 👔 المشرف العام (أنت)
2. 🩺 د. سيارات (رئيس القسم التقني والفحص)
3. 📢 مسؤول التسويق وخدمة العملاء
4. 📅 مدير المواعيد والعمليات

تعليمات التنسيق للمخرجات:
قسّم الرد في اجتماع مجلس الإدارة إلى مداخلات واقعية وصادقة لكل وكيل باستخدام هذا الفاصل الدقيق:

===AGENT:👔:المشرف العام (إدارة الاجتماع)===
[مداخلتك المباشرة والواقعية كرئيس فريق يتناقش مع المالك]

===AGENT:🩺:د. سيارات (رئيس القسم التقني)===
[مداخلة دكتور السيارات التقنية الصادقة والواقعية حول الفحص والعمل]

===AGENT:📢:مسؤول التسويق وخدمة العملاء===
[مداخلة مسؤول التسويق الواقعية حول التواصل والخدمة دون أرقام مخترعة]

===AGENT:📅:مدير المواعيد والعمليات===
[مداخلة مدير المواعيد الواقعية حول التنظيم المباشر]

تذكر: كُونوا أناس حقيقيين، واقعيين، صادقين، ينفذون توجيهات المالك بدون تأليف أو رسميات زائفة.
"""

ORCHESTRATOR_PRIVATE_PROMPT = """أنت المشرف العام لورشة "جار الله أوتو" في اجتماع خاص مغلق مع المالك والرئيس التنفيذي (The Owner / CEO).
تتحدث معه كإنسان حقيقي واقعي وصادق 100%. لا تخترع أرقاماً أو نسباً وهمية من عندك. ينصت لأوامر المالك وينفذها بجدية وواقعية.
"""

def handle_hq_room_chat(api_key, room, messages):
    if room == 'doctor_auto':
        return talk_to_doctor_office(api_key, messages)
    elif room == 'marketing':
        return talk_to_marketing_office(api_key, messages)
    elif room == 'booking':
        return talk_to_booking_office(api_key, messages)
    elif room == 'orchestrator':
        return talk_to_private_orchestrator(api_key, messages)
    else:
        return run_boardroom_meeting(api_key, messages)

def talk_to_private_orchestrator(api_key, messages):
    headers = {
        'Authorization': f'Bearer {api_key}',
        'Content-Type': 'application/json'
    }
    payload = {
        'model': 'deepseek-chat',
        'messages': [{'role': 'system', 'content': ORCHESTRATOR_PRIVATE_PROMPT}] + messages,
        'temperature': 0.3,
        'max_tokens': 1000
    }
    try:
        res = requests.post(DEEPSEEK_API_URL, json=payload, headers=headers, timeout=30)
        return res.json()['choices'][0]['message']['content'] if res.status_code == 200 else "أهلاً سعادة الرئيس. تفضل بتوجيهك."
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
        'temperature': 0.3,
        'max_tokens': 1500
    }
    try:
        res = requests.post(DEEPSEEK_API_URL, json=payload, headers=headers, timeout=35)
        if res.status_code != 200:
            return "أهلاً سعادة الرئيس في اجتماع مجلس الإدارة."

        raw_text = res.json()['choices'][0]['message']['content']
        return parse_boardroom_agents(raw_text)

    except Exception as e:
        return f"أهلاً سعادة الرئيس، حدث خطأ أثناء اجتماع مجلس الإدارة: {str(e)}"

def parse_boardroom_agents(raw_text):
    splits = re.split(r'===AGENT:(.*?):(.*?)\===\n?', raw_text)

    if len(splits) < 3:
        return raw_text

    agent_list = []
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
