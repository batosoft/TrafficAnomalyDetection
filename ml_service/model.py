import numpy as np
from sklearn.ensemble import IsolationForest
from sklearn.preprocessing import StandardScaler
from typing import List, Dict, Any
import joblib
import os

class AnomalyDetector:
    def __init__(self, model_path: str = "isolation_forest.joblib"):
        self.model_path = model_path
        self.model = IsolationForest(
            contamination=0.4,  # Increased to detect more anomalies
            random_state=42,
            n_estimators=500,  # Increased for better detection
            max_samples='auto'
        )
        self.scaler = StandardScaler()
        # Initialize with more diverse default data
        default_data = [
            {"vehicle_count": 100, "average_speed": 60.0, "congestion_level": 0.5, "time_of_day": 8.0},
            {"vehicle_count": 250, "average_speed": 30.0, "congestion_level": 0.8, "time_of_day": 9.0},
            {"vehicle_count": 150, "average_speed": 55.0, "congestion_level": 0.6, "time_of_day": 13.0},
            {"vehicle_count": 300, "average_speed": 25.0, "congestion_level": 0.9, "time_of_day": 17.0},
            {"vehicle_count": 80, "average_speed": 65.0, "congestion_level": 0.3, "time_of_day": 22.0}
        ]
        # Train the model with default data
        X = self.preprocess_data(default_data)
        self.model.fit(X)
        joblib.dump(self.model, self.model_path)
    
    def load_or_train_model(self):
        if os.path.exists(self.model_path):
            self.model = joblib.load(self.model_path)
        else:
            self.model = IsolationForest(
                contamination=0.1,
                random_state=42
            )
            # Train with some default data if model doesn't exist
            default_data = [
                {"vehicle_count": 100, "average_speed": 60.0, "congestion_level": 0.5, "time_of_day": 12.0},
                {"vehicle_count": 150, "average_speed": 55.0, "congestion_level": 0.6, "time_of_day": 13.0},
                {"vehicle_count": 200, "average_speed": 50.0, "congestion_level": 0.7, "time_of_day": 14.0}
            ]
            self.train(default_data)
    
    def preprocess_data(self, data: List[Dict[str, Any]]) -> np.ndarray:
        features = np.array([
            [
                d['vehicle_count'],
                d['average_speed'],
                d['congestion_level'],
                d['time_of_day']
            ] for d in data
        ])
        return self.scaler.fit_transform(features)
    
    def detect_anomalies(self, data: List[Dict[str, Any]]) -> List[bool]:
        if not data:
            return []
        
        X = self.preprocess_data(data)
        predictions = self.model.predict(X)
        # Convert predictions to Python native boolean values
        return [bool(pred == -1) for pred in predictions]
    
    def train(self, training_data: List[Dict[str, Any]]):
        X = self.preprocess_data(training_data)
        self.model.fit(X)
        joblib.dump(self.model, self.model_path)
    
    def get_anomaly_score(self, data_point: Dict[str, Any]) -> float:
        X = self.preprocess_data([data_point])
        return -self.model.score_samples(X)[0]
    
    def analyze_anomaly(self, data_point: Dict[str, Any]) -> Dict[str, Any]:
        score = self.get_anomaly_score(data_point)
        severity = min(1.0, score / 2)  # Normalize score to 0-1 range
        
        analysis = {
            "severity": severity,
            "anomaly_type": self._determine_anomaly_type(data_point),
            "description": self._generate_description(data_point, severity)
        }
        return analysis
    
    def _determine_anomaly_type(self, data: Dict[str, Any]) -> str:
        if data['vehicle_count'] > 150:  # Further lowered threshold
            return "high_traffic_volume"
        elif data['average_speed'] < 40:  # Increased threshold
            return "traffic_congestion"
        elif data['average_speed'] > 60:  # Lowered threshold
            return "speeding_violation"
        elif data['congestion_level'] > 0.6:  # Lowered threshold
            return "severe_congestion"
        return "unusual_pattern"
    
    def _generate_description(self, data: Dict[str, Any], severity: float) -> str:
        anomaly_type = self._determine_anomaly_type(data)
        severity_level = "high" if severity > 0.7 else "moderate" if severity > 0.4 else "low"
        
        descriptions = {
            "high_traffic_volume": f"Unusually {severity_level} traffic volume detected with {data['vehicle_count']} vehicles",
            "traffic_congestion": f"{severity_level.capitalize()} congestion detected with average speed of {data['average_speed']}km/h",
            "speeding_violation": f"{severity_level.capitalize()} speed violation detected with average speed of {data['average_speed']}km/h",
            "unusual_pattern": f"{severity_level.capitalize()} anomaly detected in traffic pattern"
        }
        return descriptions[anomaly_type]