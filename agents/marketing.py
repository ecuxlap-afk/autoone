"""
Marketing & Customer Service Agent - Independent Execution Module
"""
import requests

DEEPSEEK_API_URL = 'https://api.deepseek.com/chat/completions'

MARKETING_SYSTEM_PROMPT = """أنت وكيل التسويق وخدمة العملاء لورشة "جار الله أوتو" (AutoOne).

مهمتك المستقلة:
- الترحيب بالعميل والرد عليه بأعلى مستويات اللباقة، الاحترام، والود.
- أخذ التقرير التقني المقدم من (د. سيارات) وعرضه للعميل بطريقة مريحة، مفهومة، ومطمئنة.
- التأكيد على تميز ورشة "جار الله أوتو" في الصيانة والبرمجة وحرصها على سلامة العميل.
- دمج التقرير التقني والمصطلحات الإنجليزية بشكل احترافي وجذاب.
"""

def format_customer_response(api_key, user_query, technical_diagnosis):
    """
    Independent API execution for Marketing & Customer Service Agent.
    """
    headers = {
        'Authorization': f'Bearer {api_key}',
        'Content-Type': 'application/json'
    }

    user_content = f"""استفسار العميل: {user_query}

تقرير د. سيارات التقني:
{technical_diagnosis}

صغ رد خدمة العملاء والتسويق النهائي للعميل بناءً على التقرير التقني أعلاه."""

    payload = {
        'model': 'deepseek-chat',
        'messages': [
            {'role': 'system', 'content': MARKETING_SYSTEM_PROMPT},
            {'role': 'user', 'content': user_content}
        ],
        'temperature': 0.7,
        'max_tokens': 1000
    }

    try:
        response = requests.post(DEEPSEEK_API_URL, json=payload, headers=headers, timeout=30)
        if response.status_code == 200:
            res_json = response.json()
            return res_json['choices'][0]['message']['content']
        return technical_diagnosis
    except Exception:
        return technical_diagnosis
