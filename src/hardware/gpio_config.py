"""
GPIO Configuration for Robot Arm Control System

This module defines GPIO-related constants and configuration,
particularly for PWM control of continuous rotation servos.
"""

import os
from gpiozero import Device
from gpiozero.pins.rpigpio import RPiGPIOFactory

# Set up RPi.GPIO as the default pin factory
os.environ['GPIOZERO_PIN_FACTORY'] = 'rpigpio'
Device.pin_factory = RPiGPIOFactory()

# PWM Configuration for Continuous Rotation Servos
PWM_FREQUENCY = 50  # 50Hz standard for servos

# PWM Duty Cycle Configuration
# For continuous rotation servos:
# - Empirically determined center point for stopped position
# - Range from 1ms to 2ms pulse
# - 1ms = max speed counter-clockwise
# - 2ms = max speed clockwise

# Convert millisecond pulse widths to duty cycle percentages:
# duty_cycle = (pulse_width_ms / 20ms) = (pulse_width_ms * 50Hz / 1000)
CENTER_DUTY_CYCLE = 0.0696  # ~1.392ms pulse (empirically determined stop position)
MIN_DUTY_CYCLE = 0.05     # 1.0ms pulse (max counter-clockwise)
MAX_DUTY_CYCLE = 0.10     # 2.0ms pulse (max clockwise)

# Utility functions for speed conversion
def speed_to_duty_cycle(speed: float) -> float:
    """
    Convert a speed value (-1.0 to 1.0) to a PWM duty cycle.
    
    Args:
        speed: Float between -1.0 (max CCW) and 1.0 (max CW), 0.0 is stopped
        
    Returns:
        Float representing PWM duty cycle
    """
    if not -1.0 <= speed <= 1.0:
        raise ValueError("Speed must be between -1.0 and 1.0")
    
    if speed == 0:
        return CENTER_DUTY_CYCLE
    elif speed > 0:
        # Map 0->1 to CENTER->MAX
        return CENTER_DUTY_CYCLE + (speed * (MAX_DUTY_CYCLE - CENTER_DUTY_CYCLE))
    else:
        # Map -1->0 to MIN->CENTER
        return CENTER_DUTY_CYCLE + (speed * (CENTER_DUTY_CYCLE - MIN_DUTY_CYCLE))

def duty_cycle_to_speed(duty_cycle: float) -> float:
    """
    Convert a PWM duty cycle to a speed value.
    
    Args:
        duty_cycle: PWM duty cycle value
        
    Returns:
        Float between -1.0 and 1.0 representing speed
    """
    if not MIN_DUTY_CYCLE <= duty_cycle <= MAX_DUTY_CYCLE:
        raise ValueError(f"Duty cycle must be between {MIN_DUTY_CYCLE} and {MAX_DUTY_CYCLE}")
    
    if duty_cycle == CENTER_DUTY_CYCLE:
        return 0.0
    elif duty_cycle > CENTER_DUTY_CYCLE:
        # Map CENTER->MAX to 0->1
        return (duty_cycle - CENTER_DUTY_CYCLE) / (MAX_DUTY_CYCLE - CENTER_DUTY_CYCLE)
    else:
        # Map MIN->CENTER to -1->0
        return (duty_cycle - CENTER_DUTY_CYCLE) / (CENTER_DUTY_CYCLE - MIN_DUTY_CYCLE) 