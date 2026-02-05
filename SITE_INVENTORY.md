# Safe Harbor Network Site Inventory

**Last Updated:** 2026-02-04  
**Total Sites:** 18

---

## 🔵 UniFi Sites (1)

### The Preserve at Spring Creek
- **Platform:** UniFi Site Manager
- **Site ID:** `6955d7ba43f1f93b98b1388b`
- **Organization:** Safe Harbor Solutions
- **Gateway:** UDM Pro SE (`6c:63:f8:68:28:2d`)
- **Total Devices:** 70
  - 64 WiFi Devices (APs)
  - 5 Wired Devices (Switches)
  - 1 Gateway Device
- **Active Clients:** 676
  - 159 WiFi Clients
  - 517 Wired Clients
- **ISP:** Frontier Communications
- **WAN Uptime:** 100%
- **Timezone:** America/Chicago

---

## 🔶 Meraki Sites (17)

### Frontier Management (5 sites)
1. **Safe Harbor Solutions**
   - Internal office/datacenter
2. **Frontier Management - Portland**
   - Portland office location
3. **Frontier Dallas Office**
   - Dallas office location
4. **SHS Colo**
   - Colocation facility
5. **Sache International**
   - Client site

### Welltower - CIS (7 sites)
1. **ID Boise - Overland Court** (BSE002)
2. **WA Bremerton - Bay Pointe MC** (BTN004)
3. **AZ Lake Havasu - Lake View Terrace** (LKH003)
4. **OR Happy Valley - Monterey Court** (PRT000)
5. **MS Hattiesburg - Crescent Landing** (HAT002)
6. **UT Ogden - The Auberge** (OGD000)
7. **CIS TEST** (Test environment)

### Welltower - QSL (1 site)
1. **GA Carrollton - Laurel Glen** (CRO000)

### Embassy - OH7 (4 sites)
1. **Euclid**
2. **Newark**
3. **Lyndhurst**
4. **Painesville**

---

## 📊 Summary Statistics

| Platform | Sites | Organizations |
|----------|-------|---------------|
| UniFi    | 1     | 1             |
| Meraki   | 17    | 4             |
| **Total**| **18**| **5**         |

### By Organization
- **Safe Harbor Solutions:** 1 site (UniFi)
- **Frontier Management:** 5 sites (Meraki)
- **Welltower - CIS:** 7 sites (Meraki)
- **Welltower - QSL:** 1 site (Meraki)
- **Embassy - OH7:** 4 sites (Meraki)

---

## 🔔 Pending Actions

### UniFi Site Manager
- **Pending Invitations:** Check https://account.ui.com for new site invitations from John
- **Action Required:** Accept pending invitations to add more UniFi sites to inventory
- **Expected:** Additional sites may appear after accepting invitations

### Data Collection
- [ ] Pull device counts for all Meraki sites
- [ ] Pull client counts for all Meraki sites
- [ ] Set up automated inventory refresh (daily)

---

## 📝 Notes

- **The Preserve at Spring Creek** is a large deployment (70 devices, 676 clients) - likely a senior living facility
- Meraki API key configured: `42feb43f88e3bdef877072b2054819a0e8eed31e`
- UniFi API key configured: `Ajrp9STpka1hiGFswsH-LxFogbLhe___`
- All site data stored in Tech Portal database (`tickets.db`, `sites` table)

---

**Data Sources:**
- UniFi: https://api.ui.com/ea/sites
- Meraki: https://api.meraki.com/api/v1/organizations
