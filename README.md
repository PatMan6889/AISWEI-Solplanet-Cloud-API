# AISWEI / Solplanet Cloud API Client

[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)

A Python client library for the AISWEI/Solplanet Cloud API that enables monitoring and management of solar inverter systems with Pro-level access.

## 🌞 Overview

This library provides a streamlined interface to access real-time and historical data from your AISWEI/Solplanet solar installation. It handles all authentication, signature generation, and request formatting required by the AISWEI Cloud API.

### Key Features

- **Complete Pro API Support**: Access all available Pro API endpoints
- **Real-time Monitoring**: Get current power production and inverter status
- **Historical Data**: Analyze daily, monthly and yearly energy production
- **Event Tracking**: Monitor system errors, warnings and events
- **Easy Authentication**: Simplified credential management

### Data Access Examples

- Plant overview and performance metrics
- Detailed inverter status and operational parameters
- Error reports and event histories
- Energy production statistics
- Battery status (for hybrid systems)

## 📋 Requirements

- Python 3.6 or higher
- Active internet connection
- AISWEI/Solplanet Pro user account
- API access credentials

## 🔑 Authentication & Configuration

### Required Credentials

To use this API client, you need five credential components:

1. **APP_KEY** - Application key for your Pro account
2. **APP_SECRET** - Application secret for authentication
3. **API_KEY** - API key specific to your inverter
4. **TOKEN** - Pro access token for elevated permissions
5. **SN** - Serial number of your inverter

### How to Obtain Credentials

1. Create a Pro user account on the AISWEI/Solplanet portal
2. Contact AISWEI/Solplanet support to request API access for your account
3. After approval, you'll receive your APP_KEY, APP_SECRET, API_KEY, and TOKEN
4. The SN (serial number) is found on your physical inverter or in your portal account

### Configuration Setup

This package uses a separate configuration file to securely store your credentials:

1. Create a copy of the provided template:
   ```bash
   cp config_template.py config.py
   ```

2. Edit `config.py` with your actual credentials:
   ```python
   APP_KEY = "your_app_key_here"       # From AISWEI support
   APP_SECRET = "your_app_secret_here" # From AISWEI support
   API_KEY = "your_api_key_here"       # Inverter-specific API key
   TOKEN = "your_token_here"           # Pro user access token
   SN = "your_serial_number_here"      # Your inverter's serial number
   ```

> **⚠️ Security Note**: The `config.py` file is automatically excluded from version control via `.gitignore` to protect your credentials. Never commit this file to a public repository.

## 📦 Installation

```bash
# Clone the repository
git clone https://github.com/yourusername/aiswei-solar-api.git
cd aiswei-solar-api

# Install dependencies
pip install -r requirements.txt
```

### Dependencies

This library requires the following packages (included in requirements.txt):

- **requests** - For HTTP communication with the API
- **datetime** - For date and time handling
- **typing** - For type hints (Python 3.6+)

The following standard libraries are also used:
- json - For JSON parsing
- hashlib - For cryptographic hash functions
- hmac - For HMAC authentication
- base64 - For Base64 encoding/decoding

## 🚀 Usage Examples

### Basic Usage

```python
from aiswei_api import AisweiSolarAPI
from config import APP_KEY, APP_SECRET, API_KEY, TOKEN, SN

# Initialize the API client
api = AisweiSolarAPI(
    app_key=APP_KEY,
    app_secret=APP_SECRET,
    api_key=API_KEY,
    token=TOKEN,
    sn=SN
)

# Get plant overview with current production data
plant_overview = api.getPlantOverviewPro()

# Check for successful response
if plant_overview.get('success'):
    data = plant_overview['data']
    print(f"Current Power: {data.get('power', 'N/A')} kW")
    print(f"Today's Production: {data.get('etoday', 'N/A')} kWh")
    print(f"Total Energy: {data.get('etotal', 'N/A')} kWh")
    print(f"System Status: {data.get('status', 'Unknown')}")
else:
    print(f"Error: {plant_overview.get('errorMsg', 'Unknown error')}")
```

### Retrieving Real-Time Inverter Data

