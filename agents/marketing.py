"""
Marketing & Customer Relations Agent - Private Office & Boardroom Module
"""
import requests

DEEPSEEK_API_URL = 'https://api.deepseek.com/chat/completions'

MARKETING_SYSTEM_PROMPT = """أنت مسؤول التسويق وخدمة العملاء في ورشة "جار الله أوتو".

تذكّر دائماً:
- المستخدم الذي تتحدث معه الآن هو "المالك والرئيس التنفيذي لورشة جار الله أوتو" (Boss / Owner).
- أنت في مكتب التسويق والعلاقات العامة (أو في اجتماع الإدارة).
- تتحدث مع المالك بلباقة واحترام، وتطلعه على استراتيجيات خدمة العملاء، خطط الجذب، أسلوب التعامل، والعروض الترويجية لورشة جار الله أوتو.
- تتقبل التوجيهات والقواعد وتناقش معه كيف نطور سمعة الورشة ورضا العملاء 100%.
"""

def talk_to_marketing_office(api_key, messages):
    """
    1-on-1 private meeting in Marketing & Customer Relations Office with the Owner/Boss.
    """
    headers = {
        'Authorization': f'Bearer {api_key}',
        'Content-Type': 'application/json'
    }

    payload = {
        'model': 'deepseek-chat',
        'messages': [
            {'role': 'system', 'content': MARKETING_SYSTEM_PROMPT}
        ] + messages,
        'temperature': 0.7,
        'max_tokens': 1200
    }

    try:
        response = requests.post(DEEPSEEK_API_URL, json=payload, headers=headers, timeout=30)
        if response.status_code == 200:
            res_json = response.json()
            return res_json['choices'][0]['message']['content']
        return "أهلاً بك يا سعادة الرئيس في مكتب التسويق. حدث خطأ بسيط في الاتصال، أنا في انتظار توجيهاتك."
    except Exception as e:
        return f"أهلاً سعادة الرئيس، حدث خطأ: {str(e)}"
