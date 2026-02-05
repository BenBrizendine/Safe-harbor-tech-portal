#!/usr/bin/env python3
"""
Safe Harbor Tech Portal - Futuristic Enhanced Edition
"""

import streamlit as st
import json
import os
import subprocess
from datetime import datetime
from ticket_system import get_tickets, get_ticket_stats, create_ticket, update_ticket

# Page config
st.set_page_config(
    page_title="Safe Harbor Tech Portal",
    page_icon="⚓",
    layout="wide",
    initial_sidebar_state="collapsed"
)

# Enhanced futuristic CSS with glassmorphism and Safe Harbor branding
st.markdown("""
<style>
    /* Import tech font */
    @import url('https://fonts.googleapis.com/css2?family=Orbitron:wght@400;500;600;700;900&family=Rajdhani:wght@300;400;500;600;700&display=swap');
    
    /* Safe Harbor Brand Colors */
    :root {
        --primary: #145F82;
        --primary-glow: rgba(20, 95, 130, 0.3);
        --secondary: #2E86AB;
        --success: #34A853;
        --warning: #FBBC04;
        --danger: #EA4335;
        --light: #F8F9FA;
        --dark: #0A1929;
        --glass: rgba(255, 255, 255, 0.1);
    }
    
    /* Dark theme background */
    .main {
        background: linear-gradient(135deg, #0A1929 0%, #1a2332 50%, #0f1b2d 100%);
        color: #E0E7FF;
    }
    
    .stApp {
        background: linear-gradient(135deg, #0A1929 0%, #1a2332 50%, #0f1b2d 100%);
    }
    
    /* Tech font for headers */
    h1, h2, h3, h4 {
        font-family: 'Orbitron', monospace !important;
        color: #ffffff;
        text-shadow: 0 0 20px var(--primary-glow);
        letter-spacing: 1px;
    }
    
    h1 {
        font-size: 2.5rem !important;
        font-weight: 700 !important;
        background: linear-gradient(135deg, #145F82 0%, #2E86AB 100%);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
        background-clip: text;
    }
    
    /* Body text font */
    body, .stMarkdown, p, div, span {
        font-family: 'Rajdhani', sans-serif;
        color: #E0E7FF;
    }
    
    /* Status Light Bar Styles */
    .status-bar {
        display: flex;
        gap: 8px;
        padding: 20px;
        background: rgba(10, 25, 41, 0.7);
        border-radius: 16px;
        backdrop-filter: blur(10px);
        border: 1px solid rgba(20, 95, 130, 0.3);
        margin-bottom: 30px;
        overflow-x: auto;
        box-shadow: 0 8px 32px rgba(0, 0, 0, 0.4);
    }
    
    .status-light {
        position: relative;
        min-width: 60px;
        height: 60px;
        border-radius: 50%;
        cursor: pointer;
        transition: all 0.3s cubic-bezier(0.4, 0, 0.2, 1);
        display: flex;
        align-items: center;
        justify-content: center;
        font-size: 10px;
        font-weight: 600;
        text-align: center;
        border: 2px solid transparent;
    }
    
    .status-light.green {
        background: radial-gradient(circle, #34A853 0%, #2d9048 100%);
        box-shadow: 0 0 20px rgba(52, 168, 83, 0.6), 0 0 40px rgba(52, 168, 83, 0.3);
        border-color: #34A853;
    }
    
    .status-light.yellow {
        background: radial-gradient(circle, #FBBC04 0%, #e0a803 100%);
        box-shadow: 0 0 20px rgba(251, 188, 4, 0.6), 0 0 40px rgba(251, 188, 4, 0.3);
        border-color: #FBBC04;
    }
    
    .status-light.red {
        background: radial-gradient(circle, #EA4335 0%, #d23b2f 100%);
        box-shadow: 0 0 20px rgba(234, 67, 53, 0.6), 0 0 40px rgba(234, 67, 53, 0.3);
        border-color: #EA4335;
        animation: pulse-red 2s infinite;
    }
    
    .status-light:hover {
        transform: scale(1.15) translateY(-5px);
        filter: brightness(1.3);
    }
    
    @keyframes pulse-red {
        0%, 100% { box-shadow: 0 0 20px rgba(234, 67, 53, 0.6), 0 0 40px rgba(234, 67, 53, 0.3); }
        50% { box-shadow: 0 0 30px rgba(234, 67, 53, 0.9), 0 0 60px rgba(234, 67, 53, 0.5); }
    }
    
    .status-label {
        position: absolute;
        bottom: -25px;
        font-size: 11px;
        white-space: nowrap;
        color: #B0BEC5;
        font-weight: 500;
    }
    
    /* Glassmorphism cards */
    .stButton > button {
        background: rgba(255, 255, 255, 0.05);
        backdrop-filter: blur(10px);
        color: #E0E7FF;
        border: 1px solid rgba(20, 95, 130, 0.3);
        border-radius: 16px;
        padding: 24px;
        font-size: 14px;
        font-family: 'Rajdhani', sans-serif;
        font-weight: 500;
        text-align: left;
        transition: all 0.3s cubic-bezier(0.4, 0, 0.2, 1);
        box-shadow: 0 8px 32px rgba(0, 0, 0, 0.3);
    }
    
    .stButton > button:hover {
        background: rgba(20, 95, 130, 0.2);
        border-color: #145F82;
        box-shadow: 0 8px 32px var(--primary-glow), 0 0 20px var(--primary-glow);
        transform: translateY(-4px);
    }
    
    /* Metric cards with glow */
    [data-testid="stMetricValue"] {
        font-size: 32px;
        color: #ffffff;
        font-weight: 700;
        font-family: 'Orbitron', monospace;
        text-shadow: 0 0 10px var(--primary-glow);
    }
    
    [data-testid="metric-container"] {
        background: rgba(20, 95, 130, 0.1);
        backdrop-filter: blur(10px);
        border: 1px solid rgba(20, 95, 130, 0.3);
        border-radius: 12px;
        padding: 16px;
        box-shadow: 0 4px 16px rgba(0, 0, 0, 0.3);
    }
    
    [data-testid="stMetricLabel"] {
        color: #B0BEC5;
        font-size: 14px;
        font-weight: 600;
    }
    
    /* Tab styling */
    .stTabs [data-baseweb="tab-list"] {
        gap: 12px;
        background: transparent;
    }
    
    .stTabs [data-baseweb="tab"] {
        background: rgba(255, 255, 255, 0.05);
        backdrop-filter: blur(10px);
        border-radius: 12px;
        padding: 12px 24px;
        font-weight: 600;
        border: 1px solid rgba(20, 95, 130, 0.3);
        color: #B0BEC5;
        font-family: 'Rajdhani', sans-serif;
        transition: all 0.3s;
    }
    
    .stTabs [aria-selected="true"] {
        background: linear-gradient(135deg, #145F82 0%, #2E86AB 100%);
        color: white !important;
        border-color: #145F82 !important;
        box-shadow: 0 4px 16px var(--primary-glow);
    }
    
    /* Login form */
    .login-container {
        background: rgba(20, 95, 130, 0.1);
        backdrop-filter: blur(20px);
        border: 1px solid rgba(20, 95, 130, 0.3);
        border-radius: 24px;
        padding: 40px;
        box-shadow: 0 16px 64px rgba(0, 0, 0, 0.5);
    }
    
    .login-header {
        text-align: center;
        font-size: 2.5rem;
        font-weight: 700;
        font-family: 'Orbitron', monospace;
        margin-bottom: 10px;
        background: linear-gradient(135deg, #145F82 0%, #2E86AB 100%);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
        background-clip: text;
    }
    
    .login-subheader {
        text-align: center;
        color: #B0BEC5;
        font-size: 18px;
        margin-bottom: 30px;
        font-weight: 500;
    }
    
    /* Input fields */
    .stTextInput > div > div > input,
    .stTextArea > div > div > textarea,
    .stSelectbox > div > div {
        background: rgba(255, 255, 255, 0.05) !important;
        backdrop-filter: blur(10px);
        border: 1px solid rgba(20, 95, 130, 0.3) !important;
        border-radius: 8px;
        color: #E0E7FF !important;
        font-family: 'Rajdhani', sans-serif;
    }
    
    .stTextInput > div > div > input:focus,
    .stTextArea > div > div > textarea:focus {
        border-color: #145F82 !important;
        box-shadow: 0 0 16px var(--primary-glow) !important;
    }
    
    /* Expander styling */
    .streamlit-expanderHeader {
        background: rgba(20, 95, 130, 0.1);
        backdrop-filter: blur(10px);
        border-radius: 12px;
        border: 1px solid rgba(20, 95, 130, 0.3);
        color: #E0E7FF;
        font-weight: 600;
    }
    
    .streamlit-expanderHeader:hover {
        border-color: #145F82;
        box-shadow: 0 4px 16px var(--primary-glow);
    }
    
    /* Code blocks */
    .stCodeBlock {
        background: rgba(10, 25, 41, 0.8) !important;
        border: 1px solid rgba(20, 95, 130, 0.3);
        border-radius: 8px;
    }
    
    code {
        color: #4FC3F7 !important;
        font-family: 'Courier New', monospace;
    }
    
    /* Divider */
    hr {
        margin: 30px 0;
        border: none;
        height: 1px;
        background: linear-gradient(90deg, transparent 0%, rgba(20, 95, 130, 0.5) 50%, transparent 100%);
    }
    
    /* Success/Error/Warning/Info boxes */
    .stSuccess, .stError, .stWarning, .stInfo {
        background: rgba(255, 255, 255, 0.05);
        backdrop-filter: blur(10px);
        border-radius: 8px;
        border-left: 4px solid;
    }
    
    .stSuccess {
        border-left-color: #34A853;
    }
    
    .stError {
        border-left-color: #EA4335;
    }
    
    .stWarning {
        border-left-color: #FBBC04;
    }
    
    .stInfo {
        border-left-color: #145F82;
    }
    
    /* Logo container */
    .logo-container {
        display: flex;
        align-items: center;
        gap: 20px;
    }
    
    /* Smooth transitions */
    * {
        transition: background-color 0.3s, border-color 0.3s, color 0.3s;
    }
    
    /* Custom scrollbar */
    ::-webkit-scrollbar {
        width: 8px;
        height: 8px;
    }
    
    ::-webkit-scrollbar-track {
        background: rgba(10, 25, 41, 0.5);
    }
    
    ::-webkit-scrollbar-thumb {
        background: rgba(20, 95, 130, 0.5);
        border-radius: 4px;
    }
    
    ::-webkit-scrollbar-thumb:hover {
        background: rgba(20, 95, 130, 0.8);
    }
</style>
""", unsafe_allow_html=True)

