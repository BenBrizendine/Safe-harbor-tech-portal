# Deploy Safe Harbor Tech Portal to Streamlit Cloud

## Step 1: Create GitHub Repository

1. Go to https://github.com/new
2. **Repository name:** `safe-harbor-tech-portal`
3. **Visibility:** Private (recommended) or Public
4. **Don't** initialize with README (we already have files)
5. Click **Create repository**

## Step 2: Push Code to GitHub

Copy these commands and run them on your machine:

```bash
cd /home/administrator/.openclaw/workspace/projects/tech-portal

# Add GitHub remote (replace YOUR-USERNAME with your GitHub username)
git remote add origin https://github.com/YOUR-USERNAME/safe-harbor-tech-portal.git

# Push code
git branch -M main
git push -u origin main
```

**If you need a token:**
- Go to https://github.com/settings/tokens
- Generate new token (classic)
- Select: `repo` scope
- Use token as password when pushing

## Step 3: Deploy to Streamlit Cloud

1. Go to https://share.streamlit.io
2. Click **"New app"**
3. Connect your GitHub account (if not already)
4. Select:
   - **Repository:** `YOUR-USERNAME/safe-harbor-tech-portal`
   - **Branch:** `main`
   - **Main file path:** `app.py`
5. Click **"Deploy"**

## Step 4: Add Secrets

Once app is deployed:

1. Click **"⚙️ Settings"** (gear icon)
2. Go to **"Secrets"**
3. Paste this into the secrets box:

```toml
UNIFI_API_KEY = "Ajrp9STpka1hiGFswsH-LxFogbLhe___"
MERAKI_API_KEY = "42feb43f88e3bdef877072b2054819a0e8eed31e"
```

4. Click **"Save"**
5. App will automatically restart with secrets

## Step 5: Test the App

Your app will be live at:
`https://YOUR-USERNAME-safe-harbor-tech-portal.streamlit.app`

**Test login with:**
- john / john123
- ben / ben123
- caleb / caleb123
- craig / craig123

## Step 6: Share with the Team

Send the team:
- **URL:** (your app URL)
- **Logins:** john/john123, ben/ben123, caleb/caleb123, craig/craig123
- **Purpose:** "Network ops dashboard - test it out and let me know what you think"

---

## Troubleshooting

**"Module not found" errors:**
- Check `requirements.txt` has all dependencies
- Streamlit Cloud auto-installs from requirements.txt

**"Secrets not found" errors:**
- Make sure you added secrets in Settings → Secrets
- Secrets must be valid TOML format

**App won't start:**
- Check logs in Streamlit Cloud dashboard
- Most common: missing dependency in requirements.txt

**Need to update code:**
```bash
cd /home/administrator/.openclaw/workspace/projects/tech-portal
git add .
git commit -m "Update: description of changes"
git push
```
Streamlit Cloud auto-deploys on push.

---

## Current Status

✅ Git repo initialized  
✅ Code committed locally  
⏳ **Next:** Push to GitHub and deploy to Streamlit Cloud

**Ready to go!** Just follow steps 1-6 above.
