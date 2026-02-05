# Safe Harbor Tech Portal - Quick Start Guide

## 🚀 Access the Portal

### URLs
- **Local**: http://localhost:8501
- **Network**: http://172.30.40.248:8501
- **External**: http://204.57.128.22:8501

### Login Credentials
```
john     / john123     (John Wong)
ben      / ben123      (Ben Brizendine)
caleb    / caleb123    (Caleb Galloway)
craig    / craig123    (Craig Murrell)
```

---

## 🎯 First-Time Tour

### 1. Login Page
- Enter username (lowercase)
- Enter password
- Click "🔐 Login"

### 2. Main Dashboard
**Status Light Bar** (Top of page)
- 🟢 Green lights = Healthy sites
- 🟡 Yellow lights = Warning sites  
- 🔴 Red lights = Critical sites (pulsing animation)
- **Click any light** to go to that site

**Summary Metrics** (Below status bar)
- Total sites count
- Total devices
- Total clients
- Offline devices

**Tabs** (Navigation)
- 📡 Sites - Browse all locations
- 🖥️ Devices - Manage hardware
- 👥 Clients - User management
- 📶 Wireless - WiFi optimization
- 🎫 Tickets - Support system

---

## 🏢 Working with Sites

### View All Sites
1. Stay on **Sites** tab (default view)
2. Scroll through site cards (20+ sites)
3. Use **search bar** to filter by name

### Site Card Information
Each card shows:
- Status indicator (🟢🟡🔴)
- Site name
- Type (UniFi/Meraki)
- Organization (if applicable)
- Device count
- Client count
- Alert badge (if any)

### Navigate to Site
**Method 1:** Click status light in top bar  
**Method 2:** Click site card button  

### Site Detail Page
Shows:
- Site metrics (devices, clients, alerts, offline)
- Internet connection info (WAN provider)
- WiFi optimization tools
- Device management
- Client management
- **Back button** (top right) → return to dashboard

---

## 🖥️ Device Management

### View All Devices
1. Go to **Devices** tab
2. Click "📋 List All Devices"
3. See output in code block

### Device Actions
1. Expand "🔧 Device Actions"
2. Enter device MAC address (format: 00:00:00:00:00:00)
3. Choose action:
   - **🔄 Restart** - Reboot device
   - **⬆️ Upgrade** - Firmware update
   - **💡 Locate** - Flash LED (find in rack)
   - **ℹ️ Info** - View device details

### Refresh Status
- Click "🔄 Refresh Device Status"
- Shows network health summary

---

## 👥 Client Management

### View Connected Clients
1. Go to **Clients** tab
2. Click "📋 List All Clients"
3. See all WiFi/wired connections

### Client Actions
1. Expand "🔧 Client Actions"
2. Enter client MAC address
3. Available actions:
   - **ℹ️ Info** - Connection details
   - **🚫 Block** - Disconnect & prevent
   - **✅ Unblock** - Remove block
   - **🔄 Reconnect** - Force re-auth

**Common Use Cases:**
- Troubleshooting connection issues
- Security: blocking unauthorized devices
- Bandwidth management

---

## 📶 Wireless Optimization

### Full Network Scan
1. Go to **Wireless** tab
2. Click "🚀 Run Full Network Optimization"
3. Wait for analysis (15-30 seconds)
4. Review recommendations

### View WiFi Networks
- Click "📋 View WiFi Networks"
- Shows all WLANs with IDs

### Quick Actions
1. Expand "🔧 WiFi Network Management"
2. Enter WLAN ID (from network list)
3. Actions available:
   - **🟢 Enable** - Turn on WiFi
   - **🔴 Disable** - Turn off WiFi
   - **🔑 Change Password** - Update PSK

### Optimization Recommendations
The tool analyzes and suggests:
- ✓ Auto channel selection
- ✓ Transmit power levels
- ✓ Band steering (5GHz)
- ✓ Legacy protocol removal
- ✓ Fast roaming (802.11r)
- ✓ Minimum data rates

---

## 🎫 Ticket System

### Dashboard Metrics (Top)
- 🔵 Open tickets
- 🟡 In progress
- 🔴 Critical priority
- ✅ Resolved today

### Create New Ticket
1. Click "➕ New Ticket"
2. Fill out form:
   - **Title** * (required)
   - **Client** * (required)
   - **Site Location** (optional)
   - **Priority** (low/medium/high/critical)
   - **Network Type** (UniFi/Meraki/Both/Other)
   - **Assign To** (technician name, optional)
   - **Description** (details)
3. Click "✅ Create Ticket"

### Filter Tickets
- **Status**: open, in-progress, waiting, resolved, closed, all
- **Priority**: low, medium, high, critical, all

### Update Ticket
1. Click on any ticket to expand
2. View details & history
3. Add update in text area
4. Change status if needed
5. Reassign if needed
6. Click "💾 Update Ticket"

