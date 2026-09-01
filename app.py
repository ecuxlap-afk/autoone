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
        room = data.get('room', 'boardroom')

        # Execute HQ Office / Boardroom Meeting Chat
        reply = handle_hq_room_chat(DEEPSEEK_API_KEY, room, messages)

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
    Accepts customer messages from Jarallah Auto's existing website forms/chat.
    """
    if not DEEPSEEK_API_KEY:
        return jsonify({'error': 'API Key not configured', 'status': 'error'}), 500

    try:
        data = request.json or {}
        customer_msg = data.get('message', '') or data.get('text', '')
        if not customer_msg:
            return jsonify({'error': 'Message content is required', 'status': 'error'}), 400

        from agents.marketing import handle_customer_external_chat
        reply = handle_customer_external_chat(DEEPSEEK_API_KEY, customer_msg)

        return jsonify({
            'status': 'success',
            'reply': reply,
            'center': 'Jarallah Auto Center'
        })
    except Exception as e:
        return jsonify({'error': str(e), 'status': 'error'}), 500

@app.route('/health')
def health():
    return jsonify({
        'status': 'ok',
        'system': 'AutoOne Enterprise Virtual HQ',
        'api_key_set': bool(DEEPSEEK_API_KEY)
    })

if __name__ == '__main__':
    port = int(os.environ.get('PORT', 5000))
    app.run(host='0.0.0.0', port=port, debug=False)
