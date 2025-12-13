/**
 * ML-UEBA API Client
 * centralized error handling and request wrapping.
 */

const API_BASE = 'http://localhost:8000/api'; // Defaulting to standard FastAPI port

export class ApiClient {
    static async post(endpoint, data) {
        return this.request(endpoint, {
            method: 'POST',
            headers: { 'Content-Type': 'application/json' },
            body: JSON.stringify(data)
        });
    }

    static async upload(endpoint, formData) {
        return this.request(endpoint, {
            method: 'POST',
            body: formData
            // Content-Type is auto-set for FormData
        });
    }

    static async get(endpoint) {
        return this.request(endpoint, { method: 'GET' });
    }

    static async request(endpoint, options) {
        try {
            const response = await fetch(`${API_BASE}${endpoint}`, options);

            if (!response.ok) {
                const errorBody = await response.json().catch(() => ({}));
                throw new Error(errorBody.detail || `HTTP Error: ${response.status}`);
            }

            return await response.json();
        } catch (error) {
            console.error('API Request Failed:', error);
            throw error;
        }
    }
}
