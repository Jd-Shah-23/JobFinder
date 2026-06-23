import json
import sys
from job_scraper import JobScraper
from email_sender import EmailSender
from auto_applier import AutoApplier

def load_config():
    """Load configuration from config.json"""
    try:
        with open('config.json', 'r') as f:
            return json.load(f)
    except FileNotFoundError:
        print("Error: config.json not found")
        sys.exit(1)
    except json.JSONDecodeError:
        print("Error: Invalid JSON in config.json")
        sys.exit(1)

def main():
    """Main function to orchestrate job search, auto-apply, and email sending"""
    print("=" * 60)
    print("Java Developer Job Search & Auto-Apply Automation")
    print("=" * 60)
    
    # Load configuration
    config = load_config()
    print("\n✓ Configuration loaded")
    
    # Initialize job scraper
    scraper = JobScraper(config)
    
    # Search for jobs
    print("\n" + "=" * 60)
    print("Starting job search...")
    print("=" * 60)
    jobs = scraper.search_jobs()
    
    # Get summary
    summary = scraper.get_jobs_summary()
    
    # Display search results
    print("\n" + "=" * 60)
    print("Search Results")
    print("=" * 60)
    if summary and isinstance(summary, dict):
        print(f"\nTotal jobs found: {summary['total_jobs']}")
        print("\nJobs by location:")
        for location, count in summary['by_location'].items():
            print(f"  - {location}: {count}")
    
    # Auto-apply to jobs if enabled
    application_summary = None
    if config.get('auto_apply', {}).get('enabled', False):
        print("\n" + "=" * 60)
        print("Starting auto-apply process...")
        print("=" * 60)
        
        auto_applier = AutoApplier(config)
        applied_jobs, failed_jobs = auto_applier.apply_to_jobs(jobs)
        application_summary = auto_applier.get_application_summary()
        
        print(f"\n✓ Auto-apply completed")
        print(f"  Applications submitted: {len(applied_jobs)}")
        print(f"  Applications failed: {len(failed_jobs)}")
    else:
        print("\n⊘ Auto-apply is disabled")
    
    # Send email report
    print("\n" + "=" * 60)
    print("Sending email report...")
    print("=" * 60)
    email_sender = EmailSender(config)
    success = email_sender.send_job_report(jobs, summary, application_summary)
    
    if success:
        print("\n✓ Job search completed successfully!")
        print("✓ Email report sent!")
    else:
        print("\n✗ Failed to send email report")
        sys.exit(1)
    
    print("\n" + "=" * 60)
    print("Automation Complete")
    print("=" * 60)

if __name__ == "__main__":
    main()

# Made with Bob
