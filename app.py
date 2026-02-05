#!/usr/bin/env python3
"""
Safe Harbor Tech Portal - Enhanced Futuristic UI with Email/Password Auth
"""

import streamlit as st
import json
import os
import subprocess
import hashlib
from datetime import datetime
from ticket_system import get_tickets, get_ticket_stats, create_ticket, update_ticket

# Page config
st.set_page_config(
    page_title="Safe Harbor Tech Portal",
    page_icon="⚓",
    layout="wide",
    initial_sidebar_state="collapsed"
)

# User credentials (email: hashed_password)
USERS = {
    "john.wong@safeharborsolutionsllc.com": {
        "password": hashlib.sha256("SafeHarbor2026!John".encode()).hexdigest(),
        "name": "John Wong"
    },
    "ben.brizendine@safeharborsolutionsllc.com": {
        "password": hashlib.sha256("SafeHarbor2026!Ben".encode()).hexdigest(),
        "name": "Ben Brizendine"
    },
    "caleb.davis@safeharborsolutionsllc.com": {
        "password": hashlib.sha256("SafeHarbor2026!Caleb".encode()).hexdigest(),
        "name": "Caleb Davis"
    },
    "craig.arnold@safeharborsolutionsllc.com": {
        "password": hashlib.sha256("SafeHarbor2026!Craig".encode()).hexdigest(),
        "name": "Craig Arnold"
    }
}

# Site-level access password (first layer of security)
SITE_PASSWORD = "SafeHarbor2026Access"

def check_site_password():
    """Site-level password protection"""
    if 'site_authenticated' not in st.session_state:
        st.session_state.site_authenticated = False
    
    if not st.session_state.site_authenticated:
        st.markdown("""
            <div style='text-align: center; padding: 50px;'>
                <img src='data:image/png;base64,{}' width='150'>
                <h1 style='color: #145F82; margin-top: 20px;'>Safe Harbor Tech Portal</h1>
                <p style='color: #666;'>Enter site access code to continue</p>
            </div>
        """.format(get_logo_base64()), unsafe_allow_html=True)
        
        password = st.text_input("Access Code", type="password", key="site_pw")
        
        if st.button("Access Portal"):
            if password == SITE_PASSWORD:
                st.session_state.site_authenticated = True
                st.rerun()
            else:
                st.error("❌ Invalid access code")
        
        st.stop()

def hash_password(password):
    """Hash password with SHA-256"""
    return hashlib.sha256(password.encode()).hexdigest()

def check_credentials(email, password):
    """Verify email and password"""
    if email in USERS:
        hashed = hash_password(password)
        if hashed == USERS[email]["password"]:
            return True, USERS[email]["name"]
    return False, None

def login_page():
    """Login page with email/password"""
    st.markdown("""
        <style>
            .login-container {
                max-width: 400px;
                margin: 100px auto;
                padding: 40px;
                background: rgba(255, 255, 255, 0.95);
                border-radius: 12px;
                box-shadow: 0 8px 32px rgba(0,0,0,0.1);
            }
        </style>
    """, unsafe_allow_html=True)
    
    col1, col2, col3 = st.columns([1, 2, 1])
    
    with col2:
        st.markdown("<div class='login-container'>", unsafe_allow_html=True)
        
        # Logo
        try:
            st.image("logo-black.png", width=200)
        except:
            st.markdown("### Safe Harbor Tech Portal")
        
        st.markdown("#### Network Command Center")
        st.markdown("---")
        
        # Login form
        email = st.text_input("Email Address", placeholder="your.name@safeharborsolutionsllc.com")
        password = st.text_input("Password", type="password")
        
        if st.button("🔐 Login", use_container_width=True):
            valid, name = check_credentials(email, password)
            if valid:
                st.session_state.authenticated = True
                st.session_state.user_email = email
                st.session_state.user_name = name
                st.success(f"✅ Welcome, {name}!")
                st.rerun()
            else:
                st.error("❌ Invalid email or password")
        
        st.markdown("</div>", unsafe_allow_html=True)
        
        # Help text
        st.markdown("""
            <div style='text-align: center; margin-top: 20px; color: #666; font-size: 12px;'>
                Need access? Contact your administrator.
            </div>
        """, unsafe_allow_html=True)

def get_logo_base64():
    """Get logo as base64 for embedding"""
    try:
        import base64
        with open("logo-black.png", "rb") as f:
            return base64.b64encode(f.read()).decode()
    except:
        return ""

# Initialize session state
if 'authenticated' not in st.session_state:
    st.session_state.authenticated = False
if 'site_authenticated' not in st.session_state:
    st.session_state.site_authenticated = False

# Check site password first
check_site_password()

# Check authentication
if not st.session_state.authenticated:
    login_page()
    st.stop()

