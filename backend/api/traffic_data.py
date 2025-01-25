from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from typing import List
from datetime import datetime
import json
import os
import requests

from database import get_db
from models import TrafficData, User, Anomaly

router = APIRouter()

@router.get("/", response_model=List[dict])
async def get_traffic_data(db: Session = Depends(get_db)):
    try:
        # Read from the synthetic data file using relative path
        file_path = os.path.join(os.path.dirname(os.path.dirname(__file__)), 'synthetic_traffic_data.json')
        with open(file_path, 'r') as f:
            traffic_data = json.load(f)
            
        # Send data to ML service for anomaly detection
        try:
            ml_response = requests.post(
                'http://ml_service:8001/detect',
                json={"data": traffic_data}
            )
            anomalies = ml_response.json().get('anomalies', [])
            
            # Process anomalies from the response data
            for i, is_anomaly in enumerate(anomalies):
                if is_anomaly:
                    # Get detailed analysis for the anomaly
                    analysis = requests.post(
                        'http://ml_service:8001/analyze',
                        json=traffic_data[i]
                    ).json()
                    
                    # Store anomaly in database
                    anomaly = Anomaly(
                        location="System",
                        anomaly_type=analysis.get('anomaly_type', 'Unknown'),
                        severity=analysis.get('severity', 0.5),
                        description=analysis.get('description', ''),
                        status="detected"
                    )
                    db.add(anomaly)
            
            db.commit()
            
            # Return the original traffic data for the frontend
            return traffic_data
        except requests.RequestException as e:
            print(f"Warning: ML service communication error: {e}")
            
        return traffic_data
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=str(e)
        )