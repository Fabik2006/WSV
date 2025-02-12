import os.path

import requests
from bs4 import BeautifulSoup
from collections import OrderedDict
import csv
import schedule
import time
import re
import pandas as pd

URL = {
    "Bertrandt": "https://bertrandtgroup.onlyfy.jobs/"
}
CSV_LINK = "job_opportunities.csv"


def scrape_jobs():
    """
    This function provides methods to extract all relevant information out of the websites.
    It stores the information in a dictionary to access them easier by key-value-pairs.

    :return: jobs
    """
    response = requests.get(URL["Bertrandt"])
    soup = BeautifulSoup(response.content, "html.parser")
    job_elements = soup.find_all("div", id="jobList")
    job_links = job_elements[0].find_all("a", href=True)
    job_location = soup.find_all("div", attrs={"class": "inner", "style": "white-space: normal;"})
    jobs = []
    company = re.search(r'/([^/]+)\.', URL["Bertrandt"])
    for job, location in zip(job_links, job_location):
        jobs.append(OrderedDict({
            "Title": job.get_text(),
            "Link": f'=HYPERLINK("https://{company[1] + ".jobs" + job["href"]}")',
            "Location": location.get_text(strip=True),
            "Company": company[1]
        }))

    return jobs


def check_new_entries():
    """
    If there is a new entry on a website, it get's tracked and the user gets an information.
    :return:
    """
    if os.path.exists(CSV_LINK):
        old_jobs_df = pd.read_csv(CSV_LINK,
                                  delimiter=";",
                                  encoding="latin-1",
                                  )
    else:
        old_jobs_df = pd.DataFrame(columns=["Title, Link"])

    new_jobs = scrape_jobs()
    if not new_jobs:
        return

    new_jobs_df = pd.DataFrame(new_jobs)
    merged_df = new_jobs_df.merge(old_jobs_df, on=["Title", "Link", "Location", "Company"], how="left",
                                  indicator=True)

    new_entries = merged_df[merged_df["_merge"] == "left_only"].drop(columns=["_merge"])
    new_job_title = new_entries.iloc[:, 0].to_string(index=False)
    new_job_company = new_entries.iloc[:, 2].to_string(index=False)
    if not new_entries.empty:
        print(f"\n📬 {new_job_company} hire! This is the role: {new_job_title}")
        print("\n Checking...")
    else:
        print("\n❌ No new entry at the moment!")
        print("\n Checking...")

    write_csv(new_jobs)


def write_csv(data):
    """
    Here a csv-file get's created which stores all relevant information.
    :param data:
    """
    with open(CSV_LINK, "w", newline='') as csvfile:
        fieldnames = ["Title", "Link", "Location", "Company"]
        writer = csv.DictWriter(csvfile, delimiter=";", fieldnames=fieldnames)
        writer.writeheader()
        writer.writerows(data)


schedule.every(1).minute.do(check_new_entries)

print(f"Job scrapper is running on ... Press Ctrl+C to stop")

while True:
    schedule.run_pending()
    time.sleep(60)
