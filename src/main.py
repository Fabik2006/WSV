import os.path
import csv

import schedule
import time
import pandas as pd

from websites_to_scrap import scrape_options
from website_scrapper import ScrapeJobs

CSV_LINK = "job_opportunities.csv"

class writecsv():
    def __init__(self, CSV_LINK, URL, company, scrape_option):
        self.CSV_LINK = CSV_LINK
        self.company = company
        self.URL = URL
        self.option = scrape_option

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
            old_jobs_df = pd.DataFrame(columns=["Title", "Link", "Location", "Company"])


        for i, option in enumerate(self.option):
            instance = ScrapeJobs(self.URL[i], option)
            new_jobs = instance.scrape_jobs()

            if not new_jobs:
                return

            new_jobs_df = pd.DataFrame(new_jobs)
            merged_df = new_jobs_df.merge(old_jobs_df, on=["Title", "Link", "Location", "Company"], how="left",
                                          indicator=True)

            new_entries = merged_df[merged_df["_merge"] == "left_only"].drop(columns=["_merge"])
            new_job_title = new_entries.loc[:,"Title"]

            if not new_entries.empty:
                print(f"\n📬 {self.company[i]} hires! These are the new roles: \n {new_job_title.to_string(index=False)}")
                print("\n Checking...")
            else:
                print("\n❌ No new entry at the moment!")
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
                    writer = csv.DictWriter(csvfile, delimiter=";", fieldnames=fieldnames)
                    writer.writeheader()
                    writer.writerows(data)
        else:
            with open(CSV_LINK, "a", newline="") as csvfile:
                fieldnames = ["Title", "Link", "Location", "Company"]
                writer = csv.DictWriter(csvfile, delimiter=";", fieldnames=fieldnames)
                writer.writerows(data)

scrape_option, websites = scrape_options()
URL = []
company = []
for key, values in websites.items():
    URL.append(values)
    company.append(key)

run_scrapper = writecsv(CSV_LINK, URL, company, scrape_option)

def safe_check():
    try:
        run_scrapper.check_new_entries()
    except Exception as e:
        print(f"Error in job checking: {e}")

schedule.every(60).minutes.do(safe_check)

print(f"Job scrapper is running on ... Press Ctrl+C to stop")

while True:
    schedule.run_pending()
    time.sleep(60)
