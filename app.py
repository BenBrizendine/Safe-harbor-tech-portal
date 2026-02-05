#!/usr/bin/env python3
"""
Safe Harbor Tech Portal - Enhanced Futuristic UI
"""

import streamlit as st
import json
import os
from datetime import datetime
from ticket_system import get_tickets, get_ticket_stats, create_ticket, update_ticket

# Page config
st.set_page_config(
    page_title="Safe Harbor Tech Portal",
    page_icon="⚓",
    layout="wide",
    initial_sidebar_state="collapsed"
)

# Futuristic CSS with Safe Harbor branding
st.markdown("""
<style>
    /* Import tech fonts */
    @import url('https://fonts.googleapis.com/css2?family=Rajdhani:wght@300;400;500;600;700&family=Orbitron:wght@400;500;600;700;900&display=swap');
    
    /* Safe Harbor Brand Colors */
    :root {
        --sh-blue: #145F82;
        --sh-blue-light: #1A7AA8;
        --sh-blue-dark: #0D4059;
        --success: #00FF88;
        --warning: #FFB800;
        --danger: #FF3366;
        --bg-dark: #0A0E1A;
        --bg-darker: #050810;
        --bg-card: rgba(20, 95, 130, 0.08);
        --glass: rgba(255, 255, 255, 0.05);
        --glass-border: rgba(255, 255, 255, 0.1);
        --text-primary: #E8EAED;
        --text-secondary: #9AA0A6;
    }
    
    /* Global dark theme */
    .stApp {
        background: linear-gradient(135deg, var(--bg-darker) 0%, var(--bg-dark) 100%);
        font-family: 'Rajdhani', sans-serif;
        color: var(--text-primary);
    }
    
    /* Main content area */
    .main {
        background: transparent;
    }
    
    /* Hide Streamlit branding */
    #MainMenu {visibility: hidden;}
    footer {visibility: hidden;}
    header {visibility: hidden;}
    
    /* Status Light Bar - Streamlit Button Style Override */
    div[data-testid="column"] > div > div > button[key^="status_light_"] {
        min-height: 70px !important;
        height: auto !important;
        padding: 12px 8px !important;
        background: rgba(255, 255, 255, 0.03) !important;
        border: 1px solid var(--glass-border) !important;
        border-radius: 8px !important;
        font-size: 28px !important;
        line-height: 1.2 !important;
        white-space: pre-line !important;
        transition: all 0.3s cubic-bezier(0.4, 0, 0.2, 1) !important;
        font-family: 'Rajdhani', sans-serif !important;
    }
    
    div[data-testid="column"] > div > div > button[key^="status_light_"]:hover {
        transform: translateY(-4px) !important;
        box-shadow: 0 8px 24px rgba(20, 95, 130, 0.4) !important;
        border-color: var(--sh-blue) !important;
        background: rgba(20, 95, 130, 0.15) !important;
    }
    
    /* Pulse animation for status emojis */
    @keyframes pulse {
        0%, 100% { opacity: 1; transform: scale(1); }
        50% { opacity: 0.7; transform: scale(0.95); }
    }
    
    /* Glassmorphism cards */
    .stButton > button {
        background: var(--glass);
        backdrop-filter: blur(20px);
        color: var(--text-primary);
        border: 1px solid var(--glass-border);
        border-radius: 12px;
        padding: 24px;
        font-size: 14px;
        font-weight: 500;
        text-align: left;
        transition: all 0.3s cubic-bezier(0.4, 0, 0.2, 1);
        box-shadow: 0 4px 16px rgba(0, 0, 0, 0.2);
        width: 100%;
        font-family: 'Rajdhani', sans-serif;
    }
    
    .stButton > button:hover {
        border-color: var(--sh-blue);
        box-shadow: 0 8px 32px rgba(20, 95, 130, 0.4);
        transform: translateY(-4px);
        background: rgba(20, 95, 130, 0.15);
    }
    
    /* Headers with tech font */
    h1, h2, h3 {
        font-family: 'Orbitron', sans-serif;
        font-weight: 700;
        letter-spacing: 1px;
        background: linear-gradient(135deg, var(--sh-blue-light) 0%, var(--sh-blue) 100%);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
        background-clip: text;
    }
    
    h1 {
        font-size: 42px;
        margin-bottom: 8px;
    }
    
    /* Metric cards with glow */
    [data-testid="stMetricValue"] {
        font-family: 'Orbitron', sans-serif;
        font-size: 36px;
        font-weight: 700;
        color: var(--sh-blue-light);
        text-shadow: 0 0 20px rgba(20, 95, 130, 0.5);
    }
    
    [data-testid="stMetricLabel"] {
        font-size: 14px;
        font-weight: 600;
        color: var(--text-secondary);
        text-transform: uppercase;
        letter-spacing: 2px;
    }
    
    .stMetricDelta {
        font-family: 'Rajdhani', sans-serif;
    }
    
    /* Modern tabs */
    .stTabs [data-baseweb="tab-list"] {
        gap: 12px;
        background: transparent;
    }
    
    .stTabs [data-baseweb="tab"] {
        background: var(--glass);
        backdrop-filter: blur(20px);
        border: 1px solid var(--glass-border);
        border-radius: 10px 10px 0 0;
        padding: 14px 28px;
        font-weight: 600;
        font-family: 'Rajdhani', sans-serif;
        font-size: 16px;
        color: var(--text-secondary);
        transition: all 0.3s ease;
    }
    
    .stTabs [data-baseweb="tab"]:hover {
        background: rgba(20, 95, 130, 0.1);
        color: var(--sh-blue-light);
    }
    
    .stTabs [aria-selected="true"] {
        background: linear-gradient(135deg, var(--sh-blue) 0%, var(--sh-blue-dark) 100%) !important;
        color: white !important;
        border-color: var(--sh-blue) !important;
        box-shadow: 0 4px 20px rgba(20, 95, 130, 0.4);
    }
    
    /* Login page */
    .login-container {
        max-width: 400px;
        margin: 80px auto;
        padding: 48px;
        background: var(--glass);
        backdrop-filter: blur(30px);
        border: 1px solid var(--glass-border);
        border-radius: 20px;
        box-shadow: 0 16px 48px rgba(0, 0, 0, 0.4);
    }
    
    .login-header {
        font-family: 'Orbitron', sans-serif;
        text-align: center;
        font-size: 32px;
        font-weight: 700;
        margin-bottom: 8px;
        background: linear-gradient(135deg, var(--sh-blue-light) 0%, var(--sh-blue) 100%);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
    }
    
    .login-subheader {
        text-align: center;
        color: var(--text-secondary);
        font-size: 16px;
        margin-bottom: 32px;
        font-weight: 500;
    }
    
    /* Logo container */
    .logo-header {
        display: flex;
        align-items: center;
        gap: 20px;
        margin-bottom: 32px;
        padding: 20px;
        background: var(--glass);
        backdrop-filter: blur(20px);
        border: 1px solid var(--glass-border);
        border-radius: 12px;
        box-shadow: 0 4px 16px rgba(0, 0, 0, 0.2);
    }
    
    /* Input fields */
    .stTextInput > div > div > input,
    .stTextArea > div > div > textarea,
    .stSelectbox > div > div > div {
        background: rgba(255, 255, 255, 0.05) !important;
        border: 1px solid var(--glass-border) !important;
        border-radius: 8px !important;
        color: var(--text-primary) !important;
        font-family: 'Rajdhani', sans-serif !important;
        transition: all 0.3s ease !important;
    }
    
    .stTextInput > div > div > input:focus,
    .stTextArea > div > div > textarea:focus {
        border-color: var(--sh-blue) !important;
        box-shadow: 0 0 20px rgba(20, 95, 130, 0.3) !important;
    }
    
    /* Expander */
    .streamlit-expanderHeader {
        background: var(--glass);
        backdrop-filter: blur(20px);
        border: 1px solid var(--glass-border);
        border-radius: 10px;
        font-weight: 600;
        font-family: 'Rajdhani', sans-serif;
        color: var(--text-primary);
        transition: all 0.3s ease;
    }
    
    .streamlit-expanderHeader:hover {
        border-color: var(--sh-blue);
        box-shadow: 0 4px 16px rgba(20, 95, 130, 0.3);
    }
    
    /* Code blocks */
    .stCodeBlock {
        background: rgba(0, 0, 0, 0.4) !important;
        border: 1px solid var(--glass-border) !important;
        border-radius: 8px !important;
        font-family: 'Fira Code', monospace !important;
    }
    
    /* Divider */
    hr {
        margin: 32px 0;
        border: none;
        height: 1px;
        background: linear-gradient(90deg, transparent, var(--glass-border), transparent);
    }
    
    /* Success/Error/Info boxes */
    .stSuccess, .stError, .stWarning, .stInfo {
        background: var(--glass);
        backdrop-filter: blur(20px);
        border-radius: 10px;
        border-left-width: 4px;
    }
    
    /* Spinner */
    .stSpinner > div {
        border-top-color: var(--sh-blue) !important;
    }
    
    /* Scrollbar */
    ::-webkit-scrollbar {
        width: 10px;
        height: 10px;
    }
    
    ::-webkit-scrollbar-track {
        background: rgba(255, 255, 255, 0.02);
    }
    
    ::-webkit-scrollbar-thumb {
        background: var(--sh-blue);
        border-radius: 5px;
    }
    
    ::-webkit-scrollbar-thumb:hover {
        background: var(--sh-blue-light);
    }
    
    /* Animation for page transitions */
    @keyframes fadeIn {
        from { opacity: 0; transform: translateY(20px); }
        to { opacity: 1; transform: translateY(0); }
    }
    
    .main > div {
        animation: fadeIn 0.5s ease-out;
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

# Load combined site data
def load_site_data():
    """Load site data with error handling"""
    try:
        with open('/home/administrator/.openclaw/workspace/projects/tech-portal/combined_sites.json', 'r') as f:
            data = json.load(f)
            # Ensure all required fields exist
            if 'sites' not in data:
                data['sites'] = []
            if 'summary' not in data:
                data['summary'] = {
                    'total_devices': 0,
                    'total_clients': 0,
                    'offline_devices': 0,
                    'critical_alerts': 0
                }
            if 'total_sites' not in data:
                data['total_sites'] = len(data.get('sites', []))
            return data
    except FileNotFoundError:
        st.error("⚠️ Site data not found. Please run refresh_sites.py")
        return {"sites": [], "summary": {}, "total_sites": 0}
    except json.JSONDecodeError:
        st.error("⚠️ Invalid site data format")
        return {"sites": [], "summary": {}, "total_sites": 0}

# UniFi Cloud API integration
try:
    from unifi_cloud import execute_command as run_unifi_cloud_command
    UNIFI_CLOUD_AVAILABLE = True
except ImportError:
    UNIFI_CLOUD_AVAILABLE = False

def run_unifi_command(cmd):
    """Execute UniFi command via Cloud API"""
    if not UNIFI_CLOUD_AVAILABLE:
        return "⚠️ UniFi Cloud API module not available. Please ensure unifi_cloud.py is in the project directory."
    
    try:
        return run_unifi_cloud_command(cmd)
    except Exception as e:
        return f"⚠️ Error executing UniFi command: {str(e)}"

# Status light bar component
def render_status_bar(sites):
    """Render futuristic status light bar with clickable status indicators"""
    if not sites:
        return
    
    # Create columns for status lights (max 10 per row for readability)
    sites_per_row = min(len(sites), 10)
    
    # Render sites in rows of 10
    for row_start in range(0, len(sites), sites_per_row):
        row_sites = sites[row_start:row_start + sites_per_row]
        cols = st.columns(len(row_sites))
        
        for idx, (col, site) in enumerate(zip(cols, row_sites)):
            with col:
                site_name = site.get('name', 'Unknown')
                offline = site.get('offline', 0)
                alerts = site.get('alerts', 0)
                devices = site.get('devices', 0)
                
                # Determine status emoji
                if offline > 0 or alerts > 0:
                    status_emoji = '🔴'
                    status_text = 'Critical'
                elif devices == 0:
                    status_emoji = '🟡'
                    status_text = 'Warning'
                else:
                    status_emoji = '🟢'
                    status_text = 'Online'
                
                # Truncate long names for display
                display_name = site_name[:10] + '...' if len(site_name) > 10 else site_name
                
                # Create clickable status button
                button_label = f"{status_emoji}\n{display_name}"
                
                if st.button(
                    button_label,
                    key=f"status_light_{row_start + idx}",
                    help=f"{site_name} - {status_text}",
                    use_container_width=True
                ):
                    st.session_state.current_site = site_name
                    st.rerun()

# Login page
def login_page():
    """Enhanced login page with Safe Harbor branding"""
    # Center the login form
    col1, col2, col3 = st.columns([1, 1.5, 1])
    
    with col2:
        # Logo
        try:
            st.image("/home/administrator/.openclaw/workspace/projects/tech-portal/logo-black.png", width=250)
        except:
            st.markdown('<p class="login-header">⚓ SAFE HARBOR</p>', unsafe_allow_html=True)
        
        st.markdown('<p class="login-subheader">TECH PORTAL</p>', unsafe_allow_html=True)
        st.markdown("---")
        
        # Login form
        with st.form("login_form"):
            username = st.text_input("Username", placeholder="Enter username").lower()
            password = st.text_input("Password", type="password", placeholder="Enter password")
            
            submit = st.form_submit_button("🔐 LOGIN", use_container_width=True)
            
            if submit:
                if username in VALID_USERS and VALID_USERS[username]["password"] == password:
                    st.session_state.authenticated = True
                    st.session_state.username = username
                    st.session_state.user_name = VALID_USERS[username]["name"]
                    st.rerun()
                else:
                    st.error("❌ Invalid credentials")

# Site card component
def site_card(site):
    """Render site card with proper error handling"""
    try:
        site_name = site.get('name', 'Unknown Site')
        site_type = site.get('type', 'Unknown')
        devices = site.get('devices', 0)
        clients = site.get('clients', '?')
        offline = site.get('offline', 0)
        alerts = site.get('alerts', 0)
        gateway = site.get('gateway', 'N/A')
        org = site.get('organization', '')
        
        # Status indicator
        status_emoji = "🟢" if offline == 0 else "🔴"
        alert_badge = f" ⚠️ {alerts}" if alerts > 0 else ""
        
        # Build label
        label = f"{site_type}"
        if org:
            label += f" | {org}"
        
        # Display clients safely
        client_display = str(clients) if clients is not None else "?"
        
        button_text = f"""{status_emoji} **{site_name}**

🏢 {label}
🖥️ {devices} devices • 👥 {client_display} clients{alert_badge}"""
        
        if st.button(button_text, key=f"site_{site_name.replace(' ', '_').replace('/', '_')}", use_container_width=True):
            st.session_state.current_site = site_name
            st.rerun()
    except Exception as e:
        st.error(f"Error rendering site card: {str(e)}")

# Main dashboard
def main_dashboard():
    """Main dashboard with status bar and site cards"""
    # Load data
    data = load_site_data()
    sites = data.get('sites', [])
    summary = data.get('summary', {})
    total_sites = data.get('total_sites', len(sites))
    
    # Header with logo
    col1, col2, col3 = st.columns([1, 4, 1])
    with col1:
        try:
            st.image("/home/administrator/.openclaw/workspace/projects/tech-portal/logo-black.png", width=100)
        except:
            st.markdown("# ⚓")
    with col2:
        st.markdown("# SAFE HARBOR TECH PORTAL")
        st.caption("🌐 Network Command Center")
    with col3:
        st.write(f"**{st.session_state.user_name}**")
        if st.button("🚪 Logout", use_container_width=True):
            st.session_state.authenticated = False
            st.session_state.username = None
            st.session_state.current_site = None
            st.rerun()
    
    st.markdown("---")
    
    # Status Light Bar
    st.markdown("### 🔆 SITE STATUS OVERVIEW")
    render_status_bar(sites)
    
    st.markdown("---")
    
    # Summary metrics
    col1, col2, col3, col4 = st.columns(4)
    with col1:
        st.metric("🏢 Sites", total_sites)
    with col2:
        total_devices = summary.get('total_devices', 0)
        st.metric("🖥️ Devices", total_devices)
    with col3:
        total_clients = summary.get('total_clients', 0)
        st.metric("👥 Clients", total_clients)
    with col4:
        offline = summary.get('offline_devices', 0)
        st.metric("⚠️ Offline", offline, delta=None if offline == 0 else "Alert")
    
    st.divider()
    
    # Tabs for different sections
    tab1, tab2, tab3, tab4, tab5 = st.tabs(["📡 SITES", "🖥️ DEVICES", "👥 CLIENTS", "📶 WIRELESS", "🎫 TICKETS"])
    
    with tab1:
        sites_tab_content(sites)
    
    with tab2:
        devices_tab_content()
    
    with tab3:
        clients_tab_content()
    
    with tab4:
        wireless_tab_content()
    
    with tab5:
        tickets_tab_content()

# Sites tab
def sites_tab_content(sites):
    """Sites tab with improved layout"""
    st.subheader("📡 Network Sites")
    
    if not sites:
        st.warning("⚠️ No sites available. Please run refresh_sites.py")
        return
    
    # Filter options
    col1, col2 = st.columns([2, 1])
    with col1:
        search = st.text_input("🔍 Search sites", placeholder="Type to filter...")
    with col2:
        site_type_filter = st.selectbox("Filter by type", ["All", "UniFi", "Meraki"])
    
    # Filter sites
    filtered_sites = sites
    if search:
        filtered_sites = [s for s in filtered_sites if search.lower() in s.get('name', '').lower()]
    if site_type_filter != "All":
        filtered_sites = [s for s in filtered_sites if s.get('type', '') == site_type_filter]
    
    st.write(f"**Showing {len(filtered_sites)} of {len(sites)} sites**")
    
    # Display sites in grid
    for i in range(0, len(filtered_sites), 3):
        cols = st.columns(3)
        for j, col in enumerate(cols):
            if i + j < len(filtered_sites):
                with col:
                    site_card(filtered_sites[i + j])

# Devices tab
def devices_tab_content():
    """Devices management tab"""
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
    
    # Device actions
    with st.expander("🔧 Device Actions", expanded=False):
        device_mac = st.text_input("Device MAC Address", placeholder="00:00:00:00:00:00")
        
        if device_mac:
            st.write("**Available Actions:**")
            col1, col2, col3, col4 = st.columns(4)
            
            with col1:
                if st.button("🔄 Restart", use_container_width=True):
                    with st.spinner("Restarting device..."):
                        output = run_unifi_command(f"restart {device_mac}")
                        st.success(output)
            
            with col2:
                if st.button("⬆️ Upgrade", use_container_width=True):
                    with st.spinner("Upgrading firmware..."):
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

# Clients tab
def clients_tab_content():
    """Client management tab"""
    st.subheader("👥 Client Management")
    
    col1, col2 = st.columns(2)
    
    with col1:
        if st.button("📋 List All Clients", use_container_width=True):
            with st.spinner("Loading clients..."):
                output = run_unifi_command("clients")
                st.code(output, language="text")
    
    with col2:
        if st.button("📊 Client Statistics", use_container_width=True):
            st.info("Use 'List All Clients' to view connected devices")
    
    st.divider()
    
    # Client actions
    with st.expander("🔧 Client Actions", expanded=False):
        client_mac = st.text_input("Client MAC Address", placeholder="aa:bb:cc:dd:ee:ff")
        
        if client_mac:
            st.write("**Available Actions:**")
            col1, col2, col3, col4 = st.columns(4)
            
            with col1:
                if st.button("ℹ️ Info", use_container_width=True):
                    output = run_unifi_command(f"client {client_mac}")
                    st.code(output, language="text")
            
            with col2:
                if st.button("🚫 Block", use_container_width=True):
                    if st.session_state.get('confirm_block'):
                        output = run_unifi_command(f"block {client_mac}")
                        st.warning(output)
                        st.session_state.confirm_block = False
                    else:
                        st.session_state.confirm_block = True
                        st.warning("⚠️ Click again to confirm block")
            
            with col3:
                if st.button("✅ Unblock", use_container_width=True):
                    output = run_unifi_command(f"unblock {client_mac}")
                    st.success(output)
            
            with col4:
                if st.button("🔄 Reconnect", use_container_width=True):
                    output = run_unifi_command(f"reconnect {client_mac}")
                    st.info(output)

# Wireless tab
def wireless_tab_content():
    """Wireless optimization tab"""
    st.subheader("📶 Wireless Optimization")
    
    st.write("Analyze and optimize WiFi performance across all network sites.")
    
    col1, col2, col3 = st.columns(3)
    
    with col1:
        if st.button("📋 View WiFi Networks", use_container_width=True):
            with st.spinner("Loading WiFi networks..."):
                output = run_unifi_command("wlans")
                st.code(output, language="text")
    
    with col2:
        if st.button("🔍 Network Health", use_container_width=True):
            with st.spinner("Checking network health..."):
                output = run_unifi_command("health")
                st.code(output, language="text")
    
    with col3:
        if st.button("🚀 Optimization Tips", use_container_width=True):
            st.info("""
**WiFi Optimization Best Practices:**
✓ Use Auto channel selection
✓ Set transmit power to Auto/Medium  
✓ Enable band steering (prefer 5GHz)
✓ Disable 802.11b for modern networks
✓ Enable Fast Roaming (802.11r)
✓ Set minimum data rate to 12Mbps
            """)
    
    st.divider()
    
    # WiFi network management
    with st.expander("🔧 WiFi Network Management", expanded=False):
        wlan_id = st.text_input("WLAN ID", placeholder="Get from 'View WiFi Networks'")
        
        if wlan_id:
            st.write("**Available Actions:**")
            col1, col2, col3 = st.columns(3)
            
            with col1:
                if st.button("🟢 Enable", use_container_width=True):
                    output = run_unifi_command(f"wlan-enable {wlan_id}")
                    st.success(output)
            
            with col2:
                if st.button("🔴 Disable", use_container_width=True):
                    output = run_unifi_command(f"wlan-disable {wlan_id}")
                    st.warning(output)
            
            with col3:
                new_password = st.text_input("New Password", type="password", key="wlan_pwd")
                if new_password and st.button("🔑 Update Password", use_container_width=True):
                    output = run_unifi_command(f"wlan-password {wlan_id} {new_password}")
                    st.success(output)

# Tickets tab
def tickets_tab_content():
    """Service tickets management"""
    st.subheader("🎫 Service Tickets")
    
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
        with st.form("new_ticket", clear_on_submit=True):
            st.subheader("Create New Ticket")
            
            title = st.text_input("Title*", placeholder="Brief description of the issue")
            client = st.text_input("Client*", placeholder="Client name")
            
            col1, col2 = st.columns(2)
            with col1:
                priority = st.selectbox("Priority", ["low", "medium", "high", "critical"])
                site = st.text_input("Site Location", placeholder="Optional")
            with col2:
                network = st.selectbox("Network Type", ["unifi", "meraki", "both", "other"])
                assigned = st.text_input("Assign To", placeholder="Optional")
            
            description = st.text_area("Description", placeholder="Detailed information about the issue...")
            
            col1, col2 = st.columns(2)
            with col1:
                submit = st.form_submit_button("✅ Create Ticket", use_container_width=True)
            with col2:
                cancel = st.form_submit_button("❌ Cancel", use_container_width=True)
            
            if submit:
                if not title or not client:
                    st.error("⚠️ Title and Client are required")
                else:
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
                        st.error(f"⚠️ Error creating ticket: {str(e)}")
            
            if cancel:
                st.session_state.show_new_ticket = False
                st.rerun()
    
    st.divider()
    
    # Ticket list
    try:
        tickets = get_tickets(status=None if status_filter == "all" else status_filter)
        
        if priority_filter != "all":
            tickets = [t for t in tickets if t.get('priority') == priority_filter]
        
        if tickets:
            st.write(f"**{len(tickets)} ticket(s) found**")
            
            for ticket in tickets:
                status_emoji = {
                    "open": "🔵",
                    "in-progress": "🟡",
                    "waiting": "🟠",
                    "resolved": "🟢",
                    "closed": "⚫"
                }.get(ticket.get('status', 'open'), "⚪")
                
                priority_emoji = {
                    "low": "⬇️",
                    "medium": "➡️",
                    "high": "⬆️",
                    "critical": "🔴"
                }.get(ticket.get('priority', 'medium'), "")
                
                ticket_title = f"{status_emoji} #{ticket.get('id')} - {ticket.get('title', 'Untitled')} {priority_emoji}"
                
                with st.expander(ticket_title):
                    col1, col2 = st.columns([2, 1])
                    
                    with col1:
                        st.write(f"**Client:** {ticket.get('client', 'N/A')}")
                        if ticket.get('site'):
                            st.write(f"**Site:** {ticket['site']}")
                        if ticket.get('description'):
                            st.write(f"**Description:** {ticket['description']}")
                        if ticket.get('network_type'):
                            st.write(f"**Network:** {ticket['network_type'].upper()}")
                    
                    with col2:
                        st.write(f"**Status:** {ticket.get('status', 'N/A')}")
                        st.write(f"**Priority:** {ticket.get('priority', 'N/A')}")
                        st.write(f"**Created:** {ticket.get('created_at', 'N/A')}")
                        st.write(f"**Created By:** {ticket.get('created_by', 'N/A')}")
                        st.write(f"**Assigned:** {ticket.get('assigned_to') or 'Unassigned'}")
                    
                    # Updates history
                    if ticket.get('updates'):
                        st.write("---")
                        st.write("**Updates:**")
                        for update in ticket['updates']:
                            st.write(f"• {update[1]} - *{update[0]}* ({update[2]})")
                    
                    # Update form
                    st.write("---")
                    with st.form(f"update_{ticket['id']}"):
                        update_text = st.text_area("Add Update", key=f"update_text_{ticket['id']}", placeholder="Enter update notes...")
                        
                        col1, col2, col3 = st.columns(3)
                        with col1:
                            new_status = st.selectbox(
                                "Change Status",
                                ["open", "in-progress", "waiting", "resolved", "closed"],
                                index=["open", "in-progress", "waiting", "resolved", "closed"].index(ticket.get('status', 'open')),
                                key=f"status_{ticket['id']}"
                            )
                        with col2:
                            new_assigned = st.text_input(
                                "Reassign",
                                value=ticket.get('assigned_to', ''),
                                key=f"assign_{ticket['id']}",
                                placeholder="Technician name"
                            )
                        with col3:
                            submit_update = st.form_submit_button("💾 Update", use_container_width=True)
                        
                        if submit_update:
                            if not update_text:
                                st.warning("⚠️ Please enter update notes")
                            else:
                                try:
                                    kwargs = {'status': new_status}
                                    if new_assigned:
                                        kwargs['assigned_to'] = new_assigned
                                    
                                    update_ticket(ticket['id'], st.session_state.user_name, update_text, **kwargs)
                                    st.success("✅ Ticket updated")
                                    st.rerun()
                                except Exception as e:
                                    st.error(f"⚠️ Error updating ticket: {str(e)}")
        else:
            st.info("📭 No tickets found matching the selected filters")
    
    except Exception as e:
        st.error(f"⚠️ Error loading tickets: {str(e)}")
        st.info("Make sure the ticket database is initialized. Run: python3 ticket_system.py init")

# Site details page
def site_details_page(site_name):
    """Detailed view of a specific site"""
    data = load_site_data()
    site = next((s for s in data.get('sites', []) if s.get('name') == site_name), None)
    
    if not site:
        st.error("⚠️ Site not found")
        if st.button("← Back to Dashboard", use_container_width=True):
            st.session_state.current_site = None
            st.rerun()
        return
    
    # Header
    col1, col2, col3 = st.columns([1, 4, 1])
    with col1:
        try:
            st.image("/home/administrator/.openclaw/workspace/projects/tech-portal/logo-black.png", width=80)
        except:
            st.markdown("# ⚓")
    with col2:
        st.markdown(f"# 📍 {site.get('name', 'Unknown')}")
        site_type = site.get('type', 'Unknown')
        gateway = site.get('gateway', 'N/A')
        org = site.get('organization', '')
        caption = f"{site_type} • {gateway}"
        if org:
            caption += f" • {org}"
        st.caption(caption)
    with col3:
        if st.button("← Back", use_container_width=True):
            st.session_state.current_site = None
            st.rerun()
    
    st.divider()
    
    # Site metrics
    col1, col2, col3, col4 = st.columns(4)
    with col1:
        devices = site.get('devices', 0)
        st.metric("🖥️ Devices", devices)
    with col2:
        clients = site.get('clients')
        client_display = str(clients) if clients is not None else "N/A"
        st.metric("👥 Clients", client_display)
    with col3:
        offline = site.get('offline', 0)
        st.metric("⚠️ Offline", offline, delta=None if offline == 0 else "Alert")
    with col4:
        alerts = site.get('alerts', 0)
        st.metric("🚨 Alerts", alerts, delta=None if alerts == 0 else "Action Needed")
    
    st.divider()
    
    # WAN/Internet info
    if site.get('wan_provider') and site['wan_provider'] != 'N/A':
        st.subheader("🌐 Internet Connection")
        col1, col2 = st.columns(2)
        with col1:
            st.write(f"**Provider:** {site['wan_provider']}")
        with col2:
            st.write(f"**Gateway:** {site.get('gateway', 'N/A')}")
        st.divider()
    
    # Actions
    st.subheader("⚡ Quick Actions")
    
    col1, col2, col3 = st.columns(3)
    
    with col1:
        if st.button("🖥️ View Devices", use_container_width=True):
            with st.spinner("Loading devices..."):
                output = run_unifi_command("devices")
                st.code(output, language="text")
    
    with col2:
        if st.button("👥 View Clients", use_container_width=True):
            with st.spinner("Loading clients..."):
                output = run_unifi_command("clients")
                st.code(output, language="text")
    
    with col3:
        if st.button("📶 WiFi Networks", use_container_width=True):
            with st.spinner("Loading WiFi..."):
                output = run_unifi_command("wlans")
                st.code(output, language="text")

# Main app logic
def main():
    """Main application entry point"""
    if not st.session_state.authenticated:
        login_page()
    elif st.session_state.current_site:
        site_details_page(st.session_state.current_site)
    else:
        main_dashboard()

if __name__ == "__main__":
    main()
