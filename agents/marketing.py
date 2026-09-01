"""
Marketing Agent Module (Private Memory & Real Inter-Agent Consultation)
"""
import requests
from .memory import get_private_memory, record_private_memory

DEEPSEEK_API_URL = 'https://api.deepseek.com/chat/completions'

MARKETING_SYSTEM_PROMPT = """أنت مسؤول التسويق وخدمة العملاء في ورشة "جار الله أوتو".

ذاكرتك الخاصة وحريتك:
- لديك ذاكرة العلاقات العامة والتسويق الخاصة بك المحفوظة من لقاءاتك السابقة مع المالك.
- تتناقش مع المالك والرئيس التنفيذي (The Owner / CEO) بواقعية تامة وصدق.
- عندما يعطي دكتور السيارات رأيه الفني، تبني عليه وتناقش مع المالك أسلوب تقديم الخدمة للعميل والمتابعة بأسلوب واقعي وصادق 100% دون أرقام مفبركة.
"""

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
مداخلة د. سيارات الفنية في الاجتماع: '{doctor_insight}'

من واقع ذاكرتك الخاصة بخدمة العملاء، قدم مداخلتك للتفاعل مع توجيه المالك ورأي د. سيارات بواقعية وبدون أرقام وهمية."""

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