# Valid users
VALID_USERS = {
    "john": {"password": "john123", "name": "John Wong"},
    "ben": {"password": "ben123", "name": "Ben Brizendine"},
    "caleb": {"password": "caleb123", "name": "Caleb Galloway"},
    "craig": {"password": "craig123", "name": "Craig Murrell"}
}

# Initialize session state
if 'authenticated' not in st.session_state:
    st.session_state.authenticated = False
if 'username' not in st.session_state:
    st.session_state.username = None
if 'current_site' not in st.session_state:
    st.session_state.current_site = None
if 'show_new_ticket' not in st.session_state:
    st.session_state.show_new_ticket = False

# Login page
def login_page():
    col1, col2, col3 = st.columns([1, 2, 1])
    
    with col2:
        st.markdown('<div class="login-container">', unsafe_allow_html=True)
        
        # Logo
        try:
            logo_col1, logo_col2, logo_col3 = st.columns([1, 2, 1])
            with logo_col2:
                st.image("/home/administrator/.openclaw/workspace/projects/tech-portal/logo-black.png", width=250)
        except:
            st.markdown('<p class="login-header">⚓ Safe Harbor</p>', unsafe_allow_html=True)
        
        st.markdown('<p class="login-subheader">Tech Portal</p>', unsafe_allow_html=True)
        st.markdown("---")
        
        username = st.text_input("Username", key="login_username").lower()
        password = st.text_input("Password", type="password", key="login_password")
        
        if st.button("🔐 Login", use_container_width=True):
            if username in VALID_USERS and VALID_USERS[username]["password"] == password:
                st.session_state.authenticated = True
                st.session_state.username = username
                st.session_state.user_name = VALID_USERS[username]["name"]
                st.rerun()
            else:
                st.error("❌ Invalid username or password")
        
        st.markdown('</div>', unsafe_allow_html=True)