# Rest of your existing app code below (all the Streamlit UI components)
# [Keep all the existing code from line ~200 onwards - the CSS, functions, main app logic, etc.]

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
    
    /* Header styling */
    h1, h2, h3 {
        font-family: 'Orbitron', sans-serif;
        color: var(--sh-blue-light);
        text-shadow: 0 0 20px rgba(26, 122, 168, 0.3);
    }
    
    /* Status button styling */
    .stButton button {
        background: var(--glass);
        border: 1px solid var(--glass-border);
        color: var(--text-primary);
        border-radius: 8px;
        padding: 8px 16px;
        font-family: 'Rajdhani', sans-serif;
        font-weight: 600;
        transition: all 0.3s ease;
        backdrop-filter: blur(10px);
    }
    
    .stButton button:hover {
        transform: translateY(-2px);
        box-shadow: 0 4px 12px rgba(26, 122, 168, 0.3);
        border-color: var(--sh-blue);
    }
    
    /* Card styling */
    .element-container {
        background: var(--glass);
        border: 1px solid var(--glass-border);
        border-radius: 12px;
        padding: 20px;
        backdrop-filter: blur(10px);
        margin: 10px 0;
    }
    
    /* Metric styling */
    [data-testid="stMetricValue"] {
        font-size: 2.5em;
        font-weight: 700;
        font-family: 'Orbitron', sans-serif;
        color: var(--sh-blue-light);
        text-shadow: 0 0 20px rgba(26, 122, 168, 0.5);
    }
    
    /* Status light animation */
    @keyframes pulse {
        0%, 100% { opacity: 1; }
        50% { opacity: 0.7; }
    }
    
    .status-indicator {
        display: inline-block;
        width: 12px;
        height: 12px;
        border-radius: 50%;
        margin-right: 8px;
        animation: pulse 2s infinite;
    }
    
    .status-online { background: var(--success); }
    .status-warning { background: var(--warning); }
    .status-offline { background: var(--danger); }
