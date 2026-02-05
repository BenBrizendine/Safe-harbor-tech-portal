# Tech Portal - UniFi Cloud API Usage Guide

**Version:** 2.0 (Cloud API Edition)  
**Last Updated:** 2026-02-05

---

## Quick Start

### Accessing the Portal
- **URL:** http://localhost:8501 (or http://172.30.40.248:8501)
- **Login:** Use your existing credentials (john, ben, caleb, craig)

---

## UniFi Cloud API - What You Can Do

### ✅ View & Monitor (Full Support)

#### 1. Sites Overview
- View all UniFi sites at a glance
- See device counts per site
- See client counts (WiFi + Wired)
- Check site health status
- Interactive status bar (click site to view details)

**How:** Navigate to **SITES** tab → Browse or search sites

#### 2. Device Monitoring
- List all devices across sites
- Check online/offline status
- View basic device info (model, MAC, firmware)
- See which site each device belongs to

**How:** Navigate to **DEVICES** tab → Click "List All Devices"

#### 3. Network Statistics
- Total sites count
- Total devices count
- Total active clients
- Offline device alerts

**How:** View dashboard metrics at top of screen

---

### ⚠️ Device Commands (Web UI Required)

The UniFi Cloud API is **read-only**. For device control actions, you'll need to use the web interface:

#### How to Control Devices

1. **Visit:** https://unifi.ui.com
2. **Select:** Your site from the list
3. **Navigate to:** Devices section
4. **Choose:** The device you want to manage
5. **Action:** Click the desired action button

#### Available Web UI Actions
- 🔄 Restart devices
- ⬆️ Upgrade firmware
- 💡 Locate devices (LED blink)
- 🔧 Change device settings
- 📊 View detailed device stats

**Portal Behavior:** When you try these commands in the portal, you'll see a helpful message guiding you to the web UI.

---

### ℹ️ Client Information (Web UI for Details)

#### What the Portal Shows
- Total client count per site
- WiFi vs. Wired breakdown
- Site-level client statistics

#### What Requires Web UI
- Individual client details
- Client history
- Block/unblock clients
- Reconnect specific clients
- Bandwidth usage per client

**How to View Client Details:**
1. Go to https://unifi.ui.com
2. Select your site
3. Navigate to **Clients** section
4. Click any client for detailed info

---

### 📶 WiFi Management (Web UI Required)

#### What the Portal Shows
- WiFi network presence detection
- Network health status

#### What Requires Web UI
- View SSID list
- Change WiFi passwords
- Enable/disable networks
- Modify WiFi settings (channels, power, etc.)
- Create new networks

**How to Manage WiFi:**
1. Go to https://unifi.ui.com
2. Select your site
3. Navigate to **WiFi** or **Settings → WiFi** section
4. Manage networks as needed

---

## Tech Portal Commands Reference

### Working Commands (Portal + API)

```
sites              → List all UniFi sites with stats
health             → Show site health (same as 'sites')
devices            → List all devices (limited info)
```

### Commands Requiring Web UI

```
restart <device>   → Restart a device
upgrade <device>   → Upgrade device firmware
locate <device>    → Blink device LED
clients            → View detailed client list
block <client>     → Block a client
unblock <client>   → Unblock a client
reconnect <client> → Force client reconnect
wlans              → List WiFi networks
wlan-enable <id>   → Enable WiFi network
wlan-disable <id>  → Disable WiFi network
wlan-password <id> → Change WiFi password
```

**Note:** When you try these in the portal, you'll get clear instructions on how to do it via web UI.

---

## Common Tasks

### Task: Check Site Health
1. **Portal:** Dashboard → View status bar
2. **Portal:** SITES tab → See device/client counts
3. **Web:** Visit unifi.ui.com for detailed health metrics

### Task: Find Offline Devices
1. **Portal:** Dashboard → Check "Offline" metric
2. **Portal:** SITES tab → Look for sites with offline alerts
3. **Web:** Visit unifi.ui.com → Devices → Filter by offline

### Task: Restart a Device
1. **Portal:** Note the device MAC/name
2. **Web:** Visit unifi.ui.com
3. **Web:** Select site → Devices → Find device → Restart

### Task: Change WiFi Password
1. **Portal:** Note the site name
2. **Web:** Visit unifi.ui.com
3. **Web:** Select site → WiFi → Edit network → Update password

### Task: View Client Bandwidth
1. **Portal:** Note the site name
2. **Web:** Visit unifi.ui.com
3. **Web:** Select site → Clients → Click client → View stats

---

## Meraki Integration

**Good News:** Meraki integration is **unchanged** and fully functional!

### Meraki Features (Fully Working)
- ✅ List networks
- ✅ View devices
- ✅ View clients
- ✅ Network statistics
- ✅ Organization management

**Note:** Meraki has a different API with more capabilities than UniFi Cloud API.

