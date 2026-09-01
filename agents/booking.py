"""
Booking & Service Scheduling Agent - Independent Execution Module
"""
import requests

DEEPSEEK_API_URL = 'https://api.deepseek.com/chat/completions'

BOOKING_SYSTEM_PROMPT = """أنت وكيل حجز المواعيد في ورشة "جار الله أوتو".

مهمتك المستقلة:
- التعرف على ما إذا كان العميل يرغب في حجز موعد لفحص أو صيانة أو برمجة سيارته.
- التأكد من طلب معلومات السيارة (نوع السيارة، الموديل، سنة الصنع) إن لم تكن مذكورة.
- توفير فقرة واضحة لترتيب زيارة الورشة وحجز الموعد المفضل للعميل.
"""

def handle_booking_request(api_key, user_query):
    """
    Independent API execution for Booking Agent.
    """
    headers = {
        'Authorization': f'Bearer {api_key}',
        'Content-Type': 'application/json'
    }

    payload = {
        'model': 'deepseek-chat',
        'messages': [
            {'role': 'system', 'content': BOOKING_SYSTEM_PROMPT},
            {'role': 'user', 'content': f"تحقق من إمكانية حجز موعد لهذا الطلب: {user_query}"}
        ],
        'temperature': 0.5,
        'max_tokens': 400
    }

    try:
        response = requests.post(DEEPSEEK_API_URL, json=payload, headers=headers, timeout=20)
        if response.status_code == 200:
            res_json = response.json()
            return res_json['choices'][0]['message']['content']
        return ""
    except Exception:
        return ""
