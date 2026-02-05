#!/usr/bin/env python3
"""
Tech Portal Dashboard - Streamlit UI for Meraki + UniFi + Tickets
"""

import streamlit as st
import subprocess
import json
import os
from ticket_system import get_tickets, get_ticket_stats, create_ticket, update_ticket

# Page config
st.set_page_config(
    page_title="Safe Harbor Tech Portal",
    page_icon="🔧",
    layout="wide"
)

# Load Meraki API key
MERAKI_API_KEY = os.getenv('MERAKI_API_KEY', '42feb43f88e3bdef877072b2054819a0e8eed31e')

# Header
st.title("🔧 Safe Harbor Tech Portal")
st.markdown("**Unified Dashboard** | Meraki • UniFi • Service Tickets")

# Tabs
tab1, tab2, tab3, tab4 = st.tabs(["📊 Overview", "📡 Networks", "🎫 Tickets", "⚙️ Actions"])

# Tab 1: Overview
with tab1:
    col1, col2, col3, col4 = st.columns(4)
    
    # Ticket stats
    stats = get_ticket_stats()
    
    with col1:
        st.metric("Open Tickets", stats['open'], delta=None)
    
    with col2:
        st.metric("In Progress", stats['in_progress'], delta=None)
    
    with col3:
        st.metric("Critical", stats['critical'], delta=None, delta_color="inverse")
    
    with col4:
        st.metric("Resolved Today", stats['resolved_today'], delta=None)
    
    st.divider()
    
    # Recent tickets
    st.subheader("Recent Tickets")
    recent = get_tickets(limit=5)
    
    if recent:
        for ticket in recent:
            with st.expander(f"#{ticket['id']} - {ticket['title']} ({ticket['status']})"):
                st.write(f"**Client:** {ticket['client']}")
                st.write(f"**Priority:** {ticket['priority']}")
                st.write(f"**Assigned:** {ticket['assigned_to'] or 'Unassigned'}")
                st.write(f"**Created:** {ticket['created_at']}")
                if ticket['description']:
                    st.write(f"**Description:** {ticket['description']}")
    else:
        st.info("No tickets yet")

