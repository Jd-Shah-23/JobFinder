# ✅ Setup Complete!

## What's Ready

✅ **Your Resume**: Already added (Jaydeep Shah Resume.pdf)
✅ **Auto-Apply**: Configured to apply to up to 5 jobs per week
✅ **Skip Companies**: TCS, UFFIZIO, IBM (your previous employers)
✅ **Locations**: Ahmedabad, Gandhinagar, Pune, Mumbai
✅ **Schedule**: Every Monday 8:00 AM IST

## What You Need to Do

### 1. Update Your Personal Info (Required)

Edit `config.json` and update these fields:

```json
"personal_info": {
  "full_name": "Jaydeep Shah",
  "email": "YOUR_EMAIL@gmail.com",        // ← Update this
  "phone": "+91-XXXXXXXXXX",              // ← Update this
  "current_location": "Ahmedabad",
  "linkedin_url": "https://linkedin.com/in/yourprofile",  // ← Update this
  "notice_period": "30 days",
  "expected_salary": "As per industry standards"
}
```

### 2. Push to GitHub

```bash
cd JavaJobs
git init
git add .
git commit -m "Setup automated job search"
git branch -M main
git remote add origin https://github.com/YOUR_USERNAME/YOUR_REPO.git
git push -u origin main
```

### 3. Setup GitHub Secrets

In your GitHub repository:
- Go to: Settings → Secrets and variables → Actions
- Add these 3 secrets:

| Secret Name | Value |
|------------|-------|
| EMAIL_SENDER | your.email@gmail.com |
| EMAIL_PASSWORD | Your Gmail App Password (16 chars) |
| EMAIL_RECEIVER | where.to.receive@gmail.com |

**Get Gmail App Password:**
1. https://myaccount.google.com/security
2. Enable 2-Step Verification
3. App passwords → Mail → Generate
4. Copy the 16-character code

### 4. Test It!

- Go to Actions tab
- Click "Job Search Automation"
- Click "Run workflow"
- Wait 2-3 minutes
- Check your email!

## What Happens Every Monday

```
8:00 AM IST
    ↓
Searches for Java Developer jobs
    ↓
Finds jobs in Ahmedabad/Gandhinagar/Pune/Mumbai
    ↓
Skips: TCS, UFFIZIO, IBM
    ↓
Applies to up to 5 jobs with your resume
    ↓
Emails you the report
```

## Your Email Will Show

- 📊 Total jobs found
- 🤖 Applications submitted (max 5)
- 💼 Job listings with application status
- ✓ Which jobs were applied to
- 🔗 Links to view each job

## Need to Change Something?

**Apply to more jobs per week:**
```json
"max_applications_per_run": 10
```

**Add more companies to skip:**
```json
"skip_companies": ["TCS", "UFFIZIO", "IBM", "Company X"]
```

**Change locations:**
```json
"locations": ["Bangalore", "Hyderabad"]
```

**Disable auto-apply (just search):**
```json
"auto_apply": { "enabled": false }
```

## Files Overview

- ✅ `resume/resume.pdf` - Your resume (80KB)
- ✅ `config.json` - Your settings (companies to skip configured)
- ✅ `.github/workflows/job-search.yml` - Runs every Monday
- ✅ `src/` - All automation code ready

## Important Notes

- Your resume is protected by .gitignore (won't be pushed to GitHub)
- Email credentials are encrypted as GitHub Secrets
- System applies to max 5 jobs per week (configurable)
- You'll get an email report every Monday
- Some applications may need manual completion

---

## Quick Commands

**Update personal info:**
```bash
nano config.json  # or use any text editor
```

**Test locally (optional):**
```bash
pip install -r requirements.txt
export EMAIL_SENDER="your@gmail.com"
export EMAIL_PASSWORD="app-password"
export EMAIL_RECEIVER="receiver@gmail.com"
python src/main.py
```

---

**🎉 You're all set! Just push to GitHub and configure secrets.**

**Total setup time: ~10 minutes**