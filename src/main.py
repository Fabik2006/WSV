import os.path

import schedule
import time
from datetime import datetime

from websites_to_scrape import scrape_options
from scrapper_output import ScrapperOutput


class RunJobScrapper:
    def __init__(self, output_dir="job_opportunities.csv"):
        self._output_dir = None
        self.output_dir = output_dir

    @property
    def output_dir(self):
        return self._output_dir

    @output_dir.setter
    def output_dir(self, value):
        if not value.endswith(".csv"):
            raise ValueError(f"{value} must be a CSV-file")
        else:
            self._output_dir = os.path.abspath(value)

    def collect_information(self):
        scrape_option, websites = scrape_options()
        URL = []
        company = []
        for key, values in websites.items():
            URL.append(values)
            company.append(key)

        self.error_handling(URL, company, scrape_option, websites)

        return self.output_dir, URL, company, scrape_option

    @staticmethod
    def error_handling(URL, company, scrape_option, websites):

        if not all(URL) or not all(company):
            raise AttributeError(
                "Please check if every company is assigned to a link")

        if len(scrape_option) != len(websites):
            raise AttributeError(
                "Please check if all scrape options are assigned")

    @staticmethod
    def run_scrapper(CSV_LINK, URL, company, scrape_option):

        run_scrapper = ScrapperOutput(CSV_LINK, URL, company, scrape_option)
        try:
            run_scrapper.check_new_entries()
        except Exception as e:
            print(f"Error in job checking: {e}")


Scraper_instance = RunJobScrapper(output_dir="job_opportunities.csv")
CSV_LINK, URL, company, scrape_option = Scraper_instance.collect_information()

schedule.every(20).seconds.do(lambda:Scraper_instance.run_scrapper(
    CSV_LINK, URL, company, scrape_option)
)

print(f"Job scrapper is running on ... Press Ctrl+C to stop")

while True:
    schedule.run_pending()
    time.sleep(1)
