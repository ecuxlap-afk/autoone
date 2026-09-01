from flask import Flask, request, jsonify, render_template
from flask_cors import CORS
import os
from agents.orchestrator import process_user_request

app = Flask(__name__)
CORS(app)

DEEPSEEK_API_KEY = os.environ.get('DEEPSEEK_API_KEY', '')

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/chat', methods=['POST'])
def chat():
    # Verify API key is set
    if not DEEPSEEK_API_KEY:
        return jsonify({
            'error': 'الـ API Key غير مضبوط على السيرفر. تواصل مع المسؤول.',
            'status': 'error'
        }), 500

    try:
        data = request.json
        messages = data.get('messages', [])

        # Execute Multi-Agent Orchestrator Pipeline
        reply = process_user_request(DEEPSEEK_API_KEY, messages)

        return jsonify({
            'reply': reply,
            'status': 'success',
            'system_type': 'Multi-Agent Network'
        })

    except Exception as e:
        return jsonify({
            'error': f'خطأ في شبكة الوكلاء: {str(e)}',
            'status': 'error'
        }), 500

@app.route('/health')
def health():
    return jsonify({
        'status': 'ok',
        'system': 'AutoOne Multi-Agent Network',
        'api_key_set': bool(DEEPSEEK_API_KEY),
        'active_agents': [
            'Chief Orchestrator',
            'Dr. Auto Technical Diagnostic',
            'Marketing & Customer Service',
            'Booking & Scheduling'
        ]
    })

if __name__ == '__main__':
    port = int(os.environ.get('PORT', 5000))
    app.run(host='0.0.0.0', port=port, debug=False)
