# Tech Portal - Meraki + UniFi Unified Dashboard

## Overview
Unified dashboard for Safe Harbor technicians to manage both UniFi and Meraki networks, create service tickets, and receive notifications.

## Phase 1: Meraki Integration
- [ ] Obtain Meraki API key
- [ ] Build Meraki CLI tool (similar to ez-unifi)
- [ ] Features:
  - List organizations, networks, devices
  - Restart/reboot devices
  - View clients and usage
  - Check alerts and events
  - Firmware status
  - Network health

## Phase 2: Service Ticket System
- [ ] SQLite database for tickets
- [ ] Ticket fields:
  - ID, title, description, priority, status
  - Client/site, assigned tech, created/updated timestamps
  - Resolution notes
- [ ] CLI for ticket management
- [ ] Email notifications (Gmail API)

## Phase 3: Unified Web Dashboard
- [ ] Single interface for both networks
- [ ] Tabs: UniFi | Meraki | Tickets | Alerts
- [ ] Tech login/authentication
- [ ] Real-time device status
- [ ] Quick actions (restart, adopt, etc.)

## Phase 4: Notifications
- [ ] Email alerts (Gmail API)
- [ ] Push notifications (OpenClaw nodes?)
- [ ] Alert rules (device offline, high utilization, etc.)

## Tech Stack
- **Backend:** Python, SQLite
- **APIs:** Meraki REST API, UniFi API
- **Frontend:** Streamlit or React
- **Email:** Gmail API (now authenticated)
- **Deployment:** Netlify (or local server)

## Next Actions
1. Get Meraki API key from Ben
2. Build Meraki CLI wrapper
3. Design ticket schema
4. Build unified dashboard UI
