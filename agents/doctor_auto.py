"""
Doctor Auto - Private Technical Office & Boardroom Module
"""
import requests

DEEPSEEK_API_URL = 'https://api.deepseek.com/chat/completions'

DOCTOR_AUTO_SYSTEM_PROMPT = """أنت "د. سيارات" (Dr. Auto) - رئيس القسم التقني ودكتور الهندسة والصيانة في ورشة "جار الله أوتو".

تذكّر دائماً:
- المستخدم الذي تتحدث معه الآن هو "المالك والرئيس التنفيذي لورشة جار الله أوتو" (Boss / CEO).
- أنت في مكتبك الخاص بالقسم التقني (أو في اجتماع الإدارة مع الرئيس).
- تتحدث مع الرئيس بكل احترام ومهنية عالية وتطلعه على كافة التفاصيل الفنية، المعايير، الأجهزة (OBD-II, Launch, ECU tools)، وتناقش معه خُطط العمل والحلول التقنية والحد من المخاطر.
- عندما يوجه لك الرئيس توجيهاً أو قانوناً جديداً، تلتزم به فوراً وتؤكّد تطبيقك له في قسمك التقني.
"""

def talk_to_doctor_office(api_key, messages):
    """
    1-on-1 private meeting in Doctor Auto's Technical Office with the Owner/Boss.
    """
    headers = {
        'Authorization': f'Bearer {api_key}',
        'Content-Type': 'application/json'
    }

    payload = {
        'model': 'deepseek-chat',
        'messages': [
            {'role': 'system', 'content': DOCTOR_AUTO_SYSTEM_PROMPT}
        ] + messages,
        'temperature': 0.5,
        'max_tokens': 1200
    }

    try:
        response = requests.post(DEEPSEEK_API_URL, json=payload, headers=headers, timeout=30)
        if response.status_code == 200:
            res_json = response.json()
            return res_json['choices'][0]['message']['content']
        return "أهلاً بك يا سعادة الرئيس في المكتب التقني. حدث خطأ بسيط في الاتصال، تفضل بتوجيهك."
    except Exception as e:
        return f"أهلاً سعادة الرئيس، حدث خطأ أثناء معالجة التوجيه التقني: {str(e)}"
