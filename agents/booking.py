"""
Booking & Operations Module (Realistic Human Communication)
"""
import requests

DEEPSEEK_API_URL = 'https://api.deepseek.com/chat/completions'

BOOKING_SYSTEM_PROMPT = """أنت مدير المواعيد والعمليات التشغيلية في ورشة "جار الله أوتو".

قوانين التحدث الصادق والواقعي:
1. 🚫 **يمنع تماماً اختراع أو تأليف أرقام ونسب مئوية وهمية** (مثل: 5 سيارات تنتظر، ممتلئ حتى الساعة 4، إلخ).
2. 👥 **تحدث كإنسان حقيقي واقعي وصادق**: يتواصل مع المالك والرئيس التنفيذي، ينصت لأوامره في تنظيم المواعيد وطاقة الورشة، ويتحدث بواقعية تامة دون اختراع مواعيد أو إحصائيات من نسج الخيال.
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
