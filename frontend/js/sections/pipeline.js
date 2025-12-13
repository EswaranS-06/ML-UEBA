import { ApiClient } from '../api/client.js';

export class PipelineSection {
    constructor() {
        this.saveButton = document.querySelector('#pipeline-panel .btn-primary');
        this.init();
    }

    init() {
        if (this.saveButton) {
            this.saveButton.removeAttribute('onclick');
            this.saveButton.addEventListener('click', () => this.saveConfiguration());
        }
    }

    async saveConfiguration() {
        const btn = this.saveButton;
        this.setLoading(btn, true);

        const config = this.gatherConfig();

        try {
            await ApiClient.post('/pipeline/config', config);
            this.showSuccess(btn);
            if (window.logAction) window.logAction(`[INFO] Pipeline configuration updated.`);
        } catch (error) {
            alert(`Error saving pipeline: ${error.message}`);
            this.showError(btn);
        }
    }

    gatherConfig() {
        // We will target checkboxes by their labels or direct IDs if available.
        // Since the current HTML structure relies on label > input, but doesn't have unique IDs for every single one,
        // we can select by the text content or order.
        // For robustness, I'll recommend we add data-attributes or IDs in the HTML update.
        // Assuming the HTML update (which runs in parallel/next) adds IDs or data-keys.

        // Fallback: gathering by specific order or known text if IDs are missing (fragile),
        // so I will implement this EXPECTING IDs to be added in the HTML step.

        return {
            preprocessing: {
                enabled: this.isChecked('check-preprocessing'),
                parsing: this.isChecked('check-parsing'),
                feature_engineering: this.isChecked('check-feature-eng')
            },
            nlp: {
                username_recovery: this.isChecked('check-nlp-username'),
                entity_enrichment: this.isChecked('check-nlp-regex'),
                embeddings: this.isChecked('check-nlp-embed')
            },
            models: {
                isolation_forest: this.isChecked('check-ml-if'),
                lstm: this.isChecked('check-ml-lstm')
            },
            drift: {
                page_hinkley: this.isChecked('check-drift-ph')
            }
        };
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
            this.resetBtn(btn);
        }, 2000);
    }

    showError(btn) {
        btn.innerText = "Error ❌";
        setTimeout(() => {
            this.resetBtn(btn);
        }, 2000);
    }

    resetBtn(btn) {
        btn.innerText = btn.dataset.originalText || "Save Pipeline Configuration";
        btn.classList.remove('btn-success');
        btn.disabled = false;
    }
}
