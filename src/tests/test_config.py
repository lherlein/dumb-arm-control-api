#!/usr/bin/env python3
"""
Test script for the configuration manager.

This script demonstrates how to use the configuration manager and validates
that the configuration is loaded correctly.
"""

import sys
import os
from pathlib import Path

# Add the src directory to the Python path
sys.path.insert(0, str(Path(__file__).parent.parent.parent))

from src.utils.config_manager import ConfigManager, initialize_config


def test_config_loading():
    """Test basic configuration loading."""
    print("Testing configuration loading...")
    
    try:
        config_manager = ConfigManager()
        print("✅ Configuration loaded successfully")
        return config_manager
    except Exception as e:
        print(f"❌ Failed to load configuration: {e}")
        return None


def test_servo_configuration(config_manager: ConfigManager):
    """Test servo configuration access."""
    print("\nTesting servo configuration...")
    
    servos = config_manager.get_all_servos()
    print(f"Found {len(servos)} configured servos:")
    
    for servo_id, servo_config in servos.items():
        print(f"  {servo_id}: {servo_config.name}")
        print(f"    Pin: {servo_config.pin}")
        print()


def test_safety_configuration(config_manager: ConfigManager):
    """Test safety configuration access."""
    print("Testing safety configuration...")
    
    safety_config = config_manager.get_safety_config()
    print(f"Safety enabled: {safety_config.enabled}")
    print(f"Emergency stop enabled: {safety_config.emergency_stop_enabled}")
    print(f"Bounds checking enabled: {safety_config.bounds_checking_enabled}")
    print(f"Speed limiting enabled: {safety_config.speed_limiting_enabled}")
    print(f"Global max speed: {safety_config.global_max_speed}%")
    print(f"Command timeout: {safety_config.command_timeout}ms")
    print()


def test_api_configuration(config_manager: ConfigManager):
    """Test API configuration access."""
    print("Testing API configuration...")
    
    api_config = config_manager.get_api_config()
    print(f"API Host: {api_config.host}")
    print(f"API Port: {api_config.port}")
    print(f"Debug mode: {api_config.debug}")
    print(f"CORS enabled: {api_config.cors.enabled}")
    print(f"Rate limiting enabled: {api_config.rate_limiting.enabled}")
    print()


def main():
    """Main test function."""
    print("🤖 Robot Arm Control System - Configuration Test")
    print("=" * 50)
    
    # Test configuration loading
    config_manager = test_config_loading()
    if not config_manager:
        print("❌ Configuration test failed. Exiting.")
        return 1
    
    # Test various configuration aspects
    test_servo_configuration(config_manager)
    test_safety_configuration(config_manager)
    test_api_configuration(config_manager)
    
    print("✅ All configuration tests completed successfully!")
    return 0


if __name__ == "__main__":
    exit(main()) 