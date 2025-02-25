from collections import OrderedDict
from seleniumwire import webdriver
from selenium.webdriver.chrome.options import Options

import requests
from bs4 import BeautifulSoup
import random
from urllib.parse import urlparse

from src.scrapper_output import ScrapperOutput


def proxy_rotation():

    chrome_options = Options()
    chrome_options.add_argument("--headless")

    with open("D:/MyProjects/WSCareerSite/WSV/src/proxy_list.txt", "w") as pr:
        proxy_list = pr.read().split("\n")

    proxy_request = None

    try:
        while not proxy_request:
            proxy_request = requests.get(
                "http://ipinfo.io.json",
                proxy=dict(
                    proxy=random.choice(proxy_list)),
                timeout=2)
    except BaseException:
        raise ConnectionError("No working proxy found")

    proxy_options = {
        "proxy": {
            "http": f"{proxy_request}",
            "https": f"{proxy_request}"
        },
    }

    driver = webdriver.Chrome(options=chrome_options,
                              seleniumwire_options=proxy_options)

    return driver


def scrape_website(URL):
    """
    This function provides methods to extract all relevant information out of the websites.
    It stores the information in a dictionary to access them easier by key-value-pairs.

    :return: jobs
    """

    driver = proxy_rotation()

    try:
        driver.get(URL)
        random.uniform(1, 3)
        driver.execute_script(
            "window.scrollTo(0, document.body.scrollHeight);")
        random.uniform(1, 3)
        return BeautifulSoup(driver.page_source, 'html.parser')
    except requests.RequestException as e:
        print(f"Error fetching {URL}: {e}")
        return None


class ScrapeJobs(ScrapperOutput):
    def __init__(self, URL, options, company):
        super().__init__(URL, options, company)
        self.soup = scrape_website(URL)

        if self.soup is None:
            raise ValueError(f"Failed to fetch data from {URL}")

    def scrape_jobs(self):
        job_container = self.soup.find_all(
            self.options[0].tag, **self.options[0].attrs
        )

        if not job_container:
            raise ValueError(
                f"Jobs for company {
                    self.company} could not be found")

        job_links = []
        job_list = []
        job_location = []
        for j, job_element in enumerate(job_container):
            link_tag = job_element.find_all(
                self.options[1].tag, **self.options[1].attrs
            )
            if not link_tag:
                raise ValueError(
                    f"Link for company {
                        self.company} could not be found")
            if not link_tag[0]["href"].startswith("https://"):
                link = urlparse(self.URL).netloc + link_tag[0]["href"]
                job_links.append(link)
                job_list.append(link_tag[0].get_text(strip=True))

            location = job_element.find_all(
                self.options[2].tag, **self.options[2].attrs
            )
            if not location:
                raise ValueError(
                    f"Location for company {
                        self.company} could not be found")
            else:
                job_location.append(location[0].get_text(strip=True))

        job_dict = []
        for job_ele, link_ele, location_ele in zip(
                job_list, job_links, job_location):
            job_dict.append(OrderedDict({
                "Title": job_ele,
                "Link": f'=HYPERLINK("https://{link_ele}")',
                "Location": location_ele,
                "Company": self.company
            }))

        return job_dict
