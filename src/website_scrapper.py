import re
from collections import OrderedDict
from selenium import webdriver
from selenium.webdriver.chrome.options import Options

import requests
from bs4 import BeautifulSoup


chrome_options = Options()
chrome_options.add_argument("--headless=new")
driver = webdriver.Chrome(options=chrome_options)


def scrape_website(URL):
    """
    This function provides methods to extract all relevant information out of the websites.
    It stores the information in a dictionary to access them easier by key-value-pairs.

    :return: jobs
    """

    try:
        driver.get(URL)
        driver.execute_script(
            "window.scrollTo(0, document.body.scrollHeight);")
        return BeautifulSoup(driver.page_source, 'html.parser')
    except requests.RequestException as e:
        print(f"Error fetching {URL}: {e}")
        return None


class ScrapeJobs:
    def __init__(self, URL, options):
        self.soup = scrape_website(URL)
        self.URL = URL
        self.options = options

        if self.soup is None:
            raise ValueError(f"Failed to fetch data from {URL}")

    def scrape_jobs(self):
        job_container = self.soup.find_all(
            self.options[0].tag, **self.options[0].attrs
        )

        job_links = []
        job_location = []
        for job_element in job_container:
            link = job_element.find_all(
                self.options[1].tag, **self.options[1].attrs
            )
            location = job_element.find_all(
                self.options[2].tag, **self.options[2].attrs
            )

            job_links.append(link)
            job_location.append(location)

        job_company = re.search(r'https?://([^/]+)\.', self.URL)

        job_dict = []
        for job, location in zip(job_links, job_location):
            job_dict.append(OrderedDict({
                "Title": job[0].get_text(),
                "Link": f'=HYPERLINK("https://{job_company[1] + ".jobs" + job[0]["href"]}")',
                "Location": location[0].get_text(strip=True),
                "Company": job_company[1]
            }))

        return job_dict
