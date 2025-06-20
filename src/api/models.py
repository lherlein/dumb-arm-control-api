"""
API models for the Robot Arm Control System.

This module defines the Pydantic models used for request/response validation
in the REST API endpoints.
"""

from typing import Optional, Literal, Dict
from pydantic import BaseModel, Field, validator
from datetime import datetime


class ServoStartRequest(BaseModel):
    """Request model for starting a servo."""
    direction: Literal["forward", "backward"]


class ServoResponse(BaseModel):
    """Base response model for servo operations."""
    success: bool
    servo_id: str
    message: Optional[str] = None
    timestamp: datetime


class ServoStartResponse(ServoResponse):
    """Response model for servo start operation."""
    direction: Literal["forward", "backward"]


class ServoStopResponse(ServoResponse):
    """Response model for servo stop operation."""
    pass


class EmergencyStopResponse(BaseModel):
    """Response model for emergency stop operation."""
    success: bool
    message: str
    timestamp: datetime


class ServoSpeedRequest(BaseModel):
    """Request model for setting servo speed."""
    speed: float = Field(
        ...,  # Required field
        ge=-1.0,
        le=1.0,
        description="Speed value between -1.0 (max CCW) and 1.0 (max CW), 0.0 is stopped"
    )


class ServoSpeedResponse(BaseModel):
    """Response model for servo speed operations."""
    success: bool
    servo_id: str
    speed: float
    message: Optional[str] = None


class ServoStatus(BaseModel):
    """Model for individual servo status."""
    status: str
    direction: Optional[str] = None
    runtime: float
    speed: float
    is_running: bool


class SystemStatus(BaseModel):
    """Response model for system status."""
    system_status: str = "running"
    emergency_stop_active: bool
    servos: Dict[str, ServoStatus]
    timestamp: datetime


class ErrorResponse(BaseModel):
    """Model for error responses."""
    success: bool = False
    error: str
    details: Optional[str] = None 