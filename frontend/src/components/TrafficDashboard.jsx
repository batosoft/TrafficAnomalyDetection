import React, { useEffect, useState } from 'react';
import { trafficService } from '../services/trafficService';
import { Line } from 'react-chartjs-2';
import {
  Chart as ChartJS,
  CategoryScale,
  LinearScale,
  PointElement,
  LineElement,
  Title,
  Tooltip,
  Legend
} from 'chart.js';

ChartJS.register(
  CategoryScale,
  LinearScale,
  PointElement,
  LineElement,
  Title,
  Tooltip,
  Legend
);

export const TrafficDashboard = () => {
  const [trafficData, setTrafficData] = useState([]);
  const [anomalies, setAnomalies] = useState([]);

  useEffect(() => {
    // Start polling for traffic data
    const stopPolling = trafficService.startPolling(({ trafficData, anomalies }) => {
      setTrafficData(trafficData);
      setAnomalies(anomalies);
    });

    // Cleanup polling on unmount
    return () => stopPolling();
  }, []);

  const chartData = {
    labels: trafficData.map(data => new Date(data.timestamp).toLocaleTimeString()),
    datasets: [
      {
        label: 'Vehicle Count',
        data: trafficData.map(data => data.vehicle_count),
        borderColor: 'rgb(75, 192, 192)',
        backgroundColor: 'rgba(75, 192, 192, 0.1)',
        fill: true,
        tension: 0.4,
        pointRadius: 2,
        pointHoverRadius: 5,
        borderWidth: 2
      },
      {
        label: 'Average Speed',
        data: trafficData.map(data => data.average_speed),
        borderColor: 'rgb(255, 99, 132)',
        backgroundColor: 'rgba(255, 99, 132, 0.1)',
        fill: true,
        tension: 0.4,
        pointRadius: 2,
        pointHoverRadius: 5,
        borderWidth: 2
      }
    ]
  };

  const chartOptions = {
    responsive: true,
    animation: {
      duration: 750,
      easing: 'easeInOutQuart'
    },
    interaction: {
      intersect: false,
      mode: 'index'
    },
    plugins: {
      legend: {
        position: 'top',
        labels: {
          usePointStyle: true,
          padding: 20
        }
      },
      title: {
        display: true,
        text: 'Traffic Overview',
        font: {
          size: 20
        },
        padding: 20
      },
      tooltip: {
        enabled: true,
        backgroundColor: 'rgba(0, 0, 0, 0.8)',
        titleFont: {
          size: 13
        },
        bodyFont: {
          size: 12
        },
        padding: 10,
        displayColors: true,
        callbacks: {
          label: function(context) {
            const label = context.dataset.label || '';
            const value = context.parsed.y;
            return `${label}: ${value} ${label === 'Average Speed' ? 'mph' : 'vehicles'}`;
          }
        }
      }
    },
    scales: {
      x: {
        grid: {
          display: false
        },
        ticks: {
          maxRotation: 45,
          minRotation: 45
        }
      },
      y: {
        beginAtZero: true,
        grid: {
          color: 'rgba(0, 0, 0, 0.1)'
        }
      }
    },
    transitions: {
      zoom: {
        animation: {
          duration: 1000,
          easing: 'easeOutCubic'
        }
      }
    }
  };

  return (
    <div className="p-4">
      <div className="mb-8">
        <Line data={chartData} options={chartOptions} />
      </div>
      
      <div className="mt-4">
        <h2 className="text-xl font-bold mb-4">Recent Anomalies</h2>
        {anomalies.length > 0 ? (
          <div className="space-y-4">
            {anomalies.map((anomaly, index) => (
              <div key={index} className="bg-red-100 border-l-4 border-red-500 p-4">
                <h3 className="font-bold">{anomaly.anomaly_type}</h3>
                <p className="text-sm">{anomaly.description}</p>
                <p className="text-xs text-gray-600 mt-1">Severity: {anomaly.severity}</p>
              </div>
            ))}
          </div>
        ) : (
          <p>No recent anomalies detected</p>
        )}
      </div>
    </div>
  );
};