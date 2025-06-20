"""
Test script for continuous rotation servo control.

This script performs a smooth sweep through the entire speed range
of a continuous rotation servo, from full speed CCW to full speed CW.
"""

import time
from gpiozero import PWMOutputDevice
import numpy as np
from ..hardware import gpio_config

def test_servo_sweep():
    """Test servo by sweeping through its entire speed range."""
    # Create PWM device for servo on GPIO 18
    servo = PWMOutputDevice(
        pin=18,
        frequency=gpio_config.PWM_FREQUENCY,
        initial_value=gpio_config.CENTER_DUTY_CYCLE
    )
    
    try:
        print("Starting servo speed sweep test...")
        print("Press Ctrl+C to stop the test")
        
        while True:  # Loop until interrupted
            # Sweep from -1.0 to 1.0 (CCW to CW)
            print("\nSweeping from max CCW to max CW...")
            for speed in np.arange(-1.0, 1.01, 0.1):  # Include 1.0 with 1.01
                duty_cycle = gpio_config.speed_to_duty_cycle(speed)
                servo.value = duty_cycle
                print(f"Speed: {speed:5.1f}, Duty Cycle: {duty_cycle:.3f}")
                time.sleep(1)  # Hold each speed for 1 second
            
            # Hold at max CW for 2 seconds
            print("\nHolding at max CW...")
            time.sleep(2)
            
            # Sweep from 1.0 to -1.0 (CW to CCW)
            print("\nSweeping from max CW to max CCW...")
            for speed in np.arange(1.0, -1.01, -0.1):  # Include -1.0 with -1.01
                duty_cycle = gpio_config.speed_to_duty_cycle(speed)
                servo.value = duty_cycle
                print(f"Speed: {speed:5.1f}, Duty Cycle: {duty_cycle:.3f}")
                time.sleep(1)  # Hold each speed for 1 second
            
            # Hold at max CCW for 2 seconds
            print("\nHolding at max CCW...")
            time.sleep(2)
            
            # Return to center (stopped) position
            print("\nReturning to stop position...")
            servo.value = gpio_config.CENTER_DUTY_CYCLE
            time.sleep(2)
            
            # Ask if user wants to continue
            response = input("\nPress Enter to run again, or 'q' to quit: ")
            if response.lower() == 'q':
                break
    
    except KeyboardInterrupt:
        print("\nTest interrupted by user")
    
    finally:
        print("\nStopping servo and cleaning up...")
        servo.value = gpio_config.CENTER_DUTY_CYCLE
        time.sleep(0.5)  # Brief pause at center
        servo.close()
        print("Test complete")


def test_speed_positions():
    """Test specific speed positions of the servo."""
    servo = PWMOutputDevice(
        pin=18,
        frequency=gpio_config.PWM_FREQUENCY,
        initial_value=gpio_config.CENTER_DUTY_CYCLE
    )
    
    try:
        print("Testing specific speed positions...")
        
        # Test positions to check
        test_speeds = [
            (0.0, "Stopped"),
            (1.0, "Full CW"),
            (0.0, "Stopped"),
            (-1.0, "Full CCW"),
            (0.0, "Stopped"),
            (0.5, "Half CW"),
            (0.0, "Stopped"),
            (-0.5, "Half CCW"),
            (0.0, "Stopped")
        ]
        
        for speed, description in test_speeds:
            duty_cycle = gpio_config.speed_to_duty_cycle(speed)
            print(f"\nSetting {description}")
            print(f"Speed: {speed:5.1f}, Duty Cycle: {duty_cycle:.3f}")
            servo.value = duty_cycle
            time.sleep(2)  # Hold each position for 2 seconds
    
    except KeyboardInterrupt:
        print("\nTest interrupted by user")
    
    finally:
        print("\nStopping servo and cleaning up...")
        servo.value = gpio_config.CENTER_DUTY_CYCLE
        time.sleep(0.5)
        servo.close()
        print("Test complete")


if __name__ == "__main__":
    print("Continuous Rotation Servo Test")
    print("1. Run continuous sweep test")
    print("2. Test specific speed positions")
    
    choice = input("Select test (1 or 2): ")
    
    if choice == "1":
        test_servo_sweep()
    elif choice == "2":
        test_speed_positions()
    else:
        print("Invalid choice") 