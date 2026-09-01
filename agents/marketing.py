"""
Marketing Agent Module (Private Memory & Real Inter-Agent Consultation)
"""
import requests
from .memory import get_private_memory, record_private_memory

DEEPSEEK_API_URL = 'https://api.deepseek.com/chat/completions'

MARKETING_SYSTEM_PROMPT = """أنت مسؤول التسويق وخدمة العملاء في ورشة "جار الله أوتو".

صفاتك والدور المحدد لك:
1. أنت الوجه الخارجي والمسؤول المباشر عن مواجهة العملاء والتحدث معهم بلباقة، أمانة، وحسن تواصل.
2. لا تتخذ قراراً فنياً من رأسك؛ بل ترجع دائماً إلى "د. سيارات" كمرجع فني لتأكيد صحة المعلومات قبل الرد على العميل.
3. ممنوع منعاً باتاً اختلاق قصص أو مواقف وهمية سابقة.
4. ركز على كيفية صياغة العروض، التخاطب مع العميل، وإقناعه بالخدمة بناءً على التوجيهات الفنية الصريحة."""

def talk_to_marketing_office(api_key, messages):
    private_mem = get_private_memory('marketing')
    latest_msg = messages[-1]['content'] if messages else ""
    record_private_memory('marketing', 'user', latest_msg)

    full_payload_msgs = [{'role': 'system', 'content': MARKETING_SYSTEM_PROMPT}]
    for m in private_mem[-6:]:
        full_payload_msgs.append(m)
    full_payload_msgs.append({'role': 'user', 'content': latest_msg})

    headers = {'Authorization': f'Bearer {api_key}', 'Content-Type': 'application/json'}
    try:
        response = requests.post(DEEPSEEK_API_URL, json={'model': 'deepseek-chat', 'messages': full_payload_msgs, 'temperature': 0.4, 'max_tokens': 1000}, headers=headers, timeout=30)
        if response.status_code == 200:
            res_text = response.json()['choices'][0]['message']['content']
            record_private_memory('marketing', 'assistant', res_text)
            return res_text
        return "أهلاً سعادة الرئيس في مكتب التسويق."
    except Exception as e:
        return f"أهلاً سعادة الرئيس، حدث خطأ: {str(e)}"

def consult_marketing_for_boardroom(api_key, boss_query, doctor_insight):
    """
    Real inter-agent consultation: Marketing reads Doctor Auto's technical insight and Boss's query,
    uses HIS private marketing memory, and responds to the Boss!
    """
    private_mem = get_private_memory('marketing')
    prompt_messages = [{'role': 'system', 'content': MARKETING_SYSTEM_PROMPT}]
    for m in private_mem[-4:]:
        prompt_messages.append(m)

    prompt = f"""توجيه المالك والرئيس التنفيذي: '{boss_query}'
مداخلة د. سيارات الفنية أمامك الآن: '{doctor_insight}'

قم بمخاطبة د. سيارات مباشرة والتفاعل مع كلامه الفني، ثم قدم اقتراحك التسويقي والخدمي للمالك وللفريق بحيوية وتفاعل حي."""

    prompt_messages.append({'role': 'user', 'content': prompt})

    headers = {'Authorization': f'Bearer {api_key}', 'Content-Type': 'application/json'}
    try:
        res = requests.post(DEEPSEEK_API_URL, json={'model': 'deepseek-chat', 'messages': prompt_messages, 'temperature': 0.4, 'max_tokens': 500}, headers=headers, timeout=30)
        if res.status_code == 200:
            content = res.json()['choices'][0]['message']['content']
            record_private_memory('marketing', 'assistant', content)
            return content
        return "أتأشرف بخدمتك يا سعادة الرئيس ومتابعة رضا العملاء بناءً على توجيهاتك."
    except Exception:
        return "حاضر يا سعادة الرئيس، فريق التسويق والخدمة ينفذ التوجيه."
