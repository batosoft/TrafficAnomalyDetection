# Road Traffic Anomaly Detection and Reporting System

A comprehensive application that uses AI and ML algorithms for detecting and reporting traffic anomalies in real-time.

## System Architecture

- **Backend**: FastAPI (Python) with PostgreSQL database
- **Frontend**: ReactJS for UI
- **ML Service**: Anomaly detection using Isolation Forest and AutoEncoders
- **Generative AI**: Ollama and GPT-4 integration
- **Notifications**: SendGrid (Email) and OneSignal (Push Notifications)
- **Deployment**: Docker-based microservices

## Project Structure

```
├── backend/              # FastAPI backend service
├── frontend/             # React frontend application
├── ml_service/           # ML model training and inference
├── notification_service/ # Email and push notification service
├── docker/              # Docker configuration files
├── docs/                # Project documentation
└── scripts/             # Utility scripts
```

## Features

- Real-time anomaly detection using ML algorithms
- AI-generated detailed anomaly reports
- Interactive dashboard with data visualization
- Admin interface for system management
- Email alerts and push notifications
- RESTful APIs with JWT authentication
- Role-based access control

## Setup Instructions

1. Clone the repository
2. Install Docker and Docker Compose
3. Configure environment variables
4. Run `docker-compose up` to start all services

## API Documentation

API documentation is available at `/docs` endpoint when the server is running.

## Development

### Backend Setup
```bash
cd backend
python -m venv venv
source venv/bin/activate  # On Windows: .\venv\Scripts\activate
pip install -r requirements.txt
uvicorn main:app --reload
```

### Frontend Setup
```bash
cd frontend
npm install
npm run dev
```

## License

MIT