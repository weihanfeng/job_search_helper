import re
from joblib import Parallel, delayed
import numpy as np
from urllib.parse import urljoin
from selenium import webdriver
from bs4 import BeautifulSoup
from datetime import datetime

class GetJobOpenings:
    """Scrape job openings from a website"""
    
    def __init__(self, website, query, num_results):
        self.website = website
        self.query = query
        self.num_results = num_results
    
    def get_job_openings(self):
        if self.website == "mcf":
            return self._get_job_openings_mcf()
    
    def _get_job_openings_mcf(self):
        pass

class MCFScraper:
    def __init__(self, job_title, main_url, base_post_url):
        self.job_title = job_title
        self.main_url = main_url
        self.base_post_url = base_post_url

    def extract_html_text(self, soup, element, attribute):
        result = soup.find(element, attribute)
        try:
            result = result.text
        except:
            result = "Not found"

        return result

    def configure_driver(self):
        options = webdriver.EdgeOptions()
        options.add_argument("headless")
        driver = webdriver.Edge("../msedgedriver.exe", options=options)
        return driver

    def convert_date(self, date):
        try:
            date = datetime.strptime(date, "%d %b %Y")
        except:
            date = np.nan

        return date

    def get_job_urls(self, page):
        driver = self.configure_driver()
        formatted_job_title = re.sub(" ", "%20", self.job_title)
        driver.get(self.main_url.format(formatted_job_title, page))

        # Get the HTML content of the page
        html_content = driver.page_source
        # Parse the HTML content with BeautifulSoup
        soup = BeautifulSoup(html_content, 'html.parser')
        # Find the elements which contains url 
        target_elements = soup.find_all('a', attrs={"data-testid":'job-card-link'}, href=True)
        # Extract the urls from the elements
        hrefs = []
        for target_element in target_elements:
            href = urljoin(self.base_post_url, target_element['href'])
            hrefs.append(href)
        
        return hrefs

    def get_job_details(self, url):
        driver = self.configure_driver()
        driver.get(url)

        html_content = driver.page_source

        # Parse the HTML content with BeautifulSoup
        soup = BeautifulSoup(html_content, 'html.parser')

        result = {}
        # Find elements
        result['title'] = self.extract_html_text(soup, None, {"id": "job_title"})
        result['company'] = self.extract_html_text(soup, None, {"data-testid": "company-hire-info"})
        result['address'] = self.extract_html_text(soup, None, {"id": "address"})
        result['experience'] = self.extract_html_text(soup, None, {"id": "min_experience"})
        result['category'] = self.extract_html_text(soup, None, {"id": "job-categories"})
        salary_range = re.sub(r"\$", r"", self.extract_html_text(soup, None, {"data-testid": "salary-range"})).split("to")
        result['salary_min'] = int(re.sub(r"\,", r"", salary_range[0])) if len(salary_range) > 1 else np.nan
        result['salary_max'] = int(re.sub(r"\,", r"", salary_range[1])) if len(salary_range) > 1 else np.nan
        result['posted'] = self.convert_date(self.extract_html_text(soup, None, {"id": "last_posted_date"}).strip("Posted"))
        result['closing'] = self.convert_date(self.extract_html_text(soup, None, {"id": "expiry_date"}).strip("Closing on "))
        num_applications = self.extract_html_text(soup, None, {"id": "num_of_applications"})
        num_applications = re.search(r'\d+', num_applications)
        result['num_applications'] = int(num_applications.group(0)) if num_applications else np.nan
        result['description'] = self.extract_html_text(soup, None, {"id": "description-content"})

        driver.quit()

        return result