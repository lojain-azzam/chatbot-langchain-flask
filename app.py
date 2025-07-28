import os
import json
from datetime import datetime
from flask import Flask, request, jsonify, render_template
from flask_cors import CORS
from dotenv import load_dotenv
from langchain_openai import ChatOpenAI
try:
    from langchain_google_genai import ChatGoogleGenerativeAI
    GEMINI_AVAILABLE = True
except ImportError:
    GEMINI_AVAILABLE = False
    print("Warning: Gemini dependencies not available. Only ChatGPT will be available.")
from langchain.schema import HumanMessage, SystemMessage
from langchain.memory import ConversationBufferMemory
from langchain_core.prompts import PromptTemplate

# Load environment variables
load_dotenv()

app = Flask(__name__)
CORS(app)

class ChatbotManager:
    def __init__(self):
        self.conversations = {}
        self.models = {
            'gemini': None,
            'chatgpt': None
        }
        self._initialize_models()
    
    def _initialize_models(self):
        """Initialize the available models"""
        print("Initializing models...")
        
        # Initialize Gemini
        if GEMINI_AVAILABLE and os.getenv('GOOGLE_API_KEY'):
            try:
                self.models['gemini'] = ChatGoogleGenerativeAI(
                    model="gemini-1.5-pro",
                    google_api_key=os.getenv('GOOGLE_API_KEY'),
                    temperature=0.7
                )
                print("✓ Gemini initialized successfully")
            except Exception as e:
                print(f"✗ Failed to initialize Gemini: {e}")
        
        # Initialize ChatGPT
        openai_key = os.getenv('OPENAI_API_KEY')
        print(f"OpenAI API key found: {'Yes' if openai_key else 'No'}")
        if openai_key:
            try:
                self.models['chatgpt'] = ChatOpenAI(
                    model="gpt-3.5-turbo-0125",  # More cost-effective model
                    openai_api_key=openai_key,
                    temperature=0.7
                )
                print("✓ ChatGPT initialized successfully")
            except Exception as e:
                print(f"✗ Failed to initialize ChatGPT: {e}")
        else:
            print("✗ No OpenAI API key found")
        
        print(f"Available models: {list(self.models.keys())}")
    
    def get_conversation(self, session_id, model_type, memory_mode, initial_context=None, use_context_persistently=False):
        """Get or create a conversation for the session"""
        if session_id not in self.conversations:
            self.conversations[session_id] = {
                'model_type': model_type,
                'memory_mode': memory_mode,
                'initial_context': initial_context,
                'use_context_persistently': use_context_persistently,
                'memory': ConversationBufferMemory() if memory_mode == 'active' else None,
                'messages': []
            }
        
        return self.conversations[session_id]
    
    def send_message(self, session_id, message, model_type, memory_mode, initial_context=None, use_context_persistently=False):
        """Send a message to the chatbot"""
        conversation = self.get_conversation(session_id, model_type, memory_mode, initial_context, use_context_persistently)
        
        # Get the appropriate model
        model = self.models.get(model_type)
        if not model:
            return {"error": f"Model {model_type} is not available. Please check your API keys."}
        
        try:
            if memory_mode == 'active':
                # Use conversation memory
                # Add initial context if provided and persistent
                if initial_context and use_context_persistently and not conversation.get('context_added'):
                    conversation['memory'].save_context(
                        {"input": f"System Context: {initial_context}"},
                        {"output": "I understand the context and will keep it in mind for our conversation."}
                    )
                    conversation['context_added'] = True
                
                # Get conversation history
                history = conversation['memory'].load_memory_variables({})
                conversation_history = history.get('history', '')
                
                # Create messages with history
                messages = []
                if conversation_history:
                    messages.append(SystemMessage(content=f"Previous conversation:\n{conversation_history}"))
                if initial_context and not use_context_persistently:
                    messages.append(SystemMessage(content=initial_context))
                messages.append(HumanMessage(content=message))
                
                response = model.invoke(messages).content
                
                # Save to memory
                conversation['memory'].save_context(
                    {"input": message},
                    {"output": response}
                )
                
            else:
                # Memoryless mode - treat each message independently
                messages = []
                
                # Add initial context if provided
                if initial_context:
                    messages.append(SystemMessage(content=initial_context))
                
                messages.append(HumanMessage(content=message))
                
                response = model.invoke(messages).content
            
            # Store the message in conversation history
            conversation['messages'].append({
                'user': message,
                'bot': response,
                'timestamp': datetime.now().isoformat()
            })
            
            return {"response": response, "success": True}
            
        except Exception as e:
            error_msg = str(e)
            if "insufficient_quota" in error_msg or "429" in error_msg:
                return {"error": "API quota exceeded. Please check your billing or try again later. You can also add payment information to get more credits."}
            elif "rate_limit" in error_msg.lower():
                return {"error": "Rate limit reached. Please wait a moment and try again."}
            else:
                return {"error": f"Error processing message: {error_msg}"}
    
    def clear_conversation(self, session_id):
        """Clear conversation history for a session"""
        if session_id in self.conversations:
            del self.conversations[session_id]
        return {"success": True, "message": "Conversation cleared"}

# Initialize chatbot manager
chatbot_manager = ChatbotManager()

@app.route('/')
def index():
    """Serve the main chat interface"""
    return render_template('index.html')

@app.route('/api/chat', methods=['POST'])
def chat():
    """Handle chat messages"""
    try:
        data = request.get_json()
        
        session_id = data.get('session_id', 'default')
        message = data.get('message', '')
        model_type = data.get('model_type', 'chatgpt')
        memory_mode = data.get('memory_mode', 'active')
        initial_context = data.get('initial_context', '')
        use_context_persistently = data.get('use_context_persistently', False)
        
        if not message:
            return jsonify({"error": "Message is required"}), 400
        
        response = chatbot_manager.send_message(
            session_id=session_id,
            message=message,
            model_type=model_type,
            memory_mode=memory_mode,
            initial_context=initial_context,
            use_context_persistently=use_context_persistently
        )
        
        return jsonify(response)
        
    except Exception as e:
        return jsonify({"error": f"Server error: {str(e)}"}), 500

@app.route('/api/clear', methods=['POST'])
def clear_conversation():
    """Clear conversation history"""
    try:
        data = request.get_json()
        session_id = data.get('session_id', 'default')
        
        response = chatbot_manager.clear_conversation(session_id)
        return jsonify(response)
        
    except Exception as e:
        return jsonify({"error": f"Server error: {str(e)}"}), 500

@app.route('/api/models', methods=['GET'])
def get_available_models():
    """Get available models"""
    available_models = []
    
    if chatbot_manager.models['gemini']:
        available_models.append('gemini')
    
    if chatbot_manager.models['chatgpt']:
        available_models.append('chatgpt')
    
    if not available_models:
        available_models.append('chatgpt')  # Default fallback
    
    return jsonify({"models": available_models})

if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=5001) 