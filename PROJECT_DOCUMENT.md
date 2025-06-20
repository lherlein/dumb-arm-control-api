# Robot Arm Control System - Project Document

## Project Overview

This project implements a Raspberry Pi-based control system for a robotic arm, designed with AI-driven autonomy in mind. The system provides a simple REST API for direct motor control while being architected to support intelligent agent control through MCP (Model Context Protocol) servers.

### Core Philosophy
- **Simple but Extensible**: The base application provides basic servo start/stop control while maintaining an architecture that supports complex AI-driven behaviors
- **Safety First**: All operations include safety checks and emergency stop capabilities
- **AI-Ready**: Designed from the ground up to work with MCP servers and autonomous agents
- **Modular**: Clean separation between hardware control, API layer, and AI integration

## System Architecture

```
┌─────────────────┐    ┌─────────────────┐    ┌─────────────────┐
│   AI Agents     │    │   MCP Server    │    │  REST API       │
│   (Future)      │◄──►│   (Future)      │◄──►│  (Current)      │
└─────────────────┘    └─────────────────┘    └─────────────────┘
                                                        │
                                                        ▼
                                               ┌─────────────────┐
                                               │  Motor Control  │
                                               │     Layer       │
                                               └─────────────────┘
                                                        │
                                                        ▼
                                               ┌─────────────────┐
                                               │   Hardware      │
                                               │  (Servos)       │
                                               └─────────────────┘
```

## Hardware Specifications

### Target Platform
- **Device**: Raspberry Pi (4B recommended for performance)
- **OS**: Raspberry Pi OS (Debian-based)
- **Python Version**: 3.9+

### Servo Motors
- **Type**: Standard hobby servos (SG90, MG996R, etc.)
- **Control**: PWM-based direction control (forward/backward/stop)
- **Power**: 5V supply with adequate current capacity
- **Communication**: GPIO PWM pins

### Safety Hardware
- **Emergency Stop**: Physical button connected to GPIO
- **Status LEDs**: Visual feedback for system state
- **Power Management**: Proper voltage regulation and current monitoring

## Application Design

### 1. Core Components

#### Motor Control Layer
```python
# Core servo control abstraction
class ServoController:
    - initialize_servos()
    - start_servo(servo_id, direction)  # direction: 'forward' or 'backward'
    - stop_servo(servo_id)
    - emergency_stop()
    - get_status()
```

#### REST API Layer
```python
# FastAPI-based REST endpoints
- POST /api/servos/{servo_id}/start
- POST /api/servos/{servo_id}/stop
- POST /api/emergency-stop
- GET /api/status
- GET /api/servos
```

#### Configuration Management
```python
# Hardware configuration
servo_config = {
    "base": {"name": "base", "pin": 18},
    "shoulder": {"name": "shoulder", "pin": 19},
    "elbow": {"name": "elbow", "pin": 20},
    "wrist_rotate": {"name": "wrist_rotate", "pin": 24},
    "gripper": {"name": "gripper", "pin": 26}
}
```

### 2. API Design

#### REST Endpoints

**Start Servo**
```
POST /api/servos/{servo_id}/start
Content-Type: application/json

{
    "direction": "forward"  // or "backward"
}

Response:
{
    "success": true,
    "servo_id": "base",
    "direction": "forward",
    "timestamp": "2024-01-01T12:00:00Z"
}
```

**Stop Servo**
```
POST /api/servos/{servo_id}/stop

Response:
{
    "success": true,
    "servo_id": "base",
    "message": "Servo stopped",
    "timestamp": "2024-01-01T12:00:00Z"
}
```

**Emergency Stop**
```
POST /api/emergency-stop

Response:
{
    "success": true,
    "message": "Emergency stop activated",
    "timestamp": "2024-01-01T12:00:00Z"
}
```

**System Status**
```
GET /api/status

Response:
{
    "system_status": "running",
    "emergency_stop_active": false,
    "servos": {
        "base": {"status": "stopped"},
        "shoulder": {"status": "running", "direction": "forward"},
        "elbow": {"status": "stopped"},
        "wrist_rotate": {"status": "stopped"},
        "gripper": {"status": "stopped"}
    },
    "timestamp": "2024-01-01T12:00:00Z"
}
```

### 3. Safety Features

#### Built-in Safety Mechanisms
- **Emergency Stop**: Immediate halt of all motor movement
- **Timeout Protection**: Automatic stop if commands exceed time limits
- **Current Monitoring**: Detect potential hardware issues
- **Status Monitoring**: Track which servos are running and in what direction

#### Safety Configuration
```python
safety_config = {
    "max_runtime": 30000,  // Maximum time a servo can run continuously (ms)
    "command_timeout": 5000,  // ms
    "emergency_stop_pin": 21,
    "status_led_pin": 22,
    "enable_safety_checks": True
}
```

## MCP Server Integration (Future)