# Load combined site data
def load_site_data():
    try:
        with open('/home/administrator/.openclaw/workspace/projects/tech-portal/combined_sites.json', 'r') as f:
            return json.load(f)
    except Exception as e:
        st.error(f"Error loading site data: {e}")
        return {"sites": [], "summary": {}}

# Run UniFi command
def run_unifi_command(cmd):
    try:
        result = subprocess.run(
            f"cd /home/administrator/.openclaw/workspace/skills/ez-unifi && uv run scripts/unifi.py {cmd}",
            shell=True,
            capture_output=True,
            text=True,
            timeout=30
        )
        return result.stdout if result.returncode == 0 else result.stderr
    except Exception as e:
        return f"Error: {str(e)}"

# Calculate site health status
def get_site_health(site):
    """Determine site health: green (healthy), yellow (warning), red (critical)"""
    offline = site.get('offline', 0)
    alerts = site.get('alerts', 0)
    
    if offline > 0 or alerts > 0:
        return 'red'
    elif site.get('devices', 0) == 0:
        return 'yellow'
    else:
        return 'green'

# Status light bar component
def render_status_bar(sites):
    """Render futuristic status light bar"""
    
    # Group sites by health
    green_sites = [s for s in sites if get_site_health(s) == 'green']
    yellow_sites = [s for s in sites if get_site_health(s) == 'yellow']
    red_sites = [s for s in sites if get_site_health(s) == 'red']
    
    st.markdown(f"""
    <div style="margin-bottom: 20px; text-align: center;">
        <h3 style="margin-bottom: 5px;">🌐 Network Status Overview</h3>
        <p style="color: #B0BEC5; font-size: 14px;">
            <span style="color: #34A853;">●</span> {len(green_sites)} Healthy &nbsp;&nbsp;
            <span style="color: #FBBC04;">●</span> {len(yellow_sites)} Warning &nbsp;&nbsp;
            <span style="color: #EA4335;">●</span> {len(red_sites)} Critical
        </p>
    </div>
    """, unsafe_allow_html=True)
    
    # Render status lights in a scrollable container
    lights_html = '<div class="status-bar">'
    
    # Red sites first (critical)
    for site in red_sites:
        site_name = site['name']
        lights_html += f'''
        <div class="status-light red" onclick="window.parent.postMessage({{type: 'streamlit:setComponentValue', value: '{site_name}'}}, '*')">
            <span style="color: white; font-size: 9px;">{site_name[:8]}</span>
            <div class="status-label">{site_name[:12]}</div>
        </div>
        '''
    
    # Yellow sites (warning)
    for site in yellow_sites:
        site_name = site['name']
        lights_html += f'''
        <div class="status-light yellow" onclick="window.parent.postMessage({{type: 'streamlit:setComponentValue', value: '{site_name}'}}, '*')">
            <span style="color: white; font-size: 9px;">{site_name[:8]}</span>
            <div class="status-label">{site_name[:12]}</div>
        </div>
        '''
    
    # Green sites (healthy)
    for site in green_sites:
        site_name = site['name']
        lights_html += f'''
        <div class="status-light green" onclick="window.parent.postMessage({{type: 'streamlit:setComponentValue', value: '{site_name}'}}, '*')">
            <span style="color: white; font-size: 9px;">{site_name[:8]}</span>
            <div class="status-label">{site_name[:12]}</div>
        </div>
        '''
    
    lights_html += '</div>'
    st.markdown(lights_html, unsafe_allow_html=True)
    
    # Handle clicks on status lights
    st.markdown("""
    <script>
    window.addEventListener('message', function(event) {
        if (event.data.value) {
            window.location.href = '?site=' + event.data.value;
        }
    });
    </script>
    """, unsafe_allow_html=True)

