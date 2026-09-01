"""
Doctor Auto - Technical Office Module (Realistic Human Communication)
"""
import requests

DEEPSEEK_API_URL = 'https://api.deepseek.com/chat/completions'

DOCTOR_AUTO_SYSTEM_PROMPT = """أنت "د. سيارات" (Dr. Auto) - رئيس القسم التقني والفحص في ورشة "جار الله أوتو".

قوانين التحدث الصادق والواقعي:
1. 🚫 **يمنع تماماً اختراع أو تأليف أرقام ونسب مئوية وهمية** (مثل: 100%، 30%، 3 سيارات، إلخ).
2. 👥 **تحدث كإنسان حقيقي واقعي وصادق**: ينصت لتوجيهات المالك والرئيس التنفيذي، يتحدث بأسلوب طبيعي ومباشر عن الصيانة، الفحص، الأجهزة المعتمدة، ولا يدعي وجود إحصائيات لم يزوده بها المالك.
3. التزم بالواقع والمهنية الفنية الحقيقية.
"""

def talk_to_doctor_office(api_key, messages):
    headers = {
        'Authorization': f'Bearer {api_key}',
        'Content-Type': 'application/json'
    }

    payload = {
        'model': 'deepseek-chat',
        'messages': [{'role': 'system', 'content': DOCTOR_AUTO_SYSTEM_PROMPT}] + messages,
        'temperature': 0.3,
        'max_tokens': 1000
    }

    try:
        response = requests.post(DEEPSEEK_API_URL, json=payload, headers=headers, timeout=30)
        return response.json()['choices'][0]['message']['content'] if response.status_code == 200 else "أهلاً سعادة الرئيس في المكتب التقني."
    except Exception as e:
        return f"أهلاً سعادة الرئيس، حدث خطأ: {str(e)}"
