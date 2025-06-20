"""
Servo Controller for Robot Arm Control System

This module provides servo control functionality for continuous rotation servos
with variable speed control.
"""

import logging
from typing import Dict, Optional
from dataclasses import dataclass
from threading import Lock
from gpiozero import PWMOutputDevice

from . import gpio_config
from ..utils.config_manager import get_config_manager


@dataclass
class ServoState:
    """Data class to track servo state."""
    speed: float = 0.0  # -1.0 to 1.0
    is_running: bool = False


class ServoController:
    """Controller for managing continuous rotation servo motors."""
    
    def __init__(self):
        """Initialize the servo controller."""
        self.config = get_config_manager()
        self.logger = logging.getLogger(__name__)
        
        # Servo state tracking
        self._servos: Dict[str, PWMOutputDevice] = {}
        self._servo_states: Dict[str, ServoState] = {}
        self._lock = Lock()
        
        # Safety settings
        self._emergency_stop_active = False
        
        self.logger.info("Servo controller initialized")
    
    def initialize_servos(self) -> bool:
        """Initialize all configured servos."""
        try:
            with self._lock:
                # Clear any existing servos
                self._cleanup_servos()
                
                # Get servo configurations
                servo_configs = self.config.get_all_servos()
                
                if not servo_configs:
                    self.logger.warning("No servos configured")
                    return False
                
                # Initialize each servo
                for servo_id, servo_config in servo_configs.items():
                    try:
                        # Create PWM device for servo
                        servo = PWMOutputDevice(
                            pin=servo_config.pin,
                            frequency=gpio_config.PWM_FREQUENCY,
                            initial_value=gpio_config.CENTER_DUTY_CYCLE
                        )
                        
                        # Store servo and initialize state
                        self._servos[servo_id] = servo
                        self._servo_states[servo_id] = ServoState()
                        
                        self.logger.info(f"Initialized servo {servo_id} on pin {servo_config.pin}")
                        
                    except Exception as e:
                        self.logger.error(f"Failed to initialize servo {servo_id}: {e}")
                        return False
                
                self.logger.info(f"Successfully initialized {len(self._servos)} servos")
                return True
                
        except Exception as e:
            self.logger.error(f"Failed to initialize servos: {e}")
            return False
    
    def set_servo_speed(self, servo_id: str, speed: float) -> bool:
        """
        Set the speed of a servo.
        
        Args:
            servo_id: The ID of the servo to control
            speed: Float between -1.0 (max CCW) and 1.0 (max CW), 0.0 is stopped
            
        Returns:
            True if speed was set successfully, False otherwise
        """
        try:
            with self._lock:
                if self._emergency_stop_active:
                    self.logger.warning("Cannot set speed - emergency stop active")
                    return False
                
                if servo_id not in self._servos:
                    self.logger.error(f"Servo {servo_id} not found")
                    return False
                
                # Convert speed to duty cycle
                duty_cycle = gpio_config.speed_to_duty_cycle(speed)
                
                # Set the servo speed
                self._servos[servo_id].value = duty_cycle
                
                # Update state
                self._servo_states[servo_id].speed = speed
                self._servo_states[servo_id].is_running = (speed != 0.0)
                
                self.logger.info(f"Set servo {servo_id} speed to {speed:.2f}")
                return True
                
        except Exception as e:
            self.logger.error(f"Failed to set servo {servo_id} speed: {e}")
            return False
    
    def stop_servo(self, servo_id: str) -> bool:
        """Stop a specific servo."""
        return self.set_servo_speed(servo_id, 0.0)
    
    def stop_all_servos(self) -> bool:
        """Stop all servos."""
        try:
            with self._lock:
                success = True
                for servo_id in self._servos:
                    if not self.stop_servo(servo_id):
                        success = False
                return success
        except Exception as e:
            self.logger.error(f"Failed to stop all servos: {e}")
            return False
    
    def emergency_stop(self) -> bool:
        """Activate emergency stop."""
        try:
            with self._lock:
                self._emergency_stop_active = True
                return self.stop_all_servos()
        except Exception as e:
            self.logger.error(f"Failed to activate emergency stop: {e}")
            return False
    
    def clear_emergency_stop(self) -> bool:
        """Clear emergency stop state."""
        with self._lock:
            self._emergency_stop_active = False
            return True
    
    def get_servo_status(self, servo_id: str) -> Optional[Dict]:
        """Get status of a specific servo."""
        if servo_id not in self._servo_states:
            return None
            
        state = self._servo_states[servo_id]
        return {
            "speed": state.speed,
            "is_running": state.is_running
        }
    
    def get_all_servo_status(self) -> Dict[str, Dict]:
        """Get status of all servos."""
        return {
            servo_id: self.get_servo_status(servo_id)
            for servo_id in self._servo_states
        }
    
    def is_emergency_stop_active(self) -> bool:
        """Check if emergency stop is active."""
        return self._emergency_stop_active
    
    def cleanup(self):
        """Clean up resources."""
        self.stop_all_servos()
        self._cleanup_servos()
    
    def _cleanup_servos(self):
        """Clean up servo resources."""
        for servo in self._servos.values():
            servo.close()
        self._servos.clear()
        self._servo_states.clear() 