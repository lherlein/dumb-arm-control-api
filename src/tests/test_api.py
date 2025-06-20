"""
Test script for the Robot Arm Control REST API.
This script tests all API endpoints and verifies responses.
"""

import requests
import time
import json
from typing import Dict, Any

class APITester:
    def __init__(self, base_url: str = "http://localhost:8000"):
        self.base_url = base_url
        
    def test_root_endpoint(self) -> bool:
        """Test the root endpoint."""
        print("\nTesting root endpoint...")
        try:
            response = requests.get(f"{self.base_url}/")
            response.raise_for_status()
            print(f"Response: {response.json()}")
            return True
        except Exception as e:
            print(f"Error: {str(e)}")
            return False

    def test_start_servo(self, servo_id: str, direction: str) -> bool:
        """Test starting a servo."""
        print(f"\nTesting start servo {servo_id} {direction}...")
        try:
            response = requests.post(
                f"{self.base_url}/api/servos/{servo_id}/start",
                json={"direction": direction}
            )
            response.raise_for_status()
            print(f"Response: {response.json()}")
            return True
        except Exception as e:
            print(f"Error: {str(e)}")
            return False

    def test_stop_servo(self, servo_id: str) -> bool:
        """Test stopping a servo."""
        print(f"\nTesting stop servo {servo_id}...")
        try:
            response = requests.post(
                f"{self.base_url}/api/servos/{servo_id}/stop"
            )
            response.raise_for_status()
            print(f"Response: {response.json()}")
            return True
        except Exception as e:
            print(f"Error: {str(e)}")
            return False

    def test_emergency_stop(self) -> bool:
        """Test emergency stop."""
        print("\nTesting emergency stop...")
        try:
            response = requests.post(
                f"{self.base_url}/api/emergency-stop"
            )
            response.raise_for_status()
            print(f"Response: {response.json()}")
            return True
        except Exception as e:
            print(f"Error: {str(e)}")
            return False

    def test_get_status(self) -> Dict[str, Any]:
        """Test getting system status."""
        print("\nTesting get status...")
        try:
            response = requests.get(f"{self.base_url}/api/status")
            response.raise_for_status()
            status = response.json()
            print(f"Response: {json.dumps(status, indent=2)}")
            return status
        except Exception as e:
            print(f"Error: {str(e)}")
            return {}

    def run_servo_movement_test(self, servo_id: str) -> bool:
        """Run a complete movement test for a servo."""
        print(f"\nRunning movement test for servo {servo_id}")
        
        try:
            # Start forward
            if not self.test_start_servo(servo_id, "forward"):
                return False
            time.sleep(2)  # Run for 2 seconds
            
            # Stop
            if not self.test_stop_servo(servo_id):
                return False
            time.sleep(1)  # Pause
            
            # Start backward
            if not self.test_start_servo(servo_id, "backward"):
                return False
            time.sleep(2)  # Run for 2 seconds
            
            # Stop
            if not self.test_stop_servo(servo_id):
                return False
            
            return True
            
        except Exception as e:
            print(f"Error during movement test: {str(e)}")
            return False

def main():
    """Run API tests."""
    # Use the Raspberry Pi's IP address
    api_tester = APITester("http://192.168.2.120:8000")
    
    try:
        # Test root endpoint
        if not api_tester.test_root_endpoint():
            print("Root endpoint test failed")
            return
        
        # Get initial status
        initial_status = api_tester.test_get_status()
        if not initial_status:
            print("Failed to get initial status")
            return
        
        # Test each servo
        servos = ["base", "shoulder", "elbow", "wrist_rotate", "gripper"]
        for servo_id in servos:
            input(f"\nPress Enter to test {servo_id} servo (or Ctrl+C to skip)...")
            if not api_tester.run_servo_movement_test(servo_id):
                print(f"Movement test failed for {servo_id}")
                api_tester.test_emergency_stop()
                return
        
        # Test emergency stop
        if not api_tester.test_emergency_stop():
            print("Emergency stop test failed")
            return
        
        # Get final status
        final_status = api_tester.test_get_status()
        if not final_status:
            print("Failed to get final status")
            return
        
        print("\nAPI tests completed successfully!")
        
    except KeyboardInterrupt:
        print("\nTests interrupted by user")
        api_tester.test_emergency_stop()
    except Exception as e:
        print(f"\nError during testing: {str(e)}")
        api_tester.test_emergency_stop()

if __name__ == "__main__":
    main() 