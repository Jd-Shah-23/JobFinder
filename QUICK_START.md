# ⚡ Quick Start Guide

Your resume is already added! Follow these 4 simple steps:

## Step 1: Update Your Info (2 minutes)

Edit `config.json` and update:
```json
"personal_info": {
  "full_name": "Jaydeep Shah",           // Your name
  "email": "your.email@gmail.com",       // Your email
  "phone": "+91-XXXXXXXXXX",             // Your phone
  "linkedin_url": "https://linkedin.com/in/yourprofile"
}
```

## Step 2: Push to GitHub (2 minutes)

```bash
cd JavaJobs
git init
git add .
git commit -m "Setup job automation"
git branch -M main
git remote add origin https://github.com/YOUR_USERNAME/YOUR_REPO.git
git push -u origin main
```

## Step 3: Get Gmail App Password (3 minutes)

1. Go to: https://myaccount.google.com/security
2. Enable 2-Step Verification
3. Go to App passwords
4. Create password for "Mail"
5. Copy the 16-character code

## Step 4: Add GitHub Secrets (2 minutes)

In your GitHub repo → Settings → Secrets → Actions:

Add these 3 secrets:
- `EMAIL_SENDER`: your.email@gmail.com
- `EMAIL_PASSWORD`: (16-char code from step 3)
- `EMAIL_RECEIVER`: where.to.send@gmail.com

## ✅ Done! Test It

Go to Actions tab → Job Search Automation → Run workflow

---

**Total Time: ~10 minutes**

Every Monday 8 AM, you'll get an email with:
- Jobs found
- Applications submitted automatically
- Links to view each job

🎉 **Your resume is ready. Just configure and go!**