#!/usr/bin/env python3
import os
import json
import requests

API_KEY = "42feb43f88e3bdef877072b2054819a0e8eed31e"
BASE_URL = "https://api.meraki.com/api/v1"
HEADERS = {"X-Cisco-Meraki-API-Key": API_KEY}

def get_request(endpoint):
    try:
        response = requests.get(f"{BASE_URL}/{endpoint}", headers=HEADERS, timeout=10)
        response.raise_for_status()
        return response.json()
    except Exception as e:
        print(f"Error: {e}")
        return []

# Get all orgs
orgs = get_request("organizations")
all_sites = []

for org in orgs:
    org_id = org['id']
    org_name = org['name']
    
    # Get networks for this org
    networks = get_request(f"organizations/{org_id}/networks")
    
    for net in networks:
        net_id = net['id']
        net_name = net['name']
        
        # Get devices
        devices = get_request(f"networks/{net_id}/devices")
        device_count = len(devices)
        
        # Get clients (can be slow, so we'll skip for now)
        # clients = get_request(f"networks/{net_id}/clients")
        
        site_data = {
            "name": net_name,
            "organization": org_name,
            "network_id": net_id,
            "type": "Meraki",
            "devices": device_count,
            "gateway": net.get('productTypes', ['Unknown'])[0],
            "location": "N/A"
        }
        
        all_sites.append(site_data)
        print(f"✓ {org_name} / {net_name}: {device_count} devices")

# Save to JSON
output_file = "meraki_sites.json"
with open(output_file, "w") as f:
    json.dump({"sites": all_sites, "total": len(all_sites)}, f, indent=2)

print(f"\n✓ Saved {len(all_sites)} Meraki sites to {output_file}")