</style>
""", unsafe_allow_html=True)

# Header with logout
col_logo, col_title, col_user = st.columns([1, 3, 1])

with col_logo:
    try:
        st.image("logo-black.png", width=100)
    except:
        st.markdown("### ⚓")

with col_title:
    st.markdown("""
        <h1 style='margin: 0; padding: 0;'>SAFE HARBOR TECH PORTAL</h1>
        <p style='margin: 0; color: var(--sh-blue); font-size: 0.9em;'>🌐 Network Command Center</p>
    """, unsafe_allow_html=True)

with col_user:
    st.markdown(f"**{st.session_state.user_name}**")
    if st.button("🚪 Logout"):
        st.session_state.authenticated = False
        st.session_state.site_authenticated = False
        st.rerun()

st.markdown("---")

# Load site data
def load_site_data():
    """Load combined site data from JSON"""
    try:
        with open('combined_sites.json', 'r') as f:
            return json.load(f)
    except:
        return {
            'unifi_sites': 0,
            'meraki_sites': 0,
            'total_sites': 0,
            'sites': [],
            'total_devices': 0,
            'total_clients': 0,
            'offline_devices': 0
        }

data = load_site_data()

# Dashboard metrics
col1, col2, col3, col4 = st.columns(4)

with col1:
    st.metric("📍 SITES", data['total_sites'])

with col2:
    st.metric("🖥️ DEVICES", data['total_devices'])

with col3:
    st.metric("👥 CLIENTS", data['total_clients'])

with col4:
    status_color = "🟢" if data['offline_devices'] == 0 else "🔴"
    st.metric(f"⚠️ OFFLINE", data['offline_devices'])
    if data['offline_devices'] > 0:
        st.markdown(f"<p style='color: var(--danger); font-size: 0.8em;'>🚨 Alert</p>", unsafe_allow_html=True)

st.markdown("---")

# Status light bar
st.markdown("### 🔆 SITE STATUS OVERVIEW")

# Create status buttons
status_cols = st.columns(min(len(data['sites']), 8))

for idx, site in enumerate(data['sites'][:8]):
    with status_cols[idx]:
        status = site.get('status', 'online')
        offline = site.get('offline_devices', 0)
        
        if offline > 0 or status == 'offline':
            emoji = "🔴"
        elif status == 'warning':
            emoji = "🟡"
        else:
            emoji = "🟢"
        
        # Truncate long site names
        short_name = site['name'][:8] + "..." if len(site['name']) > 8 else site['name']
        
        if st.button(f"{emoji} {short_name}", key=f"site_{idx}", help=f"{site['name']} - {site['type']}"):
            st.info(f"**{site['name']}**\n\nType: {site['type']}\nDevices: {site.get('devices', 0)}\nClients: {site.get('clients', '?')}")

# Show more if there are additional sites
if len(data['sites']) > 8:
    with st.expander(f"➕ Show {len(data['sites']) - 8} more sites"):
        more_cols = st.columns(min(len(data['sites']) - 8, 8))
        for idx, site in enumerate(data['sites'][8:]):
            col_idx = idx % 8
            with more_cols[col_idx]:
                status = site.get('status', 'online')
                offline = site.get('offline_devices', 0)
                
                if offline > 0 or status == 'offline':
                    emoji = "🔴"
                elif status == 'warning':
                    emoji = "🟡"
                else:
                    emoji = "🟢"
                
                short_name = site['name'][:8] + "..." if len(site['name']) > 8 else site['name']
                
                if st.button(f"{emoji} {short_name}", key=f"site_more_{idx}", help=f"{site['name']} - {site['type']}"):
                    st.info(f"**{site['name']}**\n\nType: {site['type']}\nDevices: {site.get('devices', 0)}\nClients: {site.get('clients', '?')}")

st.markdown("---")

# Main navigation tabs
tab1, tab2, tab3, tab4, tab5 = st.tabs(["🏢 SITES", "🖥️ DEVICES", "👥 CLIENTS", "📡 WIRELESS", "🎫 TICKETS"])

with tab1:
    st.subheader("🏢 Network Sites")
    
    # Search and filter
    search = st.text_input("🔍 Search sites", placeholder="Type to filter...")
    filter_type = st.selectbox("Filter by type", ["All", "UniFi", "Meraki"])
    
    # Filter sites
    filtered_sites = data['sites']
    
    if search:
        filtered_sites = [s for s in filtered_sites if search.lower() in s['name'].lower()]
    
    if filter_type != "All":
        filtered_sites = [s for s in filtered_sites if s['type'].lower() == filter_type.lower()]
    
    st.markdown(f"Showing **{len(filtered_sites)}** of **{len(data['sites'])}** sites")
    
    # Display sites in cards
    for site in filtered_sites:
        with st.container():
            col_status, col_name, col_stats, col_actions = st.columns([1, 3, 3, 2])
            
            with col_status:
                status = site.get('status', 'online')
                offline = site.get('offline_devices', 0)
                if offline > 0 or status == 'offline':
                    st.markdown("🔴")
                elif status == 'warning':
                    st.markdown("🟡")
                else:
                    st.markdown("🟢")
            
            with col_name:
                st.markdown(f"**{site['name']}**")
                st.caption(f"🏢 {site['type'].upper()}")
            
            with col_stats:
                st.caption(f"🖥️ {site.get('devices', 0)} devices • 👥 {site.get('clients', '?')} clients")
            
            with col_actions:
                if st.button("View Details", key=f"view_{site['name']}"):
                    st.info("Detail view coming soon")

with tab2:
    st.subheader("🖥️ Device Management")
    st.info("ℹ️ **UniFi Cloud API** provides read-only monitoring. For device control (restart, upgrade), visit unifi.ui.com")
    
    if st.button("📊 Refresh Device Status"):
        st.success("✅ Device status refreshed")

with tab3:
    st.subheader("👥 Client Management")
    st.info("ℹ️ Client management features available for UniFi sites via unifi.ui.com")

with tab4:
    st.subheader("📡 Wireless Optimization")
    st.info("ℹ️ Wireless optimization available for UniFi networks via local controller or unifi.ui.com")

with tab5:
    st.subheader("🎫 Service Tickets")
    
    # Ticket stats
    stats = get_ticket_stats()
    
    col_open, col_progress, col_closed = st.columns(3)
    with col_open:
        st.metric("Open", stats['open'])
    with col_progress:
        st.metric("In Progress", stats['in_progress'])
    with col_closed:
        st.metric("Closed", stats['closed'])
    
    # Create new ticket
    with st.expander("➕ Create New Ticket"):
        with st.form("new_ticket"):
            title = st.text_input("Title")
            description = st.text_area("Description")
            priority = st.selectbox("Priority", ["Low", "Medium", "High", "Critical"])
            assigned = st.selectbox("Assign to", ["Unassigned", "John Wong", "Ben Brizendine", "Caleb Davis", "Craig Arnold"])
            
            if st.form_submit_button("Create Ticket"):
                if title and description:
                    create_ticket(
                        title=title,
                        description=description,
                        priority=priority,
                        assigned_to=assigned if assigned != "Unassigned" else None,
                        created_by=st.session_state.user_name
                    )
                    st.success("✅ Ticket created!")
                    st.rerun()
                else:
                    st.error("Title and description are required")
    
    # Display tickets
    tickets = get_tickets()
    
    for ticket in tickets:
        status_emoji = {
            'open': '🔵',
            'in_progress': '🟡',
            'closed': '🟢'
        }.get(ticket[5], '⚪')
        
        with st.expander(f"{status_emoji} #{ticket[0]} - {ticket[1]} ({ticket[4]})"):
            st.markdown(f"**Description:** {ticket[2]}")
            st.caption(f"Created by {ticket[8]} on {ticket[6]}")
            
            if ticket[7]:
                st.caption(f"Assigned to: {ticket[7]}")
            
            # Update ticket
            new_status = st.selectbox("Status", ["open", "in_progress", "closed"], 
                                     index=["open", "in_progress", "closed"].index(ticket[5]),
                                     key=f"status_{ticket[0]}")
            
            if st.button("Update", key=f"update_{ticket[0]}"):
                update_ticket(ticket[0], status=new_status)
                st.success("Ticket updated!")
                st.rerun()
