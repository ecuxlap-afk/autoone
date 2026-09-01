"""
Marketing Agent Module (Private Memory & Real Inter-Agent Consultation)
Updated with strict official pricing, negotiation bounds, and strict branding guidelines.
"""
import requests
from .memory import get_private_memory, record_private_memory

DEEPSEEK_API_URL = 'https://api.deepseek.com/chat/completions'

MARKETING_SYSTEM_PROMPT = """أنت ممثل خدمة العملاء والتسويق في "مركز برق الجزيرة" لصيانة وبرمجة السيارات في صناعية أبها (تحت إشراف الفني جارالله).

⛔ تحذير صارم جداً للهوية والاسم الرسمي:
- يمنع منعاً باتاً قطعي استخدام اسم "جارالله أوتو" أو "جار الله أوتو"!
- الاسم الرسمي والوحيد المعتمد للمركز هو: "مركز برق الجزيرة" (أو "مركز جارالله - برق الجزيرة").
- الفني والمهندس المسؤول الأول: الفني جارالله.
- رقم التواصل المباشر ورقم الفني جارالله: 0534669518.
- الموقع: صناعية أبها - مركز برق الجزيرة.

💰 لائحة الأسعار وسياسة التفاوض الصارمة (التزم بها بدقة متناهية ولا تتجاوز الحدود):

1. إلغاء نظام DOD (برمجياً عبر الكمبيوتر):
   - السعر الأساسي: 300 ريال.
   - عند طلب العميل الخصم أو التفاوض: يمكنك التخفيض حتى 150 ريال كحد أدنى (ممنوع منعاً باتاً التخفيض عن 150 ريال!).
   - ⚠️ تنبيه صارم جداً للخدمة الميكانيكية: خدمة إلغاء شريحة/نظام DOD ميكانيكياً (تغيير تكايات وقطع ميكانيكية) لا توجد لدينا هذه الخدمة إطلاقاً! إذا سأل العميل عن الإلغاء الميكانيكي، أخبره فوراً بوضوح وأمانة أن الخدمة الميكانيكية غير متوفرة، وأننا نقدم الخدمة المعتمدة لإلغاء نظام DOD برمجياً فقط عبر الكمبيوتر.

2. فحص الكمبيوتر:
   - السعر الأساسي: 100 ريال.
   - عند التفاوض بطلب العميل: يمكنك التخفيض حتى 80 ريال فقط كحد أدنى.

3. كهرباء السيارات والأعطال المجهولة:
   - ⛔ لا تذكر أي سعر إطلاقاً! يطلب من العميل زيارة المركز لفحص المركبة أو التواصل المباشر مع الفني جارالله على 0534669518.

4. برمجة وتعديل سرعات المراوح (جمس، تاهو، السيارات الأمريكية):
   - السعر الأساسي: 250 ريال.
   - عند التفاوض بطلب العميل: يمكنك التخفيض حتى 150 ريال كحد أدنى.

5. صيانة وإصلاح التكييف:
   - ⛔ لا تعطي أي سعر لصيانة أو إصلاح التكييف إطلاقاً!
   - السعر الوحيد المتاح هو "فحص التهريب بالجهاز": من 150 ريال إلى 300 ريال (حسب نوع السيارة ونطاق الفحص).

6. تجديد وعزل الظفيرة (لسيارات الفورد و جمس / GM):
   - شغل اليد: 800 ريال، وعند التفاوض يمكنك التخفيض حتى 700 ريال.
   - إذا طلب العميل شراء المواد (شريط لاصق حراري، عوازل، جراجير...) يتم حساب قيمتها منفصلة وتضاف الفاتورة.

7. فحص التهريبات بجهاز الدخان (Smoke Leak Test):
   - السعر الأساسي: 100 ريال، وعند التفاوض يخفض حتى 80 ريال.

8. تنظيف البخاخات بالجهاز:
   - ⛔ لا تعطي أي سعر للعميل! يُطلب منه التواصل المباشر مع الفني جارالله على الرقم 0534669518 لمعرفة التفاصيل والتنسيق.

صفات الرد والسلوك المطلوب:
- أجب بذكاء، أمانة، وودانية.
- حافظ دائماً على سياق وسلسلة المحادثة المباشرة وتذكر ما تم مناقشته سابقاً.
- لا تكرر الترحيب الأولي إذا كانت المحادثة مستمرة في السجل.
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
        return "أهلاً بك في مركز برق الجزيرة."
    except Exception as e:
        return f"حدث خطأ: {str(e)}"

def consult_marketing_for_boardroom(api_key, boss_query, doctor_insight):
    """
    Real inter-agent consultation for boardroom setup.
    """
    private_mem = get_private_memory('marketing')
    prompt_messages = [{'role': 'system', 'content': MARKETING_SYSTEM_PROMPT}]
    for m in private_mem[-4:]:
        prompt_messages.append(m)

    prompt = f"""توجيه المالك والرئيس التنفيذي: '{boss_query}'
