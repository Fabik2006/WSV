from dataclasses import dataclass


@dataclass
class ScrapeOptionBertrandt:
    tag:str
    attrs:dict

@dataclass
class ScrapeOptionAtlasCopco:
    tag:str
    attrs:dict

def scrape_options():
    websites = {
        "Bertrandt": "https://bertrandtgroup.onlyfy.jobs/",
        "AtlasCopco": "https://www.atlascopco.com/de-de/jobs/job-overview?function=Research%20and%20Development"
    }

    scrapeOptionsBertrandt= [
        ScrapeOptionBertrandt("div", {"class": ["row row-table row-24 collapsed row-table-condensed",
                             "row row-table row-24 collapsed even row-table-condensed"]}),
        ScrapeOptionBertrandt("a", { "href": True}),
        ScrapeOptionBertrandt("div", {"class_": "inner", "style": "white-space: normal;"})
    ]

    scrapeOptionsAtlasCopco = [
        ScrapeOptionBertrandt("article", {"class": "o-grid o-grid--small u-stb"}),
        ScrapeOptionBertrandt("a", { "href": True}),
        ScrapeOptionBertrandt("p", {"class_": "c-caption u-mb-alpha"})
    ]
    return [scrapeOptionsBertrandt, scrapeOptionsAtlasCopco], websites