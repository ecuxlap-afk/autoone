from flask import Flask, request, jsonify, render_template
from flask_cors import CORS
import os
from dotenv import load_dotenv
from agents.orchestrator import handle_hq_room_chat

load_dotenv()

app = Flask(__name__)
CORS(app)

def get_api_key(data=None):
    raw_key = ""
    if data and isinstance(data, dict) and data.get('api_key'):
        raw_key = data.get('api_key')
    else:
        raw_key = request.headers.get('X-Api-Key') or os.environ.get('DEEPSEEK_API_KEY', '')
    return raw_key.strip('\'" \t\r\n') if raw_key else ""

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/chat', methods=['POST'])
def chat():
    data = request.json or {}
    api_key = get_api_key(data)
    if not api_key:
        return jsonify({
            'error': 'الـ API Key غير مضبوط على السيرفر. يرجى إضافة DEEPSEEK_API_KEY في ملف .env أو إعدادات البيئة.',
            'status': 'error'
        }), 500

    try:
        messages = data.get('messages', [])
        room = data.get('room', 'boardroom')

        # Execute HQ Office / Boardroom Meeting Chat
        reply = handle_hq_room_chat(api_key, room, messages)

        if isinstance(reply, list):
            # Boardroom multi-agent separate responses
            return jsonify({
                'status': 'success',
                'room': room,
                'is_multi': True,
                'agent_replies': reply,
                'system_type': 'AutoOne Enterprise Boardroom'
            })
        else:
            # Single office response
            return jsonify({
                'status': 'success',
                'room': room,
                'is_multi': False,
                'reply': reply,
                'system_type': 'AutoOne Private Office'
            })

    except Exception as e:
        return jsonify({
            'error': f'خطأ في مقر العمل الرقمي: {str(e)}',
            'status': 'error'
        }), 500

@app.route('/api/customer/chat', methods=['POST'])
def customer_api_chat():
    """
    Public Customer Messaging API for external website integration.
    Accepts customer messages & conversation history from Jarallah Auto's chat widget.
    """
    data = request.json or {}
    api_key = get_api_key(data)
    if not api_key:
        return jsonify({'error': 'API Key not configured. Please add DEEPSEEK_API_KEY in .env or environment settings.', 'status': 'error'}), 500

    try:
        customer_msg = data.get('message', '') or data.get('text', '')
        history = data.get('history', [])
        if not customer_msg:
            return jsonify({'error': 'Message content is required', 'status': 'error'}), 400

        from agents.marketing import handle_customer_external_chat
        reply = handle_customer_external_chat(api_key, customer_msg, history=history)

        return jsonify({
            'status': 'success',
            'reply': reply,
            'center': 'Barq Al-Jazeera Center'
        })
    except Exception as e:
        return jsonify({'error': str(e), 'status': 'error'}), 500

@app.route('/health')
def health():
    api_key = get_api_key()
    return jsonify({
        'status': 'ok',
        'system': 'AutoOne Enterprise Virtual HQ',
        'api_key_set': bool(api_key)
    })

if __name__ == '__main__':
    port = int(os.environ.get('PORT', 5000))
    app.run(host='0.0.0.0', port=port, debug=False)
