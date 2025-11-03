# How to Deploy Changes to Git and Streamlit Cloud

## Quick Steps

### 1. Check Current Status
First, see what files have changed:
```bash
cd defi-risk-gauge
git status
```

### 2. Stage Changes
Add all modified files:
```bash
git add app.py
```

Or add all changes at once:
```bash
git add .
```

### 3. Commit Changes
Create a commit with a descriptive message:
```bash
git commit -m "Improve UI: change spinner messages to 'Processing', add rate limiting for comparison mode, enhance error handling"
```

### 4. Push to GitHub
Push your changes to the repository:
```bash
git push origin main
```

If you're on a different branch (like `master`):
```bash
git push origin master
```

### 5. Streamlit Cloud Auto-Deploy
Streamlit Cloud will **automatically detect** the push and redeploy your app. You'll see:
- A deployment notification in the Streamlit Cloud dashboard
- The app will redeploy automatically (usually takes 1-2 minutes)

---

## Detailed Step-by-Step Guide

### Step 1: Navigate to Your Project Directory

```bash
cd /Users/swatisahu/Desktop/MSFT/FinancialMarketsProcessesandTechnology/defi-risk-gauge
```

### Step 2: Check What Changed

```bash
git status
```

This will show you:
- Modified files (like `app.py`)
- New files (if any)
- Files that are staged or unstaged

### Step 3: Review Changes (Optional)

If you want to see what changed in a file:
```bash
git diff app.py
```

### Step 4: Stage Your Changes

**Option A: Stage specific files**
```bash
git add app.py
```

**Option B: Stage all changes**
```bash
git add .
```

**Option C: Stage specific types of files**
```bash
git add *.py
git add *.md
```

### Step 5: Commit Your Changes

Create a commit with a clear message describing what you changed:
```bash
git commit -m "Update UI: change spinner messages to 'Processing', improve error handling and rate limiting"
```

**Good commit messages:**
- ✅ "Improve UI: change spinner messages to 'Processing'"
- ✅ "Add rate limiting delays for protocol comparison to avoid timeouts"
- ✅ "Enhance error handling and retry logic for API calls"
- ❌ "update"
- ❌ "fix"
- ❌ "changes"

### Step 6: Push to GitHub

```bash
git push origin main
```

If you get an error about the branch name:
```bash
git branch
```
This shows your current branch. Then push to that branch:
```bash
git push origin <your-branch-name>
```

### Step 7: Verify Streamlit Cloud Deployment

1. **Go to Streamlit Cloud Dashboard**
   - Visit [share.streamlit.io](https://share.streamlit.io)
   - Sign in and open your app

2. **Check Deployment Status**
   - You'll see "Deploying..." or a timestamp of last deployment
   - Wait 1-2 minutes for deployment to complete

3. **View Deployment Logs** (if needed)
   - Click on your app
   - Go to "Settings" → "Deployment logs"
   - Check for any errors

4. **Test Your App**
   - Open your app URL
   - Verify the changes are working
   - Test the spinner message shows "Processing..."
   - Test protocol comparison with delays

---

## Troubleshooting

### Issue: "fatal: not a git repository"

**Solution:** Initialize git first:
```bash
git init
git remote add origin https://github.com/YOUR_USERNAME/YOUR_REPO_NAME.git
```

### Issue: "error: failed to push some refs"

**Solution:** Pull latest changes first:
```bash
git pull origin main
# Resolve any conflicts if needed
git push origin main
```

### Issue: Streamlit Cloud Not Deploying

**Solutions:**
1. **Check Repository Connection**
   - Go to Streamlit Cloud dashboard
   - Verify repository is connected
   - Check if it's pointing to the correct branch

2. **Trigger Manual Deploy**
   - In Streamlit Cloud dashboard
   - Click "Reboot app" or "Redeploy"

3. **Check Deployment Logs**
   - Look for error messages
   - Verify `app.py` is the main file
   - Check `requirements.txt` is present

### Issue: Changes Not Showing on Streamlit

**Solutions:**
1. **Clear Browser Cache**
   - Hard refresh: `Cmd+Shift+R` (Mac) or `Ctrl+Shift+R` (Windows)
   - Or use incognito/private window

2. **Wait for Deployment**
   - Deployment takes 1-2 minutes
   - Check deployment status in dashboard

3. **Verify File Paths**
   - Ensure `app.py` is in the root directory
   - Check that all dependencies are in `requirements.txt`

---

## Quick Reference Commands

```bash
# See what changed
git status

# See detailed changes
git diff app.py

# Stage all changes
git add .

# Commit with message
git commit -m "Your commit message here"

# Push to GitHub
git push origin main

# Check recent commits
git log --oneline -5
```

---

## Git Best Practices for This Project

### 1. Commit Frequently
- Commit after each logical change
- Don't wait too long between commits

### 2. Write Clear Commit Messages
- Start with a verb: "Fix", "Add", "Update", "Improve"
- Be specific about what changed
- Keep messages under 72 characters if possible

### 3. Don't Commit Large Files
- Don't commit `venv/` directory
- Don't commit `logs/` directory
- Check `.gitignore` is working

### 4. Test Before Pushing
- Test locally: `streamlit run app.py`
- Fix any errors before pushing

---

## Streamlit Cloud Deployment Tips

### Automatic Deployment
- Streamlit Cloud watches your GitHub repository
- Any push to the connected branch triggers a redeploy
- Usually takes 1-2 minutes

### Manual Deployment
If automatic deployment isn't working:
1. Go to Streamlit Cloud dashboard
2. Click on your app
3. Click "Reboot app" or "Deploy"

### Deployment Notifications
- Streamlit Cloud will show deployment status
- You'll see "Deploying..." → "Deployed" or errors
- Check logs if deployment fails

---

## Example Workflow

```bash
# 1. Navigate to project
cd ~/Desktop/MSFT/FinancialMarketsProcessesandTechnology/defi-risk-gauge

# 2. Check what changed
git status

# 3. Stage changes
git add app.py

# 4. Commit
git commit -m "Update spinner messages to 'Processing' and improve rate limiting"

# 5. Push to GitHub
git push origin main

# 6. Wait 1-2 minutes, then check Streamlit Cloud dashboard
# 7. Test your deployed app
```

---

## Need Help?

If you encounter issues:
1. Check the deployment logs in Streamlit Cloud dashboard
2. Verify your git remote is correct: `git remote -v`
3. Ensure you have write access to the repository
4. Check that Streamlit Cloud is connected to the right branch

---

**That's it!** Your changes should now be live on Streamlit Cloud. 🚀

