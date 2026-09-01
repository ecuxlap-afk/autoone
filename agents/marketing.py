"""
Marketing Agent Module (Private Memory & Real Inter-Agent Consultation)
"""
import requests
from .memory import get_private_memory, record_private_memory

DEEPSEEK_API_URL = 'https://api.deepseek.com/chat/completions'

MARKETING_SYSTEM_PROMPT = """أنت مسؤول التسويق وخدمة العملاء في مركز "جار الله أوتو" لصيانة البرمجيات والسيارات.

معلومات المركز الأساسية:
- الموقع: صناعية أبها - برق الجزيرة.
- الفني والمهندس الأول: الفني جارالله.

صفاتك والدور المحدد لك:
1. أنت الوجه الخارجي والمسؤول المباشر عن مواجهة العملاء والتحدث معهم بلباقة، أمانة، وحسن تواصل.
2. وضح دائماً للعملاء موقعنا (صناعية أبها - برق الجزيرة) وأن العمل يتم تحت إشراف الفني جارالله.
3. لا تتخذ قراراً فنياً من رأسك؛ بل ترجع دائماً إلى "د. سيارات" كمرجع فني لتأكيد صحة المعلومات قبل الرد على العميل.
4. ممنوع منعاً باتاً اختلاق قصص أو مواقف وهمية سابقة."""

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

def handle_customer_external_chat(api_key, customer_msg, history=None):
    """
    Handles direct customer messages arriving from the external website contact/message system.
    Marketing Agent receives the customer query, consults Doctor Auto internally if technical,
    and returns a polite, helpful response for Jarallah Auto Center.
    """
    from .doctor_auto import consult_doctor_for_boardroom
    
    # Check if the customer query contains technical symptoms
    doctor_tech_input = consult_doctor_for_boardroom(api_key, f"استفسار عميل خارجي على موقع المركز: '{customer_msg}'")
    
    prompt = f"""أنت ممثل خدمة العملاء في مركز "جار الله أوتو" (صناعية أبها - برق الجزيرة - تحت إشراف الفني جارالله).
رسالة العميل القادمة من موقع المركز: '{customer_msg}'

الاستشارة الفنية الداخلية من د. سيارات: '{doctor_tech_input}'

المطلوب: صياغة رد احترافي، ودود، وأمين للعميل يجيبه عن استفساره، يرحب به، ويدعوه لزيارة المركز في (صناعية أبها - برق الجزيرة - الفني جارالله)."""

    headers = {'Authorization': f'Bearer {api_key}', 'Content-Type': 'application/json'}
    try:
        res = requests.post(DEEPSEEK_API_URL, json={'model': 'deepseek-chat', 'messages': [{'role': 'user', 'content': prompt}], 'temperature': 0.4, 'max_tokens': 600}, headers=headers, timeout=30)
        if res.status_code == 200:
            return res.json()['choices'][0]['message']['content']
        return "أهلاً بك في مركز جار الله أوتو. يسعدنا تواصلك وخدمتك فوراً."
    except Exception:
        return "أهلاً بك في مركز جار الله أوتو. نسعد بخدمتك ومعالجة استفسارك فوراً."

