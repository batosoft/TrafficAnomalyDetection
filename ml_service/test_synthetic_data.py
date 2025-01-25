import json
import requests
from generate_synthetic_data import generate_dataset

def test_with_synthetic_data():
    # Generate synthetic dataset
    print("Generating synthetic dataset...")
    dataset = generate_dataset(num_normal=50, num_anomalies=10)
    
    # Prepare the request data
    test_data = {"data": dataset}
    
    try:
        # Send request to the ML service
        print("\nSending data to ML service...")
        response = requests.post(
            "http://localhost:8001/detect",
            json=test_data
        )
        
        if response.status_code == 200:
            result = response.json()
            print("\nAnomaly Detection Results:")
            print(json.dumps(result, indent=2))
            
            # Count detected anomalies
            anomalies_detected = sum(result['anomalies'])
            print(f"\nDetected {anomalies_detected} anomalies out of {len(dataset)} records")
            
            # Analyze detection rate
            expected_anomalies = 10  # We generated 10 anomalies
            print(f"Expected anomalies: {expected_anomalies}")
            print(f"Detection rate: {(anomalies_detected/expected_anomalies)*100:.2f}%")
            
        else:
            print(f"\nTest failed: Received status code {response.status_code}")
            print(f"Error: {response.text}")
            
    except requests.exceptions.ConnectionError:
        print("\nTest failed: Could not connect to the ML service")
        print("Make sure the ML service is running on port 8001")
    except Exception as e:
        print(f"\nTest failed: {str(e)}")

if __name__ == '__main__':
    test_with_synthetic_data()