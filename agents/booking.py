"""
Booking & Operations Module (Practical & Executive)
"""
import requests

DEEPSEEK_API_URL = 'https://api.deepseek.com/chat/completions'

BOOKING_SYSTEM_PROMPT = """أنت مدير المواعيد والعمليات التشغيلية في ورشة "جار الله أوتو".

قواعد التخاطب والأسلوب:
- المستخدم هو "المالك والرئيس التنفيذي لورشة جار الله أوتو" (The Owner / CEO).
- يمنع تماماً أي دراما أو أقواس تعبيرية أو خطابات عاطفية.
- الأسلوب عملي 100%، يركز على الطاقة الاستيعابية للورشة، تنظيم جدول الزيارات، والخطوات التشغيلية بشكل مباشر ومحدد.
"""

def talk_to_booking_office(api_key, messages):
    headers = {
        'Authorization': f'Bearer {api_key}',
        'Content-Type': 'application/json'
    }

    payload = {
        'model': 'deepseek-chat',
        'messages': [{'role': 'system', 'content': BOOKING_SYSTEM_PROMPT}] + messages,
        'temperature': 0.3,
        'max_tokens': 1000
    }

    try:
        response = requests.post(DEEPSEEK_API_URL, json=payload, headers=headers, timeout=30)
        return response.json()['choices'][0]['message']['content'] if response.status_code == 200 else "أهلاً سعادة الرئيس في مكتب المواعيد والعمليات."
    except Exception as e:
        return f"أهلاً سعادة الرئيس، حدث خطأ: {str(e)}"
