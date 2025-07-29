#!/usr/bin/env python3
import requests
import hashlib
import hmac
import base64
import json
from datetime import datetime
from typing import Dict, Any

class AisweiSolarAPI:
    """Client for the AISWEI/Solplanet Solar API (Pro User) for Hybrid Inverter with Meter."""
    
    def __init__(
        self,
        app_key: str,
        app_secret: str,
        api_key: str,
        token: str,
        sn: str
    ):
        """
        Initialize the AISWEI Solar API client for Pro users.
        
        Args:
            app_key: The App Key from your account
            app_secret: The App Secret from your account
            api_key: The API Key for your inverter
            token: The token for Pro API authentication
            sn: The Serial Number for your inverter
        """
        self.app_key = app_key
        self.app_secret = app_secret
        self.api_key = api_key
        self.token = token
        self.sn = sn
        
        # Set the base URL for Pro API
        self.base_url = "https://eu-api-genergal.aisweicloud.com"
    
    def _make_request(self, endpoint: str) -> Dict[str, Any]:
        """
        Make an API request with proper authentication.
        
        Args:
            endpoint: API endpoint with query parameters
            
        Returns:
            API response as a dictionary
        """
        method = "GET"
        content_type = "application/json; charset=UTF-8"
        accept = "application/json"
        
        # Add API key,token and serial number parameters
        endpoint += ('&' if '?' in endpoint else '?') + f"apikey={self.api_key}"
        endpoint += f"&token={self.token}"
        endpoint += f"&isnos={self.sn}"
        
        # Sort parameters alphabetically as required by API
        s1 = endpoint.split('?')
        if len(s1) > 1:
            s2 = sorted(s1[1].split('&'))
            endpoint = s1[0] + '?' + '&'.join(s2)
        
        # Prepare headers
        headers = {
            "User-Agent": "app 1.0",
            "Content-Type": content_type,
            "Accept": accept,
            "X-Ca-Signature-Headers": "X-Ca-Key",
            "X-Ca-Key": self.app_key
        }
        
        # Generate signature
        string_to_sign = f"{method}\n{accept}\n\n{content_type}\n\nX-Ca-Key:{self.app_key}\n{endpoint}"
        signature = base64.b64encode(
            hmac.new(
                self.app_secret.encode('utf-8'),
                string_to_sign.encode('utf-8'),
                hashlib.sha256
            ).digest()
        ).decode()
        
        headers["X-Ca-Signature"] = signature
        
        # Make the request
        url = f"{self.base_url}{endpoint}"
        
        try:
            response = requests.get(url, headers=headers)
            
            if response.status_code == 200:
                try:
                    return response.json()
                except:
                    return {"error": "Failed to parse JSON response", "status": response.status_code}
            else:
                print(f"Error: {response.status_code}")
                print(f"Headers: {dict(response.headers)}")
                print(f"Response: {response.text}")
                return {"error": response.text, "status": response.status_code, "headers": dict(response.headers)}
                
        except requests.exceptions.RequestException as e:
            print(f"Request failed: {str(e)}")
            return {"error": str(e)}

    def getPlanListPro(self) -> Dict[str, Any]:
        """
        API List 3.1
        Get the list of devices/plants for Pro user.
        
        Returns:
            Dictionary containing device information and current status
        """
        endpoint = "/pro/getPlanListPro"
        return self._make_request(endpoint)
    
    def getPlantOverviewPro(self) -> Dict[str, Any]:
        """
        API List 3.2
        Get the list of devices/plants for Pro user.
        
        Returns:
            Dictionary containing device information and current status
        """
        endpoint = "/pro/getPlantOverviewPro"
        return self._make_request(endpoint)
    
    def getPlantOutputPro(self) -> Dict[str, Any]:
        """
        API List 3.3
        Get the list of devices/plants for Pro user.
        
        Returns:
            Dictionary containing device information and current status
        """
        date = datetime.now().strftime("%Y-%m-%d")
        endpoint = f"/pro/getPlantOutputPro?period=bydays&date={date}"
        return self._make_request(endpoint)

    def getPlantEventPro(self) -> Dict[str, Any]: #Parameter `sdt` is required
        """
        API List 3.4
        Get the list of devices/plants for Pro user.
        
        Returns:
            Dictionary containing device information and current status
        """
        endpoint = "/pro/getPlantEventPro"
        return self._make_request(endpoint)
    
    def getDeviceListPro(self) -> Dict[str, Any]:
        """
        API List 3.5
        Get the list of devices/plants for Pro user.
        
        Returns:
            Dictionary containing device information and current status
        """
        endpoint = "/pro/getDeviceListPro"
        return self._make_request(endpoint)

    def getLocationPro(self) -> Dict[str, Any]: #Parameter `psno` is required
        """
        API List 3.6
        Get the list of devices/plants for Pro user.
        
        Returns:
            Dictionary containing device information and current status
        """
        endpoint = "/pro/getLocationPro"
        return self._make_request(endpoint)

    def getLastTsDataPro(self) -> Dict[str, Any]: #Parameter `isnos` is required
        """
        API List 3.7
        Get the list of devices/plants for Pro user.
        
        Returns:
            Dictionary containing device information and current status
        """
        endpoint = "/pro/getLastTsDataPro"
        return self._make_request(endpoint)
    
    def getInverterDataPagePro(self) -> Dict[str, Any]: #Parameter `startDate` is required
        """
        API List 3.8
        Get the list of devices/plants for Pro user.
        
        Returns:
            Dictionary containing device information and current status
        """
        endpoint = "/pro/getInverterDataPagePro"
        return self._make_request(endpoint)
    
    def getInverterETodayPro(self) -> Dict[str, Any]:
        """
        API List 3.9
        Get the list of devices/plants for Pro user.
        
        Returns:
            Dictionary containing device information and current status
        """
        date = datetime.now().strftime("%Y-%m-%d")
        endpoint = f"/pro/getInverterETodayPro?date={date}"
        return self._make_request(endpoint)
    
    def getInverterHisErrorPagePro(self) -> Dict[str, Any]: #Parameter `startDate` is required
        """
        API List 3.10
        Get the list of devices/plants for Pro user.
        
        Returns:
            Dictionary containing device information and current status
        """
        endpoint = "/pro/getInverterHisErrorPagePro"
        return self._make_request(endpoint)
    
    def getInverterCurrentErrorPro(self) -> Dict[str, Any]:
        """
        API List 3.11
        Get the list of devices/plants for Pro user.
        
        Returns:
            Dictionary containing device information and current status
        """
        endpoint = "/pro/getInverterCurrentErrorPro"
        return self._make_request(endpoint)

    def getInverterOverviewPro(self) -> Dict[str, Any]:
        """
        API List 3.12
        Get the list of devices/plants for Pro user.
        
        Returns:
            Dictionary containing device information and current status
        """
        endpoint = "/pro/getInverterOverviewPro"
        return self._make_request(endpoint)

    def getInverterRecoverStatusPro(self) -> Dict[str, Any]: #Parameter `faultCodes` is required
        """
        API List 3.13
        Get the list of devices/plants for Pro user.
        
        Returns:
            Dictionary containing device information and current status
        """
        endpoint = "/pro/getInverterRecoverStatusPro"
        return self._make_request(endpoint)
    
    def createstationPro(self) -> Dict[str, Any]:
        """
        API List 3.14
        Get the list of devices/plants for Pro user.
        
        Returns:
            Dictionary containing device information and current status
        """
        endpoint = "/pro/createstationPro"
        return self._make_request(endpoint)
  