# Site card component
def site_card(site):
    site_type = site.get('type', 'Unknown')
    site_name = site['name']
    health = get_site_health(site)
    
    # Status indicator
    status_colors = {'green': '🟢', 'yellow': '🟡', 'red': '🔴'}
    status_emoji = status_colors.get(health, '⚪')
    
    # Alert badge
    alerts = site.get('alerts', 0)
    alert_badge = f" ⚠️ {alerts}" if alerts > 0 else ""
    
    # Device and client counts
    device_count = site.get('devices', 0)
    client_count = site.get('clients', '?')
    if client_count is None:
        client_count = "?"
    
    # Organization info
    org = site.get('organization', '')
    gateway = site.get('gateway', 'N/A')
    
    label = f"{site_type}"
    if org:
        label += f" • {org}"
    
    if st.button(
        f"{status_emoji} **{site_name}**\n\n"
        f"🏢 {label}\n"
        f"🖥️ {device_count} devices • "
        f"👥 {client_count} clients{alert_badge}",
        key=f"site_{site_name.replace(' ', '_').replace('-', '_')}",
        use_container_width=True
    ):
        st.session_state.current_site = site_name
        st.rerun()

# Optimize wireless function
def optimize_wireless(site_name):
    results = []
    results.append("🔍 Analyzing wireless environment...")
    
    # Get WiFi networks
    wlans_output = run_unifi_command("wlans")
    results.append("\n📡 Current WiFi Networks:")
    results.append(wlans_output)
    
    # Get client distribution
    clients_output = run_unifi_command("clients")
    results.append("\n👥 Client Distribution:")
    results.append(clients_output)
    
    # Recommendations
    results.append("\n💡 Optimization Recommendations:")
    results.append("✓ Use Auto channel selection (enabled by default)")
    results.append("✓ Set transmit power to Auto or Medium (prevents oversaturation)")
    results.append("✓ Enable band steering (5GHz preferred)")
    results.append("✓ Disable older protocols (802.11b) if no legacy devices")
    results.append("✓ Enable Fast Roaming (802.11r) for seamless handoff")
    results.append("✓ Set minimum data rate to 12Mbps (reduces airtime)")
    
    return "\n".join(results)

