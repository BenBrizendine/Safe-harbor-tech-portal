#!/usr/bin/env python3
"""
Refresh site data from UniFi Cloud and Meraki APIs
Run this script to update the Tech Portal with latest sites/devices
"""

import json
import os
from unifi_cloud import UniFiCloudAPI
from dotenv import load_dotenv

# Load environment variables
load_dotenv('/home/administrator/.openclaw/workspace/.env')

def refresh_unifi_sites():
    """Fetch latest UniFi Cloud sites"""
    api_key = os.getenv('UNIFI_API_KEY')
    if not api_key:
        print("❌ UNIFI_API_KEY not found in .env")
        return None
    
    print("🔄 Fetching UniFi Cloud sites...")
    client = UniFiCloudAPI(api_key)
    
    # Get all sites
    result = client.list_sites()
    if not result.get('success'):
        print(f"❌ Error: {result.get('error')}")
        return None
    
    sites_data = result['data']
    sites = sites_data.get('sites', []) if isinstance(sites_data, dict) else sites_data
    
    print(f"✅ Found {len(sites)} UniFi sites")
    
    # Format for Tech Portal
    formatted_sites = []
    for site in sites:
        formatted_sites.append({
            'name': site.get('meta', {}).get('name', 'Unknown'),
            'type': 'unifi',
            'id': site.get('meta', {}).get('id'),
            'devices': site.get('meta', {}).get('deviceCount', 0),
            'clients': site.get('meta', {}).get('clientCount', 0),
            'status': 'online' if site.get('meta', {}).get('isUp') else 'offline'
        })
    
    return formatted_sites

def refresh_meraki_sites():
    """Load existing Meraki sites (already working)"""
    meraki_file = '/home/administrator/.openclaw/workspace/projects/tech-portal/meraki_sites.json'
    
    if not os.path.exists(meraki_file):
        print("⚠️ Meraki sites file not found")
        return []
    
    with open(meraki_file, 'r') as f:
        data = json.load(f)
    
    sites = data.get('sites', [])
    print(f"✅ Loaded {len(sites)} Meraki sites")
    return sites

def combine_sites(unifi_sites, meraki_sites):
    """Combine UniFi and Meraki sites into unified format"""
    combined = {
        'unifi_sites': len(unifi_sites) if unifi_sites else 0,
        'meraki_sites': len(meraki_sites),
        'total_sites': (len(unifi_sites) if unifi_sites else 0) + len(meraki_sites),
        'sites': []
    }
    
    if unifi_sites:
        combined['sites'].extend(unifi_sites)
    combined['sites'].extend(meraki_sites)
    
    # Calculate totals
    total_devices = sum(s.get('devices', 0) for s in combined['sites'])
    total_clients = sum(s.get('clients', 0) for s in combined['sites'] if s.get('clients'))
    offline_devices = sum(1 for s in combined['sites'] if s.get('status') == 'offline')
    
    combined['total_devices'] = total_devices
    combined['total_clients'] = total_clients
    combined['offline_devices'] = offline_devices
    
    return combined

def save_combined_sites(data):
    """Save combined sites to JSON file"""
    output_file = '/home/administrator/.openclaw/workspace/projects/tech-portal/combined_sites.json'
    
    with open(output_file, 'w') as f:
        json.dump(data, f, indent=2)
    
    print(f"\n✅ Saved combined data to {output_file}")
    print(f"📊 Summary:")
    print(f"   - UniFi sites: {data['unifi_sites']}")
    print(f"   - Meraki sites: {data['meraki_sites']}")
    print(f"   - Total sites: {data['total_sites']}")
    print(f"   - Total devices: {data['total_devices']}")
    print(f"   - Total clients: {data['total_clients']}")
    print(f"   - Offline devices: {data['offline_devices']}")

if __name__ == "__main__":
    print("🚀 Refreshing Tech Portal site data...\n")
    
    # Fetch UniFi sites
    unifi_sites = refresh_unifi_sites()
    
    # Load Meraki sites
    meraki_sites = refresh_meraki_sites()
    
    # Combine and save
    combined = combine_sites(unifi_sites, meraki_sites)
    save_combined_sites(combined)
    
    print("\n✅ Refresh complete! Restart the Tech Portal to see updated sites.")
    print("   Run: pkill -f 'streamlit run app.py' && streamlit run app.py &")
