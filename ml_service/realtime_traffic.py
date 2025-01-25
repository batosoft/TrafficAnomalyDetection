import asyncio
import random
from datetime import datetime
from generate_synthetic_data import generate_normal_traffic, generate_anomaly
from model import AnomalyDetector
import json
import os

class RealtimeTrafficSimulator:
    def __init__(self, 
                 data_interval: float = 1.0,
                 anomaly_probability: float = 0.2,
                 save_interval: float = 5.0,
                 data_file: str = 'synthetic_traffic_data.json'):
        self.data_interval = data_interval
        self.anomaly_probability = anomaly_probability
        self.save_interval = save_interval
        self.data_file = data_file
        self.traffic_data = []
        self.detector = AnomalyDetector()
        self.is_running = False
        
        # Initialize with some data if file exists
        if os.path.exists(self.data_file):
            try:
                with open(self.data_file, 'r') as f:
                    self.traffic_data = json.load(f)
            except Exception as e:
                print(f"Error loading existing data: {e}")

    async def generate_traffic_data(self):
        """Generate either normal traffic data or an anomaly based on probability"""
        if random.random() < self.anomaly_probability:
            return generate_anomaly()
        return generate_normal_traffic()

    async def save_to_file(self):
        """Save accumulated traffic data to file"""
        try:
            with open(self.data_file, 'w') as f:
                json.dump(self.traffic_data, f, indent=2)
        except Exception as e:
            print(f"Error saving data: {e}")

    async def process_data(self, data):
        """Process traffic data through anomaly detector"""
        is_anomaly = self.detector.detect_anomalies([data])[0]
        if is_anomaly:
            analysis = self.detector.analyze_anomaly(data)
            print(f"Anomaly detected! {analysis['description']}")
        return is_anomaly

    async def start_simulation(self):
        """Start continuous traffic data generation and processing"""
        self.is_running = True
        last_save = datetime.now()

        while self.is_running:
            try:
                # Generate new traffic data
                data = await self.generate_traffic_data()
                
                # Process the data
                is_anomaly = await self.process_data(data)
                
                # Add to accumulated data
                self.traffic_data.append(data)
                
                # Keep only last 1000 records
                if len(self.traffic_data) > 1000:
                    self.traffic_data = self.traffic_data[-1000:]
                
                # Save to file periodically
                if (datetime.now() - last_save).total_seconds() >= self.save_interval:
                    await self.save_to_file()
                    last_save = datetime.now()
                
                # Wait for next interval
                await asyncio.sleep(self.data_interval)
                
            except Exception as e:
                print(f"Error in simulation: {e}")
                await asyncio.sleep(1)  # Wait before retrying

    def stop_simulation(self):
        """Stop the traffic simulation"""
        self.is_running = False
        
    async def cleanup(self):
        """Cleanup when stopping the simulation"""
        self.stop_simulation()
        await self.save_to_file()  # Final save

# Example usage
async def main():
    simulator = RealtimeTrafficSimulator(
        data_interval=1.0,  # Generate data every second
        anomaly_probability=0.2,  # 20% chance of anomaly
        save_interval=5.0  # Save to file every 5 seconds
    )
    try:
        await simulator.start_simulation()
    except KeyboardInterrupt:
        simulator.stop_simulation()
        await simulator.save_to_file()  # Final save

if __name__ == "__main__":
    asyncio.run(main())