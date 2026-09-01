from flask import Flask, request, jsonify, render_template
from flask_cors import CORS
import os
from agents.orchestrator import handle_hq_room_chat

app = Flask(__name__)
CORS(app)

DEEPSEEK_API_KEY = os.environ.get('DEEPSEEK_API_KEY', '')

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/chat', methods=['POST'])
def chat():
    if not DEEPSEEK_API_KEY:
        return jsonify({
            'error': 'الـ API Key غير مضبوط على السيرفر. تواصل مع المسؤول.',
            'status': 'error'
        }), 500

    try:
        data = request.json or {}
        messages = data.get('messages', [])
        room = data.get('room', 'boardroom') # Default to Boardroom meeting with Boss

        # Execute HQ Office / Boardroom Meeting Chat
        reply = handle_hq_room_chat(DEEPSEEK_API_KEY, room, messages)

        return jsonify({
            'reply': reply,
            'status': 'success',
            'room': room,
            'system_type': 'AutoOne Enterprise Virtual HQ'
        })

    except Exception as e:
        return jsonify({
            'error': f'خطأ في مقر العمل الرقمي: {str(e)}',
            'status': 'error'
        }), 500

@app.route('/health')
def health():
    return jsonify({
        'status': 'ok',
        'system': 'AutoOne Enterprise Virtual HQ',
        'api_key_set': bool(DEEPSEEK_API_KEY),
        'headquarters_rooms': [
            'Executive Boardroom (غرفة الاجتماعات الجماعية)',
            'Chief Orchestrator Private Office (مكتب المشرف العام)',
            'Doctor Auto Technical Office (مكتب دكتور السيارات)',
            'Marketing & Customer Service Office (مكتب التسويق والعملاء)',
            'Operations & Booking Office (مكتب المواعيد والعمليات)'
        ]
    })

if __name__ == '__main__':
    port = int(os.environ.get('PORT', 5000))
    app.run(host='0.0.0.0', port=port, debug=False)
