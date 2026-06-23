import requests
from bs4 import BeautifulSoup
import json
import time
from datetime import datetime, timedelta
from urllib.parse import quote_plus, urljoin
import re

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
            
            # Search multiple sources
            jobs_found = []
            
            # Try Naukri API
            jobs_naukri = self._search_naukri_api(job_title, location, experience, max_results)
            jobs_found.extend(jobs_naukri)
            time.sleep(2)
            
            # Try Indeed
            jobs_indeed = self._search_indeed(job_title, location, max_results)
            jobs_found.extend(jobs_indeed)
            time.sleep(2)
            
            # Try Shine
            jobs_shine = self._search_shine(job_title, location, max_results)
            jobs_found.extend(jobs_shine)
            time.sleep(2)
            
            # If we got actual jobs, add them
            if jobs_found:
                self.jobs.extend(jobs_found)
            else:
                # Add curated search links as fallback
                self.jobs.append(self._create_search_link(job_title, location, 'Naukri.com', experience))
                self.jobs.append(self._create_search_link(job_title, location, 'Indeed', experience))
                self.jobs.append(self._create_search_link(job_title, location, 'LinkedIn', experience))
            
        print(f"\nTotal jobs found: {len(self.jobs)}")
        return self.jobs
    
    def _search_naukri_api(self, job_title, location, experience, max_results):
        """Search Naukri using their API endpoints"""
        jobs = []
        
        try:
            # Naukri's job listing API
            search_query = quote_plus(job_title)
            location_query = quote_plus(location)
            
            # Try multiple URL patterns
            urls = [
                f"https://www.naukri.com/{search_query}-jobs-in-{location_query}?experience={experience}",
                f"https://www.naukri.com/{search_query}-jobs?cityCode={location_query}&experience={experience}",
            ]
            
            headers = {
                'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36',
                'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8',
                'Accept-Language': 'en-US,en;q=0.5',
                'Referer': 'https://www.naukri.com/'
            }
            
            for url in urls:
                try:
                    response = requests.get(url, headers=headers, timeout=15)
                    
                    if response.status_code == 200:
                        soup = BeautifulSoup(response.content, 'html.parser')
                        
                        # Try multiple selectors for job cards
                        job_cards = (
                            soup.find_all('article', class_='jobTuple') or
                            soup.find_all('div', {'class': re.compile('.*job.*tuple.*', re.I)}) or
                            soup.find_all('div', {'class': re.compile('.*srp-jobtuple.*', re.I)})
                        )
                        
                        for card in job_cards[:max_results]:
                            try:
                                # Try multiple ways to extract job URL
                                job_link = None
                                title_elem = None
                                
                                # Method 1: Find title link
                                title_elem = card.find('a', {'class': re.compile('.*title.*', re.I)})
                                if title_elem and title_elem.get('href'):
                                    job_link = title_elem['href']
                                
                                # Method 2: Find any link with job ID
                                if not job_link:
                                    all_links = card.find_all('a', href=True)
                                    for link in all_links:
                                        if 'job-listings' in link['href'] or 'jobId' in link['href']:
                                            job_link = link['href']
                                            title_elem = link
                                            break
                                
                                if job_link and title_elem:
                                    # Ensure full URL
                                    if not job_link.startswith('http'):
                                        job_link = 'https://www.naukri.com' + job_link
                                    
                                    # Extract other details
                                    company_elem = card.find('a', {'class': re.compile('.*company.*|.*subtitle.*', re.I)})
                                    location_elem = card.find('span', {'class': re.compile('.*loc.*', re.I)}) or card.find('li', {'class': re.compile('.*location.*', re.I)})
                                    exp_elem = card.find('span', {'class': re.compile('.*exp.*', re.I)}) or card.find('li', {'class': re.compile('.*experience.*', re.I)})
                                    salary_elem = card.find('span', {'class': re.compile('.*salary.*', re.I)})
                                    
                                    job = {
                                        'title': title_elem.text.strip(),
                                        'company': company_elem.text.strip() if company_elem else 'Company name on site',
                                        'location': location_elem.text.strip() if location_elem else location,
                                        'experience': exp_elem.text.strip() if exp_elem else f'{experience}+ years',
                                        'salary': salary_elem.text.strip() if salary_elem else 'Not disclosed',
                                        'description': 'Click to view full job details',
                                        'url': job_link,
                                        'source': 'Naukri.com',
                                        'search_location': location,
                                        'posted_date': 'Recently posted'
                                    }
                                    jobs.append(job)
                                    
                            except Exception as e:
                                continue
                        
                        if jobs:
                            print(f"  Naukri: Found {len(jobs)} jobs")
                            break
                            
                except Exception as e:
                    continue
                    
        except Exception as e:
            print(f"  Naukri: Error - {str(e)[:50]}")
        
        return jobs
    
    def _search_indeed(self, job_title, location, max_results):
        """Search Indeed India"""
        jobs = []
        
        try:
            search_query = quote_plus(job_title)
            location_query = quote_plus(location)
            
            url = f"https://in.indeed.com/jobs?q={search_query}&l={location_query}&fromage=7&sort=date"
            
            headers = {
                'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36',
                'Accept-Language': 'en-US,en;q=0.9'
            }
            
            response = requests.get(url, headers=headers, timeout=15)
            
            if response.status_code == 200:
                soup = BeautifulSoup(response.content, 'html.parser')
                
                # Find job cards with multiple selectors
                job_cards = (
                    soup.find_all('div', {'class': re.compile('.*job_seen_beacon.*', re.I)}) or
                    soup.find_all('div', {'class': re.compile('.*jobsearch.*card.*', re.I)}) or
                    soup.find_all('td', {'class': 'resultContent'})
                )
                
                for card in job_cards[:max_results]:
                    try:
                        # Find title and link
                        title_elem = card.find('h2', {'class': re.compile('.*jobTitle.*', re.I)}) or card.find('a', {'class': re.compile('.*jcs-JobTitle.*', re.I)})
                        
                        if title_elem:
                            link = title_elem.find('a') if title_elem.name != 'a' else title_elem
                            
                            if link and link.get('href'):
                                job_url = urljoin('https://in.indeed.com', link['href'])
                                
                                company_elem = card.find('span', {'class': re.compile('.*companyName.*', re.I)})
                                location_elem = card.find('div', {'class': re.compile('.*companyLocation.*', re.I)})
                                salary_elem = card.find('div', {'class': re.compile('.*salary.*', re.I)})
                                snippet_elem = card.find('div', {'class': re.compile('.*job-snippet.*', re.I)}) or card.find('div', {'class': 'summary'})
                                
                                job = {
                                    'title': title_elem.text.strip(),
                                    'company': company_elem.text.strip() if company_elem else 'View on Indeed',
                                    'location': location_elem.text.strip() if location_elem else location,
                                    'experience': 'Check job details',
                                    'salary': salary_elem.text.strip() if salary_elem else 'Not disclosed',
                                    'description': snippet_elem.text.strip()[:200] + '...' if snippet_elem else 'Click to view details',
                                    'url': job_url,
                                    'source': 'Indeed',
                                    'search_location': location,
                                    'posted_date': 'Last 7 days'
                                }
                                jobs.append(job)
                    except Exception as e:
                        continue
                
                if jobs:
                    print(f"  Indeed: Found {len(jobs)} jobs")
                    
        except Exception as e:
            print(f"  Indeed: Error - {str(e)[:50]}")
        
        return jobs
    
    def _search_shine(self, job_title, location, max_results):
        """Search Shine.com"""
        jobs = []
        
        try:
            search_query = quote_plus(job_title)
            location_query = quote_plus(location)
            
            url = f"https://www.shine.com/job-search/{search_query}-jobs-in-{location_query}"
            
            headers = {
                'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36'
            }
            
            response = requests.get(url, headers=headers, timeout=15)
            
            if response.status_code == 200:
                soup = BeautifulSoup(response.content, 'html.parser')
                
                job_cards = soup.find_all('div', {'class': re.compile('.*job.*card.*', re.I)}, limit=max_results)
                
                for card in job_cards:
                    try:
                        title_elem = card.find('a', {'class': re.compile('.*job.*title.*', re.I)})
                        
                        if title_elem and title_elem.get('href'):
                            job_url = urljoin('https://www.shine.com', title_elem['href'])
                            
                            company_elem = card.find('div', {'class': re.compile('.*company.*', re.I)})
                            location_elem = card.find('div', {'class': re.compile('.*location.*', re.I)})
                            
                            job = {
                                'title': title_elem.text.strip(),
                                'company': company_elem.text.strip() if company_elem else 'View on Shine',
                                'location': location_elem.text.strip() if location_elem else location,
                                'experience': 'Check job details',
                                'salary': 'Not disclosed',
                                'description': 'Click to view full details',
                                'url': job_url,
                                'source': 'Shine.com',
                                'search_location': location,
                                'posted_date': 'Recently posted'
                            }
                            jobs.append(job)
                    except Exception as e:
                        continue
                
                if jobs:
                    print(f"  Shine: Found {len(jobs)} jobs")
                    
        except Exception as e:
            print(f"  Shine: Error - {str(e)[:50]}")
        
        return jobs
    
    def _create_search_link(self, job_title, location, source, experience):
        """Create a curated search link as fallback"""
        search_query = quote_plus(job_title)
        location_query = quote_plus(location)
        
        if source == 'Naukri.com':
            url = f"https://www.naukri.com/{search_query}-jobs-in-{location_query}?experience={experience}&qp=7"
        elif source == 'Indeed':
            url = f"https://in.indeed.com/jobs?q={search_query}&l={location_query}&fromage=7&sort=date"
        elif source == 'LinkedIn':
            url = f"https://www.linkedin.com/jobs/search?keywords={search_query}&location={location_query}&f_TPR=r604800"
        else:
            url = f"https://www.naukri.com/{search_query}-jobs-in-{location_query}"
        
        return {
            'title': f'{job_title} - {location}',
            'company': 'Multiple Companies',
            'location': location,
            'experience': f'{experience}+ years',
            'salary': 'Varies',
            'description': f'Browse latest {job_title} jobs in {location}. Click to see all current openings.',
            'url': url,
            'source': source,
            'search_location': location,
            'posted_date': 'Updated daily'
        }
    
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
