# Robot Arm Control System

A Raspberry Pi-based control system for robotic arms, designed with AI-driven autonomy in mind. This system provides a simple REST API for direct motor control while being architected to support intelligent agent control through MCP (Model Context Protocol) servers.

## 🚀 Features

- **Simple REST API** for direct servo control
- **Comprehensive safety features** including emergency stop and bounds checking
- **Configurable hardware settings** via YAML configuration
- **AI-ready architecture** for future MCP server integration
- **Mock hardware mode** for development and testing
- **Extensive logging and monitoring**

## 📋 Requirements

### Hardware
- Raspberry Pi 4B (2GB+ RAM recommended)
- Servo motors (SG90, MG996R, or similar)
- 5V power supply with adequate current capacity
- Breadboard and jumper wires
- Emergency stop button (optional but recommended)
- Status LEDs (optional)

### Software
- Raspberry Pi OS (Debian-based)
- Python 3.9+
- Required Python packages (see `requirements.txt`)

## 🛠️ Installation

### 1. Clone the Repository
```bash
git clone <repository-url>
cd robo-arm-control
```

### 2. Install Dependencies
```bash
# Install system dependencies
sudo apt-get update
sudo apt-get install python3-pip python3-venv

# Create virtual environment
python3 -m venv venv
source venv/bin/activate

# Install Python dependencies
pip install -r requirements.txt
```

### 3. Configure Hardware
1. Connect servos to GPIO pins as defined in `config/config.yaml`
2. Connect emergency stop button to GPIO pin 21 (configurable)
3. Connect status LED to GPIO pin 22 (configurable)
4. Ensure proper power supply for all servos

### 4. Configure the System
Edit `config/config.yaml` to match your hardware setup:

```yaml
hardware:
  servos:
    servo_1:
      name: "Base Rotation"
      pin: 18
      min_angle: 0
      max_angle: 180
      # ... other settings
```

## ⚙️ Configuration

The system uses a comprehensive YAML configuration file (`config/config.yaml`) that includes:

### Hardware Configuration
- **Servo settings**: Pin assignments, angle ranges, pulse widths
- **GPIO configuration**: Emergency stop, status LEDs
- **Safety limits**: Soft limits for each servo

### Safety Configuration
- **Emergency stop**: Enable/disable and timeout settings
- **Bounds checking**: Position validation
- **Speed limiting**: Global and per-servo limits
- **Timeout protection**: Command and movement timeouts

### API Configuration
- **Server settings**: Host, port, debug mode
- **CORS settings**: Cross-origin resource sharing
- **Rate limiting**: Request limits and burst protection

### Development Configuration
- **Mock hardware**: Enable for testing without physical hardware
- **Test mode**: Reduced servo count for testing
- **Logging**: Verbose logging and diagnostics

## 🧪 Testing the Configuration

Run the configuration test to validate your setup:

```bash
python src/utils/test_config.py
```

This will:
- Load and validate the configuration file
- Display all configured servos and their settings
- Test position validation and speed limits
- Verify safety and API settings

## 🚀 Usage

### Starting the API Server
```bash
# From the project root
python -m src.main
```

The API will be available at `http://localhost:8000`

### API Endpoints

#### Set Servo Position
```bash
curl -X POST "http://localhost:8000/api/servos/servo_1/position" \
     -H "Content-Type: application/json" \
     -d '{"position": 90, "speed": 50}'
```

#### Get Servo Position
```bash
curl "http://localhost:8000/api/servos/servo_1/position"
```

#### Emergency Stop
```bash
curl -X POST "http://localhost:8000/api/emergency-stop"
```

#### System Status
```bash
curl "http://localhost:8000/api/status"
```

### Interactive API Documentation
Visit `http://localhost:8000/docs` for interactive API documentation powered by Swagger UI.

## 🔧 Development

### Project Structure
```
robo-arm-control/
├── .cursorrules                 # Cursor AI rules
├── PROJECT_DOCUMENT.md          # Project specification
├── README.md                    # This file
├── requirements.txt             # Python dependencies
├── config/
│   └── config.yaml             # Main configuration file
├── src/
│   ├── main.py                 # FastAPI application entry point
│   ├── hardware/               # Hardware control modules
│   ├── api/                    # REST API modules
│   ├── utils/                  # Utility modules
│   └── tests/                  # Test modules
├── scripts/                    # Setup and utility scripts
└── docs/                       # Documentation
```

### Running Tests
```bash
# Run configuration tests
python src/utils/test_config.py

# Run unit tests (when implemented)
pytest src/tests/
```

### Development Mode
Enable mock hardware for development without physical servos:

```yaml
development:
  mock_hardware: true
  test_mode: true
  test_servo_count: 2
```

## 🔒 Safety Features

### Built-in Safety Mechanisms
- **Position bounds checking**: Prevents servos from moving beyond safe limits
- **Speed limiting**: Maximum speed constraints to prevent damage
- **Emergency stop**: Immediate halt of all motor movement
- **Timeout protection**: Automatic stop if commands exceed time limits
- **Soft limits**: Software-enforced limits more restrictive than hardware limits

### Safety Configuration
All safety features can be configured in `config/config.yaml`:

```yaml
safety:
  enabled: true
  emergency_stop_enabled: true
  bounds_checking_enabled: true
  speed_limiting_enabled: true
  global_max_speed: 80
  command_timeout: 5000
```

## 🔮 Future Features

### Phase 2: Enhanced API Features
- Movement sequences and coordination
- Advanced safety features
- Status monitoring and logging
- Performance optimization

### Phase 3: MCP Server Integration
- MCP server implementation
- AI agent tools and capabilities
- Autonomous movement algorithms
- Multi-agent coordination

### Phase 4: Advanced AI Features
- Computer vision integration
- Path planning algorithms
- Learning from demonstration
- Predictive maintenance

## 🐛 Troubleshooting

### Common Issues

#### Configuration File Not Found
```
FileNotFoundError: Configuration file not found: config/config.yaml
```
**Solution**: Ensure the configuration file exists and the path is correct.

#### GPIO Permission Errors
```
PermissionError: [Errno 13] Permission denied
```
**Solution**: Run with sudo or add your user to the `gpio` group:
```bash
sudo usermod -a -G gpio $USER
```

#### Servo Not Responding
- Check power supply voltage and current
- Verify GPIO pin connections
- Check servo pulse width settings in configuration
- Test with mock hardware mode first

### Debug Mode
Enable debug mode in the configuration for detailed logging:

```yaml
system:
  debug_mode: true
  log_level: "DEBUG"
```

## 📝 Contributing

1. Follow the coding standards defined in `.cursorrules`
2. Add tests for new features
3. Update documentation as needed
4. Ensure all safety features are properly implemented

## 📄 License

[Add your license information here]

## 🤝 Support

For issues and questions:
1. Check the troubleshooting section
2. Review the configuration documentation
3. Test with mock hardware mode
4. Create an issue with detailed error information

---

**⚠️ Safety Warning**: Always test in a safe environment before full operation. Ensure emergency stop functionality is working and easily accessible. 