# Tab 2: Networks
with tab2:
    network_type = st.radio("Network Type", ["Meraki", "UniFi"], horizontal=True)
    
    if network_type == "Meraki":
        st.subheader("Cisco Meraki Networks")
        
        if st.button("🔄 Refresh Meraki Data"):
            with st.spinner("Loading Meraki organizations..."):
                result = subprocess.run(
                    ['python3', 'meraki_cli.py', 'orgs'],
                    cwd='/home/administrator/.openclaw/workspace/projects/tech-portal',
                    capture_output=True,
                    text=True,
                    env={**os.environ, 'MERAKI_API_KEY': MERAKI_API_KEY}
                )
                
                if result.returncode == 0:
                    st.text(result.stdout)
                else:
                    st.error(f"Error: {result.stderr}")
        
        # Organization selector
        org_id = st.text_input("Organization ID (from list above)")
        
        if org_id:
            col1, col2 = st.columns(2)
            
            with col1:
                if st.button("List Networks"):
                    result = subprocess.run(
                        ['python3', 'meraki_cli.py', 'networks', '--org-id', org_id],
                        cwd='/home/administrator/.openclaw/workspace/projects/tech-portal',
                        capture_output=True,
                        text=True,
                        env={**os.environ, 'MERAKI_API_KEY': MERAKI_API_KEY}
                    )
                    st.text(result.stdout)
            
            network_id = st.text_input("Network ID")
            
            if network_id:
                if st.button("List Devices"):
                    result = subprocess.run(
                        ['python3', 'meraki_cli.py', 'devices', '--network-id', network_id],
                        cwd='/home/administrator/.openclaw/workspace/projects/tech-portal',
                        capture_output=True,
                        text=True,
                        env={**os.environ, 'MERAKI_API_KEY': MERAKI_API_KEY}
                    )
                    st.text(result.stdout)
    
    else:  # UniFi
        st.subheader("Ubiquiti UniFi Networks")
        
        # Load UniFi data
        try:
            with open('unifi_data.json', 'r') as f:
                unifi = json.load(f)
            
            # Summary metrics
            col1, col2, col3, col4 = st.columns(4)
            
            with col1:
                st.metric("Sites", unifi['summary']['totalSites'])
            with col2:
                st.metric("Devices", unifi['summary']['totalDevices'])
            with col3:
                st.metric("Clients", unifi['summary']['totalClients'])
            with col4:
                st.metric("Offline", unifi['summary']['offlineDevices'], delta_color="inverse")
            
            st.divider()
            
            # Site cards
            for site in unifi['sites']:
                with st.expander(f"📍 {site['desc']} - {site['location']}", expanded=False):
                    col1, col2, col3 = st.columns(3)
                    
                    with col1:
                        st.write("**Gateway:**")
                        st.write(f"{site['gateway']}")
                        if site['wan']['provider'] != 'N/A':
                            st.write(f"**ISP:** {site['wan']['provider']}")
                            st.write(f"**IP:** {site['wan']['ip']}")
                            if site['wan']['uptime']:
                                st.write(f"**Uptime:** {site['wan']['uptime']}%")
                    
                    with col2:
                        st.write("**Devices:**")
                        st.write(f"Total: {site['devices']['total']}")
                        st.write(f"WiFi APs: {site['devices']['wifi']}")
                        st.write(f"Switches: {site['devices']['wired']}")
                        if site['devices']['offline'] > 0:
                            st.write(f"⚠️ Offline: {site['devices']['offline']}")
                    
                    with col3:
                        st.write("**Clients:**")
                        st.write(f"Total: {site['clients']['total']}")
                        st.write(f"WiFi: {site['clients']['wifi']}")
                        st.write(f"Wired: {site['clients']['wired']}")
                        if site['clients']['guest'] > 0:
                            st.write(f"Guest: {site['clients']['guest']}")
                    
                    if site['alerts'] > 0:
                        st.warning(f"⚠️ {site['alerts']} alert(s) active")
                    
                    # Quick actions
                    st.write("**Quick Actions:**")
                    col1, col2, col3 = st.columns(3)
                    with col1:
                        st.button(f"View in UniFi Console", key=f"view_{site['siteId']}")
                    with col2:
                        st.button(f"Refresh Data", key=f"refresh_{site['siteId']}")
            
            st.caption(f"Last updated: {unifi['lastUpdated']}")
            
        except FileNotFoundError:
            st.warning("UniFi data not loaded. Run: `curl -H 'X-API-KEY: ...' https://api.ui.com/ea/sites > unifi_data.json`")

