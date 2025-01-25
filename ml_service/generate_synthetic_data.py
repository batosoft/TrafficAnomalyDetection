import random
from datetime import datetime, timedelta
import json

def generate_normal_traffic():
    return {
        'vehicle_count': random.randint(50, 150),
        'average_speed': random.uniform(40, 70),
        'congestion_level': random.uniform(0.3, 0.7),
        'time_of_day': random.randint(0, 23),
        'timestamp': datetime.now().isoformat()
    }

def generate_anomaly():
    anomaly_types = [
        # High traffic volume anomaly
        lambda: {
            'vehicle_count': random.randint(151, 250),
            'average_speed': random.uniform(20, 35),
            'congestion_level': random.uniform(0.7, 0.9),
            'time_of_day': random.randint(0, 23),
            'timestamp': datetime.now().isoformat()
        },
        # Traffic congestion anomaly
        lambda: {
            'vehicle_count': random.randint(80, 150),
            'average_speed': random.uniform(5, 19),
            'congestion_level': random.uniform(0.8, 1.0),
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

def generate_dataset(num_normal=50, num_anomalies=10):
    data = []
    
    # Generate normal traffic data
    for _ in range(num_normal):
        data.append(generate_normal_traffic())
    
    # Generate anomalies
    for _ in range(num_anomalies):
        data.append(generate_anomaly())
    
    # Shuffle the data to mix normal and anomalous patterns
    random.shuffle(data)
    return data

def save_to_file(data, filename='synthetic_traffic_data.json'):
    with open(filename, 'w') as f:
        json.dump(data, f, indent=2)

if __name__ == '__main__':
    # Generate synthetic dataset with 50 normal records and 10 anomalies
    dataset = generate_dataset()
    save_to_file(dataset)
    print(f'Generated {len(dataset)} traffic records with anomalies')