---

## Ticket System

**Fully Functional** - No changes!

### Create Tickets
- Click "➕ New Ticket" button
- Fill in details (client, site, priority)
- Assign to technician
- Add description

### Update Tickets
- Expand ticket card
- Add update notes
- Change status
- Reassign if needed

### Filter Tickets
- By status (open, in-progress, waiting, resolved, closed)
- By priority (low, medium, high, critical)
- Search by keyword

---

## Tips & Best Practices

### 1. Use the Portal For
✅ Quick overview of all sites  
✅ Monitoring device/client counts  
✅ Checking online/offline status  
✅ Ticket management  
✅ Cross-site statistics

### 2. Use unifi.ui.com For
✅ Device control actions  
✅ Detailed client information  
✅ WiFi management  
✅ Advanced analytics  
✅ Configuration changes

### 3. Workflow Optimization
- **Morning Check:** Portal → Dashboard → Check status bar for issues
- **Device Issues:** Portal → Note device details → Switch to Web UI for fix
- **Client Support:** Portal → Check site stats → Web UI for client details
- **WiFi Changes:** Web UI directly (no need to check portal first)

---

## API Key Management

### Current Setup
- **Key Location:** `/home/administrator/.openclaw/workspace/.env`
- **Key Variable:** `UNIFI_API_KEY`
- **Generated At:** https://unifi.ui.com/api

### If API Stops Working
1. Check if key is still valid at unifi.ui.com/api
2. Generate new key if needed
3. Update `.env` file
4. Restart Streamlit app:
   ```bash
   pkill -f streamlit
   cd /home/administrator/.openclaw/workspace/projects/tech-portal
   source venv/bin/activate
   nohup streamlit run app.py --server.port 8501 --server.address 0.0.0.0 &
   ```

---

## Troubleshooting

### Problem: "UniFi API key not configured"
**Solution:** Check that `UNIFI_API_KEY` is set in `.env` file

### Problem: "Error: Request timed out"
**Solution:** Check internet connection; api.ui.com may be unreachable

### Problem: Sites not showing devices
**Solution:** This is normal if sites are newly created; devices show up after they check in

### Problem: Want to restart device but can't
**Solution:** This is expected; use unifi.ui.com web interface (see guide above)

### Problem: Portal shows wrong site name ("Default")
**Solution:** Update site description at unifi.ui.com → Site Settings

---

## Comparison: Old vs. New

### Old Setup (ez-unifi skill + local controller)
- ❌ Required local UniFi controller
- ❌ Required VPN access to controller
- ❌ Needed username/password authentication
- ❌ Per-site configuration
- ✅ Full device control via CLI

### New Setup (UniFi Cloud API)
- ✅ Works with unifi.ui.com cloud management
- ✅ No VPN needed
- ✅ Single API key for all sites
- ✅ Centralized, secure authentication
- ⚠️ Device control via web UI only

**Trade-off:** Lost CLI device control, gained cloud-native monitoring and simplified authentication.

---

## Feature Matrix

| Feature                    | Portal | Web UI | Notes                          |
|----------------------------|--------|--------|--------------------------------|
| View sites                 | ✅     | ✅     | Portal shows quick overview    |
| View devices               | ⚠️     | ✅     | Portal shows limited info      |
| View clients               | ⚠️     | ✅     | Portal shows counts only       |
| Device control             | ❌     | ✅     | Restart, upgrade, etc.         |
| WiFi management            | ❌     | ✅     | Passwords, settings            |
| Client management          | ❌     | ✅     | Block, unblock                 |
| Site statistics            | ✅     | ✅     | Portal great for overview      |
| Ticket system              | ✅     | ❌     | Portal exclusive               |
| Cross-platform (Meraki)    | ✅     | ❌     | Portal handles both            |
| Offline monitoring         | ✅     | ✅     | Portal quick alerts            |

Legend:
- ✅ Full support
- ⚠️ Partial support
- ❌ Not available

---

## Getting Help

### Portal Issues
- Check: `/home/administrator/.openclaw/workspace/projects/tech-portal/streamlit.log`
- Restart: Kill streamlit process and restart as shown above

### UniFi API Issues
- Check: API key is valid at unifi.ui.com/api
- Check: Internet connection to api.ui.com
- Check: `.env` file has correct key

### Feature Requests
- Document in ticket system
- Tag with "enhancement" priority
- Assign to development team

---

## Summary

The Tech Portal is now a **monitoring and ticketing** platform for UniFi networks, with the understanding that **device control** happens via the official UniFi web interface.

**Think of it as:**
- **Portal** = Eyes (see everything, all sites, one place)
- **Web UI** = Hands (make changes, control devices)

This division actually makes sense for production environments where you want **monitoring** to be automated/centralized but **control actions** to be deliberate and logged via the official UI.

---

**Enjoy the updated Tech Portal!** 🚀
