import requests
from bs4 import BeautifulSoup
from collections import OrderedDict
import re


def job_fetching(url):
    """
    This function provides methods to extract all relevant information out of the websites.
    It stores the information in a dictionary to access them easier by key-value-pairs.

    :param url:
    :return: jobs
    """
    response = requests.get(url)
    soup = BeautifulSoup(response.content, "html.parser")
    job_elements = soup.find_all("div", id="jobList")
    job_links = job_elements[0].find_all("a", href=True)
    job_location = soup.find_all("div", attrs={"class": "inner", "style": "white-space: normal;"})
    jobs = []
    company = re.search(r'/([^/]+)\.([^.]*)$', url)
    for job, location in zip(job_links, job_location):
            jobs.append(OrderedDict({
                         "Title": job.get_text(),
                         "Link": job["href"],
                         "Location": location.get_text(strip=True),
                         "Company": company[1]
            }))

    return jobs

if __name__ == "__main__":
    # Jobs URL
    URL = {
        "Bertrandt": "https://bertrandtgroup.onlyfy.jobs/"
    }

    # Receiver Mail
    sender_mail = "Fabi.kind@web.de"
    receiver_mail = "Fabi.kind@web.de"

    job_fetching(URL["Bertrandt"])
