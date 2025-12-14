import { ApiClient } from '../api/client.js';

export class LogsSection {
    constructor() {
        this.logContainer = document.getElementById('log-output');
        this.btnClear = document.getElementById('btn-clear-logs');
        this.lastLogId = 0; // Tracking cursor for incremental updates

        this.init();
    }

    init() {
        if (this.btnClear) {
            this.btnClear.addEventListener('click', () => this.clearLogs());
        }

        // Poll for new logs every 1.5 seconds
        setInterval(() => this.fetchLogs(), 1500);
    }

    async fetchLogs() {
        try {
            // GET /api/logs?after_id=123
            const data = await ApiClient.get(`/logs?after_id=${this.lastLogId}`);

            if (data && data.logs && data.logs.length > 0) {
                this.appendLogs(data.logs);
                // Update cursor
                this.lastLogId = data.logs[data.logs.length - 1].id || this.lastLogId;
            }
        } catch (error) {
            // Silent fail for logs, or maybe a small console warn
            // console.warn("Log fetch failed", error);
        }
    }

    appendLogs(logs) {
        if (!this.logContainer) return;

        logs.forEach(log => {
            const div = document.createElement('div');
            // Check level for styling
            const levelClass = (log.level || 'INFO').toLowerCase();
            // map 'warning' to 'warn' if needed, assuming css has .info .warn .error

            div.className = `log-line ${levelClass}`;

            // Format Timestamp
            // Assuming log.timestamp is ISO string
            const tsStr = log.timestamp ? `[${this.formatTime(log.timestamp)}]` : '';

            div.innerHTML = `<span class="ts">${tsStr}</span> ${log.message}`;
            this.logContainer.appendChild(div);
        });

        // Auto-scroll to bottom
        this.logContainer.scrollTop = this.logContainer.scrollHeight;
    }

    clearLogs() {
        if (this.logContainer) {
            this.logContainer.innerHTML = '';
            // Reset cursor if we cleared? Depends on UX. 
            // Usually "Clear Console" is local only.
        }
    }

    formatTime(isoString) {
        try {
            const d = new Date(isoString);
            return `${d.getFullYear()}-${String(d.getMonth() + 1).padStart(2, '0')}-${String(d.getDate()).padStart(2, '0')} ${String(d.getHours()).padStart(2, '0')}:${String(d.getMinutes()).padStart(2, '0')}:${String(d.getSeconds()).padStart(2, '0')}`;
        } catch (e) {
            return isoString;
        }
    }
}
