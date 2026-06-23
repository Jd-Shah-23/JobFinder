import requests
from bs4 import BeautifulSoup
import json
import time
from datetime import datetime, timedelta
from urllib.parse import quote_plus, urljoin

class JobScraper:
    def __init__(self, config):
        self.config = config
        self.jobs = []
        
    def search_jobs(self):
        """Search for jobs across all configured locations and multiple sites"""
        job_title = self.config['job_search']['job_title']
        locations = self.config['job_search']['locations']
        experience = self.config['job_search']['experience_years']
        max_results = self.config['job_search']['max_results_per_location']
        
        print(f"Searching for {job_title} positions with {experience} years experience...")
        
        for location in locations:
            print(f"\nSearching in {location}...")
            
            # Search Naukri.com
            jobs_naukri = self._search_naukri(job_title, location, experience, max_results)
            self.jobs.extend(jobs_naukri)
            time.sleep(2)
            
            # Search Indeed
            jobs_indeed = self._search_indeed(job_title, location, max_results)
            self.jobs.extend(jobs_indeed)
            time.sleep(2)
            
            # Search LinkedIn (basic)
            jobs_linkedin = self._search_linkedin(job_title, location, max_results)
            self.jobs.extend(jobs_linkedin)
            time.sleep(2)
            
        print(f"\nTotal jobs found: {len(self.jobs)}")
        return self.jobs
    
    def _search_naukri(self, job_title, location, experience, max_results):
        """Search jobs on Naukri.com"""
        jobs = []
        
        try:
            search_query = quote_plus(job_title)
            location_query = quote_plus(location)
            
            # Naukri API-like URL with filters
            url = f"https://www.naukri.com/{search_query}-jobs-in-{location_query}?experience={experience}"
            
            headers = {
                'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36'
            }
            
            response = requests.get(url, headers=headers, timeout=15)
            
            if response.status_code == 200:
                soup = BeautifulSoup(response.content, 'html.parser')
                
                # Find job listings
                job_cards = soup.find_all('article', class_='jobTuple', limit=max_results)
                
                if not job_cards:
                    job_cards = soup.find_all('div', class_='srp-jobtuple-wrapper', limit=max_results)
                
                for card in job_cards[:max_results]:
                    try:
                        # Extract job details
                        title_elem = card.find('a', class_='title') or card.find('a', {'class': 'title'})
                        company_elem = card.find('a', class_='subTitle') or card.find('div', class_='companyInfo')
                        experience_elem = card.find('span', class_='expwdth') or card.find('li', class_='fleft experience')
                        location_elem = card.find('span', class_='locWdth') or card.find('li', class_='fleft location')
                        salary_elem = card.find('span', class_='salaryWdth')
                        desc_elem = card.find('div', class_='job-description') or card.find('div', class_='row7')
                        
                        if title_elem and title_elem.get('href'):
                            job_url = title_elem['href']
                            if not job_url.startswith('http'):
                                job_url = 'https://www.naukri.com' + job_url
                            
                            job = {
                                'title': title_elem.text.strip(),
                                'company': company_elem.text.strip() if company_elem else 'Not specified',
                                'location': location_elem.text.strip() if location_elem else location,
                                'experience': experience_elem.text.strip() if experience_elem else f'{experience}+ years',
                                'salary': salary_elem.text.strip() if salary_elem else 'Not disclosed',
                                'description': desc_elem.text.strip()[:200] + '...' if desc_elem else 'View job for details',
                                'url': job_url,
                                'source': 'Naukri.com',
                                'search_location': location,
                                'posted_date': 'Recently posted'
                            }
                            jobs.append(job)
                    except Exception as e:
                        continue
                
                print(f"  Naukri: Found {len(jobs)} jobs")
                
        except Exception as e:
            print(f"  Naukri: Error - {str(e)[:50]}")
        
        return jobs
    
    def _search_indeed(self, job_title, location, max_results):
        """Search jobs on Indeed India"""
        jobs = []
        
        try:
            search_query = quote_plus(job_title)
            location_query = quote_plus(location)
            
            url = f"https://in.indeed.com/jobs?q={search_query}&l={location_query}&fromage=7"
            
            headers = {
                'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36'
            }
            
            response = requests.get(url, headers=headers, timeout=15)
            
            if response.status_code == 200:
                soup = BeautifulSoup(response.content, 'html.parser')
                
                # Find job cards
                job_cards = soup.find_all('div', class_='job_seen_beacon', limit=max_results)
                
                if not job_cards:
                    job_cards = soup.find_all('div', class_='jobsearch-SerpJobCard', limit=max_results)
                
                for card in job_cards[:max_results]:
                    try:
                        title_elem = card.find('h2', class_='jobTitle') or card.find('a', class_='jcs-JobTitle')
                        company_elem = card.find('span', class_='companyName')
                        location_elem = card.find('div', class_='companyLocation')
                        salary_elem = card.find('div', class_='salary-snippet')
                        snippet_elem = card.find('div', class_='job-snippet')
                        
                        if title_elem:
                            link = title_elem.find('a')
                            if link and link.get('href'):
                                job_url = urljoin('https://in.indeed.com', link['href'])
                                
                                job = {
                                    'title': title_elem.text.strip(),
                                    'company': company_elem.text.strip() if company_elem else 'Not specified',
                                    'location': location_elem.text.strip() if location_elem else location,
                                    'experience': 'Check job details',
                                    'salary': salary_elem.text.strip() if salary_elem else 'Not disclosed',
                                    'description': snippet_elem.text.strip()[:200] + '...' if snippet_elem else 'View job for details',
                                    'url': job_url,
                                    'source': 'Indeed',
                                    'search_location': location,
                                    'posted_date': 'Last 7 days'
                                }
                                jobs.append(job)
                    except Exception as e:
                        continue
                
                print(f"  Indeed: Found {len(jobs)} jobs")
                
        except Exception as e:
            print(f"  Indeed: Error - {str(e)[:50]}")
        
        return jobs
    
    def _search_linkedin(self, job_title, location, max_results):
        """Search jobs on LinkedIn"""
        jobs = []
        
        try:
            search_query = quote_plus(job_title)
            location_query = quote_plus(location)
            
            # LinkedIn jobs URL
            url = f"https://www.linkedin.com/jobs/search?keywords={search_query}&location={location_query}&f_TPR=r604800"
            
            headers = {
                'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36'
            }
            
            response = requests.get(url, headers=headers, timeout=15)
            
            if response.status_code == 200:
                soup = BeautifulSoup(response.content, 'html.parser')
                
                # Find job cards
                job_cards = soup.find_all('div', class_='base-card', limit=max_results)
                
                if not job_cards:
                    job_cards = soup.find_all('li', class_='jobs-search-results__list-item', limit=max_results)
                
                for card in job_cards[:max_results]:
                    try:
                        title_elem = card.find('h3', class_='base-search-card__title')
                        company_elem = card.find('h4', class_='base-search-card__subtitle')
                        location_elem = card.find('span', class_='job-search-card__location')
                        link_elem = card.find('a', class_='base-card__full-link')
                        
                        if title_elem and link_elem and link_elem.get('href'):
                            job = {
                                'title': title_elem.text.strip(),
                                'company': company_elem.text.strip() if company_elem else 'Not specified',
                                'location': location_elem.text.strip() if location_elem else location,
                                'experience': 'Check job details',
                                'salary': 'Not disclosed',
                                'description': 'View job for full details',
                                'url': link_elem['href'],
                                'source': 'LinkedIn',
                                'search_location': location,
                                'posted_date': 'Last 7 days'
                            }
                            jobs.append(job)
                    except Exception as e:
                        continue
                
                print(f"  LinkedIn: Found {len(jobs)} jobs")
                
        except Exception as e:
            print(f"  LinkedIn: Error - {str(e)[:50]}")
        
        return jobs
    
    def get_jobs_summary(self):
        """Get summary statistics of found jobs"""
        if not self.jobs:
            return "No jobs found"
        
        summary = {
            'total_jobs': len(self.jobs),
            'by_location': {},
            'by_company': {},
            'by_source': {}
        }
        
        for job in self.jobs:
            loc = job.get('search_location', 'Unknown')
            company = job.get('company', 'Unknown')
            source = job.get('source', 'Unknown')
            
            summary['by_location'][loc] = summary['by_location'].get(loc, 0) + 1
            summary['by_company'][company] = summary['by_company'].get(company, 0) + 1
            summary['by_source'][source] = summary['by_source'].get(source, 0) + 1
        
        return summary

# Made with Bob
