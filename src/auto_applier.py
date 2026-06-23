from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager
import time
import os

class AutoApplier:
    def __init__(self, config):
        self.config = config
        self.auto_apply_config = config.get('auto_apply', {})
        self.applied_jobs = []
        self.failed_applications = []
        self.driver = None
        
    def initialize_browser(self):
        """Initialize headless Chrome browser"""
        try:
            chrome_options = Options()
            chrome_options.add_argument('--headless')
            chrome_options.add_argument('--no-sandbox')
            chrome_options.add_argument('--disable-dev-shm-usage')
            chrome_options.add_argument('--disable-gpu')
            chrome_options.add_argument('--window-size=1920,1080')
            chrome_options.add_argument('user-agent=Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36')
            
            service = Service(ChromeDriverManager().install())
            self.driver = webdriver.Chrome(service=service, options=chrome_options)
            print("✓ Browser initialized successfully")
            return True
        except Exception as e:
            print(f"✗ Failed to initialize browser: {e}")
            return False
    
    def close_browser(self):
        """Close the browser"""
        if self.driver:
            self.driver.quit()
            print("✓ Browser closed")
    
    def apply_to_jobs(self, jobs):
        """Apply to jobs automatically"""
        if not self.auto_apply_config.get('enabled', False):
            print("Auto-apply is disabled in config")
            return self.applied_jobs, self.failed_applications
        
        max_applications = self.auto_apply_config.get('max_applications_per_run', 5)
        resume_path = self.auto_apply_config.get('resume_path', '')
        
        # Check if resume exists
        if not os.path.exists(resume_path):
            print(f"✗ Resume not found at: {resume_path}")
            print("Please add your resume to the specified path")
            return self.applied_jobs, self.failed_applications
        
        # Initialize browser
        if not self.initialize_browser():
            return self.applied_jobs, self.failed_applications
        
        print(f"\n{'='*60}")
        print(f"Starting auto-apply process (max {max_applications} applications)")
        print(f"{'='*60}\n")
        
        applications_count = 0
        
        for job in jobs:
            if applications_count >= max_applications:
                print(f"\n✓ Reached maximum applications limit ({max_applications})")
                break
            
            # Skip if company is in skip list
            skip_companies = self.auto_apply_config.get('preferences', {}).get('skip_companies', [])
            if job.get('company') in skip_companies:
                print(f"⊘ Skipping {job.get('company')} (in skip list)")
                continue
            
            print(f"\n[{applications_count + 1}/{max_applications}] Applying to:")
            print(f"  Title: {job.get('title')}")
            print(f"  Company: {job.get('company')}")
            print(f"  Location: {job.get('location')}")
            
            success = self._apply_to_single_job(job, resume_path)
            
            if success:
                applications_count += 1
                self.applied_jobs.append(job)
                print(f"  ✓ Application submitted successfully")
            else:
                self.failed_applications.append(job)
                print(f"  ✗ Application failed")
            
            # Wait between applications to avoid rate limiting
            time.sleep(3)
        
        self.close_browser()
        
        print(f"\n{'='*60}")
        print(f"Auto-apply Summary:")
        print(f"  Successful: {len(self.applied_jobs)}")
        print(f"  Failed: {len(self.failed_applications)}")
        print(f"{'='*60}\n")
        
        return self.applied_jobs, self.failed_applications
    
    def _apply_to_single_job(self, job, resume_path):
        """Apply to a single job"""
        try:
            url = job.get('url', '')
            if not url:
                return False
            
            # Navigate to job page
            self.driver.get(url)
            time.sleep(2)
            
            # Try to find and click apply button
            apply_button_selectors = [
                "//button[contains(text(), 'Apply')]",
                "//a[contains(text(), 'Apply')]",
                "//button[contains(@class, 'apply')]",
                "//a[contains(@class, 'apply')]",
                "//button[@id='apply-button']",
                "//a[@id='apply-button']"
            ]
            
            apply_button = None
            for selector in apply_button_selectors:
                try:
                    apply_button = WebDriverWait(self.driver, 5).until(
                        EC.element_to_be_clickable((By.XPATH, selector))
                    )
                    if apply_button:
                        break
                except:
                    continue
            
            if not apply_button:
                print("  ⚠ Apply button not found - may require manual application")
                return False
            
            # Click apply button
            apply_button.click()
            time.sleep(2)
            
            # Try to fill in application form
            personal_info = self.auto_apply_config.get('personal_info', {})
            
            # Fill name
            self._fill_field_by_labels(['name', 'full name', 'your name'], personal_info.get('full_name', ''))
            
            # Fill email
            self._fill_field_by_labels(['email', 'e-mail'], personal_info.get('email', ''))
            
            # Fill phone
            self._fill_field_by_labels(['phone', 'mobile', 'contact'], personal_info.get('phone', ''))
            
            # Upload resume
            self._upload_resume(resume_path)
            
            # Try to submit
            submit_selectors = [
                "//button[contains(text(), 'Submit')]",
                "//button[contains(text(), 'Apply')]",
                "//button[@type='submit']",
                "//input[@type='submit']"
            ]
            
            for selector in submit_selectors:
                try:
                    submit_button = self.driver.find_element(By.XPATH, selector)
                    submit_button.click()
                    time.sleep(2)
                    return True
                except:
                    continue
            
            # If we reach here, we couldn't submit
            print("  ⚠ Could not find submit button")
            return False
            
        except Exception as e:
            print(f"  ✗ Error during application: {str(e)[:100]}")
            return False
    
    def _fill_field_by_labels(self, labels, value):
        """Try to fill a field by searching for various label texts"""
        if not value:
            return False
        
        for label in labels:
            try:
                # Try by placeholder
                field = self.driver.find_element(By.XPATH, f"//input[contains(@placeholder, '{label}')]")
                field.clear()
                field.send_keys(value)
                return True
            except:
                pass
            
            try:
                # Try by name attribute
                field = self.driver.find_element(By.XPATH, f"//input[contains(@name, '{label}')]")
                field.clear()
                field.send_keys(value)
                return True
            except:
                pass
        
        return False
    
    def _upload_resume(self, resume_path):
        """Try to upload resume"""
        try:
            # Look for file input
            file_inputs = self.driver.find_elements(By.XPATH, "//input[@type='file']")
            
            for file_input in file_inputs:
                try:
                    # Get absolute path
                    abs_resume_path = os.path.abspath(resume_path)
                    file_input.send_keys(abs_resume_path)
                    time.sleep(1)
                    return True
                except:
                    continue
            
            return False
        except Exception as e:
            print(f"  ⚠ Could not upload resume: {str(e)[:50]}")
            return False
    
    def get_application_summary(self):
        """Get summary of applications"""
        return {
            'total_applied': len(self.applied_jobs),
            'total_failed': len(self.failed_applications),
            'applied_jobs': self.applied_jobs,
            'failed_jobs': self.failed_applications
        }

# Made with Bob
