#!/usr/bin/env python3
"""
OpenHAB Integration Script for AISWEI/Solplanet API
"""
import sys
import json
from datetime import datetime


# Add path to API library
sys.path.append('/etc/openhab/scripts/solplanet')

try:
    from solplanet.aiswei_api import AisweiSolarAPI
    from solplanet.config import APP_KEY, APP_SECRET, API_KEY, TOKEN, SN
except ImportError as e:
    print(json.dumps({"error": f"Import error: {str(e)}", "timestamp": datetime.now().isoformat()}))
    sys.exit(1)

def is_api_success(response):
    """Checks if API response was successful"""
    return (response.get('status') == 200 and 
            response.get('info') == 'success' and 
            'data' in response)

def extract_live_data(api_response):
    """Extracts live data from getLastTsDataPro response"""
    if not is_api_success(api_response):
        return {}
    
    devices = api_response.get('data', [])
    if not devices:
        return {}
    
    # Use first device
    device = devices[0] if isinstance(devices, list) else devices
    
    # Helper function for safe numeric conversion
    def safe_float(value, default=0):
        try:
            return float(value) if value is not None else default
        except (ValueError, TypeError):
            return default
    
    def safe_int(value, default=0):
        try:
            return int(value) if value is not None else default
        except (ValueError, TypeError):
            return default
    
    # Conversions for better representation
    pac = safe_float(device.get('pac', 0))  # AC Power (W)
    power_kw = pac / 1000 if pac else 0  # W to kW
    
    return {
        # Main values
        "power": power_kw,  # Main power in kW
        "device_name": device.get('sn', 'Unknown'),  # Serial number as device name
        "timestamp": device.get('tim', ''),  # Timestamp of the data
        "status": "Normal" if safe_int(device.get('currentState')) == 1 else "Offline",
        
        # Power values
        "pac": pac,  # Active power (W)
        "prc": safe_float(device.get('prc', 0)),  # Reactive power (W)
        "sac": safe_float(device.get('sac', 0)),  # Apparent power (W)
        "pf": safe_float(device.get('pf', 0)) / 100,  # Power factor (0.01)
        
        # Energy values
        "hto": safe_float(device.get('hto', 0)),  # Grid connection duration (h)
        "etd": safe_float(device.get('etd', 0)) / 10,  # Daily power generation (0.1kWh)
        "eto": safe_float(device.get('eto', 0)) / 10,  # Total power generation (0.1kWh)
        
        # DC input values (MPPT)
        "v1": safe_float(device.get('v1', 0)) / 10,  # MPPT Voltage 1 (0.1V)
        "v2": safe_float(device.get('v2', 0)) / 10,  # MPPT Voltage 2 (0.1V)
        "v3": safe_float(device.get('v3', 0)) / 10,  # MPPT Voltage 3 (0.1V)
        "i1": safe_float(device.get('i1', 0)) / 100,  # MPPT Current 1 (0.01A)
        "i2": safe_float(device.get('i2', 0)) / 100,  # MPPT Current 2 (0.01A)
        "i3": safe_float(device.get('i3', 0)) / 100,  # MPPT Current 3 (0.01A)
        
        # String currents
        "s1": safe_float(device.get('s1', 0)) / 10,  # String current 1 (0.1A)
        "s2": safe_float(device.get('s2', 0)) / 10,  # String current 2 (0.1A)
        "s3": safe_float(device.get('s3', 0)) / 10,  # String current 3 (0.1A)
        
        # Temperatures
        "cf": safe_float(device.get('cf', 0)) / 10,  # Heat sink temperature (0.1°C)
        "tu": safe_float(device.get('tu', 0)) / 10,  # U phase temperature (0.1°C)
        "tv": safe_float(device.get('tv', 0)) / 10,  # V phase temperature (0.1°C)
        "tw": safe_float(device.get('tw', 0)) / 10,  # W phase temperature (0.1°C)
        "cb": safe_float(device.get('cb', 0)) / 10,  # Boost temperature (0.1°C)
        
        # Voltages
        "bv": safe_float(device.get('bv', 0)) / 10,  # Bus voltage (0.1V)
        
        # AC output values
        "va1": safe_float(device.get('va1', 0)) / 10,  # AC voltage 1 (0.1V)
        "va2": safe_float(device.get('va2', 0)) / 10,  # AC voltage 2 (0.1V)
        "va3": safe_float(device.get('va3', 0)) / 10,  # AC voltage 3 (0.1V)
        "ia1": safe_float(device.get('ia1', 0)) / 10,  # AC current 1 (0.1A)
        "ia2": safe_float(device.get('ia2', 0)) / 10,  # AC current 2 (0.1A)
        "ia3": safe_float(device.get('ia3', 0)) / 10,  # AC current 3 (0.1A)
        "fac": safe_float(device.get('fac', 0)) / 100,  # Frequency (0.01Hz)
        
        # Errors and warnings
        "er": safe_float(device.get('er', 0)),    # ERROR codes
        "wn0": safe_float(device.get('wn0', 0)),  # Warning
        
        # Battery data (if available, meaning not specified in API documentation)
        "bat0": safe_float(device.get('bat0', 0)),        # PV power (W) - ppv
        "bat1": safe_float(device.get('bat1', 0)) / 10,   # Feed-in today (0.1kWh) - etdpv
        "bat2": safe_float(device.get('bat2', 0)) / 10,   # Feed-in total (0.1kWh) - etopv
        "bat3": safe_float(device.get('bat3', 0)),        # Battery status - bst
        "bat4": safe_float(device.get('bat4', 0)),        # ??? - eb1
        "bat5": safe_float(device.get('bat5', 0)),        # ??? - wb1
        "bat6": safe_float(device.get('bat6', 0)) / 100,  # Battery voltage (0.01V) - vb
        "bat7": safe_float(device.get('bat7', 0)) / 10,   # Battery current (0.1A) - cb
        "bat8": safe_float(device.get('bat8', 0)),        # Battery power (W) - pb
        "bat9": safe_float(device.get('bat9', 0)) / 10,   # Battery temperature (0.1°C) - tb
        "bat10": safe_float(device.get('bat10', 0)),      # State of charge (%) - soc
        "bat11": safe_float(device.get('bat11', 0)),      # State of health (%) - soh
        "bat12": safe_float(device.get('bat12', 0)) / 10, # Charge today (0.1kWh) - ebi
        "bat13": safe_float(device.get('bat13', 0)) / 10, # Discharge today (0.1kWh) - ebo
        "bat14": safe_float(device.get('bat14', 0)),      # ???
        "bat15": safe_float(device.get('bat15', 0)) / 10, # Max current input (0.1A) - cli
        "bat16": safe_float(device.get('bat16', 0)) / 10, # Max current output (0.1A) - clo
        "bat17": safe_float(device.get('bat17', 0)) / 10, # Charge from grid today (0.1kWh) - charge_ac_td
        "bat18": safe_float(device.get('bat18', 0)) / 10, # Charge from grid total (0.1kWh) - charge_ac_to
        
        # Meter values (Smart Meter)
        "meterPow": safe_float(device.get('meterPow', 0)),  # Grid Power (W)
        "meterIed": safe_float(device.get('meterIed', 0)),  # Grid Import Energy Daily (kWh)
        "meterOed": safe_float(device.get('meterOed', 0)),  # Grid Export Energy Daily (kWh)
        "meterIet": safe_float(device.get('meterIet', 0)),  # Grid Import Energy Total (kWh)
        "meterOet": safe_float(device.get('meterOet', 0)),  # Grid Export Energy Total (kWh)
        
        # Additional system values
        "powerRatio": safe_float(device.get('powerRatio', 0)),  # Power Ratio
        "csq": safe_float(device.get('csq', 0)),  # Signal Quality
    }

