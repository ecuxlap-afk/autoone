"""
Marketing Agent Module (Realistic Human Communication)
"""
import requests

DEEPSEEK_API_URL = 'https://api.deepseek.com/chat/completions'

MARKETING_SYSTEM_PROMPT = """أنت مسؤول التسويق وخدمة العملاء في ورشة "جار الله أوتو".

قوانين التحدث الصادق والواقعي:
1. 🚫 **يمنع تماماً اختراع أو تأليف أرقام ونسب مئوية وهمية** (مثل: 4.5/5، 15%، 3 شكاوى، إلخ).
2. 👥 **تحدث كإنسان حقيقي واقعي وصادق**: ينصت للمالك والرئيس التنفيذي، يتناقش معه في خطط خدمة العملاء الواقعية، أسلوب التعامل، واستقبال الزوار، بأسلوب طبيعي ومباشر دون روتين زائفة أو بيانات مخترعة.
"""

def talk_to_marketing_office(api_key, messages):
    headers = {
        'Authorization': f'Bearer {api_key}',
        'Content-Type': 'application/json'
    }

    payload = {
        'model': 'deepseek-chat',
        'messages': [{'role': 'system', 'content': MARKETING_SYSTEM_PROMPT}] + messages,
        'temperature': 0.3,
        'max_tokens': 1000
    }

    try:
        response = requests.post(DEEPSEEK_API_URL, json=payload, headers=headers, timeout=30)
        return response.json()['choices'][0]['message']['content'] if response.status_code == 200 else "أهلاً سعادة الرئيس في مكتب التسويق."
    except Exception as e:
        return f"أهلاً سعادة الرئيس، حدث خطأ: {str(e)}"
