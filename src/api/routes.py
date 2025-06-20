"""
API routes for the Robot Arm Control System.

This module implements the REST API endpoints for controlling the robot arm servos.
"""

from datetime import datetime
from fastapi import APIRouter, HTTPException
from typing import Dict

from .models import (
    ServoStartRequest,
    ServoStartResponse,
    ServoStopResponse,
    EmergencyStopResponse,
    ServoStatus,
    SystemStatus,
    ServoSpeedRequest,
    ServoSpeedResponse
)
from ..hardware.servo_controller import ServoController


# Create API router
router = APIRouter(prefix="/api", tags=["servo-control"])

# Initialize servo controller
servo_controller = ServoController()
servo_controller.initialize_servos()


@router.post("/servos/{servo_id}/start", response_model=ServoStartResponse)
async def start_servo(servo_id: str, request: ServoStartRequest) -> ServoStartResponse:
    """Start a servo in the specified direction."""
    success = servo_controller.start_servo(servo_id, request.direction)
    
    if not success:
        raise HTTPException(
            status_code=400,
            detail=f"Failed to start servo {servo_id}"
        )
    
    return ServoStartResponse(
        success=True,
        servo_id=servo_id,
        direction=request.direction,
        timestamp=datetime.utcnow()
    )


@router.post("/servos/{servo_id}/speed", response_model=ServoSpeedResponse)
async def set_servo_speed(servo_id: str, speed_request: ServoSpeedRequest):
    """
    Set the speed of a specific servo.
    
    Args:
        servo_id: ID of the servo to control
        speed_request: Speed control parameters
        
    Returns:
        ServoSpeedResponse with operation result
    """
    if not servo_controller.set_servo_speed(servo_id, speed_request.speed):
        raise HTTPException(
            status_code=400,
            detail=f"Failed to set speed for servo {servo_id}"
        )
    
    return ServoSpeedResponse(
        success=True,
        servo_id=servo_id,
        speed=speed_request.speed,
        message=f"Set servo {servo_id} speed to {speed_request.speed:.2f}"
    )


@router.post("/servos/{servo_id}/stop", response_model=ServoSpeedResponse)
async def stop_servo(servo_id: str):
    """
    Stop a specific servo.
    
    Args:
        servo_id: ID of the servo to stop
        
    Returns:
        ServoSpeedResponse with operation result
    """
    if not servo_controller.stop_servo(servo_id):
        raise HTTPException(
            status_code=400,
            detail=f"Failed to stop servo {servo_id}"
        )
    
    return ServoSpeedResponse(
        success=True,
        servo_id=servo_id,
        speed=0.0,
        message=f"Stopped servo {servo_id}"
    )


@router.post("/emergency-stop", response_model=ServoSpeedResponse)
async def emergency_stop():
    """
    Activate emergency stop - immediately stop all servos.
    
    Returns:
        ServoSpeedResponse with operation result
    """
    if not servo_controller.emergency_stop():
        raise HTTPException(
            status_code=500,
            detail="Failed to execute emergency stop"
        )
    
    return ServoSpeedResponse(
        success=True,
        servo_id="all",
        speed=0.0,
        message="Emergency stop activated"
    )


@router.get("/status", response_model=SystemStatus)
async def get_system_status() -> SystemStatus:
    """Get the current system status."""
    servo_statuses = servo_controller.get_all_servo_status()
    
    # Convert servo statuses to the API model format
    formatted_statuses: Dict[str, ServoStatus] = {}
    for servo_id, status in servo_statuses.items():
        formatted_statuses[servo_id] = ServoStatus(
            status=status["status"],
            direction=status.get("direction"),
            runtime=status["runtime"]
        )
    
    return SystemStatus(
        system_status="running",  # TODO: Add more detailed system status
        emergency_stop_active=servo_controller.is_emergency_stop_active(),
        servos=formatted_statuses,
        timestamp=datetime.utcnow()
    )


@router.get("/servos", response_model=Dict[str, ServoStatus])
async def get_servo_list() -> Dict[str, ServoStatus]:
    """Get a list of all servos and their current status."""
    servo_statuses = servo_controller.get_all_servo_status()
    
    # Convert to API model format
    formatted_statuses: Dict[str, ServoStatus] = {}
    for servo_id, status in servo_statuses.items():
        formatted_statuses[servo_id] = ServoStatus(
            status=status["status"],
            direction=status.get("direction"),
            runtime=status["runtime"]
        )
    
    return formatted_statuses


@router.post("/initialize", response_model=ServoSpeedResponse)
async def initialize_servos():
    """
    Initialize all configured servos.
    
    Returns:
        ServoSpeedResponse with operation result
    """
    if not servo_controller.initialize_servos():
        raise HTTPException(
            status_code=500,
            detail="Failed to initialize servos"
        )
    
    return ServoSpeedResponse(
        success=True,
        servo_id="all",
        speed=0.0,
        message="All servos initialized"
    ) 