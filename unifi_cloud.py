#!/usr/bin/env python3
"""
UniFi Cloud API Integration
Uses api.ui.com for UniFi Cloud-hosted sites
"""

import requests
import os
from typing import Dict, List, Optional

class UniFiCloudAPI:
    """UniFi Cloud API Client for Site Manager"""
    
    def __init__(self, api_key: str):
        self.api_key = api_key
        self.base_url = "https://api.ui.com/ea"
        self.headers = {
            "X-API-KEY": api_key,
            "Content-Type": "application/json"
        }
    
    def _make_request(self, method: str, endpoint: str, **kwargs) -> Dict:
        """Make API request with error handling"""
        url = f"{self.base_url}{endpoint}"
        try:
            response = requests.request(method, url, headers=self.headers, timeout=30, **kwargs)
            response.raise_for_status()
            return {"success": True, "data": response.json()}
        except requests.exceptions.Timeout:
            return {"success": False, "error": "Request timed out"}
        except requests.exceptions.RequestException as e:
            return {"success": False, "error": str(e)}
    
    def list_sites(self) -> Dict:
        """List all sites"""
        return self._make_request("GET", "/sites")
    
    def list_devices(self, site_id: Optional[str] = None) -> Dict:
        """List devices (optionally filtered by site)"""
        endpoint = "/devices"
        params = {}
        if site_id:
            params["siteId"] = site_id
        return self._make_request("GET", endpoint, params=params)
    
    def get_device(self, device_id: str) -> Dict:
        """Get specific device details"""
        return self._make_request("GET", f"/devices/{device_id}")
    
    def list_clients(self, site_id: Optional[str] = None) -> Dict:
        """List active clients"""
        # Note: Client listing may not be available in Site Manager API
        # This endpoint is provisional and may need adjustment
        endpoint = "/clients"
        params = {}
        if site_id:
            params["siteId"] = site_id
        return self._make_request("GET", endpoint, params=params)
    
    def restart_device(self, device_id: str) -> Dict:
        """Restart a device"""
        # Device control commands may require local controller API
        return {
            "success": False,
            "error": "Device restart requires local controller access. UniFi Cloud API (Site Manager) provides monitoring only."
        }
    
    def upgrade_device(self, device_id: str) -> Dict:
        """Upgrade device firmware"""
        # Device control commands may require local controller API
        return {
            "success": False,
            "error": "Device upgrade requires local controller access. UniFi Cloud API (Site Manager) provides monitoring only."
        }
    
    def format_sites_output(self, result: Dict) -> str:
        """Format sites list for display"""
        if not result.get("success"):
            return f"❌ Error: {result.get('error', 'Unknown error')}"
        
        data = result.get("data", {})
        sites = data.get("data", [])
        
        if not sites:
            return "ℹ️ No sites found"
        
        output = [f"📡 UniFi Sites ({len(sites)} total)\n"]
        output.append("=" * 80)
        
        for site in sites:
            site_id = site.get("siteId", "Unknown")
            meta = site.get("meta", {})
            stats = site.get("statistics", {})
            counts = stats.get("counts", {})
            
            site_name = meta.get("desc") or meta.get("name", "Unnamed")
            devices = counts.get("totalDevice", 0)
            wifi_clients = counts.get("wifiClient", 0)
            wired_clients = counts.get("wiredClient", 0)
            total_clients = wifi_clients + wired_clients
            
            output.append(f"\n🏢 {site_name}")
            output.append(f"   Site ID: {site_id}")
            output.append(f"   Devices: {devices}")
            output.append(f"   Clients: {total_clients} (WiFi: {wifi_clients}, Wired: {wired_clients})")
        
        return "\n".join(output)
    
    def format_devices_output(self, result: Dict) -> str:
        """Format devices list for display"""
        if not result.get("success"):
            return f"❌ Error: {result.get('error', 'Unknown error')}"
        
        data = result.get("data", {})
        devices = data.get("data", [])
        
        if not devices:
            return "ℹ️ No devices found"
        
        output = [f"🖥️ UniFi Devices ({len(devices)} total)\n"]
        output.append("=" * 80)
        output.append("ℹ️ Note: UniFi Cloud API provides limited device details.")
        output.append("For detailed device management, use unifi.ui.com web interface.\n")
        
        for device in devices:
            device_id = device.get("id", "Unknown")
            name = device.get("name", "Unnamed")
            mac = device.get("mac", "N/A")
            model = device.get("model", "Unknown")
            status = "🟢 Online" if device.get("state") == 1 else "🔴 Offline"
            firmware = device.get("firmwareVersion", "Unknown")
            site_name = device.get("siteName", "Unknown Site")
            
            output.append(f"\n{status} {name}")
            output.append(f"   Model: {model}")
            output.append(f"   MAC: {mac}")
            output.append(f"   Firmware: {firmware}")
            output.append(f"   Site: {site_name}")
            output.append(f"   Device ID: {device_id}")
        
        return "\n".join(output)
    
    def format_device_output(self, result: Dict) -> str:
        """Format single device details"""
        if not result.get("success"):
            return f"❌ Error: {result.get('error', 'Unknown error')}"
        
        data = result.get("data", {})
        device = data.get("data", {})
        
        if not device:
            return "ℹ️ Device not found"
        
        name = device.get("name", "Unnamed")
        mac = device.get("mac", "N/A")
        model = device.get("model", "Unknown")
        status = "🟢 Online" if device.get("state") == 1 else "🔴 Offline"
        firmware = device.get("firmwareVersion", "Unknown")
        uptime = device.get("uptime", 0)
        site_name = device.get("siteName", "Unknown Site")
        ip = device.get("ip", "N/A")
        
        output = [f"🖥️ Device Details: {name}\n"]
        output.append("=" * 80)
        output.append(f"Status: {status}")
        output.append(f"Model: {model}")
        output.append(f"MAC Address: {mac}")
        output.append(f"IP Address: {ip}")
        output.append(f"Firmware: {firmware}")
        output.append(f"Uptime: {uptime // 86400}d {(uptime % 86400) // 3600}h {(uptime % 3600) // 60}m")
        output.append(f"Site: {site_name}")
        
        return "\n".join(output)


