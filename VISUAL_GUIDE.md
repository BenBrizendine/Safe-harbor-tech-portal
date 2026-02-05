# Safe Harbor Tech Portal - Visual Feature Guide

## 🎨 Design System Overview

### Color Palette
```
Primary Brand:    #145F82 (Safe Harbor Blue)
Accent Light:     #1A7AA8
Accent Dark:      #0D4059
Success:          #00FF88 (Neon Green)
Warning:          #FFB800 (Amber)
Danger:           #FF3366 (Neon Red)
Background:       #0A0E1A → #050810 (Gradient)
Glass Effect:     rgba(255,255,255,0.05) with backdrop-blur
```

### Typography
```
Headers:   Orbitron (700 weight, 1px letter-spacing)
Body:      Rajdhani (400-600 weight)
Code:      Fira Code (monospace)
```

---

## 🔆 Status Light Bar (Main Feature)

### Location
- **Top of dashboard**, immediately after metrics
- Above the tab navigation
- Full-width horizontal bar

### Visual Design
```
┌────────────────────────────────────────────────┐
│  Status Bar (Glassmorphic container)           │
│  ┌──────┐ ┌──────┐ ┌──────┐ ┌──────┐ ...      │
│  │  ●   │ │  ●   │ │  ●   │ │  ●   │          │
│  │ Name │ │ Name │ │ Name │ │ Name │          │
│  └──────┘ └──────┘ └──────┘ └──────┘          │
└────────────────────────────────────────────────┘
```

### Status Indicator States

**🟢 GREEN - Healthy**
- Circular indicator with pulsing green glow
- All devices online
- No alerts
- Shadow: 0 0 20px rgba(0,255,136,0.8)

**🟡 YELLOW - Warning**
- Circular indicator with pulsing yellow glow
- Empty site or no devices
- Minor issues
- Shadow: 0 0 20px rgba(255,184,0,0.8)

**🔴 RED - Alert**
- Circular indicator with pulsing red glow
- Offline devices detected
- Active alerts
- Shadow: 0 0 20px rgba(255,51,102,0.8)

### Animations
1. **Pulse Effect** - 2s infinite ease-in-out
   - Opacity: 1 → 0.7 → 1
   - Scale: 1 → 0.95 → 1

2. **Hover Effect** - 300ms cubic-bezier
   - translateY: 0 → -4px
   - Border color: gray → blue
   - Box shadow intensifies

3. **Click Feedback**
   - Slight scale down
   - Navigates to site detail page

### Responsive Behavior
- Horizontal scrolling enabled for 20+ sites
- Maintains minimum 80px width per indicator
- Wraps on mobile devices
- Smooth scroll animation

---

## 🏠 Login Page

### Layout
```
┌─────────────────────────────────┐
│                                  │
│          [LOGO 250px]            │
│                                  │
│       TECH PORTAL                │
│       ─────────────              │
│                                  │
│    ┌─────────────────┐          │
│    │  Username        │          │
│    └─────────────────┘          │
│    ┌─────────────────┐          │
│    │  Password        │          │
│    └─────────────────┘          │
│    ┌─────────────────┐          │
│    │  🔐 LOGIN        │          │
│    └─────────────────┘          │
└─────────────────────────────────┘
```

### Visual Effects
- Glassmorphic container (frosted glass)
- Centered at 80px from top
- Max-width: 400px
- Gradient text for headers
- Input fields glow on focus

---

## 📊 Main Dashboard

### Header Section
```
┌────────────────────────────────────────────────┐
│ [Logo] SAFE HARBOR TECH PORTAL    [User] [⚪] │
│        🌐 Network Command Center                │
├────────────────────────────────────────────────┤
│ ┌──────┐ ┌──────┐ ┌──────┐ ┌──────┐           │
│ │  23  │ │ 330  │ │ 1427 │ │  2   │           │
│ │Sites │ │Device│ │Client│ │Offlin│           │
│ └──────┘ └──────┘ └──────┘ └──────┘           │
└────────────────────────────────────────────────┘
```

### Metrics Design
- **Font:** Orbitron 36px/700
- **Color:** #1A7AA8 with glow effect
- **Shadow:** 0 0 20px rgba(20,95,130,0.5)
- **Label:** Uppercase, 2px letter-spacing
- **Animation:** Fade-in on load

### Status Bar Position
```
┌────────────────────────────────────────────────┐
│ 🔆 SITE STATUS OVERVIEW                        │
│ [Status Light Bar Component Here]              │
└────────────────────────────────────────────────┘
```

---

## 🗂️ Tab System

### Visual Style
```
┌────┐ ┌────┐ ┌────┐ ┌────┐ ┌────┐
│📡  │ │🖥️  │ │👥  │ │📶  │ │🎫  │
│SITE│ │DEVI│ │CLIE│ │WIRE│ │TICK│
└────┘ └────┘ └────┘ └────┘ └────┘
  ▼
```

**Active Tab:**
- Background: Gradient #145F82 → #0D4059
- Color: White
- Box-shadow: 0 4px 20px rgba(20,95,130,0.4)

**Inactive Tab:**
- Background: Glassmorphic
- Color: Gray
- Border: 1px solid glass-border

**Hover:**
- Background: rgba(20,95,130,0.1)
- Color: #1A7AA8

---

## 🏢 Site Cards

### Card Layout
```
┌────────────────────────┐
│ 🟢 Site Name           │
│                        │
│ 🏢 UniFi | Org Name    │
│ 🖥️ 21 devices          │
│ 👥 337 clients         │
└────────────────────────┘
```

