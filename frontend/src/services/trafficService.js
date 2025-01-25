import axios from 'axios';

const API_URL = 'http://localhost:8000/api';

export const trafficService = {
    // Fetch latest traffic data
    async getTrafficData() {
        try {
            const response = await axios.get(`${API_URL}/traffic`);
            return response.data;
        } catch (error) {
            console.error('Error fetching traffic data:', error);
            return [];
        }
    },

    // Fetch recent anomalies
    async getRecentAnomalies() {
        try {
            const response = await axios.get(`${API_URL}/anomalies/recent`);
            return response.data;
        } catch (error) {
            console.error('Error fetching anomalies:', error);
            return [];
        }
    },

    // Start real-time data polling
    startPolling(callback, interval = 5000) {
        const pollId = setInterval(async () => {
            try {
                const [trafficData, anomalies] = await Promise.all([
                    this.getTrafficData(),
                    this.getRecentAnomalies()
                ]);
                callback({ trafficData, anomalies });
            } catch (error) {
                console.error('Polling error:', error);
            }
        }, interval);

        return () => clearInterval(pollId); // Return cleanup function
    }
};