#!/usr/bin/env python3
"""
Safe Harbor Device Monitoring System
- Checks all devices every 15 minutes
- Tracks down devices and verifies after 15 min
- Auto-creates tickets and emails Ben
"""

import json
import os
import sys
import time
from datetime import datetime, timedelta
from pathlib import Path

# Add parent directory to path for imports
sys.path.insert(0, str(Path(__file__).parent.parent.parent))

from ticket_system import create_ticket, init_database

# State file to track down devices
STATE_FILE = os.path.expanduser("~/.openclaw/workspace/projects/tech-portal/monitor_state.json")
SITES_FILE = os.path.expanduser("~/.openclaw/workspace/projects/tech-portal/combined_sites.json")

def load_state():
    """Load monitoring state (devices currently down)"""
    if os.path.exists(STATE_FILE):
        with open(STATE_FILE, 'r') as f:
            return json.load(f)
    return {}

def save_state(state):
    """Save monitoring state"""
    with open(STATE_FILE, 'w') as f:
        json.dump(state, f, indent=2)

def load_sites():
    """Load current site/device data"""
    if not os.path.exists(SITES_FILE):
        print(f"❌ Sites file not found: {SITES_FILE}")
        return None
    
    with open(SITES_FILE, 'r') as f:
        return json.load(f)

def get_device_priority(device_type):
    """Determine ticket priority based on device type"""
    device_type_lower = device_type.lower()
    
    # Critical: Firewalls and switches
    if any(term in device_type_lower for term in ['firewall', 'gateway', 'security', 'switch', 'core']):
        return 'critical'
    
    # High: Access points
    if any(term in device_type_lower for term in ['ap', 'access point', 'wireless', 'wifi']):
        return 'high'
    
    # Default medium
    return 'medium'

def send_email_alert(ticket_id, device_name, site_name, device_type, priority, details):
    """Send email alert to Ben using gog CLI"""
    
    subject = f"🚨 Device Down Alert - {site_name}: {device_name}"
    
    body = f"""Safe Harbor Tech Portal - Device Alert

DEVICE STATUS: OFFLINE

Site: {site_name}
Device: {device_name}
Type: {device_type}
Priority: {priority.upper()}

DETAILS:
{details}

TICKET CREATED:
Ticket #{ticket_id} has been automatically created in the Tech Portal.

View ticket: https://safe-harbor-tech-app-8gq6z73gwintyanfnqu7jp.streamlit.app

---
This is an automated alert from Safe Harbor Tech Portal Device Monitor.
The device was verified offline for 15+ minutes before this alert was sent.
"""
    
    # Send via gog CLI
    try:
        import subprocess
        result = subprocess.run([
            '/home/administrator/.local/bin/gog',
            'gmail',
            'send',
            '--to', 'Ben.Brizendine@safeharborsolutionsllc.com',
            '--subject', subject,
            '--body', body,
            '--account', 'Dude@safeharborsolutionsllc.com'
        ], env={'GOG_KEYRING_PASSWORD': 'openclaw'}, capture_output=True, text=True, timeout=30)
        
        if result.returncode == 0:
            print(f"  ✅ Email sent to Ben about {device_name}")
            return True
        else:
            print(f"  ⚠️ Email send failed: {result.stderr}")
            return False
    except Exception as e:
        print(f"  ❌ Email error: {e}")
        return False

