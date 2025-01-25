from fastapi import FastAPI, Depends, HTTPException, status
from fastapi.middleware.cors import CORSMiddleware
from fastapi.security import OAuth2PasswordBearer
from sqlalchemy.orm import Session
from datetime import datetime, timedelta
from typing import List, Optional
import uvicorn

app = FastAPI(
    title="Traffic Anomaly Detection API",
    description="API for detecting and reporting traffic anomalies using AI/ML",
    version="1.0.0"
)

# CORS configuration
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # In production, replace with specific origins
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# API routes will be included from separate modules
from api import auth, anomalies, users, admin, traffic_data

# Include routers
app.include_router(auth.router, prefix="/api/auth", tags=["Authentication"])
app.include_router(anomalies.router, prefix="/api/anomalies", tags=["Anomalies"])
app.include_router(users.router, prefix="/api/users", tags=["Users"])
app.include_router(admin.router, prefix="/api/admin", tags=["Admin"])
app.include_router(traffic_data.router, prefix="/api/traffic-data", tags=["traffic-data"])

@app.get("/")
async def root():
    return {"message": "Traffic Anomaly Detection API"}

if __name__ == "__main__":
    uvicorn.run("main:app", host="0.0.0.0", port=8000, reload=True)