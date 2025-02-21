import os.path
import csv
from collections import OrderedDict
from seleniumwire import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager

import requests
from bs4 import BeautifulSoup
import random
from urllib.parse import urlparse
import pandas as pd



class ScrapperOutput:
    def __init__(self, CSV_LINK, URL, company, scrape_option):
        self.CSV_LINK = CSV_LINK
        self.company = company
        self.URL = URL
        self.options = scrape_option

    def check_new_entries(self):
        """
        If there is a new entry on a website, it get's tracked and the user gets an information.
        :return:
        """
        if os.path.exists(self.CSV_LINK):
            old_jobs_df = pd.read_csv(self.CSV_LINK,
                                      delimiter=";",
                                      encoding="latin-1",
                                      )
        else:
            old_jobs_df = pd.DataFrame(
                columns=[
                    "Title",
                    "Link",
                    "Location",
                    "Company"])

        self.parse_info(old_jobs_df)

    def parse_info(self, old_jobs_df):

        for i, option in enumerate(self.options):
            instance = ScrapeJobs(self.URL[i], option, self.company[i], self.CSV_LINK)
            new_jobs = instance.scrape_jobs()

            if not new_jobs:
                return

            new_jobs_df = pd.DataFrame(new_jobs)
            merged_df = new_jobs_df.merge(old_jobs_df, on=["Title", "Link", "Location", "Company"], how="left",
                                          indicator=True)

            new_entries = merged_df[merged_df["_merge"]
                                    == "left_only"].drop(columns=["_merge"])
            new_job = new_entries.loc[:, "Title"]

            if not new_job.empty:
                print(
                    f"\n📬 {
                        self.company[i]} hires! These are the new roles: \n {
                        new_job.to_string(
                            index=False)}")
                print("\n Checking...")
            else:
                print(f"\n❌ No new entry for {self.company[i]} at the moment!")
                print("\n Checking...")

            if not new_entries.empty:
                self.write_csv(new_jobs, self.CSV_LINK)

    @staticmethod
    def write_csv(data, CSV_LINK):
        """
        Here a csv-file get's created which stores all relevant information.
        :param data:
        """
        if not os.path.exists(CSV_LINK):
            with open(CSV_LINK, "a", newline="") as csvfile:
                fieldnames = ["Title", "Link", "Location", "Company"]
                writer = csv.DictWriter(
                    csvfile, delimiter=";", fieldnames=fieldnames)
                writer.writeheader()
                writer.writerows(data)
        else:
            with open(CSV_LINK, "a", newline="") as csvfile:
                fieldnames = ["Title", "Link", "Location", "Company"]
                writer = csv.DictWriter(
                    csvfile, delimiter=";", fieldnames=fieldnames)
                writer.writerows(data)


def proxy_rotation():

    chrome_options = Options()
    chrome_options.add_argument("--headless")
    chrome_options.add_argument("--ignore-certificate-errors")
    chrome_options.add_argument("--allow-running-insecure-content")
    chrome_options.add_argument("--disable-web-security")

    with open("D:/MyProjects/WSCareerSite/WSV/src/valid_proxies.txt", "r") as pr:
        proxy_list = pr.read().split("\n")

    proxy = random.choice(proxy_list)
    seleniumwire_options = {
            "proxy":{
                "http": f"http://{proxy}",
                "https": f"https://{proxy}",
                 "no_proxy": "localhost,127.0.0.1"
            },
        }

    driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()),
                            options=chrome_options,
                            seleniumwire_options = seleniumwire_options)

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
    def __init__(self, URL, options, company, CSV_LINK):
        super().__init__(CSV_LINK, URL, options, company)
        self.soup = scrape_website(URL)

        if self.soup is None:
            raise ValueError(f"Failed to fetch data from {URL}")

    def scrape_jobs(self):
        job_container = self.soup.find_all(
            self.options[0].tag, **self.options[0].attrs
        )

        if not job_container:
            raise ValueError(f"Jobs for company {self.company} could not be found")

        job_links = []
        job_list = []
        job_location = []
        for j, job_element in enumerate(job_container):
            link_tag = job_element.find_all(
                self.options[1].tag, **self.options[1].attrs
            )
            if not link_tag:
                raise ValueError (f"Link for company {self.company} could not be found")
            if not link_tag[0]["href"].startswith("https://"):
                link = urlparse(self.URL).netloc + link_tag[0]["href"]
                job_links.append(link)
                job_list.append(link_tag[0].get_text(strip=True))

            location = job_element.find_all(
                self.options[2].tag, **self.options[2].attrs
            )
            if not location:
                raise ValueError (f"Location for company {self.company} could not be found")
            else:
                job_location.append(location[0].get_text(strip=True))

        job_dict = []
        for job_ele, link_ele, location_ele in zip(job_list, job_links, job_location):
            job_dict.append(OrderedDict({
                "Title": job_ele,
                "Link": f'=HYPERLINK("https://{link_ele}")',
                "Location": location_ele,
                "Company": self.company
            }))

        return job_dict
