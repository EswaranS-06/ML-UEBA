import { ApiClient } from '../api/client.js';

export class AgenticSection {
    constructor() {
        console.log('AgenticSection: Initializing...'); // Debug
        this.chatWindow = document.getElementById('agent-chat-window');
        this.input = document.getElementById('agent-input');
        this.sendBtn = document.getElementById('btn-send-agent');
        this.prompts = document.querySelectorAll('.quick-prompts .pill');

        this.init();
    }

    init() {
        if (this.sendBtn && this.input) {
            console.log('AgenticSection: Attaching listeners to send button and input'); // Debug
            this.sendBtn.addEventListener('click', () => {
                console.log('AgenticSection: Send button clicked'); // Debug
                this.sendMessage();
            });
            this.input.addEventListener('keypress', (e) => {
                if (e.key === 'Enter') {
                    console.log('AgenticSection: Enter key pressed'); // Debug
                    this.sendMessage();
                }
            });
        } else {
            console.error('AgenticSection: Input elements not found!', { btn: this.sendBtn, input: this.input }); // Debug
        }

        this.prompts.forEach(p => {
            p.addEventListener('click', () => {
                this.input.value = p.innerText;
                this.sendMessage();
            });
        });
    }

    gatherContext() {
        return {
            mode: document.getElementById('agent-mode')?.value,
            time_range: document.getElementById('agent-time-range')?.value,
            sources: {
                postgres: document.getElementById('agent-ctx-postgres')?.checked,
                ml_outputs: document.getElementById('agent-ctx-ml')?.checked,
                features: document.getElementById('agent-ctx-features')?.checked,
                logs: document.getElementById('agent-ctx-logs')?.checked
            },
            entities: {
                user: {
                    enabled: document.getElementById('agent-check-user')?.checked,
                    value: document.getElementById('agent-input-user')?.value
                },
                ip: {
                    enabled: document.getElementById('agent-check-ip')?.checked,
                    value: document.getElementById('agent-input-ip')?.value
                }
            }
        };
    }

    async sendMessage() {
        const text = this.input.value.trim();
        if (!text) return;

        // User Message
        this.appendMessage('user', text);
        this.input.value = '';

        // UI Feedback
        this.showTyping();

        try {
            const context = this.gatherContext();

            // Real API Call
            const response = await ApiClient.post('/agent/chat', {
                query: text,
                context: context
            });

            this.removeTyping();
            // Expecting response.answer or response.message
            this.appendMessage('agent', response.answer || response.message || "I received a response but it was empty.");

        } catch (error) {
            this.removeTyping();
            console.error('Agent API Error:', error);
            this.appendMessage('agent', `<span class="error-text">Connection error: ${error.message}. Is the backend running?</span>`);
        }
    }

    appendMessage(role, htmlContent) {
        if (!this.chatWindow) return;

        const msgDiv = document.createElement('div');
        msgDiv.className = `message ${role}`;

        const avatar = role === 'agent' ? '🤖' : '👤';

        msgDiv.innerHTML = `
            <div class="msg-avatar">${avatar}</div>
            <div class="msg-content">${htmlContent}</div>
        `;

        this.chatWindow.appendChild(msgDiv);
        this.scrollToBottom();
    }

    showTyping() {
        if (document.getElementById('agent-typing')) return;

        const typingDiv = document.createElement('div');
        typingDiv.id = 'agent-typing';
        typingDiv.className = 'message agent';
        typingDiv.innerHTML = `
            <div class="msg-avatar">🤖</div>
            <div class="msg-content"><em>Thinking...</em></div>
        `;
        this.chatWindow.appendChild(typingDiv);
        this.scrollToBottom();
    }

    removeTyping() {
        const typing = document.getElementById('agent-typing');
        if (typing) typing.remove();
    }

    scrollToBottom() {
        if (this.chatWindow) {
            this.chatWindow.scrollTop = this.chatWindow.scrollHeight;
        }
    }
}