if __name__ == "__main__":
    # Import credentials from config file
    try:
        from config import APP_KEY, APP_SECRET, API_KEY, TOKEN, SN
    except ImportError:
        print("Error: Could not import credentials from config.py")
        print("Please create a config.py file with your credentials based on config_template.py")
        exit(1)
    
    # Initialize the API client for Pro user
    api = AisweiSolarAPI(
        app_key=APP_KEY,
        app_secret=APP_SECRET,
        api_key=API_KEY,
        token=TOKEN,
        sn=SN
    )
    
    # Retrieve and display all current data

    print("\n=== 3.1 getPlanListPro ===")
    power_data = api.getPlanListPro()
    if isinstance(power_data, dict):
        print(json.dumps(power_data, indent=2))

    print("\n=== 3.2 getPlantOverviewPro ===")
    power_data = api.getPlantOverviewPro()
    if isinstance(power_data, dict):
        print(json.dumps(power_data, indent=2))

    print("\n=== 3.3 getPlantOutputPro ===")
    power_data = api.getPlantOutputPro()
    if isinstance(power_data, dict):
        print(json.dumps(power_data, indent=2))

    print("\n=== 3.4 getPlantEventPro ===")
    power_data = api.getPlantEventPro()
    if isinstance(power_data, dict):
        print(json.dumps(power_data, indent=2))

    print("\n=== 3.5 getDeviceListPro ===")
    devices = api.getDeviceListPro()
    if isinstance(devices, dict):
        print(json.dumps(devices, indent=2))

    print("\n=== 3.6 getLocationPro ===")
    location_data = api.getLocationPro()
    if isinstance(location_data, dict):
        print(json.dumps(location_data, indent=2))

    print("\n=== 3.7 getLastTsDataPro ===")
    last_ts_data = api.getLastTsDataPro()
    if isinstance(last_ts_data, dict):
        print(json.dumps(last_ts_data, indent=2))
        
    print("\n=== 3.8 getInverterDataPagePro ===")
    inverter_data = api.getInverterDataPagePro()
    if isinstance(inverter_data, dict):
        print(json.dumps(inverter_data, indent=2))

    print("\n=== 3.9 getInverterETodayPro ===")
    inverter_data = api.getInverterETodayPro()
    if isinstance(inverter_data, dict):
        print(json.dumps(inverter_data, indent=2))

    print("\n=== 3.10 getInverterHisErrorPagePro ===")
    inverter_data = api.getInverterHisErrorPagePro()
    if isinstance(inverter_data, dict):
        print(json.dumps(inverter_data, indent=2))
        
    print("\n=== 3.11 getInverterCurrentErrorPro ===")
    inverter_data = api.getInverterCurrentErrorPro()
    if isinstance(inverter_data, dict):
        print(json.dumps(inverter_data, indent=2))

    print("\n=== 3.12 getInverterOverviewPro ===")
    inverter_data = api.getInverterOverviewPro()
    if isinstance(inverter_data, dict):
        print(json.dumps(inverter_data, indent=2))
        
    print("\n=== 3.13 getInverterRecoverStatusPro ===")
    inverter_data = api.getInverterRecoverStatusPro()
    if isinstance(inverter_data, dict):
        print(json.dumps(inverter_data, indent=2))

    print("\n=== 3.14 createstationPro ===")
    inverter_data = api.createstationPro()
    if isinstance(inverter_data, dict):
        print(json.dumps(inverter_data, indent=2))