# Main dashboard
def main_dashboard():
    # Header with logo
    col1, col2, col3 = st.columns([1, 4, 1])
    with col1:
        try:
            st.image("/home/administrator/.openclaw/workspace/projects/tech-portal/logo-black.png", width=100)
        except:
            st.markdown("# ⚓")
    with col2:
        st.markdown("# Safe Harbor Tech Portal")
        st.caption("🌐 Network Management & Support System")
    with col3:
        st.write(f"**{st.session_state.user_name}**")
        if st.button("🚪 Logout", use_container_width=True):
            st.session_state.authenticated = False
            st.session_state.username = None
            st.session_state.current_site = None
            st.rerun()
    
    st.markdown("---")
    
    # Load data
    data = load_site_data()
    sites = data.get('sites', [])
    summary = data.get('summary', {})
    
    # Status Light Bar (Primary Feature)
    render_status_bar(sites)
    
    # Summary metrics
    col1, col2, col3, col4 = st.columns(4)
    with col1:
        total_sites = data.get('total_sites', len(sites))
        st.metric("🏢 Total Sites", total_sites)
    with col2:
        total_devices = summary.get('total_devices', 0)
        st.metric("🖥️ Devices", total_devices)
    with col3:
        total_clients = summary.get('total_clients', 0)
        st.metric("👥 Clients", total_clients)
    with col4:
        offline = summary.get('offline_devices', 0)
        st.metric("⚠️ Offline", offline, delta=None if offline == 0 else "⚠️")
    
    st.divider()
    
    # Tabs for different sections
    tab1, tab2, tab3, tab4, tab5 = st.tabs(["📡 Sites", "🖥️ Devices", "👥 Clients", "📶 Wireless", "🎫 Tickets"])
    
    with tab1:
        st.subheader("🌐 Network Sites")
        
        # Search/filter
        search = st.text_input("🔍 Search sites...", placeholder="Type site name, location, or type")
        
        # Filter sites
        filtered_sites = sites
        if search:
            search_lower = search.lower()
            filtered_sites = [
                s for s in sites 
                if search_lower in s['name'].lower() 
                or search_lower in s.get('type', '').lower()
                or search_lower in s.get('organization', '').lower()
            ]
        
        if not filtered_sites:
            st.info("No sites found matching your search.")
        else:
            # Display sites in rows of 3
            for i in range(0, len(filtered_sites), 3):
                cols = st.columns(3)
                for j, col in enumerate(cols):
                    if i + j < len(filtered_sites):
                        with col:
                            site_card(filtered_sites[i + j])
    
    with tab2:
        st.subheader("🖥️ Device Management")
        
        col1, col2 = st.columns(2)
        
        with col1:
            if st.button("📋 List All Devices", use_container_width=True):
                with st.spinner("Loading devices..."):
                    output = run_unifi_command("devices")
                    st.code(output, language="text")
        
        with col2:
            if st.button("🔄 Refresh Device Status", use_container_width=True):
                with st.spinner("Refreshing..."):
                    output = run_unifi_command("health")
                    st.code(output, language="text")
        
        st.divider()
        
        with st.expander("🔧 Device Actions"):
            device_mac = st.text_input("Device MAC Address", placeholder="00:00:00:00:00:00")
            
            if device_mac:
                col1, col2, col3, col4 = st.columns(4)
                
                with col1:
                    if st.button("🔄 Restart", use_container_width=True):
                        with st.spinner("Restarting..."):
                            output = run_unifi_command(f"restart {device_mac}")
                            st.success(output)
                
                with col2:
                    if st.button("⬆️ Upgrade", use_container_width=True):
                        with st.spinner("Upgrading..."):
                            output = run_unifi_command(f"upgrade {device_mac}")
                            st.success(output)
                
                with col3:
                    if st.button("💡 Locate", use_container_width=True):
                        output = run_unifi_command(f"locate {device_mac}")
                        st.success(output)
                
                with col4:
                    if st.button("ℹ️ Info", use_container_width=True):
                        output = run_unifi_command(f"device {device_mac}")
                        st.code(output, language="text")
    
    with tab3:
        st.subheader("👥 Client Management")
        
        col1, col2 = st.columns(2)
        
        with col1:
            if st.button("📋 List All Clients", use_container_width=True):
                with st.spinner("Loading clients..."):
                    output = run_unifi_command("clients")
                    st.code(output, language="text")
        
        with col2:
            if st.button("📊 Client Statistics", use_container_width=True):
                st.info("View detailed client statistics in the UniFi controller dashboard")
        
        st.divider()
        
        with st.expander("🔧 Client Actions"):
            client_mac = st.text_input("Client MAC Address", placeholder="aa:bb:cc:dd:ee:ff")
            
            if client_mac:
                col1, col2, col3, col4 = st.columns(4)
                
                with col1:
                    if st.button("ℹ️ Client Info", use_container_width=True):
                        output = run_unifi_command(f"client {client_mac}")
                        st.code(output, language="text")
                
                with col2:
                    if st.button("🚫 Block", use_container_width=True):
                        output = run_unifi_command(f"block {client_mac}")
                        st.warning(output)
                
                with col3:
                    if st.button("✅ Unblock", use_container_width=True):
                        output = run_unifi_command(f"unblock {client_mac}")
                        st.success(output)
                
                with col4:
                    if st.button("🔄 Reconnect", use_container_width=True):
                        output = run_unifi_command(f"reconnect {client_mac}")
                        st.info(output)
    
    with tab4:
        st.subheader("📶 Wireless Optimization")
        
        st.write("Analyze and optimize WiFi performance across all sites.")
        
        col1, col2 = st.columns(2)
        
        with col1:
            if st.button("🚀 Run Full Network Optimization", use_container_width=True):
                with st.spinner("Analyzing wireless environment..."):
                    results = optimize_wireless("All Sites")
                    st.text_area("Optimization Results", results, height=400)
        
        with col2:
            if st.button("📊 View Network Health", use_container_width=True):
                with st.spinner("Checking..."):
                    output = run_unifi_command("health")
                    st.code(output, language="text")
        
        st.divider()
        
        col1, col2, col3 = st.columns(3)
        
        with col1:
            if st.button("📋 View WiFi Networks", use_container_width=True):
                with st.spinner("Loading..."):
                    output = run_unifi_command("wlans")
                    st.code(output, language="text")
        
        with col2:
            if st.button("📡 RF Environment", use_container_width=True):
                st.info("RF scan shows nearby networks and channel utilization. Run from UniFi controller: Settings → WiFi → RF Environment")
        
        with col3:
            if st.button("🔍 Channel Analysis", use_container_width=True):
                st.info("Check channel utilization and interference in UniFi controller")
        
        st.divider()
        st.subheader("⚙️ Quick WiFi Actions")
        
        with st.expander("🔧 WiFi Network Management"):
            wlan_id = st.text_input("WLAN ID (from 'View WiFi Networks')", placeholder="5f8b3d2e1a4c7b9e0d6f8a2c")
            
            if wlan_id:
                col1, col2, col3 = st.columns(3)
                
                with col1:
                    if st.button("🟢 Enable WLAN", use_container_width=True):
                        output = run_unifi_command(f"wlan-enable {wlan_id}")
                        st.success(output)
                
                with col2:
                    if st.button("🔴 Disable WLAN", use_container_width=True):
                        output = run_unifi_command(f"wlan-disable {wlan_id}")
                        st.warning(output)
                
                with col3:
                    new_password = st.text_input("New Password", type="password")
                    if new_password and st.button("🔑 Change Password", use_container_width=True):
                        output = run_unifi_command(f"wlan-password {wlan_id} {new_password}")
                        st.success(output)
    
    with tab5:
        tickets_tab_content()