def check_devices():
    """Main monitoring function"""
    print(f"\n{'='*60}")
    print(f"🔍 Safe Harbor Device Monitor - {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
    print(f"{'='*60}\n")
    
    # Initialize database
    try:
        init_database()
    except:
        pass
    
    # Load current state and site data
    state = load_state()
    sites_data = load_sites()
    
    if not sites_data:
        print("❌ Cannot load sites data. Exiting.")
        return
    
    current_time = datetime.now().isoformat()
    new_state = {}
    
    # Check each site
    total_devices = 0
    offline_devices = 0
    new_alerts = 0
    
    for site in sites_data.get('sites', []):
        site_name = site['name']
        site_type = site['type']
        
        # Get offline devices for this site
        site_offline = site.get('offline_devices', 0)
        
        if site_offline > 0:
            print(f"📍 {site_name} ({site_type}): {site_offline} offline devices detected")
            
            # For now, we track by site since we don't have individual device IDs easily accessible
            # In production, you'd query UniFi/Meraki APIs for specific device lists
            device_key = f"{site_name}_{site_type}"
            
            if device_key in state:
                # Device was down before - check if 15+ minutes have passed
                first_seen = datetime.fromisoformat(state[device_key]['first_seen'])
                time_down = datetime.now() - first_seen
                
                if time_down >= timedelta(minutes=15) and not state[device_key].get('ticket_created'):
                    # Create ticket and send email
                    print(f"  ⚠️ DOWN for {int(time_down.total_seconds()/60)} minutes - Creating ticket...")
                    
                    # Determine priority (default to high for site-level alerts)
                    priority = 'high'
                    
                    # Create ticket
                    ticket_id = create_ticket(
                        title=f"Device(s) Offline - {site_name}",
                        client="Safe Harbor Solutions",
                        site=site_name,
                        priority=priority,
                        description=f"{site_offline} device(s) offline at {site_name} for 15+ minutes",
                        created_by="Device Monitor (Automated)",
                        network_type=site_type.lower(),
                        device_info=f"Site: {site_name} ({site_type})\nOffline devices: {site_offline}\nFirst detected: {first_seen.strftime('%Y-%m-%d %H:%M:%S')}\nConfirmed down at: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}"
                    )
                    
                    # Send email
                    details = f"Site: {site_name}\nNetwork Type: {site_type}\nOffline Device Count: {site_offline}\nFirst Detected: {first_seen.strftime('%Y-%m-%d %H:%M:%S')}\nDuration: {int(time_down.total_seconds()/60)} minutes"
                    
                    email_sent = send_email_alert(
                        ticket_id,
                        f"{site_offline} devices",
                        site_name,
                        site_type,
                        priority,
                        details
                    )
                    
                    # Update state
                    new_state[device_key] = {
                        'first_seen': state[device_key]['first_seen'],
                        'last_checked': current_time,
                        'ticket_created': True,
                        'ticket_id': ticket_id,
                        'email_sent': email_sent,
                        'offline_count': site_offline
                    }
                    
                    new_alerts += 1
                    print(f"  ✅ Ticket #{ticket_id} created and email sent")
                else:
                    # Still down but waiting for 15 min or already ticketed
                    if state[device_key].get('ticket_created'):
                        print(f"  ℹ️ Ticket #{state[device_key].get('ticket_id')} already exists")
                    else:
                        print(f"  ⏳ Waiting for 15 min confirmation ({int(time_down.total_seconds()/60)}/15 min)")
                    
                    new_state[device_key] = {
                        **state[device_key],
                        'last_checked': current_time,
                        'offline_count': site_offline
                    }
            else:
                # First time seeing this device/site down
                print(f"  🔔 First detection - will verify in 15 minutes")
                new_state[device_key] = {
                    'first_seen': current_time,
                    'last_checked': current_time,
                    'ticket_created': False,
                    'site_name': site_name,
                    'site_type': site_type,
                    'offline_count': site_offline
                }
        
        total_devices += site.get('devices', 0)
        offline_devices += site_offline
    
    # Save updated state
    save_state(new_state)
    
    # Summary
    print(f"\n{'='*60}")
    print(f"📊 SUMMARY")
    print(f"{'='*60}")
    print(f"Total Devices: {total_devices}")
    print(f"Currently Offline: {offline_devices}")
    print(f"New Alerts Created: {new_alerts}")
    print(f"Tracking {len(new_state)} potential issues")
    print(f"{'='*60}\n")

if __name__ == "__main__":
    check_devices()
