import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from datetime import datetime
import os

class EmailSender:
    def __init__(self, config):
        self.config = config
        self.sender_email = os.environ.get('EMAIL_SENDER')
        self.sender_password = os.environ.get('EMAIL_PASSWORD')
        self.receiver_email = os.environ.get('EMAIL_RECEIVER')
        
    def send_job_report(self, jobs, summary, application_summary=None):
        """Send email with job search results and application status"""
        if not self.sender_email or not self.sender_password or not self.receiver_email:
            print("Error: Email credentials not found in environment variables")
            return False
        
        try:
            # Create message
            message = MIMEMultipart("alternative")
            current_date = datetime.now().strftime("%B %d, %Y")
            subject = self.config['email']['subject'].format(date=current_date)
            message["Subject"] = subject
            message["From"] = self.sender_email
            message["To"] = self.receiver_email
            
            # Create HTML content
            html_content = self._create_html_report(jobs, summary, current_date, application_summary)
            
            # Attach HTML content
            html_part = MIMEText(html_content, "html")
            message.attach(html_part)
            
            # Send email
            print(f"Sending email to {self.receiver_email}...")
            with smtplib.SMTP_SSL("smtp.gmail.com", 465) as server:
                server.login(self.sender_email, self.sender_password)
                server.sendmail(self.sender_email, self.receiver_email, message.as_string())
            
            print("Email sent successfully!")
            return True
            
        except Exception as e:
            print(f"Error sending email: {e}")
            return False
    
    def _create_html_report(self, jobs, summary, date, application_summary=None):
        """Create HTML formatted email report with application status"""
        html = f"""
        <html>
        <head>
            <style>
                body {{
                    font-family: Arial, sans-serif;
                    line-height: 1.6;
                    color: #333;
                    max-width: 800px;
                    margin: 0 auto;
                    padding: 20px;
                }}
                h1 {{
                    color: #2c3e50;
                    border-bottom: 3px solid #3498db;
                    padding-bottom: 10px;
                }}
                h2 {{
                    color: #34495e;
                    margin-top: 30px;
                }}
                .summary {{
                    background-color: #ecf0f1;
                    padding: 15px;
                    border-radius: 5px;
                    margin: 20px 0;
                }}
                .job-card {{
                    border: 1px solid #ddd;
                    border-radius: 5px;
                    padding: 15px;
                    margin: 15px 0;
                    background-color: #fff;
                    box-shadow: 0 2px 4px rgba(0,0,0,0.1);
                }}
                .job-title {{
                    color: #2980b9;
                    font-size: 18px;
                    font-weight: bold;
                    margin-bottom: 10px;
                }}
                .job-company {{
                    color: #27ae60;
                    font-weight: bold;
                }}
                .job-details {{
                    color: #7f8c8d;
                    font-size: 14px;
                    margin: 5px 0;
                }}
                .apply-button {{
                    display: inline-block;
                    background-color: #3498db;
                    color: white;
                    padding: 10px 20px;
                    text-decoration: none;
                    border-radius: 5px;
                    margin-top: 10px;
                }}
                .apply-button:hover {{
                    background-color: #2980b9;
                }}
                .footer {{
                    margin-top: 40px;
                    padding-top: 20px;
                    border-top: 1px solid #ddd;
                    color: #7f8c8d;
                    font-size: 12px;
                }}
            </style>
        </head>
        <body>
            <h1>🚀 Java Developer Job Report</h1>
            <p><strong>Report Date:</strong> {date}</p>
        """
        
        # Add summary if enabled
        if self.config['email']['include_summary'] and summary:
            html += f"""
            <div class="summary">
                <h2>📊 Summary</h2>
                <p><strong>Total Jobs Found:</strong> {summary['total_jobs']}</p>
                
                <p><strong>Jobs by Source:</strong></p>
                <ul>
            """
            for source, count in summary.get('by_source', {}).items():
                html += f"<li>{source}: {count} jobs</li>"
            html += """
                </ul>
                
                <p><strong>Jobs by Location:</strong></p>
                <ul>
            """
            for location, count in summary['by_location'].items():
                html += f"<li>{location}: {count} jobs</li>"
            html += """
                </ul>
            """
            
            # Add application summary if auto-apply was used
            if application_summary and self.config['email'].get('include_application_status', True):
                html += f"""
                <h3>🤖 Auto-Apply Status</h3>
                <p><strong>Applications Submitted:</strong> {application_summary['total_applied']}</p>
                <p><strong>Applications Failed:</strong> {application_summary['total_failed']}</p>
                """
            
            html += """
            </div>
            """
        
        # Add job listings
        html += "<h2>💼 Job Listings</h2>"
        
        if not jobs:
            html += "<p>No jobs found this week. Try adjusting your search criteria.</p>"
        else:
            # Mark which jobs were applied to
            applied_urls = []
            if application_summary:
                applied_urls = [j.get('url') for j in application_summary.get('applied_jobs', [])]
            
            for job in jobs:
                job_url = job.get('url', '')
                was_applied = job_url in applied_urls
                
                html += f"""
                <div class="job-card">
                    <div class="job-title">{job.get('title', 'N/A')}</div>
                    <div class="job-company">🏢 {job.get('company', 'N/A')}</div>
                    <div class="job-details">📍 Location: {job.get('location', 'N/A')}</div>
                    <div class="job-details">💼 Experience: {job.get('experience', 'N/A')}</div>
                    <div class="job-details">💰 Salary: {job.get('salary', 'Not disclosed')}</div>
                    <div class="job-details">🌐 Source: {job.get('source', 'N/A')}</div>
                    <div class="job-details">📅 Posted: {job.get('posted_date', 'Recently')}</div>
                """
                
                # Show job description if available
                if job.get('description'):
                    html += f'<div class="job-details" style="margin-top: 10px; font-style: italic;">{job["description"]}</div>'
                
                if was_applied:
                    html += '<div class="job-details" style="color: #27ae60; font-weight: bold;">✓ Application Submitted</div>'
                
                if job.get('note'):
                    html += f'<div class="job-details"><em>Note: {job["note"]}</em></div>'
                
                html += f"""
                    <a href="{job_url}" class="apply-button" target="_blank">View Job</a>
                </div>
                """
        
        # Add footer
        html += """
            <div class="footer">
                <p>This is an automated report generated by your Job Search Automation system.</p>
                <p>To modify search criteria, update the config.json file in your repository.</p>
            </div>
        </body>
        </html>
        """
        
        return html

# Made with Bob
