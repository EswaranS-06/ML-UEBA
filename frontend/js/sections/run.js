import { ApiClient } from '../api/client.js';

export class RunSection {
    constructor() {
        this.statusEl = document.getElementById('pipeline-status');
        this.btnStart = document.getElementById('btn-start');
        this.btnPause = document.getElementById('btn-pause');
        this.btnStop = document.getElementById('btn-stop');

        this.metricLogsSec = document.getElementById('metric-logs-sec');
        this.metricEventsComp = document.getElementById('metric-events-processed');
        this.metricAnomalies = document.getElementById('metric-anomalies');
        this.metricDrift = document.getElementById('metric-drift');

        this.init();
    }

    init() {
        if (this.btnStart) this.btnStart.addEventListener('click', () => this.handleAction('start'));
        if (this.btnPause) this.btnPause.addEventListener('click', () => this.handleAction('pause'));
        if (this.btnStop) this.btnStop.addEventListener('click', () => this.handleAction('stop'));

        // Start polling for metrics
        setInterval(() => this.fetchMetrics(), 2000);
    }

    async handleAction(action) {
        try {
            if (window.logAction) window.logAction(`[INFO] Sending ${action.toUpperCase()} command...`);

            // POST /api/run/{action}
            await ApiClient.post(`/run/${action}`, {});

            // Optimistically update status
            this.updateStatus(action);

        } catch (error) {
            alert(`Failed to ${action} pipeline: ${error.message}`);
        }
    }

    async fetchMetrics() {
        try {
            // GET /api/run/metrics
            const data = await ApiClient.get('/run/metrics');
            this.updateUI(data);
        } catch (error) {
            // backend down or other error
            // console.warn("Metrics fetch failed", error);
        }
    }

    updateStatus(action) {
        if (!this.statusEl) return;

        switch (action) {
            case 'start':
                this.statusEl.textContent = "RUNNING";
                this.statusEl.className = "status-big running"; // Ensure CSS has .running { color: green }
                this.statusEl.style.color = "var(--success)"; // Fallback
                break;
            case 'pause':
                this.statusEl.textContent = "PAUSED";
                this.statusEl.className = "status-big";
                this.statusEl.style.color = "var(--warning)";
                break;
            case 'stop':
                this.statusEl.textContent = "STOPPED";
                this.statusEl.className = "status-big";
                this.statusEl.style.color = "var(--danger)";
                break;
        }
    }

    updateUI(data) {
        if (!data) return;

        // Status Sync (in case of external changes)
        if (data.status) {
            this.updateStatus(data.status.toLowerCase());
        }

        // Metrics
        if (this.metricLogsSec) this.metricLogsSec.textContent = data.logs_per_sec || 0;
        if (this.metricEventsComp) this.metricEventsComp.textContent = (data.events_processed || 0).toLocaleString();

        if (this.metricAnomalies) {
            const val = data.anomalies || 0;
            this.metricAnomalies.textContent = val;
            this.metricAnomalies.className = val > 0 ? "metric-val bad" : "metric-val";
        }

        if (this.metricDrift) {
            const detected = data.drift_detected === true;
            this.metricDrift.textContent = detected ? "YES" : "NO";
            this.metricDrift.className = detected ? "metric-val bad" : "metric-val good";
        }
    }
}