# Tickets tab content
def tickets_tab_content():
    st.subheader("🎫 Service Tickets")
    
    # Ticket stats
    try:
        stats = get_ticket_stats()
        col1, col2, col3, col4 = st.columns(4)
        with col1:
            st.metric("🔵 Open", stats.get('open', 0))
        with col2:
            st.metric("🟡 In Progress", stats.get('in_progress', 0))
        with col3:
            st.metric("🔴 Critical", stats.get('critical', 0))
        with col4:
            st.metric("✅ Resolved Today", stats.get('resolved_today', 0))
        
        st.divider()
    except Exception as e:
        st.warning(f"Ticket stats unavailable: {e}")
    
    # Filters
    col1, col2, col3 = st.columns(3)
    with col1:
        status_filter = st.selectbox("Status", ["all", "open", "in-progress", "waiting", "resolved", "closed"])
    with col2:
        priority_filter = st.selectbox("Priority", ["all", "low", "medium", "high", "critical"])
    with col3:
        if st.button("➕ New Ticket", use_container_width=True):
            st.session_state.show_new_ticket = True
            st.rerun()
    
    # New ticket form
    if st.session_state.get('show_new_ticket'):
        with st.form("new_ticket"):
            st.subheader("📝 Create New Ticket")
            
            title = st.text_input("Title*", placeholder="Brief description of the issue")
            client = st.text_input("Client*", placeholder="Client or site name")
            
            col1, col2 = st.columns(2)
            with col1:
                priority = st.selectbox("Priority", ["low", "medium", "high", "critical"])
                site = st.text_input("Site Location", placeholder="e.g., Chicago")
            with col2:
                network = st.selectbox("Network Type", ["unifi", "meraki", "both", "other"])
                assigned = st.text_input("Assign To", placeholder="Technician name (optional)")
            
            description = st.text_area("Description", placeholder="Detailed description of the issue")
            
            col1, col2 = st.columns(2)
            with col1:
                submit = st.form_submit_button("✅ Create Ticket", use_container_width=True)
            with col2:
                cancel = st.form_submit_button("❌ Cancel", use_container_width=True)
            
            if submit and title and client:
                try:
                    ticket_id = create_ticket(
                        title=title,
                        client=client,
                        created_by=st.session_state.user_name,
                        site=site if site else None,
                        priority=priority,
                        assigned_to=assigned if assigned else None,
                        network_type=network,
                        description=description if description else None
                    )
                    st.success(f"✅ Ticket #{ticket_id} created successfully")
                    st.session_state.show_new_ticket = False
                    st.rerun()
                except Exception as e:
                    st.error(f"Error creating ticket: {e}")
            
            if cancel:
                st.session_state.show_new_ticket = False
                st.rerun()
    
    # Ticket list
    st.divider()
    
    try:
        tickets = get_tickets(
            status=None if status_filter == "all" else status_filter
        )
        
        if priority_filter != "all":
            tickets = [t for t in tickets if t['priority'] == priority_filter]
        
        if tickets:
            for ticket in tickets:
                status_emoji = {
                    "open": "🔵", 
                    "in-progress": "🟡", 
                    "waiting": "🟠",
                    "resolved": "🟢", 
                    "closed": "⚫"
                }.get(ticket['status'], "⚪")
                
                priority_emoji = {
                    "low": "⬇️", 
                    "medium": "➡️", 
                    "high": "⬆️", 
                    "critical": "🔴"
                }.get(ticket['priority'], "")
                
                with st.expander(f"{status_emoji} #{ticket['id']} - {ticket['title']} {priority_emoji}"):
                    col1, col2 = st.columns([2, 1])
                    
                    with col1:
                        st.write(f"**Client:** {ticket['client']}")
                        if ticket.get('site'):
                            st.write(f"**Site:** {ticket['site']}")
                        if ticket.get('description'):
                            st.write(f"**Description:** {ticket['description']}")
                        if ticket.get('network_type'):
                            st.write(f"**Network:** {ticket['network_type'].upper()}")
                    
                    with col2:
                        st.write(f"**Status:** {ticket['status']}")
                        st.write(f"**Priority:** {ticket['priority']}")
                        st.write(f"**Created:** {ticket['created_at']}")
                        st.write(f"**Created By:** {ticket['created_by']}")
                        st.write(f"**Assigned:** {ticket.get('assigned_to') or 'Unassigned'}")
                    
                    # Show updates if any
                    if ticket.get('updates'):
                        st.markdown("---")
                        st.write("**Updates:**")
                        for update in ticket['updates']:
                            st.text(f"{update[2]} - {update[0]}: {update[1]}")
                    
                    # Update form
                    st.markdown("---")
                    with st.form(f"update_{ticket['id']}"):
                        update_text = st.text_area("Add Update", key=f"update_text_{ticket['id']}", placeholder="Add notes, updates, or resolution details")
                        
                        col1, col2, col3 = st.columns(3)
                        with col1:
                            new_status = st.selectbox("Change Status", 
                                ["open", "in-progress", "waiting", "resolved", "closed"],
                                index=["open", "in-progress", "waiting", "resolved", "closed"].index(ticket['status']),
                                key=f"status_{ticket['id']}")
                        with col2:
                            new_assigned = st.text_input("Reassign To", 
                                value=ticket.get('assigned_to') or '',
                                key=f"assigned_{ticket['id']}")
                        with col3:
                            submit_update = st.form_submit_button("💾 Update Ticket", use_container_width=True)
                        
                        if submit_update:
                            try:
                                kwargs = {}
                                if new_status != ticket['status']:
                                    kwargs['status'] = new_status
                                if new_assigned != (ticket.get('assigned_to') or ''):
                                    kwargs['assigned_to'] = new_assigned if new_assigned else None
                                
                                update_ticket(
                                    ticket['id'],
                                    st.session_state.user_name,
                                    update_text if update_text else None,
                                    **kwargs
                                )
                                st.success("✅ Ticket updated successfully")
                                st.rerun()
                            except Exception as e:
                                st.error(f"Error updating ticket: {e}")
        else:
            st.info("📭 No tickets found matching the selected filters")
    
    except Exception as e:
        st.error(f"Error loading tickets: {e}")