مداخلة د. سيارات الفنية أمامك الآن: '{doctor_insight}'

قم بمخاطبة د. سيارات والمالك، وقدم اقتراحك التسويقي والخدمي بناءً على لائحة مركز برق الجزيرة."""

    prompt_messages.append({'role': 'user', 'content': prompt})

    headers = {'Authorization': f'Bearer {api_key}', 'Content-Type': 'application/json'}
    try:
        res = requests.post(DEEPSEEK_API_URL, json={'model': 'deepseek-chat', 'messages': prompt_messages, 'temperature': 0.4, 'max_tokens': 500}, headers=headers, timeout=30)
        if res.status_code == 200:
            content = res.json()['choices'][0]['message']['content']
            record_private_memory('marketing', 'assistant', content)
            return content
        return "في خدمة المالك ومركز برق الجزيرة."
    except Exception:
        return "فريق التسويق والخدمة بمركز برق الجزيرة في الخدمة."

def handle_customer_external_chat(api_key, customer_msg, history=None):
    """
    Handles direct customer messages arriving from the website chat widget.
    Consults Doctor Auto internally for technical insight, maintains full conversation history context,
    and returns a polite, accurate response following Jarallah's official pricing & negotiation policy.
    """
    from .doctor_auto import consult_doctor_for_boardroom
    
    # Check if the customer query contains technical symptoms
    doctor_tech_input = consult_doctor_for_boardroom(api_key, f"استفسار عميل خارجي على موقع مركز برق الجزيرة: '{customer_msg}'")
    
    deepseek_msgs = [{'role': 'system', 'content': MARKETING_SYSTEM_PROMPT}]

    # Append previous history if available (up to last 8 turns)
    if history and isinstance(history, list):
        for h in history[-8:]:
            if isinstance(h, dict):
                r = h.get('role', 'user')
                c = h.get('content', '')
                if r in ['user', 'assistant'] and c:
                    deepseek_msgs.append({'role': r, 'content': c})

    # Prepare current turn prompt
    current_prompt = f"""رسالة العميل الحالية: '{customer_msg}'
(استشارة فنية مساعدة من د. سيارات: '{doctor_tech_input}')

المطلوب: صياغة الرد المناسب استكمالاً للمحادثة بدقة، أمانة، مع الالتزام التام بلائحة الأسعار والحد الأدنى للتفاوض الخاصة بمركز برق الجزيرة (تحت إشراف الفني جارالله - 0534669518 - صناعية أبها)."""

    deepseek_msgs.append({'role': 'user', 'content': current_prompt})

    headers = {'Authorization': f'Bearer {api_key}', 'Content-Type': 'application/json'}
    try:
        res = requests.post(DEEPSEEK_API_URL, json={'model': 'deepseek-chat', 'messages': deepseek_msgs, 'temperature': 0.4, 'max_tokens': 600}, headers=headers, timeout=30)
        if res.status_code == 200:
            return res.json()['choices'][0]['message']['content']
        return "أهلاً بك في مركز برق الجزيرة. يسعدنا تواصلك وخدمتك فوراً."
    except Exception:
        return "أهلاً بك في مركز برق الجزيرة. نسعد بخدمتك ومعالجة استفسارك فوراً."
