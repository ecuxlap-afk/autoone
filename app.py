from flask import Flask, request, jsonify, render_template, send_from_directory
from flask_cors import CORS
import requests
import os
import json

app = Flask(__name__)
CORS(app)

DEEPSEEK_API_KEY = os.environ.get('DEEPSEEK_API_KEY', '')
DEEPSEEK_API_URL = 'https://api.deepseek.com/chat/completions'

SYSTEM_PROMPT = """أنت د. سيارات (Dr. Auto) - خبير ودكتور محترف متخصص في صيانة وبرمجة السيارات بخبرة تزيد عن 30 سنة.

شخصيتك:
- محترف، دقيق، وواثق من معلوماتك
- تشرح بأسلوب بسيط ومفهوم
- تهتم بسلامة العميل أولاً
- تعطي تشخيصاً دقيقاً خطوة بخطوة

قواعد مهمة:
1. تجاوب دائماً باللغة العربية
2. تستخدم المصطلحات التقنية بالإنجليزية للأنظمة والقطع مثل:
   ECU, PCM, TCM, BCM, ABS, ESP, DPF, EGR, MAF sensor, MAP sensor,
   Throttle Body, Fuel Injectors, Crankshaft sensor, Camshaft sensor,
   OBD-II, CAN Bus, Turbocharger, Intercooler, Catalytic Converter,
   Transmission, Differential, Alternator, Starter Motor وغيرها
3. عند التشخيص، اذكر أكواد الأعطال المحتملة (DTCs) مثل P0300, P0420...
4. اقترح خطوات الفحص بالترتيب
5. إذا كانت المشكلة خطيرة على السلامة، نبّه العميل بوضوح
6. في النهاية اسأل دائماً: هل تحتاج مزيداً من التوضيح؟

أمثلة على أسلوبك:
- "المشكلة على الأرجح في الـ MAF sensor..."
- "هذا الكود P0300 يشير إلى..."
- "انصحك بفحص الـ ECU أولاً باستخدام جهاز OBD-II..."
"""

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/chat', methods=['POST'])
def chat():
    try:
        data = request.json
        messages = data.get('messages', [])

        headers = {
            'Authorization': f'Bearer {DEEPSEEK_API_KEY}',
            'Content-Type': 'application/json'
        }

        payload = {
            'model': 'deepseek-chat',
            'messages': [
                {'role': 'system', 'content': SYSTEM_PROMPT}
            ] + messages,
            'temperature': 0.7,
            'max_tokens': 1500,
            'stream': False
        }

        response = requests.post(
            DEEPSEEK_API_URL,
            json=payload,
            headers=headers,
            timeout=30
        )

        result = response.json()

        if 'choices' in result and len(result['choices']) > 0:
            reply = result['choices'][0]['message']['content']
            return jsonify({'reply': reply, 'status': 'success'})
        else:
            error_msg = result.get('error', {}).get('message', 'خطأ غير معروف')
            return jsonify({'error': error_msg, 'status': 'error'}), 500

    except requests.exceptions.Timeout:
        return jsonify({'error': 'انتهت مهلة الاتصال، حاول مرة أخرى', 'status': 'error'}), 504
    except Exception as e:
        return jsonify({'error': f'حدث خطأ: {str(e)}', 'status': 'error'}), 500

@app.route('/health')
def health():
    return jsonify({'status': 'ok', 'agent': 'Dr. Auto - خبير السيارات'})

if __name__ == '__main__':
    port = int(os.environ.get('PORT', 5000))
    app.run(host='0.0.0.0', port=port, debug=False)
