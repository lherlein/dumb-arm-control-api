#!/usr/bin/env python3
"""
Test script for the servo controller hardware interface.
This script performs basic functionality tests for each servo.
"""

import time
from ..hardware.servo_controller import ServoController

def test_single_servo(controller: ServoController, servo_id: str):
    """Test a single servo's basic movements."""
    print(f"\nTesting servo: {servo_id}")
    
    # Test forward movement
    print("Testing forward movement...")
    controller.start_servo(servo_id, "forward")
    time.sleep(2)  # Run for 2 seconds
    controller.stop_servo(servo_id)
    time.sleep(1)  # Pause between movements
    
    # Test backward movement
    print("Testing backward movement...")
    controller.start_servo(servo_id, "backward")
    time.sleep(2)  # Run for 2 seconds
    controller.stop_servo(servo_id)
    time.sleep(1)  # Pause between tests
    
    # Get and print status
    status = controller.get_all_servo_status()[servo_id]
    print(f"Servo status: {status}")

def main():
    """Run hardware tests for all servos."""
    try:
        print("Initializing Servo Controller...")
        controller = ServoController()
        controller.initialize_servos()
        
        # Test each servo
        servos = ["base", "shoulder", "elbow", "wrist_rotate", "gripper"]
        
        for servo_id in servos:
            input(f"\nPress Enter to test {servo_id} servo (or Ctrl+C to skip)...")
            test_single_servo(controller, servo_id)
        
        # Test emergency stop
        print("\nTesting emergency stop...")
        controller.start_servo("base", "forward")
        time.sleep(1)
        controller.emergency_stop()
        print("Emergency stop activated. Checking if all servos stopped...")
        
        # Verify all servos are stopped
        statuses = controller.get_all_servo_status()
        all_stopped = all(status["status"] == "stopped" for status in statuses.values())
        print(f"All servos stopped: {all_stopped}")
        
        print("\nHardware tests completed successfully!")
        
    except KeyboardInterrupt:
        print("\nTests interrupted by user.")
        controller.emergency_stop()
    except Exception as e:
        print(f"\nError during testing: {str(e)}")
        controller.emergency_stop()
    finally:
        print("Ensuring all servos are stopped...")
        controller.emergency_stop()

if __name__ == "__main__":
    main() 