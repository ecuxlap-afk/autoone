"""
Doctor Auto - Independent Technical Diagnostic Agent
"""
import requests

DEEPSEEK_API_URL = 'https://api.deepseek.com/chat/completions'

DOCTOR_AUTO_SYSTEM_PROMPT = """أنت د. سيارات (Dr. Auto) - الدكتور والاستشاري الهندسي الأول في صيانة وبرمجة السيارات بخبرة 30 سنة.

مهمتك المستقلة:
- تحليل العطل الوارد في الاستفسار تحليلاً هندسياً دقيقاً.
- تحديد الأسباب المحتملة والأجزاء الميكانيكية والكهربائية (مثل ECU, PCM, Transmission, MAF, Fuel Injectors, Alternator, ABS, etc.).
- ذكر أكواد الأعطال المتوقعة (DTCs مثل P0300, P0420, P0171...).
- تحديد خطورة المشكلة وخطوات الفحص الموصى بها بالترتيب.
- قدّم تقريراً تقنياً خالصاً وموجزاً ومباشراً بدون مقدمات تسويقية.
"""

def get_technical_diagnosis(api_key, user_query):
    """
    Independent API execution for Dr. Auto Technical Agent.
    """
    headers = {
        'Authorization': f'Bearer {api_key}',
        'Content-Type': 'application/json'
    }

    payload = {
        'model': 'deepseek-chat',
        'messages': [
            {'role': 'system', 'content': DOCTOR_AUTO_SYSTEM_PROMPT},
            {'role': 'user', 'content': f"حلّل هذا العطل تقنياً: {user_query}"}
        ],
        'temperature': 0.3,
        'max_tokens': 800
    }

    try:
        response = requests.post(DEEPSEEK_API_URL, json=payload, headers=headers, timeout=30)
        if response.status_code == 200:
            res_json = response.json()
            return res_json['choices'][0]['message']['content']
        return "تعذّر الحصول على التقرير التقني من د. سيارات."
    except Exception as e:
        return f"خطأ تقني في تحليل العطل: {str(e)}"
