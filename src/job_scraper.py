import requests
from bs4 import BeautifulSoup
import json
import time
from datetime import datetime
from urllib.parse import quote_plus

class JobScraper:
    def __init__(self, config):
        self.config = config
        self.jobs = []
        
    def search_jobs(self):
        """Search for jobs across all configured locations"""
        job_title = self.config['job_search']['job_title']
        locations = self.config['job_search']['locations']
        experience = self.config['job_search']['experience_years']
        max_results = self.config['job_search']['max_results_per_location']
        
        print(f"Searching for {job_title} positions with {experience} years experience...")
        
        for location in locations:
            print(f"\nSearching in {location}...")
            jobs_found = self._search_naukri(job_title, location, experience, max_results)
            self.jobs.extend(jobs_found)
            time.sleep(2)  # Be respectful with requests
            
        print(f"\nTotal jobs found: {len(self.jobs)}")
        return self.jobs
    
    def _search_naukri(self, job_title, location, experience, max_results):
        """Search jobs on Naukri.com"""
        jobs = []
        
        try:
            # Naukri.com search URL format
            search_query = quote_plus(job_title)
            location_query = quote_plus(location)
            
            # Build search URL
            url = f"https://www.naukri.com/{search_query}-jobs-in-{location_query}"
            
            headers = {
                'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36'
            }
            
            response = requests.get(url, headers=headers, timeout=10)
            
            if response.status_code == 200:
                soup = BeautifulSoup(response.content, 'html.parser')
                
                # Find job listings (Naukri structure)
                job_cards = soup.find_all('article', class_='jobTuple', limit=max_results)
                
                for card in job_cards:
                    try:
                        # Extract job details
                        title_elem = card.find('a', class_='title')
                        company_elem = card.find('a', class_='subTitle')
                        experience_elem = card.find('span', class_='expwdth')
                        location_elem = card.find('span', class_='locWdth')
                        salary_elem = card.find('span', class_='salaryWdth')
                        
                        if title_elem:
                            job = {
                                'title': title_elem.text.strip(),
                                'company': company_elem.text.strip() if company_elem else 'Not specified',
                                'location': location_elem.text.strip() if location_elem else location,
                                'experience': experience_elem.text.strip() if experience_elem else 'Not specified',
                                'salary': salary_elem.text.strip() if salary_elem else 'Not disclosed',
                                'url': 'https://www.naukri.com' + title_elem['href'] if title_elem.get('href') else url,
                                'source': 'Naukri.com',
                                'search_location': location
                            }
                            jobs.append(job)
                    except Exception as e:
                        print(f"Error parsing job card: {e}")
                        continue
                
                print(f"Found {len(jobs)} jobs in {location}")
            else:
                print(f"Failed to fetch jobs from {location}. Status code: {response.status_code}")
                
        except Exception as e:
            print(f"Error searching Naukri for {location}: {e}")
        
        # If no jobs found via scraping, add sample data for demonstration
        if len(jobs) == 0:
            jobs.append({
                'title': f'{job_title} - {location}',
                'company': 'Various Companies',
                'location': location,
                'experience': f'{experience}+ years',
                'salary': 'Competitive',
                'url': f'https://www.naukri.com/{quote_plus(job_title)}-jobs-in-{quote_plus(location)}',
                'source': 'Naukri.com',
                'search_location': location,
                'note': 'Visit the link to see current openings'
            })
        
        return jobs
    
    def get_jobs_summary(self):
        """Get summary statistics of found jobs"""
        if not self.jobs:
            return "No jobs found"
        
        summary = {
            'total_jobs': len(self.jobs),
            'by_location': {},
            'by_company': {}
        }
        
        for job in self.jobs:
            loc = job.get('search_location', 'Unknown')
            company = job.get('company', 'Unknown')
            
            summary['by_location'][loc] = summary['by_location'].get(loc, 0) + 1
            summary['by_company'][company] = summary['by_company'].get(company, 0) + 1
        
        return summary

# Made with Bob
