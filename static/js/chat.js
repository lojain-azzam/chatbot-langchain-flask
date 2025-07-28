// Chat interface JavaScript

class ChatInterface {
    constructor() {
        this.sessionId = this.generateSessionId();
        this.isTyping = false;
        this.initializeElements();
        this.bindEvents();
        this.updateCharacterCount();
        this.checkAvailableModels();
        this.loadConfigPreference();
    }

    initializeElements() {
        this.messageInput = document.getElementById('messageInput');
        this.sendButton = document.getElementById('sendMessage');
        this.chatMessages = document.getElementById('chatMessages');
        this.modelSelect = document.getElementById('modelSelect');
        this.memoryMode = document.getElementById('memoryMode');
        this.initialContext = document.getElementById('initialContext');
        this.useContextPersistently = document.getElementById('useContextPersistently');
        this.clearChatButton = document.getElementById('clearChat');
        this.charCount = document.getElementById('charCount');
        this.statusAlert = document.getElementById('statusAlert');
        this.statusText = document.getElementById('statusText');
        
        // Configuration toggle elements
        this.configPanel = document.getElementById('configPanel');
        this.chatPanel = document.getElementById('chatPanel');
        this.toggleConfigBtn = document.getElementById('toggleConfig');
        this.toggleConfigMobileBtn = document.getElementById('toggleConfigMobile');
        
        // Initialize config state
        this.isConfigOpen = true;
    }

    bindEvents() {
        // Send message events
        this.sendButton.addEventListener('click', () => this.sendMessage());
        this.messageInput.addEventListener('keydown', (e) => {
            if (e.ctrlKey && e.key === 'Enter') {
                e.preventDefault();
                this.sendMessage();
            }
        });

        // Character count
        this.messageInput.addEventListener('input', () => this.updateCharacterCount());

        // Clear chat
        this.clearChatButton.addEventListener('click', () => this.clearChat());

        // Configuration changes
        this.modelSelect.addEventListener('change', () => this.updateStatus());
        this.memoryMode.addEventListener('change', () => this.updateStatus());
        this.initialContext.addEventListener('input', () => this.updateStatus());
        this.useContextPersistently.addEventListener('change', () => this.updateStatus());
        
        // Configuration toggle
        this.toggleConfigBtn.addEventListener('click', () => this.toggleConfig());
        this.toggleConfigMobileBtn.addEventListener('click', () => this.toggleConfig());
    }

    generateSessionId() {
        return 'session_' + Date.now() + '_' + Math.random().toString(36).substr(2, 9);
    }

    updateCharacterCount() {
        const count = this.messageInput.value.length;
        this.charCount.textContent = count;
        
        if (count > 900) {
            this.charCount.style.color = '#dc3545';
        } else if (count > 800) {
            this.charCount.style.color = '#ffc107';
        } else {
            this.charCount.style.color = '#6c757d';
        }
    }

    async checkAvailableModels() {
        try {
            const response = await fetch('/api/models');
            const data = await response.json();
            
            // Update model select options based on available models
            const modelSelect = this.modelSelect;
            const currentValue = modelSelect.value;
            
            // Clear existing options
            modelSelect.innerHTML = '';
            
            if (data.models.includes('chatgpt')) {
                const option = document.createElement('option');
                option.value = 'chatgpt';
                option.textContent = 'ChatGPT (GPT-3.5-turbo)';
                modelSelect.appendChild(option);
            }
            
            if (data.models.includes('gemini')) {
                const option = document.createElement('option');
                option.value = 'gemini';
                option.textContent = 'Gemini Pro';
                modelSelect.appendChild(option);
            }
            
            // Restore previous selection if still available
            if (data.models.includes(currentValue)) {
                modelSelect.value = currentValue;
            } else if (data.models.length > 0) {
                modelSelect.value = data.models[0];
            }
            
            this.updateStatus();
        } catch (error) {
            console.error('Error checking available models:', error);
            this.showStatus('Error checking available models', 'error');
        }
    }

    updateStatus() {
        const model = this.modelSelect.value;
        const memory = this.memoryMode.value;
        const context = this.initialContext.value;
        const persistent = this.useContextPersistently.checked;
        
        let status = `Model: ${model === 'chatgpt' ? 'ChatGPT' : 'Gemini'} | Memory: ${memory === 'active' ? 'Active' : 'Memoryless'}`;
        
        if (context) {
            status += ` | Context: ${persistent ? 'Persistent' : 'One-time'}`;
        }
        
        this.showStatus(status, 'info');
    }

    showStatus(message, type = 'info') {
        this.statusText.textContent = message;
        this.statusAlert.className = `alert alert-${type}`;
        this.statusAlert.style.display = 'block';
        
        // Auto-hide after 5 seconds
        setTimeout(() => {
            this.statusAlert.style.display = 'none';
        }, 5000);
    }

