# Safe Harbor Tech Portal - Web

Landing page and authentication for the Tech Portal.

## Features

- Safe Harbor branded landing page
- Secure authentication
- Network grid animation
- Mobile responsive

## Credentials

**Configured users:**
- `ben` / `tech2026`
- `admin` / `safeharbor-admin`

More users can be added by editing `login.js` -> `VALID_USERS` object.

## Session

- Duration: 12 hours
- Storage: localStorage (key: `tech_session`)

## Deployment

**Netlify:** 
```bash
netlify deploy --prod --dir=.
```

**Live URL:** Will be assigned after deployment

## Local Development

```bash
# Serve locally
python3 -m http.server 8080
```

Access at: http://localhost:8080

## Integration

The dashboard page (`dashboard.html`) links to:
- Streamlit dashboard (localhost:8501)
- Meraki Dashboard
- UniFi Console

For production, embed the Streamlit dashboard or deploy it separately.

## Adding Users

Edit `login.js`:
```javascript
const VALID_USERS = {
    'ben': 'tech2026',
    'admin': 'safeharbor-admin',
    'newuser': 'newpassword'  // Add here
};
```

## Future Enhancements

- Database-backed user management
- Role-based access control (admin vs tech)
- Activity logging
- Two-factor authentication
- Integration with Safe Harbor AD/SSO
