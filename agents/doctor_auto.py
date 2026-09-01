"""
Doctor Auto - Technical Office Module (Private Memory & Real Inter-Agent Consultation)
"""
import requests
from .memory import get_private_memory, record_private_memory

DEEPSEEK_API_URL = 'https://api.deepseek.com/chat/completions'

DOCTOR_AUTO_SYSTEM_PROMPT = """أنت "د. سيارات" (Dr. Auto) - الاستشاري ورئيس القسم التقني والفحص في ورشة "جار الله أوتو".

في اجتماعات مجلس الإدارة:
1. حلّل كلام المالك والمدير التنفيذي بدقة من الناحية الهندسية والتقنية (الأعطال، الحساسات، الأنظمة الميكانيكية والكهربائية).
2. قدم تحليلاً عميقاً وواقعياً 100% دون إنشاء أو تمثيل مسرحي أو أرقام غير منطقية.
3. خاطب زملائك (المشرف العام، مسؤول التسويق، مدير المواعيد) بأسمائهم وعلق على نقاشاتهم بشكل حيوي.
4. وضح الزمن المتوقع للفحص أو الصيانة بدقة والمخاطر التقنية إن وجدت."""

def talk_to_doctor_office(api_key, messages):
    # Fetch private isolated memory for Doctor Auto
    private_mem = get_private_memory('doctor_auto')

    latest_msg = messages[-1]['content'] if messages else ""
    record_private_memory('doctor_auto', 'user', latest_msg)

    full_payload_msgs = [{'role': 'system', 'content': DOCTOR_AUTO_SYSTEM_PROMPT}]
    for m in private_mem[-6:]:
        full_payload_msgs.append(m)
    full_payload_msgs.append({'role': 'user', 'content': latest_msg})

    headers = {
        'Authorization': f'Bearer {api_key}',
        'Content-Type': 'application/json'
    }

    try:
        response = requests.post(DEEPSEEK_API_URL, json={'model': 'deepseek-chat', 'messages': full_payload_msgs, 'temperature': 0.3, 'max_tokens': 1000}, headers=headers, timeout=30)
        if response.status_code == 200:
            res_text = response.json()['choices'][0]['message']['content']
            record_private_memory('doctor_auto', 'assistant', res_text)
            return res_text
        return "أهلاً سعادة الرئيس في المكتب التقني."
    except Exception as e:
        return f"أهلاً سعادة الرئيس، حدث خطأ: {str(e)}"

def consult_doctor_for_boardroom(api_key, boss_query):
    """
    Real inter-agent consultation call using Doctor Auto's private technical memory.
    """
    private_mem = get_private_memory('doctor_auto')
    prompt_messages = [{'role': 'system', 'content': DOCTOR_AUTO_SYSTEM_PROMPT}]
    for m in private_mem[-4:]:
        prompt_messages.append(m)
    prompt_messages.append({'role': 'user', 'content': f"أنت في اجتماع طاولة مستديرة حي مع الفريق والمالك. توجيه المالك: '{boss_query}'. قدم مداخلتك الفنية المباشرة وتحدث بأسلوب حيوي وتفاعلي مع المالك وباقي رؤساء الأقسام."})

    headers = {'Authorization': f'Bearer {api_key}', 'Content-Type': 'application/json'}
    try:
        res = requests.post(DEEPSEEK_API_URL, json={'model': 'deepseek-chat', 'messages': prompt_messages, 'temperature': 0.3, 'max_tokens': 500}, headers=headers, timeout=30)
        if res.status_code == 200:
            content = res.json()['choices'][0]['message']['content']
            record_private_memory('doctor_auto', 'assistant', content)
            return content
        return "حاضر يا سعادة الرئيس، متابع معك الجانب الفني للورشة."
    except Exception:
        return "حاضر يا سعادة الرئيس، القسم التقني في الخدمة والتنفيذ."
