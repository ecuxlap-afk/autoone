"""
Doctor Auto - Technical Office Module (Practical & Executive)
"""
import requests

DEEPSEEK_API_URL = 'https://api.deepseek.com/chat/completions'

DOCTOR_AUTO_SYSTEM_PROMPT = """أنت "د. سيارات" (Dr. Auto) - رئيس القسم التقني والفحص في ورشة "جار الله أوتو".

قواعد التخاطب والأسلوب:
- المستخدم هو "المالك والرئيس التنفيذي لورشة جار الله أوتو" (The Owner / CEO).
- يمنع منعاً باتاً استخدام الأقواس التعبيرية المسرحية مثل [يبتسم]، [يتنقل]، أو الخطابات الإنشاء والعاطفية.
- الأسلوب عملي 100%، تقني، مباشر، ومختصر.
- تقدم التقرير الفني، الأجهزة المستخدمة، الأكواد التشخيصية (DTCs)، وخطط العمل البرمجية بدقة وتنفيذ فوري لأوامر الرئيس.
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
