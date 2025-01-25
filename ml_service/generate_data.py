import random
import json
from datetime import datetime, timedelta
import numpy as np

def generate_normal_traffic():
    return {
        'vehicle_count': random.randint(50, 120),
        'average_speed': random.uniform(40, 65),
        'congestion_level': random.uniform(0.2, 0.6),
        'time_of_day': random.randint(0, 23),
        'timestamp': datetime.now().isoformat()
    }

def generate_anomaly():
    anomaly_types = [
        # High traffic volume anomaly
        lambda: {
            'vehicle_count': random.randint(151, 300),
            'average_speed': random.uniform(15, 35),
            'congestion_level': random.uniform(0.6, 0.9),
            'time_of_day': random.randint(0, 23),
            'timestamp': datetime.now().isoformat()
        },
        # Traffic congestion anomaly
        lambda: {
            'vehicle_count': random.randint(80, 200),
            'average_speed': random.uniform(5, 25),
            'congestion_level': random.uniform(0.7, 1.0),
            'time_of_day': random.randint(0, 23),
            'timestamp': datetime.now().isoformat()
        },
        # Speeding violation anomaly
        lambda: {
            'vehicle_count': random.randint(20, 50),
            'average_speed': random.uniform(81, 120),
            'congestion_level': random.uniform(0.1, 0.3),
            'time_of_day': random.randint(0, 23),
            'timestamp': datetime.now().isoformat()
        }
    ]
    return random.choice(anomaly_types)()

def generate_dataset(num_normal=80, num_anomalies=40):  # Increased proportion of anomalies
    data = []
    
    # Generate normal traffic data
    for _ in range(num_normal):
        data.append(generate_normal_traffic())
    
    # Generate anomalies
    for _ in range(num_anomalies):
        data.append(generate_anomaly())
    
    # Shuffle the data
    random.shuffle(data)
    return data

if __name__ == '__main__':
    # Generate synthetic dataset
    dataset = generate_dataset()
    
    # Save to file
    with open('synthetic_traffic_data.json', 'w') as f:
        json.dump(dataset, f, indent=2)
    
    print(f'Generated {len(dataset)} traffic records with anomalies')
    print('Data saved to synthetic_traffic_data.json')