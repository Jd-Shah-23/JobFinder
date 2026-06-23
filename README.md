# 🚀 Automated Java Job Search & Auto-Apply System

This system automatically searches for Java Developer jobs every Monday at 8 AM IST, **automatically applies to them with your resume**, and emails you a detailed report.

## ✨ Features

- ✅ Searches for Java Developer positions with 5 years experience
- 📍 Focuses on locations: Ahmedabad, Gandhinagar, Pune, Mumbai
- 🤖 **Automatically applies to jobs with your resume**
- ⏰ Runs automatically via GitHub Actions every Monday at 8 AM IST
- 📧 Sends beautifully formatted email report with application status
- 🔍 Scrapes jobs from Naukri.com
- 📊 Includes summary statistics and application tracking
- 🎯 Configurable application limits and preferences

## 🛠️ Quick Setup (5 Steps)

### Step 1: Update Your Personal Information

Edit [`config.json`](config.json) and update the `personal_info` section with YOUR details:

```json
"personal_info": {
  "full_name": "Jaydeep Shah",
  "email": "your.email@gmail.com",
  "phone": "+91-XXXXXXXXXX",
  "current_location": "Ahmedabad",
  "linkedin_url": "https://linkedin.com/in/yourprofile",
  "portfolio_url": "",
  "notice_period": "30 days",
  "expected_salary": "As per industry standards"
}
```

### Step 2: Push to GitHub

```bash
cd JavaJobs
git init
git add .
git commit -m "Initial commit: Java job search automation"
git branch -M main
git remote add origin https://github.com/YOUR_USERNAME/YOUR_REPO_NAME.git
git push -u origin main
```

**Note**: Your resume.pdf is protected by .gitignore and won't be pushed to GitHub.

### Step 3: Generate Gmail App Password

1. Go to: https://myaccount.google.com/security
2. Enable **2-Step Verification** (if not already enabled)
3. Scroll down to **App passwords** → Click it
4. Select **Mail** → **Other (Custom name)**
5. Enter: "Job Search Automation"
6. Click **Generate**
7. **Copy the 16-character password** (remove spaces)

### Step 4: Add GitHub Secrets

Go to your GitHub repository:
1. Click **Settings** → **Secrets and variables** → **Actions**
2. Click **New repository secret** and add these 3 secrets:

| Secret Name | Value |
|------------|-------|
| `EMAIL_SENDER` | Your Gmail address (e.g., jaydeep@gmail.com) |
| `EMAIL_PASSWORD` | The 16-character app password from Step 3 |
| `EMAIL_RECEIVER` | Email where you want reports (can be same) |

### Step 5: Test It!

1. Go to **Actions** tab in your repository
2. Click **Job Search Automation**
3. Click **Run workflow** → **Run workflow**
4. Wait 2-3 minutes
5. Check your email! 📧

## ⏰ Automatic Schedule

- **Every Monday at 8:00 AM IST** (2:30 AM UTC)
- Searches for jobs
- Applies to up to 5 jobs automatically
- Emails you the report

## ⚙️ Configuration

### Auto-Apply Settings

Edit [`config.json`](config.json):

```json
"auto_apply": {
  "enabled": true,                          // Set false to disable auto-apply
  "max_applications_per_run": 5,            // Max applications per week
  "resume_path": "resume/resume.pdf",       // Your resume is already here!
  "preferences": {
    "work_mode": ["Remote", "Hybrid", "On-site"],
    "job_type": ["Full-time", "Contract"],
    "skip_companies": []                    // Add companies to skip
  }
}
```

### Job Search Settings

```json
"job_search": {
  "job_title": "Java Developer",
  "experience_years": 5,
  "locations": ["Ahmedabad", "Gandhinagar", "Pune", "Mumbai"],
  "keywords": ["Java", "Spring Boot", "Microservices", "REST API", "J2EE"],
  "max_results_per_location": 10
}
```

## 📁 Project Structure

```
JavaJobs/
├── .github/workflows/
│   └── job-search.yml          # Runs every Monday 8 AM
├── src/
│   ├── job_scraper.py          # Searches for jobs
│   ├── auto_applier.py         # Applies to jobs automatically
│   ├── email_sender.py         # Sends email report
│   └── main.py                 # Orchestrates everything
├── resume/
│   ├── resume.pdf              # ✓ Your resume (already added!)
│   └── cover_letter_template.txt
├── config.json                  # Your configuration
└── README.md                    # This file
```

## 📧 What You'll Receive

Every Monday, you'll get an email with:

1. **📊 Summary**
   - Total jobs found
   - Jobs by location

2. **🤖 Auto-Apply Status**
   - Applications submitted: X
   - Applications failed: Y

3. **💼 Job Listings**
   - Each job shows:
     - Title, Company, Location
     - Experience, Salary
     - ✓ **Application Status** (submitted or pending)
     - Link to view job

## 🎯 How It Works

```
Monday 8 AM IST
    ↓
GitHub Action starts
    ↓
Searches Naukri.com for Java Developer jobs
    ↓
Finds jobs in your preferred locations
    ↓
Automatically applies to up to 5 jobs with your resume
    ↓
Creates detailed report
    ↓
Emails you the report with application status
    ↓
Stops until next Monday
```

## 🔧 Troubleshooting

### No emails received?
- Check GitHub Actions logs (Actions tab)
- Verify secrets are correct
- Check spam folder

### Applications not submitting?
- Some job sites have anti-bot protections
- Check GitHub Actions logs for errors
- You may need to complete some applications manually

### Want to apply to more/fewer jobs?
```json
"max_applications_per_run": 10  // Change this number
```

### Want to skip certain companies?
```json
"skip_companies": ["Company A", "Company B"]
```

### Want different locations?
```json
"locations": ["Bangalore", "Hyderabad", "Delhi"]
```

## ⚠️ Important Notes

- ✅ Your resume is protected (not pushed to GitHub)
- ✅ Email credentials are encrypted as GitHub Secrets
- ✅ Auto-apply works on most job sites, but some may require manual completion
- ✅ Always review the weekly email to track applications
- ✅ You can disable auto-apply anytime by setting `"enabled": false`

## 🎛️ Customization Examples

**Disable Auto-Apply (Just Search)**
```json
"auto_apply": { "enabled": false }
```

**Apply to More Jobs**
```json
"max_applications_per_run": 10
```

**Remote Jobs Only**
```json
"work_mode": ["Remote"]
```

## 📞 Next Steps

1. ✅ Your resume is already added!
2. ✅ Update `personal_info` in config.json
3. ✅ Push to GitHub
4. ✅ Set up GitHub Secrets
5. ✅ Test manually or wait for Monday 8 AM
6. ✅ Check your email for the report
7. ✅ Review applications and follow up

---

**Happy Job Hunting! 🎉**

*Automate your job search, focus on interview preparation!*

**Your resume is ready. Just configure and deploy!**