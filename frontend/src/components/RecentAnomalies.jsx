import React, { useEffect, useState } from 'react';
import axios from 'axios';

const RecentAnomalies = () => {
    const [anomalies, setAnomalies] = useState([]);

    useEffect(() => {
        const fetchAnomalies = async () => {
            try {
                const response = await axios.get('http://localhost:8000/api/anomalies?limit=5&status=detected');
                setAnomalies(response.data);
            } catch (error) {
                console.error('Error fetching anomalies:', error);
            }
        };

        fetchAnomalies();
        // Refresh anomalies every 30 seconds
        const interval = setInterval(fetchAnomalies, 30000);
        return () => clearInterval(interval);
    }, []);

    const getSeverityColor = (severity) => {
        if (severity >= 0.7) return 'text-red-600';
        if (severity >= 0.4) return 'text-yellow-600';
        return 'text-green-600';
    };

    return (
        <div className="bg-white rounded-lg shadow p-6">
            <h2 className="text-xl font-semibold mb-4">Recent Anomalies</h2>
            <div className="space-y-4">
                {anomalies.length === 0 ? (
                    <p className="text-gray-500">No recent anomalies detected</p>
                ) : (
                    anomalies.map((anomaly) => (
                        <div key={anomaly.id} className="border-l-4 border-l-blue-500 pl-4 py-2">
                            <div className="flex justify-between items-start">
                                <div>
                                    <h3 className="font-medium">{anomaly.anomaly_type}</h3>
                                    <p className="text-sm text-gray-600">{anomaly.description}</p>
                                </div>
                                <span className={`${getSeverityColor(anomaly.severity)} font-medium`}>
                                    {(anomaly.severity * 100).toFixed(0)}% Severity
                                </span>
                            </div>
                        </div>
                    ))
                )}
            </div>
        </div>
    );
};

export default RecentAnomalies;