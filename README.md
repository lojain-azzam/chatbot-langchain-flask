# 🤖 Flexible LangChain Flask Chatbot

A modern, feature-rich chatbot interface built with **LangChain** and **Flask** that supports multiple AI models, memory modes, and context injection with a beautiful collapsible UI.

![Chatbot Demo](https://img.shields.io/badge/Status-Production%20Ready-brightgreen)
![Python](https://img.shields.io/badge/Python-3.8+-blue)
![Flask](https://img.shields.io/badge/Flask-2.3+-lightgrey)
![LangChain](https://img.shields.io/badge/LangChain-0.0.350+-orange)

## ✨ Features

### 🧠 **Multiple AI Models**
- **ChatGPT (GPT-3.5-turbo)**: OpenAI's powerful language model
- **Gemini Pro**: Google's advanced AI model
- **Automatic model detection** and availability checking
- **Easy switching** between models in real-time

### 🧠 **Intelligent Memory Management**
- **Active Memory**: Remembers conversation history for contextual responses
- **Memoryless Mode**: Treats each message independently (perfect for testing)
- **Session-based conversations** with unique session IDs

### 📝 **Context Injection System**
- **Initial Context**: Inject custom context at conversation start
- **Persistent Context**: Context continues to influence all future responses
- **One-time Context**: Context only applies to the initial message
- **Dynamic context management** with real-time updates

### 🎨 **Modern User Interface**
- **Collapsible Configuration Panel**: Maximize chat space when needed
- **Responsive Design**: Works perfectly on desktop and mobile
- **Real-time Typing Indicators**: Professional chat experience
- **Smooth Animations**: Beautiful transitions and effects
- **Dark/Light Theme Support**: Modern gradient design

### 🔧 **Advanced Configuration**
- **Model Selection**: Switch between ChatGPT and Gemini
- **Memory Mode Toggle**: Active vs Memoryless
- **Context Management**: Persistent or one-time context injection
- **Session Management**: Clear conversations and manage history

## 🚀 Quick Start

### Prerequisites
- Python 3.8 or higher
- OpenAI API key (for ChatGPT)
- Google API key (for Gemini) - Optional

### 1. Clone the Repository
```bash
git clone https://github.com/lojain-azzam/chatbot-langchain-flask.git
cd chatbot-langchain-flask
```

### 2. Install Dependencies
```bash
pip install -r requirements.txt
```

### 3. Configure API Keys
Create a `.env` file in the project root:
```bash
cp env_example.txt .env
```

Edit `.env` and add your API keys:
```env
# OpenAI API Key (for ChatGPT)
OPENAI_API_KEY=your_openai_api_key_here

# Google API Key (for Gemini) - Optional
GOOGLE_API_KEY=your_google_api_key_here

# Flask Configuration
FLASK_ENV=development
FLASK_DEBUG=True
```

**Get API Keys:**
- **OpenAI**: [https://platform.openai.com/api-keys](https://platform.openai.com/api-keys)
- **Google Gemini**: [https://makersuite.google.com/app/apikey](https://makersuite.google.com/app/apikey)

### 4. Run the Application
```bash
python app.py
```

The chatbot will be available at: **http://localhost:5001**

## 🎯 Usage Guide

### Configuration Panel
The left sidebar contains all configuration options:

1. **Backend Model**: Choose between ChatGPT and Gemini
2. **Memory Mode**: 
   - **Active**: Remembers conversation history
   - **Memoryless**: Each message is independent
3. **Initial Context**: Add custom context for the conversation
4. **Use Context Persistently**: Toggle whether context affects all future messages

### Chat Interface
- **Type your message** in the input field
- **Press Enter** or click the send button
- **Use Ctrl+Enter** for quick sending
- **Clear conversation** history with the "Clear Conversation" button

### Collapsible UI
- **Desktop**: Click the **←** button in the configuration header to collapse/expand
- **Mobile**: Click the **⚙️** button in the chat header to toggle
- **Auto-save**: Your preference is remembered between sessions

## 🏗️ Architecture

### Backend (Flask + LangChain)
```
app.py
├── ChatbotManager
│   ├── Model initialization (ChatGPT/Gemini)
│   ├── Conversation management
│   ├── Memory handling
│   └── Context injection
├── API Endpoints
│   ├── /api/chat - Send messages
│   ├── /api/clear - Clear conversations
│   └── /api/models - Get available models
└── Web Interface
    └── / - Main chat interface
```

### Frontend (HTML/CSS/JavaScript)
```
templates/
├── index.html - Main interface
static/
├── css/
│   └── style.css - Modern styling with animations
└── js/
    └── chat.js - Interactive functionality
```

## 📡 API Reference

### POST /api/chat
Send a message to the chatbot.

**Request Body:**
```json
{
  "session_id": "string",
  "message": "string",
  "model_type": "chatgpt|gemini",
  "memory_mode": "active|memoryless",
  "initial_context": "string",
  "use_context_persistently": boolean
}
```

**Response:**
```json
{
  "response": "string",
  "success": true
}
```

### POST /api/clear
Clear conversation history for a session.

**Request Body:**
```json
{
  "session_id": "string"
}
```

### GET /api/models
Get available AI models.

**Response:**
```json
{
  "models": ["chatgpt", "gemini"]
}
```

## ⚙️ Configuration

### Environment Variables
| Variable | Description | Required |
|----------|-------------|----------|
| `OPENAI_API_KEY` | OpenAI API key for ChatGPT | Yes |
| `GOOGLE_API_KEY` | Google API key for Gemini | No |
| `FLASK_ENV` | Flask environment | No |
| `FLASK_DEBUG` | Enable debug mode | No |

### Model Configuration
You can modify model parameters in `app.py`:

```python
# ChatGPT configuration
ChatOpenAI(
    model="gpt-3.5-turbo-0125",  # Change model version
    temperature=0.7,             # Adjust creativity (0.0-1.0)
    max_tokens=1000              # Set response length
)

# Gemini configuration
ChatGoogleGenerativeAI(
    model="gemini-1.5-pro",      # Change model version
    temperature=0.7,             # Adjust creativity (0.0-1.0)
    max_output_tokens=1000       # Set response length
)
```

## 🔧 Customization

### Adding New Models
1. Add the model to the `ChatbotManager._initialize_models()` method
2. Update the frontend model selection in `templates/index.html`
3. Add the model to the API response in `/api/models`

### Custom Memory Types
Extend the memory system by modifying the `ChatbotManager.send_message()` method:

```python
# Example: Add conversation summary memory
from langchain.memory import ConversationSummaryMemory

if memory_mode == 'summary':
    memory = ConversationSummaryMemory(llm=model)
```

### Styling Customization
Modify `static/css/style.css` to customize the appearance:

```css
/* Change color scheme */
:root {
  --primary-color: #667eea;
  --secondary-color: #764ba2;
}
```

## 🧪 Testing

Run the test script to verify your setup:

```bash
python test_setup.py
```

This will check:
- ✅ File structure
- ✅ Dependencies installation
- ✅ App import functionality
- ✅ Environment configuration

## 🚨 Troubleshooting

### Common Issues

1. **"Model not available" error**
   - Check your API keys in `.env`
   - Verify API key permissions
   - Ensure you have sufficient credits

2. **Import errors**
   - Run `pip install -r requirements.txt`
   - Check Python version (3.8+ required)

3. **CORS errors**
   - The app includes CORS support by default
   - Check browser console for specific errors

4. **Memory not working**
   - Ensure memory mode is set to "active"
   - Check if context persistence is enabled correctly

5. **API quota exceeded**
   - Add payment information to get more credits
   - Wait for quota reset (daily for Gemini, monthly for OpenAI)

### Debug Mode
Enable debug mode for detailed error messages:

```bash
export FLASK_DEBUG=True
python app.py
```

## 📊 Performance

### API Usage Optimization
- **ChatGPT**: ~$0.002 per message (very cost-effective)
- **Gemini**: Free tier with generous limits
- **Memory Management**: Efficient session-based storage
- **Response Time**: Typically 1-3 seconds per message

### Scalability
- **Session Management**: Each user gets a unique session
- **Memory Efficiency**: Conversations are stored in memory
- **API Rate Limiting**: Built-in retry mechanisms
- **Error Handling**: Graceful degradation on API failures

## 🤝 Contributing

1. Fork the repository
2. Create a feature branch (`git checkout -b feature/amazing-feature`)
3. Commit your changes (`git commit -m 'Add amazing feature'`)
4. Push to the branch (`git push origin feature/amazing-feature`)
5. Open a Pull Request

## 📄 License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

## 🙏 Acknowledgments

- [LangChain](https://langchain.com/) for the AI framework
- [Flask](https://flask.palletsprojects.com/) for the web framework
- [Bootstrap](https://getbootstrap.com/) for the UI components
- [Font Awesome](https://fontawesome.com/) for the icons
- [OpenAI](https://openai.com/) for ChatGPT API
- [Google](https://ai.google.dev/) for Gemini API

## 📞 Support

If you encounter any issues or have questions:

1. Check the [Troubleshooting](#-troubleshooting) section
2. Review the [API Reference](#-api-reference)
3. Open an issue on GitHub
4. Check the [test script](#-testing) for setup verification

---

**Made with ❤️ using LangChain and Flask**

*Ready to build intelligent conversations! 🚀* 