### Ticket Workflow
```
Open → In Progress → Waiting → Resolved → Closed
         ↓               ↓
    (working)      (awaiting info)
```

**Status Meanings:**
- **Open**: New, not started
- **In Progress**: Actively working
- **Waiting**: Awaiting response/parts
- **Resolved**: Fixed, pending verification
- **Closed**: Complete, archived

---

## 💡 Pro Tips

### Efficient Navigation
1. **Status Light Bar** → fastest way to check & navigate
2. **Search** → find sites quickly by name
3. **Tabs** → organized by task type
4. **Back Button** → always top-right on detail pages

### Monitoring Workflow
1. Start day: Check status light bar
2. Red lights? Click to investigate
3. Yellow lights? Schedule check
4. Green lights? All good! ✅

### Troubleshooting Steps
1. **Connection issue**:
   - Clients tab → find MAC → View info
   - Check signal strength & AP
   - Try reconnect
   
2. **Slow WiFi**:
   - Wireless tab → Run optimization
   - Check recommendations
   - View RF environment
   
3. **Device offline**:
   - Devices tab → Find MAC
   - Try locate (verify physical)
   - Restart if responsive
   
4. **Site down**:
   - Click red status light
   - Check WAN provider status
   - Review device list
   - Create ticket if needed

### Ticket Best Practices
- **Clear titles**: "Chicago Office - WiFi Down Floor 3"
- **Good descriptions**: Include error messages, symptoms
- **Set priority**: Critical = revenue impact
- **Assign quickly**: Get the right person on it
- **Update often**: Keep stakeholders informed
- **Close when done**: Clean up resolved tickets

---

## 🎨 Visual Indicators

### Color Meanings
- 🟢 **Green**: Healthy, operational, success
- 🟡 **Yellow**: Warning, attention needed
- 🔴 **Red**: Critical, immediate action
- 🔵 **Blue**: Info, neutral status
- ⚫ **Gray**: Closed, inactive

### Icons
- 🏢 Organization/building
- 🖥️ Devices/hardware
- 👥 Users/clients
- 📡 Wireless/network
- ⚠️ Alert/warning
- ✅ Success/complete
- ❌ Error/failed
- 🔄 Refresh/restart
- 🔍 Search/view
- ⚙️ Settings/config

---

## ⌨️ Keyboard Shortcuts

Streamlit doesn't support custom shortcuts, but:
- **Tab** = Navigate form fields
- **Enter** = Submit forms
- **Escape** = Close modals (some)
- **Ctrl+F** = Browser search

---

## 📱 Mobile Access

The portal works on mobile browsers but is optimized for desktop. For mobile:
- Rotate to landscape for better view
- Status bar scrolls horizontally
- Tap (not hover) for interactions
- Use pinch-to-zoom if needed

---

## 🔧 Admin Tasks

### Restart Portal
```bash
cd /home/administrator/.openclaw/workspace/projects/tech-portal
pkill -f "streamlit run"
source venv/bin/activate
nohup python -m streamlit run app.py --server.port 8501 --server.address 0.0.0.0 --server.headless true > streamlit.log 2>&1 &
```

### Check Status
```bash
ps aux | grep streamlit
curl http://localhost:8501
tail -f /home/administrator/.openclaw/workspace/projects/tech-portal/streamlit.log
```

### Update Site Data
```bash
cd /home/administrator/.openclaw/workspace/projects/tech-portal
./refresh_sites.py
```

### Backup Tickets
```bash
cp /home/administrator/.openclaw/workspace/projects/tech-portal/tickets.db /path/to/backup/
```

---

## 🆘 Troubleshooting

### Can't Login
- Check username is lowercase
- Verify password (no spaces)
- Try another account
- Check browser console for errors

### Site Not Loading
- Verify URL is correct
- Check network connectivity
- Ensure port 8501 is accessible
- Restart Streamlit process

### Commands Not Working
- Verify UniFi CLI is installed
- Check network connectivity to controllers
- Review command syntax
- Check logs for errors

### Slow Performance
- Close unused tabs
- Clear browser cache
- Check server resources
- Restart Streamlit

### Data Not Updating
- Refresh the page (F5)
- Click "Refresh" buttons
- Update combined_sites.json
- Check data source connectivity

---

## 📞 Support

### Documentation
- `README.md` - Project overview
- `UPGRADE_REPORT.md` - Change details
- `FEATURES.md` - Feature showcase
- `QUICK_START.md` - This guide

### Get Help
Contact Safe Harbor IT team or the administrator who deployed this portal.

---

## 🎉 Enjoy!

You now have a powerful, modern tech portal to manage your entire Safe Harbor network infrastructure. The futuristic design and intuitive interface make network management a breeze.

**Happy monitoring!** 🚀

---

*Safe Harbor Tech Portal v2.0 - Futuristic Edition*
