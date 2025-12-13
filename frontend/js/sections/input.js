import { ApiClient } from '../api/client.js';

export class InputSection {
    constructor() {
        this.typeSelect = document.getElementById('input-type-select');
        this.configs = {
            'file': document.getElementById('config-file'),
            'kafka': document.getElementById('config-kafka'),
            'http': document.getElementById('config-http')
        };
        this.saveButton = document.querySelector('#input-panel .btn-primary');

        this.init();
    }

    init() {
        // Toggle visibility
        this.typeSelect.addEventListener('change', (e) => this.switchType(e.target.value));

        // File Upload Display
        const fileInput = document.getElementById('file-upload-input');
        const fileListDisplay = document.getElementById('file-chosen-list');
        if (fileInput && fileListDisplay) {
            fileInput.addEventListener('change', (e) => {
                const files = Array.from(e.target.files);
                if (files.length > 0) {
                    fileListDisplay.textContent = `Selected: ${files.map(f => f.name).join(', ')}`;
                    fileListDisplay.style.color = 'var(--text-accent)';
                } else {
                    fileListDisplay.textContent = 'No files chosen';
                    fileListDisplay.style.color = 'var(--text-secondary)';
                }
            });
        }

        // Save Action
        if (this.saveButton) {
            // Remove old onclick attribute if exists to prevent conflicts
            this.saveButton.removeAttribute('onclick');
            this.saveButton.addEventListener('click', () => this.saveConfiguration());
        }
    }

    switchType(selected) {
        Object.values(this.configs).forEach(el => el.classList.remove('active'));
        if (this.configs[selected]) {
            this.configs[selected].classList.add('active');
        }
    }

    async saveConfiguration() {
        const type = this.typeSelect.value;
        const btn = this.saveButton;

        this.setLoading(btn, true);

        try {
            if (type === 'file') {
                await this.handleFileUpload();
            } else if (type === 'kafka') {
                await this.handleKafkaConfig();
            } else if (type === 'http') {
                await this.handleHttpConfig();
            }

            this.showSuccess(btn);
            // Optional: trigger global log
            if (window.logAction) window.logAction(`[INFO] Input configuration (${type}) saved.`);

        } catch (error) {
            alert(`Error saving configuration: ${error.message}`);
            btn.innerText = "Error ❌";
            setTimeout(() => { btn.innerText = "Save Input Configuration"; btn.disabled = false; }, 2000);
        }
    }

    async handleFileUpload() {
        const fileInput = document.getElementById('file-upload-input');
        if (!fileInput.files.length) {
            throw new Error("No files selected.");
        }

        const formData = new FormData();
        Array.from(fileInput.files).forEach(file => {
            formData.append('files', file);
        });



        await ApiClient.upload('/input/upload', formData);
    }

    async handleKafkaConfig() {
        const config = {
            type: 'kafka',
            bootstrap_servers: document.querySelector('#config-kafka input:nth-child(1)').value || 'localhost:9092', // Using generic selector/value extraction
            // Better to add IDs to inputs for reliability, but using existing DOM structure for now
            topic: document.querySelector('#config-kafka input[value="auth-logs"]').value,
            group_id: document.querySelector('#config-kafka input[value="ueba-consumer"]').value
        };

        // Let's refine the selectors in the next step by adding IDs to HTML,
        // but for now I'll use the values directly if stuck.
        // Actually, robust way:
        const inputs = document.querySelectorAll('#config-kafka input');
        config.bootstrap_servers = inputs[0].value;
        config.topic = inputs[1].value;
        config.group_id = inputs[2].value;

        await ApiClient.post('/input/config', config);
    }

    async handleHttpConfig() {
        const inputs = document.querySelectorAll('#config-http input');
        const config = {
            type: 'http',
            port: parseInt(inputs[0].value),
            auth_token: inputs[1].value
        };

        await ApiClient.post('/input/config', config);
    }

    setLoading(btn, isLoading) {
        if (isLoading) {
            btn.dataset.originalText = btn.innerText;
            btn.innerText = "Saving...";
            btn.disabled = true;
        }
    }

    showSuccess(btn) {
        btn.innerText = "Saved ✓";
        btn.classList.add('btn-success');
        setTimeout(() => {
            btn.innerText = btn.dataset.originalText || "Save Input Configuration";
            btn.classList.remove('btn-success');
            btn.disabled = false;
        }, 2000);
    }
}
