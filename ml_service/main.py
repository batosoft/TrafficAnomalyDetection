from fastapi import FastAPI, HTTPException, BackgroundTasks
from pydantic import BaseModel
from typing import List, Dict, Any
from model import AnomalyDetector
from realtime_traffic import RealtimeTrafficSimulator
import uvicorn
import asyncio

app = FastAPI(
    title="Traffic Anomaly Detection ML Service",
    description="ML service for detecting traffic anomalies",
    version="1.0.0"
)

# Initialize components
detector = AnomalyDetector()
simulator = RealtimeTrafficSimulator(
    data_interval=1.0,  # Generate data every second
    anomaly_probability=0.2,  # 20% chance of anomaly
    save_interval=5.0  # Save to file every 5 seconds
)

# Background task to run the simulator
async def run_simulator():
    await simulator.start_simulation()

# Start the simulator when the application starts
@app.on_event("startup")
async def startup_event():
    try:
        # Create a background task for the simulator
        asyncio.create_task(run_simulator())
        print("Started real-time traffic simulator")
    except Exception as e:
        print(f"Error starting simulator: {e}")

# Cleanup when the application shuts down
@app.on_event("shutdown")
async def shutdown_event():
    simulator.stop_simulation()

class TrafficData(BaseModel):
    data: List[Dict[str, Any]]

@app.post("/detect")
async def detect_anomalies(data: TrafficData):
    try:
        anomalies = detector.detect_anomalies(data.data)
        return {"anomalies": anomalies}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.post("/analyze")
async def analyze_anomaly(data: Dict[str, Any]):
    try:
        analysis = detector.analyze_anomaly(data)
        return analysis
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.get("/")
async def root():
    return {
        "service": "Traffic Anomaly Detection ML Service",
        "status": "running",
        "simulator_running": simulator.is_running
    }

if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8001)

@app.post("/train")
async def train_model(data: TrafficData):
    try:
        traffic_data = [d.dict() for d in data.data]
        detector.train(traffic_data)
        return {"message": "Model trained successfully"}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

if __name__ == "__main__":
    uvicorn.run("main:app", host="0.0.0.0", port=8002, reload=True)