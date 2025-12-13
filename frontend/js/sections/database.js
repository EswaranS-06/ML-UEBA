import { ApiClient } from '../api/client.js';

export class DatabaseSection {
    constructor() {
        console.log("DatabaseSection initialized");
        this.statusEl = document.getElementById('db-status');
        this.hostEl = document.getElementById('db-host');
        this.nameEl = document.getElementById('db-name');
        this.userEl = document.getElementById('db-user');

        this.countEventsEl = document.getElementById('db-count-events');
        this.countRiskEl = document.getElementById('db-count-risk');
        this.lastInsertEl = document.getElementById('db-last-insert');

        this.grafanaStatusEl = document.getElementById('grafana-status');

        this.init();
    }

    init() {
        // Fetch stats immediately
        this.fetchStats();

        // Poll every 5 seconds
        setInterval(() => this.fetchStats(), 5000);
    }

    async fetchStats() {
        try {
            // Attempt to fetch from real API
            // GET /api/database/stats
            const data = await ApiClient.get('/database/stats');
            this.updateUI(data);
        } catch (error) {
            // Failed to connect to backend
            this.setDisconnected();
        }
    }

    updateUI(data) {
        if (!data) {
            this.setDisconnected();
            return;
        }

        // DB Status
        if (this.statusEl) {
            const isConnected = data.connected === true;
            this.statusEl.textContent = isConnected ? "Connected" : "Disconnected";
            this.statusEl.className = isConnected ? "value status-ok" : "value status-error";
        }

        if (this.hostEl) this.hostEl.textContent = data.host || "Unknown";
        if (this.nameEl) this.nameEl.textContent = data.database || "Unknown";
        if (this.userEl) this.userEl.textContent = data.user || "Unknown";

        if (this.countEventsEl) this.countEventsEl.textContent = `${(data.rows_events || 0).toLocaleString()} rows`;
        if (this.countRiskEl) this.countRiskEl.textContent = `${(data.rows_risk || 0).toLocaleString()} rows`;

        if (this.lastInsertEl) this.lastInsertEl.textContent = data.last_insert || "Never";

        // Grafana Status
        if (this.grafanaStatusEl) {
            const grafanaOk = data.grafana_connected !== false;
            this.grafanaStatusEl.textContent = grafanaOk ? "Connected" : "Failed";
            this.grafanaStatusEl.className = grafanaOk ? "value status-ok" : "value status-error";
        }
    }

    setDisconnected() {
        // DB Status
        if (this.statusEl) {
            this.statusEl.textContent = "Failed";
            this.statusEl.className = "value status-error";
        }

        // Grafana Status
        if (this.grafanaStatusEl) {
            this.grafanaStatusEl.textContent = "Failed";
            this.grafanaStatusEl.className = "value status-error";
        }
    }
}