def main():
    try:
        # Initialize API client
        api = AisweiSolarAPI(
            app_key=APP_KEY,
            app_secret=APP_SECRET,
            api_key=API_KEY,
            token=TOKEN,
            sn=SN
        )
        
        # Prepare default output
        output_data = {
            "timestamp": datetime.now().isoformat(),
            "success": False,
            "power": 0,
            "device_name": "Unknown",
            "status": "unknown",
            
            # Power values
            "pac": 0,
            "prc": 0,
            "sac": 0,
            "pf": 0,
            
            # Energy values
            "hto": 0,
            "etd": 0,
            "eto": 0,
            
            # DC input values (MPPT)
            "v1": 0, "v2": 0, "v3": 0,
            "i1": 0, "i2": 0, "i3": 0,
            
            # String currents
            "s1": 0, "s2": 0, "s3": 0,
            
            # Temperatures
            "cf": 0, "tu": 0, "tv": 0, "tw": 0, "cb": 0,
            
            # Voltages
            "bv": 0,
            
            # AC output values
            "va1": 0, "va2": 0, "va3": 0,
            "ia1": 0, "ia2": 0, "ia3": 0,
            "fac": 0,
            
            # Errors and warnings
            "er": 0, "wn0": 0,
            
            # Battery details (bat0-18)
            "bat0": 0, "bat1": 0, "bat2": 0, "bat3": 0, "bat4": 0,
            "bat5": 0, "bat6": 0, "bat7": 0, "bat8": 0, "bat9": 0,
            "bat10": 0, "bat11": 0, "bat12": 0, "bat13": 0, "bat14": 0,
            "bat15": 0, "bat16": 0, "bat17": 0, "bat18": 0,
            
            # Meter values
            "meterPow": 0,
            "meterIed": 0,
            "meterOed": 0,
            "meterIet": 0,
            "meterOet": 0,
            
            # Additional system values
            "powerRatio": 0,
            "csq": 0
        }
        
        # Retrieve live data as main data source
        live_response = api.getLastTsDataPro()
        
        if is_api_success(live_response):
            live_data = extract_live_data(live_response)
            output_data.update(live_data)
            output_data["success"] = True
        
        # Output JSON
        print(json.dumps(output_data))
        
    except Exception as e:
        error_data = {
            "error": str(e),
            "timestamp": datetime.now().isoformat(),
            "success": False,
            "power": 0,
            "etoday": 0,
            "etotal": 0,
            "status": "error"
        }
        print(json.dumps(error_data))
        sys.exit(1)

if __name__ == "__main__":
    main()