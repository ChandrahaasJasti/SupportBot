from flask import Flask, request, jsonify
from flask_cors import CORS
import os
import logging
from datetime import datetime
import json

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Initialize Flask app
app = Flask(__name__)

# Enable CORS for cross-origin requests
CORS(app)

# Configuration
app.config['SECRET_KEY'] = os.environ.get('SECRET_KEY', 'your-secret-key-here')
app.config['DEBUG'] = os.environ.get('FLASK_DEBUG', 'False').lower() == 'true'
app.config['HOST'] = os.environ.get('FLASK_HOST', '0.0.0.0')
app.config['PORT'] = int(os.environ.get('FLASK_PORT', 5000))

# Global variables for chat history (in production, use a database)
chat_history = []



@app.route('/api/chat', methods=['POST'])
def chat():
    """Handle chat messages"""
    try:
        data = request.get_json()
        
        if not data:
            return jsonify({'error': 'No data provided'}), 400
        
        message = data.get('message', '').strip()
        image_data = data.get('image')
        
        if not message and not image_data:
            return jsonify({'error': 'Message or image required'}), 400
        
        # Log the incoming request
        logger.info(f"Received chat request: message='{message[:50]}...' image={bool(image_data)}")
        
        # TODO: Integrate with AI service here
        # For now, return a simple response
        response = {
            'message': f"I received your message: '{message}'" if message else "I received your image",
            'timestamp': datetime.utcnow().isoformat(),
            'message_id': len(chat_history) + 1
        }
        
        # Store in chat history
        chat_entry = {
            'id': len(chat_history) + 1,
            'user_message': message,
            'bot_response': response['message'],
            'timestamp': response['timestamp'],
            'has_image': bool(image_data)
        }
        chat_history.append(chat_entry)
        
        return jsonify(response)
        
    except Exception as e:
        logger.error(f"Error processing chat request: {str(e)}")
        return jsonify({'error': 'Internal server error'}), 500

@app.route('/api/chat/history', methods=['GET'])
def get_chat_history():
    """Get chat history"""
    try:
        limit = request.args.get('limit', 50, type=int)
        return jsonify({
            'history': chat_history[-limit:],
            'total_messages': len(chat_history)
        })
    except Exception as e:
        logger.error(f"Error retrieving chat history: {str(e)}")
        return jsonify({'error': 'Internal server error'}), 500



@app.errorhandler(404)
def not_found(error):
    """Handle 404 errors"""
    return jsonify({'error': 'Endpoint not found'}), 404

@app.errorhandler(500)
def internal_error(error):
    """Handle 500 errors"""
    logger.error(f"Internal server error: {str(error)}")
    return jsonify({'error': 'Internal server error'}), 500

@app.before_request
def log_request():
    """Log all incoming requests"""
    logger.info(f"{request.method} {request.path} - {request.remote_addr}")

@app.after_request
def log_response(response):
    """Log all outgoing responses"""
    logger.info(f"Response: {response.status_code}")
    return response

def create_app():
    """Application factory pattern"""
    return app

if __name__ == '__main__':
    logger.info(f"Starting Flask server on {app.config['HOST']}:{app.config['PORT']}")
    logger.info(f"Debug mode: {app.config['DEBUG']}")
    
    try:
        app.run(
            host=app.config['HOST'],
            port=app.config['PORT'],
            debug=app.config['DEBUG']
        )
    except Exception as e:
        logger.error(f"Failed to start server: {str(e)}")
        exit(1)