```python
# Get the latest time-series data
live_data = api.getLastTsDataPro()

if live_data.get('success'):
    for device in live_data.get('data', []):
        print(f"Device: {device.get('name', 'Unknown')}")
        print(f"Current Power: {device.get('pac', 'N/A')} W")
        print(f"AC Voltage: {device.get('vac', 'N/A')} V")
        print(f"DC Voltage: {device.get('vpv', 'N/A')} V")
        print(f"Frequency: {device.get('fac', 'N/A')} Hz")
        print(f"Temperature: {device.get('temp', 'N/A')} °C")
else:
    print(f"Failed to retrieve data: {live_data.get('errorMsg')}")
```

### Historical Data Analysis

```python
# Get today's energy production by hour
today_data = api.getInverterETodayPro()

if today_data.get('success'):
    for hour_data in today_data.get('data', {}).get('powersData', []):
        timestamp = hour_data.get('time')
        power = hour_data.get('value')
        print(f"Time: {timestamp}, Power: {power} W")
```

## 📚 Available API Methods

The library provides access to all Pro API endpoints through easy-to-use methods:

### Plant Management

| Method | Description | Required Parameters |
|--------|-------------|--------------------|
| `getPlanListPro()` | Get all plants under your account | None |
| `getPlantOverviewPro()` | Get plant overview and status | None |
| `getPlantOutputPro()` | Get detailed plant output data | None (defaults to current date) |
| `getPlantEventPro()` | Get plant events | `sdt` (optional, but recommended) |

### Device Information

| Method | Description | Required Parameters |
|--------|-------------|--------------------|
| `getDeviceListPro()` | List all devices in your system | None |
| `getLocationPro()` | Get geographical location | `psno` (optional, uses default) |
| `getLastTsDataPro()` | Get latest inverter data | None (uses SN from init) |

### Inverter Specific

| Method | Description | Required Parameters |
|--------|-------------|--------------------|
| `getInverterDataPagePro()` | Get detailed inverter data | `startDate` (optional, uses default) |
| `getInverterETodayPro()` | Get today's energy production | None (uses current date) |
| `getInverterOverviewPro()` | Get inverter overview | None |

### Error Management

| Method | Description | Required Parameters |
|--------|-------------|--------------------|
| `getInverterHisErrorPagePro()` | Get error history | `startDate` (optional, uses default) |
| `getInverterCurrentErrorPro()` | Get current errors | None |
| `getInverterRecoverStatusPro()` | Check error recovery status | `faultCodes` (optional, uses default) |

### Configuration

| Method | Description | Required Parameters |
|--------|-------------|--------------------|
| `createstationPro()` | Create a new station | Varies based on station details |

## 🧪 Testing Your Setup

The package includes a comprehensive test script that validates your configuration by executing all available API calls:

```bash
python aiswei_api.py
```

This will run through each API endpoint and display the results, helping you verify your credentials and connection.

## ❓ Troubleshooting

### Common Issues and Solutions

| Problem | Possible Causes | Solution |
|---------|----------------|----------|
| Authentication failure | Incorrect credentials | Verify all five credential components in `config.py` |
| Connection errors | Network issues | Check your internet connection and firewall settings |
| Empty data responses | API limitations | Some endpoints return data only during daylight hours |
| Parameter errors | Missing required parameters | Check the method documentation for required parameters |

### API Response Structure

All API methods return responses with this general structure:

```json
{
  "success": true/false,
  "errorCode": "0",     // "0" indicates success
  "errorMsg": "",      // Error description if any
  "data": { ... }       // The actual data payload
}
```

Always check the `success` field before processing the response data.

## 📝 Extending and Contributing

Contributions to improve this library are welcome! Here's how you can help:

1. **Bug Reports**: Open an issue describing the bug and how to reproduce it
2. **Feature Requests**: Suggest new features or improvements
3. **Code Contributions**: Submit pull requests with enhancements or fixes

### Development Guidelines

- Follow PEP 8 style guidelines for Python code
- Add type hints to all new methods and functions
- Include docstrings for all public methods
- Update tests to cover new functionality

## 📄 License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

## ⚠️ Disclaimer

This project is not officially affiliated with, endorsed by, or connected to AISWEI or Solplanet. This is an independent, community-developed client library. All product names, logos, and brands are the property of their respective owners.

This library interacts with the AISWEI/Solplanet API according to their published specifications, but we cannot guarantee compatibility with future API changes. Use at your own risk.

For official information about the AISWEI/Solplanet API, please contact their customer support directly.