### Visual Properties
- **Background:** Glassmorphic with blur
- **Border:** 1px solid glass-border
- **Radius:** 12px
- **Padding:** 24px
- **Shadow:** 0 4px 16px rgba(0,0,0,0.2)

### Hover Effect
- **Transform:** translateY(-4px)
- **Border:** Changes to Safe Harbor blue
- **Shadow:** 0 8px 32px rgba(20,95,130,0.4)
- **Background:** Slight blue tint

### Grid Layout
- 3 columns on desktop
- 2 columns on tablet
- 1 column on mobile
- 24px gap between cards

---

## 🎫 Ticket System

### Ticket Card
```
┌────────────────────────────────────────┐
│ 🔵 #123 - Issue Title 🔴               │
│ ┌──────────────────┬─────────────┐    │
│ │ Client: ABC Corp │ Status: Open│    │
│ │ Site: New York   │ Priority: Hi│    │
│ │ Description...   │ Created: ... │    │
│ └──────────────────┴─────────────┘    │
│ Updates:                               │
│ • Update 1 - User (timestamp)          │
│ ─────────────────────────────────      │
│ [Update Form]                          │
└────────────────────────────────────────┘
```

### Status Badges
- 🔵 Open
- 🟡 In Progress
- 🟠 Waiting
- 🟢 Resolved
- ⚫ Closed

### Priority Indicators
- ⬇️ Low
- ➡️ Medium
- ⬆️ High
- 🔴 Critical

---

## 🔧 Action Panels

### Expandable Sections
```
▼ 🔧 Device Actions
  ┌────────────────────────────────┐
  │ Device MAC: [______________]   │
  │ ┌──────┐ ┌──────┐ ┌──────┐   │
  │ │🔄 Res│ │⬆️ Upg│ │💡 Loc│   │
  │ └──────┘ └──────┘ └──────┘   │
  └────────────────────────────────┘
```

### Button Style
- **Default:** Glassmorphic background
- **Hover:** Blue tint + glow
- **Active:** Slight scale-down
- **Full-width:** Yes
- **Transitions:** 300ms smooth

---

## 📱 Responsive Design

### Breakpoints
```
Desktop:  > 1024px  (3-column grid)
Tablet:   768-1024  (2-column grid)
Mobile:   < 768px   (1-column, stacked)
```

### Mobile Optimizations
- Status bar becomes scrollable
- Cards stack vertically
- Font sizes reduce slightly
- Touch-friendly button sizes (min 44px)
- Simplified navigation

---

## ✨ Animation Timing

### Page Load
```css
fadeIn: 0.5s ease-out
```

### Hover Effects
```css
card-hover: 0.3s cubic-bezier(0.4, 0, 0.2, 1)
```

### Status Indicators
```css
pulse: 2s ease-in-out infinite
```

### Transitions
```css
all: 0.3s ease
```

---

## 🎭 Interactive States

### Buttons
1. **Default** - Resting state
2. **Hover** - Lift + glow
3. **Active** - Pressed down
4. **Loading** - Spinner overlay
5. **Disabled** - Reduced opacity

### Inputs
1. **Empty** - Placeholder visible
2. **Focused** - Blue border glow
3. **Filled** - White text
4. **Error** - Red border
5. **Success** - Green checkmark

### Cards
1. **Default** - Static
2. **Hover** - Elevated
3. **Active** - Selected state
4. **Loading** - Skeleton/spinner
5. **Error** - Red border

---

## 🔍 Detail Pages

### Site Detail Layout
```
┌────────────────────────────────────────┐
│ [Logo] 📍 Site Name         [← Back]   │
│        UniFi • UDMPRO • Org Name       │
├────────────────────────────────────────┤
│ ┌──────┐ ┌──────┐ ┌──────┐ ┌──────┐  │
│ │ 21   │ │ 337  │ │  0   │ │  0   │  │
│ │Device│ │Client│ │Offlin│ │Alert │  │
│ └──────┘ └──────┘ └──────┘ └──────┘  │
├────────────────────────────────────────┤
│ 🌐 Internet Connection                 │
│ Provider: Comcast | Gateway: UDMPRO    │
├────────────────────────────────────────┤
│ ⚡ Quick Actions                        │
│ [View Devices] [View Clients] [WiFi]   │
└────────────────────────────────────────┘
```

---

## 🌈 Accessibility Features

### Keyboard Navigation
- Tab through all interactive elements
- Enter/Space to activate buttons
- Escape to close modals/expanders
- Arrow keys in select boxes

### Screen Reader Support
- Semantic HTML5 elements
- ARIA labels on interactive components
- Alt text on images
- Role attributes on custom components

### Visual Clarity
- High contrast ratios (WCAG AAA)
- Large touch targets (44px minimum)
- Clear focus indicators
- Color is not sole indicator

---

## 🎯 Key Visual Principles

1. **Consistency** - Same patterns throughout
2. **Hierarchy** - Clear visual importance
3. **Feedback** - Immediate user response
4. **Minimalism** - Clean, uncluttered
5. **Brand** - Safe Harbor identity present
6. **Modern** - Cutting-edge design trends
7. **Professional** - Enterprise-grade appearance

---

## 💡 Usage Tips

### Best Viewing
- **Browser:** Chrome, Firefox, Edge (latest)
- **Resolution:** 1920x1080 or higher recommended
- **Dark mode:** Optimized for dark environments
- **Refresh:** Auto-updates with Streamlit

### Performance
- Fast initial load (~2 seconds)
- Smooth 60fps animations
- Efficient re-renders
- Background data loading

---

**The portal combines modern aesthetics with professional functionality - a true command center worthy of Safe Harbor's reputation.**
