import { ApiClient } from '../api/client.js';

export class OutputSection {
    constructor() {
        this.saveButton = document.querySelector('#output-panel .btn-primary');
        this.downloadButton = document.querySelector('#sub-file-output button'); // "Download Processed Data"

        this.init();
    }

    init() {
        // Toggle Logic (migrated from main.js)
        this.setupToggle('check-file-output', 'sub-file-output');
        this.setupToggle('check-kafka-output', 'sub-kafka-output');
        this.setupToggle('check-elastic-output', 'sub-elastic-output');
        this.setupToggle('check-webhook-output', 'sub-webhook-output');

        // Save Configuration
        if (this.saveButton) {
            this.saveButton.removeAttribute('onclick');
            this.saveButton.addEventListener('click', () => this.saveConfiguration());
        }

        // File Download Action
        if (this.downloadButton) {
            this.downloadButton.removeAttribute('onclick');
            this.downloadButton.addEventListener('click', () => this.handleDownload());
        }
    }

    setupToggle(checkboxId, subConfigId) {
        const checkbox = document.getElementById(checkboxId);
        const subConfig = document.getElementById(subConfigId);
        if (!checkbox || !subConfig) return;

        checkbox.addEventListener('change', () => {
            subConfig.classList.toggle('open', checkbox.checked);
        });
    }

    async saveConfiguration() {
        const btn = this.saveButton;
        this.setLoading(btn, true);

        const config = {
            storage: { postgres: true }, // Always on
            outputs: []
        };

        // File Output (Config only, not the download action)
        if (this.isChecked('check-file-output')) {
            config.outputs.push({
                type: 'file_download',
                format: document.querySelector('#sub-file-output select').value
            });
        }

        // Kafka
        if (this.isChecked('check-kafka-output')) {
            config.outputs.push({
                type: 'kafka',
                topic: document.querySelector('#sub-kafka-output input').value
            });
        }

        // Elasticsearch
        if (this.isChecked('check-elastic-output')) {
            config.outputs.push({
                type: 'elasticsearch',
                index: document.querySelector('#sub-elastic-output input').value
            });
        }

        // Webhook
        if (this.isChecked('check-webhook-output')) {
            config.outputs.push({
                type: 'webhook',
                url: document.querySelector('#sub-webhook-output input').value
            });
        }

        try {
            await ApiClient.post('/output/config', config);
            this.showSuccess(btn);
            if (window.logAction) window.logAction(`[INFO] Output configuration updated.`);
        } catch (error) {
            alert(`Error saving output config: ${error.message}`);
            this.showError(btn);
        }
    }

    async handleDownload() {
        // Trigger a download. In a real app, this might be a GET request that returns a file stream.
        // For this implementation, we'll assume the API returns a URL or blob.

        try {
            if (window.logAction) window.logAction(`[INFO] Requesting processed data download...`);

            // Example: GET /api/output/download returns a blob
            // We use fetch directly here to handle blob, or update ApiClient to support it.
            // Let's assume ApiClient.get returns JSON, so we might need a custom call or Blob support.
            // For now, let's just hit the endpoint and mock the "download start".

            // await ApiClient.post('/output/download-request', {}); 

            // Simulating a real browser download behavior
            // const response = await fetch('/api/output/download'); ...

            // Mock for UI Feedback
            alert("This would trigger the browser download of the processed file.");

        } catch (error) {
            console.error(error);
        }
    }

    isChecked(id) {
        const el = document.getElementById(id);
        return el ? el.checked : false;
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
            btn.innerText = btn.dataset.originalText || "Save Output Configuration";
            btn.classList.remove('btn-success');
            btn.disabled = false;
        }, 2000);
    }

    showError(btn) {
        btn.innerText = "Error ❌";
        setTimeout(() => {
            btn.innerText = btn.dataset.originalText || "Save Output Configuration";
            btn.classList.remove('btn-success'); // just in case
            btn.disabled = false;
        }, 2000);
    }
}