    async sendMessage() {
        const message = this.messageInput.value.trim();
        if (!message || this.isTyping) return;

        // Add user message to chat
        this.addMessage(message, 'user');
        this.messageInput.value = '';
        this.updateCharacterCount();

        // Show typing indicator
        this.showTypingIndicator();

        try {
            const response = await fetch('/api/chat', {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json',
                },
                body: JSON.stringify({
                    session_id: this.sessionId,
                    message: message,
                    model_type: this.modelSelect.value,
                    memory_mode: this.memoryMode.value,
                    initial_context: this.initialContext.value,
                    use_context_persistently: this.useContextPersistently.checked
                })
            });

            const data = await response.json();

            // Hide typing indicator
            this.hideTypingIndicator();

            if (data.error) {
                this.addErrorMessage(data.error);
            } else if (data.response) {
                this.addMessage(data.response, 'bot');
            }

        } catch (error) {
            console.error('Error sending message:', error);
            this.hideTypingIndicator();
            this.addErrorMessage('Failed to send message. Please try again.');
        }
    }

    addMessage(content, sender) {
        // Remove welcome message if it exists
        const welcomeMessage = this.chatMessages.querySelector('.welcome-message');
        if (welcomeMessage) {
            welcomeMessage.remove();
        }

        const messageDiv = document.createElement('div');
        messageDiv.className = `message ${sender}`;

        const messageContent = document.createElement('div');
        messageContent.className = 'message-content';
        messageContent.textContent = content;

        const messageTime = document.createElement('span');
        messageTime.className = 'message-time';
        messageTime.textContent = new Date().toLocaleTimeString();

        messageDiv.appendChild(messageContent);
        messageDiv.appendChild(messageTime);

        this.chatMessages.appendChild(messageDiv);
        this.scrollToBottom();
    }

    addErrorMessage(error) {
        const errorDiv = document.createElement('div');
        errorDiv.className = 'error-message';
        errorDiv.textContent = error;
        this.chatMessages.appendChild(errorDiv);
        this.scrollToBottom();
    }

    showTypingIndicator() {
        this.isTyping = true;
        this.sendButton.disabled = true;

        const typingDiv = document.createElement('div');
        typingDiv.className = 'message bot typing-indicator';
        typingDiv.id = 'typingIndicator';

        const typingContent = document.createElement('div');
        typingContent.className = 'typing-dots';
        typingContent.innerHTML = `
            <div class="typing-dot"></div>
            <div class="typing-dot"></div>
            <div class="typing-dot"></div>
        `;

        typingDiv.appendChild(typingContent);
        this.chatMessages.appendChild(typingDiv);
        this.scrollToBottom();
    }

    hideTypingIndicator() {
        this.isTyping = false;
        this.sendButton.disabled = false;

        const typingIndicator = document.getElementById('typingIndicator');
        if (typingIndicator) {
            typingIndicator.remove();
        }
    }

    async clearChat() {
        try {
            await fetch('/api/clear', {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json',
                },
                body: JSON.stringify({
                    session_id: this.sessionId
                })
            });

            // Clear chat messages and show welcome message
            this.chatMessages.innerHTML = `
                <div class="welcome-message">
                    <div class="text-center text-muted">
                        <i class="fas fa-robot fa-3x mb-3"></i>
                        <h4>Welcome to the Flexible LangChain Chatbot!</h4>
                        <p>Configure your settings on the left and start chatting.</p>
                    </div>
                </div>
            `;

            this.showStatus('Conversation cleared', 'success');
        } catch (error) {
            console.error('Error clearing chat:', error);
            this.showStatus('Error clearing conversation', 'error');
        }
    }

    scrollToBottom() {
        this.chatMessages.scrollTop = this.chatMessages.scrollHeight;
    }
    
    toggleConfig() {
        this.isConfigOpen = !this.isConfigOpen;
        
        if (this.isConfigOpen) {
            // Open configuration panel
            this.configPanel.classList.remove('collapsed');
            this.chatPanel.classList.remove('expanded');
            this.toggleConfigBtn.innerHTML = '<i class="fas fa-chevron-left"></i>';
            this.toggleConfigMobileBtn.style.display = 'none';
            
            // Show mobile config button on small screens
            if (window.innerWidth <= 768) {
                this.toggleConfigMobileBtn.style.display = 'block';
            }
        } else {
            // Close configuration panel
            this.configPanel.classList.add('collapsed');
            this.chatPanel.classList.add('expanded');
            this.toggleConfigBtn.innerHTML = '<i class="fas fa-chevron-right"></i>';
            this.toggleConfigMobileBtn.style.display = 'block';
        }
        
        // Store preference in localStorage
        localStorage.setItem('configOpen', this.isConfigOpen);
    }
    
    loadConfigPreference() {
        const savedPreference = localStorage.getItem('configOpen');
        if (savedPreference !== null) {
            this.isConfigOpen = savedPreference === 'true';
            if (!this.isConfigOpen) {
                this.toggleConfig();
            }
        }
    }
}

// Initialize the chat interface when the page loads
document.addEventListener('DOMContentLoaded', () => {
    new ChatInterface();
}); 