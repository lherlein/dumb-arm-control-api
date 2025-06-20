"""
Configuration Manager for Robot Arm Control System

This module handles loading, validating, and providing access to system configuration
from YAML files. It includes validation for hardware settings, safety parameters,
and API configuration.
"""

import os
import yaml
from typing import Dict, Any, Optional, List
from pathlib import Path
import logging
from dataclasses import dataclass
from pydantic import BaseModel, validator, Field


class ServoConfig(BaseModel):
    """Configuration model for individual servo motors."""
    name: str
    pin: int


class SafetyConfig(BaseModel):
    """Configuration model for safety settings."""
    enabled: bool = True
    emergency_stop_enabled: bool = True
    bounds_checking_enabled: bool = True
    speed_limiting_enabled: bool = True
    timeout_protection_enabled: bool = True
    command_timeout: int = Field(ge=100, le=30000)
    movement_timeout: int = Field(ge=1000, le=60000)
    emergency_stop_timeout: int = Field(ge=50, le=1000)
    global_max_speed: int = Field(ge=0, le=100)
    global_max_acceleration: int = Field(ge=0, le=100)
    power_monitoring_enabled: bool = False
    max_current_draw: float = Field(ge=0.1, le=10.0)
    voltage_monitoring_enabled: bool = False
    min_voltage: float = Field(ge=3.0, le=6.0)


class CORSConfig(BaseModel):
    """Configuration model for CORS settings."""
    enabled: bool = Field(default=True)
    allowed_origins: List[str] = Field(default_factory=lambda: ["*"])
    allowed_methods: List[str] = Field(default_factory=lambda: ["GET", "POST", "PUT", "DELETE"])
    allowed_headers: List[str] = Field(default_factory=lambda: ["*"])


class RateLimitingConfig(BaseModel):
    """Configuration model for rate limiting settings."""
    enabled: bool = Field(default=True)
    requests_per_minute: int = Field(default=60, ge=1, le=1000)
    burst_limit: int = Field(default=10, ge=1, le=100)


class AuthenticationConfig(BaseModel):
    """Configuration model for authentication settings."""
    enabled: bool = Field(default=False)
    api_key_required: bool = Field(default=False)
    jwt_enabled: bool = Field(default=False)


class APIConfig(BaseModel):
    """Configuration model for API settings."""
    host: str = Field(default="0.0.0.0")
    port: int = Field(default=8000, ge=1024, le=65535)
    debug: bool = Field(default=False)
    cors: CORSConfig = Field(default_factory=CORSConfig)
    rate_limiting: RateLimitingConfig = Field(default_factory=RateLimitingConfig)
    authentication: AuthenticationConfig = Field(default_factory=AuthenticationConfig)


class LoggingConfig(BaseModel):
    """Configuration model for logging settings."""
    level: str = "INFO"
    file_enabled: bool = True
    file_path: str = "logs/robot_arm.log"
    max_file_size: str = "10MB"
    backup_count: int = Field(ge=1, le=20)
    console_enabled: bool = True
    format: str = "%(asctime)s - %(name)s - %(levelname)s - %(message)s"
    date_format: str = "%Y-%m-%d %H:%M:%S"


class ConfigManager:
    """
    Manages configuration loading, validation, and access for the robot arm control system.
    
    This class provides a centralized way to access all configuration parameters
    with proper validation and error handling.
    """
    
    def __init__(self, config_path: Optional[str] = None):
        """
        Initialize the configuration manager.
        
        Args:
            config_path: Path to the configuration file. If None, uses default location.
        """
        self.config_path = config_path or "config/config.yaml"
        self._config: Optional[Dict[str, Any]] = None
        self._servos: Optional[Dict[str, ServoConfig]] = None
        self._safety: Optional[SafetyConfig] = None
        self._api: Optional[APIConfig] = None
        self._logging: Optional[LoggingConfig] = None
        
        self.logger = logging.getLogger(__name__)
        self._load_config()
    
    def _load_config(self) -> None:
        """Load and validate the configuration file."""
        try:
            config_file = Path(self.config_path)
            if not config_file.exists():
                raise FileNotFoundError(f"Configuration file not found: {self.config_path}")
            
            with open(config_file, 'r', encoding='utf-8') as file:
                raw_config = yaml.safe_load(file)
            
            if not raw_config:
                raise ValueError("Configuration file is empty or invalid")
            
            self._config = raw_config
            self._validate_and_parse_config()
            self.logger.info(f"Configuration loaded successfully from {self.config_path}")
            
        except Exception as e:
            self.logger.error(f"Failed to load configuration: {e}")
            raise
    
    def _validate_and_parse_config(self) -> None:
        """Validate and parse the loaded configuration."""
        try:
            # Parse servo configurations
            self._servos = {}
            for servo_id, servo_data in self._config.get('hardware', {}).get('servos', {}).items():
                self._servos[servo_id] = ServoConfig(**servo_data)
            
            # Parse other configurations
            self._safety = SafetyConfig(**self._config.get('safety', {}))
            self._api = APIConfig(**self._config.get('api', {}))
            self._logging = LoggingConfig(**self._config.get('logging', {}))
            
        except Exception as e:
            self.logger.error(f"Configuration validation failed: {e}")
            raise
    
    def reload_config(self) -> None:
        """Reload the configuration from file."""
        self.logger.info("Reloading configuration...")
        self._load_config()
    
    def get_servo_config(self, servo_id: str) -> Optional[ServoConfig]:
        """Get configuration for a specific servo."""
        return self._servos.get(servo_id) if self._servos else None
    
    def get_all_servos(self) -> Dict[str, ServoConfig]:
        """Get all servo configurations."""
        return self._servos.copy() if self._servos else {}
    
    def get_safety_config(self) -> SafetyConfig:
        """Get safety configuration."""
        return self._safety
    
    def get_api_config(self) -> APIConfig:
        """Get API configuration."""
        return self._api
    
    def get_logging_config(self) -> LoggingConfig:
        """Get logging configuration."""
        return self._logging
    
    def get_system_config(self) -> Dict[str, Any]:
        """Get system-level configuration."""
        return self._config.get('system', {}) if self._config else {}
    
    def get_hardware_config(self) -> Dict[str, Any]:
        """Get hardware configuration."""
        return self._config.get('hardware', {}) if self._config else {}
    
    def is_safety_enabled(self) -> bool:
        """Check if safety features are enabled."""
        return self._safety.enabled if self._safety else False
    
    def is_emergency_stop_enabled(self) -> bool:
        """Check if emergency stop is enabled."""
        return self._safety.emergency_stop_enabled if self._safety else False
    
    def get_servo_count(self) -> int:
        """Get the number of configured servos."""
        return len(self._servos) if self._servos else 0
    
    def to_dict(self) -> Dict[str, Any]:
        """Convert the configuration to a dictionary."""
        return {
            'system': self.get_system_config(),
            'hardware': self.get_hardware_config(),
            'safety': self._safety.dict() if self._safety else {},
            'api': self._api.dict() if self._api else {},
            'logging': self._logging.dict() if self._logging else {}
        }


# Global configuration instance
_config_manager: Optional[ConfigManager] = None


def get_config_manager() -> ConfigManager:
    """Get the global configuration manager instance."""
    global _config_manager
    if _config_manager is None:
        _config_manager = ConfigManager()
    return _config_manager


def initialize_config(config_path: Optional[str] = None) -> ConfigManager:
    """Initialize the global configuration manager."""
    global _config_manager
    _config_manager = ConfigManager(config_path)
    return _config_manager 