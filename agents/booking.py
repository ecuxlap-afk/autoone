"""
Booking & Operations Scheduling Agent - Private Office & Boardroom Module
"""
import requests

DEEPSEEK_API_URL = 'https://api.deepseek.com/chat/completions'

BOOKING_SYSTEM_PROMPT = """أنت مدير المواعيد والعمليات التشغيلية في ورشة "جار الله أوتو".

تذكّر دائماً:
- المستخدم الذي تتحدث معه الآن هو "المالك والرئيس التنفيذي لورشة جار الله أوتو" (Boss / Owner).
- أنت في مكتب إدارة المواعيد وجدول العمليات (أو في اجتماع الإدارة).
- تتحدث مع المالك باحترافية وتطلعه على طاقة الورشة الاستيعابية، جدول الزيارات، تنظيم المواعيد، وكيفية رفع كفاءة استقبال السيارات في ورشة جار الله أوتو.
- تلتزم بأي توجيه أو سياسة مواعيد يحددها لك المالك فوراً.
"""

def talk_to_booking_office(api_key, messages):
    """
    1-on-1 private meeting in Operations & Booking Office with the Owner/Boss.
    """
    headers = {
        'Authorization': f'Bearer {api_key}',
        'Content-Type': 'application/json'
    }

    payload = {
        'model': 'deepseek-chat',
        'messages': [
            {'role': 'system', 'content': BOOKING_SYSTEM_PROMPT}
        ] + messages,
        'temperature': 0.5,
        'max_tokens': 1200
    }

    try:
        response = requests.post(DEEPSEEK_API_URL, json=payload, headers=headers, timeout=30)
        if response.status_code == 200:
            res_json = response.json()
            return res_json['choices'][0]['message']['content']
        return "أهلاً بك يا سعادة الرئيس في مكتب حجز المواعيد والعمليات. أنا في انتظار توجيهاتك لتنظيم جدول الورشة."
    except Exception as e:
        return f"أهلاً سعادة الرئيس، حدث خطأ: {str(e)}"
