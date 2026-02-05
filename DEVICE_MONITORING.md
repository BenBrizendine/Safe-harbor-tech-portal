# Safe Harbor Device Monitoring System

**Status:** ✅ ACTIVE (runs every 15 minutes via cron)

---

## Overview

Automated device monitoring system that:
1. ✅ Checks all 558 devices across 34 sites every 15 minutes
2. ✅ Tracks devices that go offline
3. ✅ Verifies they're still down after 15 minutes (prevents false alarms)
4. ✅ Auto-creates tickets in Tech Portal
5. ✅ Emails Ben at Ben.Brizendine@safeharborsolutionsllc.com

---

## Priority Rules

**CRITICAL** → Firewalls, Gateways, Security Appliances, Core Switches
- Immediate attention required
- Business-critical infrastructure

**HIGH** → Access Points, Wireless Controllers
- Affects user connectivity
- Should be resolved quickly

**MEDIUM** → Other devices
- Non-critical infrastructure

---

## How It Works

### Step 1: First Detection
- Monitor checks all sites via `combined_sites.json`
- Detects devices showing as offline
- Logs to state file: `monitor_state.json`
- **No alert sent yet** (waiting for confirmation)

### Step 2: Verification (15 minutes later)
- Monitor checks again
- If device still offline → confirmed outage
- If device back online → remove from tracking

### Step 3: Alert & Ticket
- Creates ticket in Tech Portal database
- Sends formatted email to Ben
- Logs ticket ID in state file

### Step 4: Ongoing Tracking
- Continues monitoring but won't create duplicate tickets
- Only creates one ticket per device/site outage

---

## Email Format

```
Subject: 🚨 Device Down Alert - [Site Name]: [Device Name]

Safe Harbor Tech Portal - Device Alert

DEVICE STATUS: OFFLINE

Site: Coventry (CloudKey)
Device: 2 devices
Type: unifi
Priority: HIGH

DETAILS:
Site: Coventry (CloudKey)
Network Type: unifi
Offline Device Count: 2
First Detected: 2026-02-05 15:18:15
Duration: 15 minutes

TICKET CREATED:
Ticket #1 has been automatically created in the Tech Portal.

View ticket: https://safe-harbor-tech-app-8gq6z73gwintyanfnqu7jp.streamlit.app
```

---

## Files

**Monitor Script:**
`/home/administrator/.openclaw/workspace/projects/tech-portal/device_monitor.py`

**State File (tracking):**
`/home/administrator/.openclaw/workspace/projects/tech-portal/monitor_state.json`

**Log File:**
`/home/administrator/.openclaw/workspace/projects/tech-portal/monitor.log`

**Sites Data:**
`/home/administrator/.openclaw/workspace/projects/tech-portal/combined_sites.json`

---

## Cron Schedule

```cron
*/15 * * * * cd /home/administrator/.openclaw/workspace/projects/tech-portal && /usr/bin/python3 device_monitor.py >> /home/administrator/.openclaw/workspace/projects/tech-portal/monitor.log 2>&1
```

**Runs:** Every 15 minutes, 24/7  
**Next run:** Check `crontab -l` or wait for next 15-minute mark

---

## Manual Testing

### Run Monitor Once
```bash
cd /home/administrator/.openclaw/workspace/projects/tech-portal
python3 device_monitor.py
```

### View Current State
```bash
cat /home/administrator/.openclaw/workspace/projects/tech-portal/monitor_state.json | python3 -m json.tool
```

### View Log
```bash
tail -50 /home/administrator/.openclaw/workspace/projects/tech-portal/monitor.log
```

### Clear State (Reset Tracking)
```bash
rm /home/administrator/.openclaw/workspace/projects/tech-portal/monitor_state.json
```

---

## Current Status

**As of 2026-02-05 15:18:**
- Total devices: 558
- Currently offline: 8 (across 5 sites)
- Tracking: 5 potential issues (waiting for 15-min confirmation)
- Alerts created: 0 (first run, all in verification period)

**Sites with offline devices:**
- Site 6 (unifi): 2 devices
- Coventry (CloudKey) (unifi): 2 devices
- Site 7 (unifi): 1 device
- Site 9 (unifi): 1 device
- Site 13 (unifi): 2 devices

---

## Email Configuration

**Sender:** Dude@safeharborsolutionsllc.com (Safe Harbor O365)  
**Recipient:** Ben.Brizendine@safeharborsolutionsllc.com  
**Method:** gog CLI with O365 authentication  
**Password:** Set via `GOG_KEYRING_PASSWORD=openclaw`

---

## Troubleshooting

### Email Not Sending?
```bash
# Test gog CLI manually
export GOG_KEYRING_PASSWORD=openclaw
/home/administrator/.local/bin/gog gmail send \
  --to Ben.Brizendine@safeharborsolutionsllc.com \
  --subject "Test Alert" \
  --body "Testing device monitor email" \
  --account Dude@safeharborsolutionsllc.com
```

### Monitor Not Running?
```bash
# Check cron job
crontab -l | grep device_monitor

# Check cron logs
grep device_monitor /var/log/syslog
```

### Wrong Device Priority?
Edit `device_monitor.py` → `get_device_priority()` function

---

## Future Enhancements

**Possible improvements:**
- [ ] Per-device tracking (requires API integration)
- [ ] Slack/Teams integration
- [ ] SMS alerts for critical devices
- [ ] Auto-resolve tickets when device comes back online
- [ ] Weekly summary report
- [ ] Dashboard widget showing monitor status

---

**Created:** 2026-02-05  
**Status:** Production  
**Maintained by:** The Dude (OpenClaw Agent)