def load_api_key() -> Optional[str]:
    """Load UniFi API key from .env file"""
    env_path = '/home/administrator/.openclaw/workspace/.env'
    if os.path.exists(env_path):
        with open(env_path, 'r') as f:
            for line in f:
                if line.startswith('UNIFI_API_KEY='):
                    return line.strip().split('=', 1)[1]
    return None


# Convenience functions for app.py
def get_unifi_client() -> Optional[UniFiCloudAPI]:
    """Get configured UniFi Cloud API client"""
    api_key = load_api_key()
    if not api_key:
        return None
    return UniFiCloudAPI(api_key)


def execute_command(command: str) -> str:
    """
    Execute UniFi Cloud API command
    
    Supported commands:
    - sites: List all sites
    - devices: List all devices
    - devices <site_id>: List devices for specific site
    - device <device_id>: Get device details
    - clients: List active clients
    - clients <site_id>: List clients for specific site
    """
    client = get_unifi_client()
    if not client:
        return "❌ UniFi API key not configured. Please set UNIFI_API_KEY in .env file."
    
    parts = command.strip().split()
    if not parts:
        return "❌ No command specified"
    
    cmd = parts[0].lower()
    
    if cmd == "sites":
        result = client.list_sites()
        return client.format_sites_output(result)
    
    elif cmd == "devices":
        site_id = parts[1] if len(parts) > 1 else None
        result = client.list_devices(site_id)
        return client.format_devices_output(result)
    
    elif cmd == "device":
        if len(parts) < 2:
            return "❌ Usage: device <device_id>"
        device_id = parts[1]
        result = client.get_device(device_id)
        return client.format_device_output(result)
    
    elif cmd == "clients":
        site_id = parts[1] if len(parts) > 1 else None
        result = client.list_clients(site_id)
        if not result.get("success"):
            return f"ℹ️ Client listing is not available via UniFi Cloud API (Site Manager).\n\nThe Cloud API provides site-level statistics only.\n\nFor detailed client information:\n• Visit unifi.ui.com and navigate to your site\n• Use UniFi Network application for real-time client details"
        return "ℹ️ Client listing via Cloud API is limited. Use local controller for detailed client information."
    
    elif cmd in ["restart", "upgrade", "locate", "block", "unblock", "reconnect", "wlans", "wlan-enable", "wlan-disable", "wlan-password"]:
        action_descriptions = {
            "restart": "restart devices",
            "upgrade": "upgrade firmware",
            "locate": "locate devices",
            "block": "block clients",
            "unblock": "unblock clients",
            "reconnect": "reconnect clients",
            "wlans": "view WiFi networks",
            "wlan-enable": "enable WiFi networks",
            "wlan-disable": "disable WiFi networks",
            "wlan-password": "change WiFi passwords"
        }
        action = action_descriptions.get(cmd, "perform this action")
        
        return f"""ℹ️ UniFi Cloud API Limitation

Command: {cmd}
Purpose: {action}

The UniFi Cloud API (Site Manager) provides read-only monitoring and statistics.
It cannot execute device commands or modify configurations.

To {action}:
1. Visit unifi.ui.com
2. Select your site
3. Navigate to the relevant section (Devices, WiFi, Clients)
4. Use the web interface to perform the action

Note: If you have a local UniFi controller (Cloud Key, UDM, self-hosted), 
you would need local API access for these commands."""
    
    elif cmd == "health":
        # Special case - redirect to sites command
        return execute_command("sites")
    
    else:
        return f"""❌ Unknown command: {cmd}

Available UniFi Cloud API commands:
  sites              - List all sites with device/client counts
  devices            - List devices (limited info)
  devices <site_id>  - List devices for specific site
  device <device_id> - Get device details
  health             - View site health (redirects to 'sites')

Note: UniFi Cloud API is read-only. Device control commands (restart, 
upgrade, etc.) require local controller access or unifi.ui.com web interface."""


if __name__ == "__main__":
    # Test the API
    import sys
    
    if len(sys.argv) < 2:
        print("Usage: python3 unifi_cloud.py <command>")
        print("\nAvailable commands:")
        print("  sites              - List all sites")
        print("  devices            - List all devices")
        print("  devices <site_id>  - List devices for site")
        print("  device <device_id> - Get device details")
        sys.exit(1)
    
    command = " ".join(sys.argv[1:])
    print(execute_command(command))
