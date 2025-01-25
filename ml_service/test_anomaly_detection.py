import requests
import json

def test_anomaly_detection():
    # Test data
    test_data = {
        "data": [
            {
                "vehicle_count": 100,
                "average_speed": 60.0,
                "congestion_level": 0.5,
                "time_of_day": 12.0
            },
            {
                "vehicle_count": 500,  # Anomalous value
                "average_speed": 20.0,
                "congestion_level": 0.9,
                "time_of_day": 12.0
            }
        ]
    }

    try:
        # Send request to the ML service
        response = requests.post(
            "http://localhost:8001/detect",
            json=test_data
        )
        
        if response.status_code == 200:
            result = response.json()
            print("Anomaly Detection Results:")
            print(json.dumps(result, indent=2))
            
            # Verify the response structure
            if "anomalies" in result:
                print("\nTest passed: Response contains 'anomalies' key")
                print(f"Number of predictions: {len(result['anomalies'])}")
            else:
                print("\nTest failed: Response missing 'anomalies' key")
        else:
            print(f"\nTest failed: Received status code {response.status_code}")
            print(f"Error: {response.text}")
            
    except requests.exceptions.ConnectionError:
        print("\nTest failed: Could not connect to the ML service")
        print("Make sure the ML service is running on port 8001")
    except Exception as e:
        print(f"\nTest failed: {str(e)}")

if __name__ == "__main__":
    print("Running anomaly detection test...\n")
    test_anomaly_detection()