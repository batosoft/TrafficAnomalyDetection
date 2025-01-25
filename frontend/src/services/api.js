import axios from 'axios';

const API_URL = import.meta.env.VITE_API_URL || 'http://localhost:8000';

const api = axios.create({
    baseURL: API_URL,
    headers: {
        'Content-Type': 'application/json',
    },
});

// Add a request interceptor to include the JWT token
api.interceptors.request.use(
    (config) => {
        const token = localStorage.getItem('token');
        if (token) {
            config.headers.Authorization = `Bearer ${token}`;
        }
        // Ensure URL ends with trailing slash
        if (!config.url.endsWith('/')) {
            config.url += '/';
        }
        return config;
    },
    (error) => {
        return Promise.reject(error);
    }
);

// Add a response interceptor to handle errors
api.interceptors.response.use(
    (response) => response,
    (error) => {
        if (error.response?.status === 401) {
            localStorage.removeItem('token');
            window.location.href = '/login';
        }
        return Promise.reject(error);
    }
);

export const login = async (credentials) => {
    const response = await api.post('/api/auth/token/', credentials);
    const { access_token } = response.data;
    if (access_token) {
        localStorage.setItem('token', access_token);
        api.defaults.headers.common['Authorization'] = `Bearer ${access_token}`;
    }
    return response.data;
};

export const getAnomalies = async (params) => {
    const response = await api.get('/api/anomalies/', { params });
    return response.data;
};

export const getTrafficData = async (params) => {
    const response = await api.get('/api/traffic-data/', { params });
    return response.data;
};

export default api;