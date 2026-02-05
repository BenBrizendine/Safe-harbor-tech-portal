#!/usr/bin/env python3
"""
Meraki Dashboard CLI - Similar to ez-unifi
Requires: MERAKI_API_KEY environment variable
"""

import os
import sys
import json
import argparse
import requests
from typing import Optional, Dict, List

class MerakiAPI:
    def __init__(self, api_key: Optional[str] = None):
        self.api_key = api_key or os.getenv('MERAKI_API_KEY')
        if not self.api_key:
            raise ValueError("MERAKI_API_KEY not set. Set it in .env or export it.")
        
        self.base_url = "https://api.meraki.com/api/v1"
        self.headers = {
            "X-Cisco-Meraki-API-Key": self.api_key
        }
    
    def _request(self, method: str, endpoint: str, data: Dict = None) -> Dict:
        """Make API request"""
        url = f"{self.base_url}/{endpoint}"
        try:
            if method == "GET":
                response = requests.get(url, headers=self.headers, timeout=10)
            elif method == "POST":
                response = requests.post(url, headers=self.headers, json=data, timeout=10)
            elif method == "PUT":
                response = requests.put(url, headers=self.headers, json=data, timeout=10)
            elif method == "DELETE":
                response = requests.delete(url, headers=self.headers, timeout=10)
            
            response.raise_for_status()
            return response.json() if response.text else {}
        except requests.exceptions.RequestException as e:
            print(f"✗ API Error: {e}")
            sys.exit(1)
    
    def get_organizations(self) -> List[Dict]:
        """List all organizations"""
        return self._request("GET", "organizations")
    
    def get_networks(self, org_id: str) -> List[Dict]:
        """List networks in an organization"""
        return self._request("GET", f"organizations/{org_id}/networks")
    
    def get_devices(self, network_id: str) -> List[Dict]:
        """List devices in a network"""
        return self._request("GET", f"networks/{network_id}/devices")
    
    def get_device_status(self, serial: str) -> Dict:
        """Get device status"""
        return self._request("GET", f"devices/{serial}/status")
    
    def get_clients(self, network_id: str) -> List[Dict]:
        """List clients in a network"""
        return self._request("GET", f"networks/{network_id}/clients")
    
    def reboot_device(self, serial: str) -> Dict:
        """Reboot a device"""
        return self._request("POST", f"devices/{serial}/reboot")
    
    def blink_device_leds(self, serial: str, duration: int = 20) -> Dict:
        """Blink device LEDs"""
        return self._request("POST", f"devices/{serial}/blinkLeds", {"duration": duration})


def cmd_list_orgs(api: MerakiAPI, args):
    """List organizations"""
    orgs = api.get_organizations()
    print(f"\n{'ID':<20} {'Name':<30}")
    print("-" * 50)
    for org in orgs:
        print(f"{org['id']:<20} {org['name']:<30}")
    print(f"\nTotal: {len(orgs)} organizations")


def cmd_list_networks(api: MerakiAPI, args):
    """List networks in an organization"""
    if not args.org_id:
        print("✗ Error: --org-id required")
        sys.exit(1)
    
    networks = api.get_networks(args.org_id)
    print(f"\n{'ID':<20} {'Name':<30} {'Type':<15}")
    print("-" * 65)
    for net in networks:
        print(f"{net['id']:<20} {net['name']:<30} {net.get('productTypes', ['N/A'])[0]:<15}")
    print(f"\nTotal: {len(networks)} networks")


def cmd_list_devices(api: MerakiAPI, args):
    """List devices in a network"""
    if not args.network_id:
        print("✗ Error: --network-id required")
        sys.exit(1)
    
    devices = api.get_devices(args.network_id)
    print(f"\n{'Serial':<15} {'Name':<25} {'Model':<15} {'Status':<10}")
    print("-" * 70)
    for dev in devices:
        status = dev.get('status', 'unknown')
        name = dev.get('name', 'Unnamed')
        print(f"{dev['serial']:<15} {name:<25} {dev.get('model', 'N/A'):<15} {status:<10}")
    print(f"\nTotal: {len(devices)} devices")


def cmd_reboot(api: MerakiAPI, args):
    """Reboot a device"""
    if not args.serial:
        print("✗ Error: --serial required")
        sys.exit(1)
    
    result = api.reboot_device(args.serial)
    print(f"✓ Reboot command sent to {args.serial}")


def cmd_blink(api: MerakiAPI, args):
    """Blink device LEDs"""
    if not args.serial:
        print("✗ Error: --serial required")
        sys.exit(1)
    
    duration = args.duration or 20
    result = api.blink_device_leds(args.serial, duration)
    print(f"✓ Blinking LEDs on {args.serial} for {duration} seconds")


def main():
    parser = argparse.ArgumentParser(description="Meraki Dashboard CLI")
    subparsers = parser.add_subparsers(dest='command', help='Commands')
    
    # List organizations
    parser_orgs = subparsers.add_parser('orgs', help='List organizations')
    
    # List networks
    parser_networks = subparsers.add_parser('networks', help='List networks')
    parser_networks.add_argument('--org-id', required=True, help='Organization ID')
    
    # List devices
    parser_devices = subparsers.add_parser('devices', help='List devices')
    parser_devices.add_argument('--network-id', required=True, help='Network ID')
    
    # Reboot device
    parser_reboot = subparsers.add_parser('reboot', help='Reboot a device')
    parser_reboot.add_argument('--serial', required=True, help='Device serial number')
    
    # Blink LEDs
    parser_blink = subparsers.add_parser('blink', help='Blink device LEDs')
    parser_blink.add_argument('--serial', required=True, help='Device serial number')
    parser_blink.add_argument('--duration', type=int, default=20, help='Duration in seconds')
    
    args = parser.parse_args()
    
    if not args.command:
        parser.print_help()
        sys.exit(1)
    
    try:
        api = MerakiAPI()
        
        if args.command == 'orgs':
            cmd_list_orgs(api, args)
        elif args.command == 'networks':
            cmd_list_networks(api, args)
        elif args.command == 'devices':
            cmd_list_devices(api, args)
        elif args.command == 'reboot':
            cmd_reboot(api, args)
        elif args.command == 'blink':
            cmd_blink(api, args)
        
    except ValueError as e:
        print(f"✗ Configuration Error: {e}")
        sys.exit(1)


if __name__ == "__main__":
    main()
