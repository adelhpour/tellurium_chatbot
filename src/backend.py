from flask import Flask, request, jsonify
from flask_cors import CORS
import requests
import logging

# 1) import your LLM client
from llm_service import llm_service

app = Flask(__name__)
CORS(app, resources={r"/api/*": {"origins": "*"}})

# configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

@app.route('/', methods=['GET'])
def health():
    return "Flask server is running!", 200

@app.route('/api/chat', methods=['POST'])
def chat():
    data = request.get_json(force=True) or {}
    user_prompt = data.get('message', '')
    # logger.info("Incoming prompt: %r", user_prompt)

    try:
        reply = llm_service.send_message(user_prompt)
        return jsonify({ 'message': reply }), 200

    except requests.RequestException as e:
        # downstream error contacting the MCP server
        logger.exception("Backend (MCP) error")
        return jsonify({
            'error':   'backend_unavailable',
            'details': str(e)
        }), 502

    except Exception as e:
        # anything else
        logger.exception("Unexpected failure in /api/chat")
        return jsonify({
            'error':   'internal_server_error',
            'details': str(e)
        }), 500

if __name__ == '__main__':
    # turn on debug so you see exceptions in your console
    app.run(port=8000, debug=True)
