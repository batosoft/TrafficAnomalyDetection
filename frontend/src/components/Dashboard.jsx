import React, { useState, useEffect } from 'react';
import { Box, Grid, Paper, Typography, Card, CardContent } from '@mui/material';
import { Line } from 'react-chartjs-2';
import { Chart as ChartJS } from 'chart.js/auto';
import axios from 'axios';
import { toast } from 'react-toastify';

const Dashboard = () => {
  const [anomalies, setAnomalies] = useState([]);
  const [trafficData, setTrafficData] = useState({
    labels: [],
    datasets: []
  });

  useEffect(() => {
    fetchAnomalies();
    fetchTrafficData();
    
    // Set up polling for real-time updates
    const interval = setInterval(() => {
      fetchAnomalies();
      fetchTrafficData();
    }, 5000); // Update every 5 seconds
    
    return () => clearInterval(interval);
  }, []);

  const fetchAnomalies = async () => {
    try {
      const response = await axios.get('http://localhost:8000/api/anomalies');
      setAnomalies(response.data);
    } catch (error) {
      toast.error('Failed to fetch anomalies');
    }
  };

  const fetchTrafficData = async () => {
    try {
      const response = await axios.get('http://localhost:8000/api/traffic-data');
      setTrafficData({
        labels: response.data.map(d => new Date(d.timestamp).toLocaleTimeString()),
        datasets: [
          {
            label: 'Vehicle Count',
            data: response.data.map(d => d.vehicle_count),
            borderColor: '#1976d2',
            backgroundColor: 'rgba(25, 118, 210, 0.1)',
            fill: true,
            tension: 0.4,
            pointRadius: 2,
            pointHoverRadius: 5,
            borderWidth: 2
          },
          {
            label: 'Average Speed',
            data: response.data.map(d => d.average_speed),
            borderColor: '#dc004e',
            backgroundColor: 'rgba(220, 0, 78, 0.1)',
            fill: true,
            tension: 0.4,
            pointRadius: 2,
            pointHoverRadius: 5,
            borderWidth: 2
          }
        ]
      });
    } catch (error) {
      toast.error('Failed to fetch traffic data');
    }
  };

  return (
    <Box sx={{ flexGrow: 1, p: 3 }}>
      <Grid container spacing={3}>
        {/* Traffic Overview Chart */}
        <Grid item xs={12}>
          <Paper sx={{ p: 2 }}>
            <Typography variant="h6" gutterBottom>
              Traffic Overview
            </Typography>
            <Box sx={{ height: 300 }}>
              <Line
                data={trafficData}
                options={{
                  responsive: true,
                  maintainAspectRatio: false,
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
                }}
              />
            </Box>
          </Paper>
        </Grid>

        {/* Recent Anomalies */}
        <Grid item xs={12}>
          <Typography variant="h6" gutterBottom>
            Recent Anomalies
          </Typography>
          <Grid container spacing={2}>
            {anomalies.map((anomaly) => (
              <Grid item xs={12} sm={6} md={4} key={anomaly.id}>
                <Card>
                  <CardContent>
                    <Typography color="textSecondary" gutterBottom>
                      {new Date(anomaly.timestamp).toLocaleString()}
                    </Typography>
                    <Typography variant="h6" component="h2">
                      {anomaly.anomaly_type}
                    </Typography>
                    <Typography color="textSecondary">
                      Severity: {(anomaly.severity * 100).toFixed(1)}%
                    </Typography>
                    <Typography variant="body2" component="p">
                      {anomaly.description}
                    </Typography>
                    <Typography color="textSecondary">
                      Status: {anomaly.status}
                    </Typography>
                  </CardContent>
                </Card>
              </Grid>
            ))}
          </Grid>
        </Grid>
      </Grid>
    </Box>
  );
};

export default Dashboard;