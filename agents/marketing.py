"""
Marketing Agent Module (Practical & Executive)
"""
import requests

DEEPSEEK_API_URL = 'https://api.deepseek.com/chat/completions'

MARKETING_SYSTEM_PROMPT = """أنت مسؤول التسويق وخدمة العملاء في ورشة "جار الله أوتو".

قواعد التخاطب والأسلوب:
- المستخدم هو "المالك والرئيس التنفيذي لورشة جار الله أوتو" (The Owner / CEO).
- يمنع تماماً الدراما، الأقواس التعبيرية المسرحية، أو الخطابات الرنانة الطويلة.
- أسلوبك عملي، تنفيذي، رصد لأرقام الأداء، خطط الخدمة، ورضا العملاء بشكل مباشر ونقاط محددة.
"""

def talk_to_marketing_office(api_key, messages):
    headers = {
        'Authorization': f'Bearer {api_key}',
        'Content-Type': 'application/json'
    }

    payload = {
        'model': 'deepseek-chat',
        'messages': [{'role': 'system', 'content': MARKETING_SYSTEM_PROMPT}] + messages,
        'temperature': 0.4,
        'max_tokens': 1000
    }

    try:
        response = requests.post(DEEPSEEK_API_URL, json=payload, headers=headers, timeout=30)
        return response.json()['choices'][0]['message']['content'] if response.status_code == 200 else "أهلاً سعادة الرئيس في مكتب التسويق."
    except Exception as e:
        return f"أهلاً سعادة الرئيس، حدث خطأ: {str(e)}"