# Tab 3: Tickets
with tab3:
    st.subheader("Service Tickets")
    
    # Filters
    col1, col2, col3 = st.columns(3)
    
    with col1:
        status_filter = st.selectbox("Status", ["All", "open", "in-progress", "waiting", "resolved", "closed"])
    
    with col2:
        tech_filter = st.text_input("Assigned Tech")
    
    with col3:
        if st.button("➕ New Ticket"):
            st.session_state.show_new_ticket = True
    
    # New ticket form
    if st.session_state.get('show_new_ticket'):
        with st.form("new_ticket_form"):
            st.subheader("Create New Ticket")
            
            title = st.text_input("Title", placeholder="Brief description of the issue")
            client = st.text_input("Client", placeholder="Client or company name")
            site = st.text_input("Site Location", placeholder="Address or site name")
            
            col1, col2 = st.columns(2)
            with col1:
                priority = st.selectbox("Priority", ["low", "medium", "high", "critical"])
                network = st.selectbox("Network Type", ["unifi", "meraki", "both", "other"])
            
            with col2:
                assigned = st.text_input("Assign To", placeholder="Technician name")
            
            description = st.text_area("Description", placeholder="Detailed description of the issue")
            device_info = st.text_input("Device Info", placeholder="Device model, serial, etc.")
            
            col1, col2 = st.columns(2)
            with col1:
                submit = st.form_submit_button("Create Ticket")
            with col2:
                cancel = st.form_submit_button("Cancel")
            
            if submit:
                ticket_id = create_ticket(
                    title=title,
                    client=client,
                    created_by="Dashboard",
                    site=site,
                    priority=priority,
                    assigned_to=assigned if assigned else None,
                    network_type=network,
                    description=description,
                    device_info=device_info
                )
                st.success(f"✓ Ticket #{ticket_id} created")
                st.session_state.show_new_ticket = False
                st.rerun()
            
            if cancel:
                st.session_state.show_new_ticket = False
                st.rerun()
    
    # Ticket list
    tickets = get_tickets(
        status=None if status_filter == "All" else status_filter,
        assigned_to=tech_filter if tech_filter else None
    )
    
    if tickets:
        for ticket in tickets:
            with st.expander(f"#{ticket['id']} - {ticket['title']} [{ticket['status']}]"):
                col1, col2 = st.columns([2, 1])
                
                with col1:
                    st.write(f"**Client:** {ticket['client']}")
                    if ticket['site']:
                        st.write(f"**Site:** {ticket['site']}")
                    st.write(f"**Priority:** {ticket['priority']}")
                    st.write(f"**Network:** {ticket['network_type'] or 'N/A'}")
                    if ticket['description']:
                        st.write(f"**Description:** {ticket['description']}")
                
                with col2:
                    st.write(f"**Status:** {ticket['status']}")
                    st.write(f"**Assigned:** {ticket['assigned_to'] or 'Unassigned'}")
                    st.write(f"**Created:** {ticket['created_at']}")
                
                # Updates
                if ticket['updates']:
                    st.write("**Updates:**")
                    for user, text, timestamp in ticket['updates']:
                        st.text(f"[{timestamp}] {user}: {text}")
                
                # Quick actions
                st.write("**Actions:**")
                col1, col2, col3 = st.columns(3)
                
                with col1:
                    if st.button("Start Work", key=f"start_{ticket['id']}"):
                        update_ticket(ticket['id'], "Dashboard", "Work started", status='in-progress')
                        st.rerun()
                
                with col2:
                    if st.button("Mark Resolved", key=f"resolve_{ticket['id']}"):
                        update_ticket(ticket['id'], "Dashboard", "Issue resolved", status='resolved')
                        st.rerun()
                
                with col3:
                    if st.button("Close", key=f"close_{ticket['id']}"):
                        update_ticket(ticket['id'], "Dashboard", "Ticket closed", status='closed')
                        st.rerun()
    else:
        st.info("No tickets match your filters")

# Tab 4: Actions
with tab4:
    st.subheader("Quick Actions")
    
    col1, col2 = st.columns(2)
    
    with col1:
        st.write("**Meraki Actions**")
        
        device_serial = st.text_input("Device Serial Number")
        
        if device_serial:
            if st.button("🔄 Reboot Device"):
                result = subprocess.run(
                    ['python3', 'meraki_cli.py', 'reboot', '--serial', device_serial],
                    cwd='/home/administrator/.openclaw/workspace/projects/tech-portal',
                    capture_output=True,
                    text=True,
                    env={**os.environ, 'MERAKI_API_KEY': MERAKI_API_KEY}
                )
                
                if result.returncode == 0:
                    st.success(result.stdout)
                else:
                    st.error(result.stderr)
            
            if st.button("💡 Blink LEDs"):
                result = subprocess.run(
                    ['python3', 'meraki_cli.py', 'blink', '--serial', device_serial],
                    cwd='/home/administrator/.openclaw/workspace/projects/tech-portal',
                    capture_output=True,
                    text=True,
                    env={**os.environ, 'MERAKI_API_KEY': MERAKI_API_KEY}
                )
                
                if result.returncode == 0:
                    st.success(result.stdout)
                else:
                    st.error(result.stderr)
    
    with col2:
        st.write("**UniFi Actions**")
        st.info("UniFi controls coming soon")

# Sidebar
with st.sidebar:
    st.header("🔐 Safe Harbor Tech Portal")
    st.write("v1.0.0")
    
    st.divider()
    
    st.write("**Quick Stats**")
    stats = get_ticket_stats()
    st.metric("Total Active", stats['open'] + stats['in_progress'])
    
    st.divider()
    
    st.write("**Resources**")
    st.markdown("[Meraki Dashboard](https://dashboard.meraki.com)")
    st.markdown("[UniFi Console](https://unifi.ui.com)")
    
    if st.button("🔄 Refresh All"):
        st.rerun()
