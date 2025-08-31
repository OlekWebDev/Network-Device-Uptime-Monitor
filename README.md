# Network Device Uptime Monitor

A Python Tkinter Gui based network monitoring solution designed to track device uptime and send automated email notifications when devices become unresponsive after a set amount of time. Originally developed to capture VoIP phone reboot patterns for enterprise level VoIp troubleshooting. This tool can monitor the uptime on any IP-enabled devices on a network.

## 🚀 Project Overview

This application was created to solve a specific business problem: tracking when VoIP phones go offline due to user reboots, helping IT teams correlate user-reported issues with actual device downtime. The solution provides real-time monitoring with email alerts, making it an invaluable tool for network administrators and IT support teams.

## ✨ Key Features

### Core Monitoring Capabilities
- **Real-time Device Monitoring**: Continuous ping-based health checks for multiple network devices
- **Configurable Ping Intervals**: Adjustable monitoring frequency (default: 3 seconds)
- **Smart Threshold Detection**: Customizable downtime thresholds before triggering alerts (default: 10 seconds)
- **Cross-Platform Compatibility**: Works seamlessly on Windows, macOS, and Linux systems

### Intelligent Email Notifications
- **Automated Alerting**: Instant email notifications when devices exceed downtime thresholds
- **Template System**: Customizable email templates with dynamic placeholders
- **Anti-Spam Protection**: One notification per outage cycle to prevent email flooding
- **Multi-Recipient Support**: Send alerts to multiple stakeholders simultaneously

### Professional User Interface
- **Intuitive GUI**: Clean, modern interface built with Python's Tkinter
- **Device Correlation**: Side-by-side IP address and MAC address management
- **Real-time Logging**: Live status updates and monitoring activity logs
- **Configuration Management**: Easy adjustment of monitoring parameters without code changes

### Advanced Features
- **MAC Address Tracking**: Correlate network events with specific hardware devices
- **Template Variables**: Dynamic email content with `{IpAddress}`, `{MacAddress}`, and `{Time}` placeholders
- **Concurrent Processing**: Multi-threaded architecture for monitoring multiple devices simultaneously
- **Recovery Detection**: Automatic notification when devices come back online

## 🛠️ Technical Implementation

### Architecture
- **Language**: Python 3.x with standard library components only
- **GUI Framework**: Tkinter for cross-platform desktop interface
- **Networking**: Subprocess-based ping implementation for reliability
- **Email**: SMTP integration with support for Gmail and other providers
- **Concurrency**: Threading for non-blocking monitoring operations

### Dependencies
This application uses only Python standard library modules:
- `tkinter` - GUI framework
- `threading` - Concurrent monitoring operations  
- `subprocess` - System ping command execution
- `smtplib` - Email notification delivery
- `time/datetime` - Timestamp and scheduling management
- `queue` - Thread-safe logging operations

## 📋 Prerequisites

- Python 3.6 or higher
- Network connectivity to target devices
- SMTP email account (Gmail recommended with App Password)

## 🚀 Quick Start

### 1. Download and Setup
```bash
git clone https://github.com/yourusername/network-device-uptime-monitor.git
cd network-device-uptime-monitor
python uptime_monitor.py
```

### 2. Configure Email Settings
Update the email configuration in the code:
```python
self.email_username = "your_email@gmail.com"
self.email_password = "your_app_password"  # Use Gmail App Password
```

### 3. Add Devices
- Enter IP addresses in the left panel (one per line)
- Enter corresponding MAC addresses in the right panel
- Ensure each IP has a matching MAC address on the same row

### 4. Customize Notifications
- Set ping interval (how often to check devices)
- Configure downtime threshold (when to send alerts)
- Customize email subject and message template
- Add recipient email addresses (comma-separated)

### 5. Start Monitoring
Click "Start Monitoring" and observe real-time device status in the log output.

## 📧 Gmail App Password Setup

For Gmail integration:
1. Enable 2-Factor Authentication on your Google account
2. Go to Google Account Settings → Security → App Passwords
3. Generate an app password for "Mail"
4. Use this 16-character password in the application

## 🎯 Use Cases

### IT Infrastructure Monitoring
- Monitor critical network equipment (routers, switches, servers)
- Track device availability during maintenance windows
- Generate uptime reports for SLA compliance

### VoIP System Management
- Detect phone reboots and connectivity issues
- Correlate user complaints with actual device downtime
- Monitor call quality by tracking device stability

### Remote Site Monitoring
- Monitor devices across multiple locations
- Early warning system for network connectivity issues
- Automated alerting for remote equipment failures

### Development and Testing
- Monitor test environment stability
- Track deployment impact on system availability
- Validate network configuration changes

## 🔧 Configuration Options

| Setting | Default | Description |
|---------|---------|-------------|
| Ping Interval | 3 seconds | How frequently to check device status |
| Notification Threshold | 10 seconds | Downtime duration before sending alerts |
| Email Template | Customizable | Message format with dynamic placeholders |
| Recipients | Configurable | Comma-separated list of notification targets |

## 📊 Monitoring Logic

1. **Device Registration**: Parse IP and MAC address pairs from user input
2. **Continuous Monitoring**: Ping each device at configured intervals
3. **State Tracking**: Monitor device response times and downtime duration
4. **Threshold Detection**: Identify when devices exceed acceptable downtime
5. **Smart Alerting**: Send notifications once per outage cycle
6. **Recovery Tracking**: Detect and log when devices return to service

## 🤝 Contributing

This project welcomes contributions! Whether you're fixing bugs, adding features, or improving documentation, your input is valuable. Please feel free to submit issues and pull requests.

## 📜 License

This project is open source and available under the Apache 2.0 License.

## 🌐 About

Developed by Oleksiy Gorbenko of ProfitsPlusX.com as a practical solution for enterprise network device monitoring. This tool demonstrates effective problem-solving through clean code architecture, user-centered design, and robust monitoring capabilities.

---

**© 2025 Oleksiy Gorbenko of ProfitsPlusX.com** | [Visit Website](https://profitsplusx.com)