### MCP Server Design
The MCP server will act as an intelligent layer between AI agents and the REST API, providing:

#### Tools Available to AI Agents
- `move_servo(servo_id, direction)`: Start servo in specified direction
- `stop_servo(servo_id)`: Stop a specific servo
- `get_arm_status()`: Current status of all servos
- `emergency_stop()`: Immediate safety stop
- `stop_all_servos()`: Stop all running servos

#### AI Agent Capabilities
- **Autonomous Movement**: AI can control arm based on sensor input
- **Direction Control**: Start servos in forward or backward direction
- **Safety Management**: Stop servos when needed
- **Learning**: Adapt behavior based on feedback
- **Multi-Agent Coordination**: Multiple AIs can work together

## Project Structure

```
robo-arm-control/
├── .cursorrules                 # Cursor AI rules
├── PROJECT_DOCUMENT.md          # This document
├── README.md                    # Setup and usage instructions
├── requirements.txt             # Python dependencies
├── config/
│   └── config.yaml             # Main configuration file
├── src/
│   ├── main.py                 # FastAPI application entry point
│   ├── hardware/
│   │   ├── __init__.py
│   │   ├── servo_controller.py  # Core servo control logic
│   │   ├── safety_manager.py    # Safety and emergency stop
│   │   └── gpio_manager.py      # GPIO interface
│   ├── api/
│   │   ├── __init__.py
│   │   ├── routes.py            # REST API endpoints
│   │   ├── models.py            # Pydantic models
│   │   └── middleware.py        # Request/response middleware
│   ├── utils/
│   │   ├── __init__.py
│   │   ├── logger.py            # Logging configuration
│   │   └── config_manager.py    # Configuration management
│   └── tests/
│       ├── __init__.py
│       ├── test_config.py       # Configuration tests
│       ├── test_servo_controller.py
│       └── test_api.py
├── scripts/
│   ├── setup.sh                 # Initial setup script
│   ├── install_dependencies.sh  # Dependency installation
│   └── test_hardware.py         # Hardware testing script
└── docs/
    ├── api_documentation.md     # Detailed API docs
    ├── hardware_setup.md        # Hardware assembly guide
    └── troubleshooting.md       # Common issues and solutions
```

## Development Phases

### Phase 1: Core Servo Control (Current Focus)
- [ ] Basic servo start/stop implementation
- [ ] REST API with essential endpoints
- [ ] Safety mechanisms and emergency stop
- [ ] Configuration management
- [ ] Hardware testing and validation

### Phase 2: Enhanced API Features
- [ ] Status monitoring and logging
- [ ] Advanced safety features
- [ ] Performance optimization
- [ ] Comprehensive testing

### Phase 3: MCP Server Integration
- [ ] MCP server implementation
- [ ] AI agent tools and capabilities
- [ ] Autonomous movement algorithms
- [ ] Multi-agent coordination

### Phase 4: Advanced AI Features
- [ ] Computer vision integration
- [ ] Movement coordination algorithms
- [ ] Learning from demonstration
- [ ] Predictive maintenance

## Technical Requirements

### Software Dependencies
```python
# Core dependencies
fastapi>=0.104.0
uvicorn>=0.24.0
pydantic>=2.5.0
gpiozero>=2.0.0  # For GPIO control
pyyaml>=6.0.1    # For configuration
python-multipart>=0.0.6
```

### Hardware Requirements
- Raspberry Pi 4B (2GB+ RAM)
- Servo motors (quantity depends on arm design)
- Power supply (5V, adequate current)
- Breadboard and jumper wires
- Emergency stop button
- Status LEDs

## Safety Considerations

### Critical Safety Rules
1. **Always test in a safe environment** before full operation
2. **Emergency stop must be easily accessible** at all times
3. **Servos must have runtime limits** to prevent overheating
4. **Power supply must be adequate** for all servos
5. **Regular hardware inspection** for wear and damage

### Development Safety
- Use low-power servos during development
- Implement software limits before hardware limits
- Test emergency stop functionality regularly
- Log all movements for debugging
- Have physical safety barriers during testing

## Next Steps

1. **Hardware Setup**: Assemble and test basic servo connections
2. **Core Implementation**: Build the servo controller and basic API
3. **Safety Testing**: Validate all safety mechanisms
4. **Documentation**: Complete setup and usage guides
5. **Integration Testing**: Test with actual robot arm hardware

## Questions for Clarification

1. **Arm Design**: How many degrees of freedom does the arm have?
2. **Servo Specifications**: What specific servo models will be used?
3. **Power Requirements**: What is the total power draw of all servos?
4. **Safety Environment**: What are the physical constraints and safety requirements?
5. **AI Integration Timeline**: When do you plan to implement the MCP server?

This document provides a solid foundation for the project. As development progresses, we can refine and expand these specifications based on actual requirements and constraints. 