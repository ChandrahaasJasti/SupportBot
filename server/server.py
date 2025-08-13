from flask import Flask, request, jsonify
from flask_cors import CORS
import os
import logging
from datetime import datetime
import base64

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Initialize Flask app
current_dir = os.path.dirname(os.path.abspath(__file__))
CLIENT_DIR = os.path.join(current_dir, '..', 'client')
app = Flask(__name__, static_folder=CLIENT_DIR, static_url_path='')

# Enable CORS
CORS(app)

# Configuration
app.config['SECRET_KEY'] = 'your-secret-key-here'
app.config['DEBUG'] = True
app.config['HOST'] = '0.0.0.0'
app.config['PORT'] = 5000

# Chat history storage
chat_history = []

@app.route('/', methods=['GET'])
def serve_index():
    """Serve the main HTML page"""
    return app.send_static_file('index.html')

@app.route('/api/chat', methods=['POST'])
def chat():
    """Handle chat messages and images"""
    try:
        data = request.get_json()
        
        if not data:
            return jsonify({'error': 'No data provided'}), 400
        
        message = data.get('message', '').strip()
        image_data = data.get('image')
        
        if not message and not image_data:
            return jsonify({'error': 'Message or image required'}), 400
        
        # Log request
        logger.info(f"Chat request: message='{message[:50]}...' image={bool(image_data)}")
        
        # Process image if present
        image_info = None
        if image_data:
            image_info = validate_image(image_data)
        
        # Generate response
        if message and image_info:
            response_message = f"Received message: '{message}' and {image_info['format']} image ({image_info['size']} bytes)"
        elif message:
            response_message = f"Received message: '{message}'"
        elif image_info:
            response_message = f"Received {image_info['format']} image ({image_info['size']} bytes). Please add a message."
        else:
            response_message = "No valid message or image received"
        
        # Create response
        response = {
            'message': response_message,
            'timestamp': datetime.utcnow().isoformat(),
            'message_id': len(chat_history) + 1,
            'image_processed': bool(image_info)
        }
        
        # Store in history
        chat_entry = {
            'id': len(chat_history) + 1,
            'user_message': message,
            'bot_response': response['message'],
            'timestamp': response['timestamp'],
            'has_image': bool(image_info)
        }
        chat_history.append(chat_entry)
        
        return jsonify(response)
        
    except Exception as e:
        logger.error(f"Chat error: {str(e)}")
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
        logger.error(f"History error: {str(e)}")
        return jsonify({'error': 'Internal server error'}), 500

def validate_image(base64_string):
    """Validate base64 image data"""
    try:
        if not base64_string or not isinstance(base64_string, str):
            return None
        
        # Handle data URLs
        if base64_string.startswith('data:image/'):
            parts = base64_string.split(',')
            if len(parts) != 2:
                return None
            base64_string = parts[1]
        
        # Validate base64
        if len(base64_string) % 4 != 0:
            return None
        
        # Decode and check
        decoded_bytes = base64.b64decode(base64_string)
        size_bytes = len(decoded_bytes)
        
        # Check size limits
        if size_bytes < 100 or size_bytes > 10 * 1024 * 1024:
            return None
        
        # Check image signatures
        signatures = {
            b'\xff\xd8\xff': 'JPEG',
            b'\x89PNG\r\n\x1a\n': 'PNG',
            b'GIF87a': 'GIF',
            b'GIF89a': 'GIF',
            b'BM': 'BMP',
            b'RIFF': 'WEBP'
        }
        
        for signature, format_name in signatures.items():
            if decoded_bytes.startswith(signature):
                return {
                    'format': format_name,
                    'size': size_bytes,
                    'valid': True
                }
        
        return None
        
    except Exception:
        return None

if __name__ == '__main__':
    logger.info(f"Starting Flask server on {app.config['HOST']}:{app.config['PORT']}")
    app.run(
        host=app.config['HOST'],
        port=app.config['PORT'],
        debug=app.config['DEBUG']
    )