# Site details page
def site_details_page(site_name):
    data = load_site_data()
    site = next((s for s in data['sites'] if s['name'] == site_name), None)
    
    if not site:
        st.error("❌ Site not found")
        if st.button("← Back to Dashboard"):
            st.session_state.current_site = None
            st.rerun()
        return
    
    # Header with logo
    col1, col2, col3 = st.columns([1, 4, 1])
    with col1:
        try:
            st.image("/home/administrator/.openclaw/workspace/projects/tech-portal/logo-black.png", width=80)
        except:
            st.markdown("# ⚓")
    with col2:
        health = get_site_health(site)
        status_emoji = {'green': '🟢', 'yellow': '🟡', 'red': '🔴'}[health]
        st.markdown(f"# {status_emoji} {site['name']}")
        
        org = site.get('organization', '')
        gateway = site.get('gateway', 'N/A')
        caption_text = f"{site['type']} Network"
        if org:
            caption_text += f" • {org}"
        caption_text += f" • Gateway: {gateway}"
        st.caption(caption_text)
    with col3:
        if st.button("← Back", use_container_width=True):
            st.session_state.current_site = None
            st.rerun()
    
    st.divider()
    
    # Site metrics
    col1, col2, col3, col4 = st.columns(4)
    with col1:
        st.metric("🖥️ Total Devices", site.get('devices', 0))
    with col2:
        st.metric("👥 Clients", site.get('clients', 'N/A'))
    with col3:
        alerts = site.get('alerts', 0)
        st.metric("⚠️ Alerts", alerts, delta=None if alerts == 0 else "⚠️")
    with col4:
        offline = site.get('offline', 0)
        st.metric("🔴 Offline", offline, delta=None if offline == 0 else "⚠️")
    
    st.divider()
    
    # WAN info
    wan_provider = site.get('wan_provider', 'N/A')
    if wan_provider != 'N/A':
        st.subheader("🌐 Internet Connection")
        col1, col2 = st.columns(2)
        with col1:
            st.write(f"**Provider:** {wan_provider}")
        with col2:
            st.write(f"**Gateway:** {site.get('gateway', 'N/A')}")
        st.divider()
    
    # Wireless Optimization for this site
    st.subheader("📶 Wireless Optimization")
    
    col1, col2 = st.columns(2)
    
    with col1:
        if st.button("🚀 Run WiFi Optimization", key=f"opt_{site_name}", use_container_width=True):
            with st.spinner("Analyzing wireless environment..."):
                results = optimize_wireless(site['name'])
                st.text_area("Optimization Results", results, height=400)
    
    with col2:
        if st.button("📡 View WiFi Networks", key=f"wlan_{site_name}", use_container_width=True):
            with st.spinner("Loading..."):
                output = run_unifi_command("wlans")
                st.code(output, language="text")
    
    st.divider()
    
    # Device & client management
    col1, col2 = st.columns(2)
    
    with col1:
        st.subheader("🖥️ Device Management")
        if st.button("📋 View All Devices", key=f"dev_{site_name}", use_container_width=True):
            with st.spinner("Loading devices..."):
                output = run_unifi_command("devices")
                st.code(output, language="text")
    
    with col2:
        st.subheader("👥 Client Management")
        if st.button("📋 View All Clients", key=f"cli_{site_name}", use_container_width=True):
            with st.spinner("Loading clients..."):
                output = run_unifi_command("clients")
                st.code(output, language="text")

# Main app logic
def main():
    if not st.session_state.authenticated:
        login_page()
    elif st.session_state.current_site:
        site_details_page(st.session_state.current_site)
    else:
        main_dashboard()

if __name__ == "__main__":
    main()
