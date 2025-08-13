from flask import Flask, request, jsonify
from flask_cors import CORS
import os
import logging
from datetime import datetime
import json
import sys
from flask import send_from_directory

# Add the project root to the Python path so package imports work
current_dir = os.path.dirname(os.path.abspath(__file__))
project_root = os.path.abspath(os.path.join(current_dir, '..'))
if project_root not in sys.path:
    sys.path.insert(0, project_root)

# Import EmbRag from the utils package
from utils.rag import EmbRag
from utils.context import ContextManager
# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Initialize Flask app
CLIENT_DIR = os.path.join(current_dir, '..', 'client')
app = Flask(__name__, static_folder=CLIENT_DIR, static_url_path='')

# Enable CORS for cross-origin requests
CORS(app)

# Configuration
app.config['SECRET_KEY'] = os.environ.get('SECRET_KEY', 'your-secret-key-here')
app.config['DEBUG'] = os.environ.get('FLASK_DEBUG', 'False').lower() == 'true'
app.config['HOST'] = os.environ.get('FLASK_HOST', '0.0.0.0')
app.config['PORT'] = int(os.environ.get('FLASK_PORT', 5000))

# Global variables for chat history (in production, use a database)
chat_history = []

# Initialize EmbRag
try:
    # You can configure these paths as needed
    docs_path = r"/home/chandrahaas/codes/Bot/DOCS"
    faiss_path = r"/home/chandrahaas/codes/Bot/Faiss"
    
    # Create directories if they don't exist
    os.makedirs(docs_path, exist_ok=True)
    os.makedirs(faiss_path, exist_ok=True)
    
    rag_system = EmbRag(docs_path, faiss_path)
    logger.info("EmbRag system initialized successfully")
    context_obj=ContextManager()
except Exception as e:
    logger.error(f"Failed to initialize EmbRag: {str(e)}")
    rag_system = None

# Serve frontend: index.html
@app.route('/', methods=['GET'])
def serve_index():
    return app.send_static_file('index.html')

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
        
        # Use EmbRag system for intelligent responses
        if rag_system and message:
            try:
                # Get response from RAG system
                rag_response = rag_system.queryDB(message,context_obj)
                response_message = rag_response if rag_response else "I couldn't find a relevant response for your query."
                context_obj.add_context(message,response_message)
            except Exception as e:
                logger.error(f"Error in RAG system: {str(e)}")
                response_message = "I encountered an error while processing your request. Please try again."
        else:
            # Fallback response for images or when RAG is not available
            response_message = f"I received your message: '{message}'" if message else "I received your image"
        
        response = {
            'message': response_message,
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
