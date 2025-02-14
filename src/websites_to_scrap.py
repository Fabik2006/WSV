from dataclasses import dataclass


@dataclass
class ScrapeOption:
    tag: str
    attrs: dict


def scrape_options():
    websites = {
        "Bertrandt": "https://bertrandtgroup.onlyfy.jobs/",
        "AtlasCopco": "https://www.atlascopco.com/de-de/jobs/job-overview?function=Research%20and%20Development"
    }

    scrapeOptionsBertrandt = [
        ScrapeOption("div", {"class": ["row row-table row-24 collapsed row-table-condensed",
                             "row row-table row-24 collapsed even row-table-condensed"]}),
        ScrapeOption("a", {"href": True}),
        ScrapeOption(
            "div", {
                "class_": "inner", "style": "white-space: normal;"})
    ]

    scrapeOptionsAtlasCopco = [
        ScrapeOption("article", {"class": "o-grid o-grid--small u-stb"}),
        ScrapeOption("a", {"href": True}),
        ScrapeOption("p", {"class_": "c-caption u-mb-alpha"})
    ]
    return [scrapeOptionsBertrandt, scrapeOptionsAtlasCopco], websites
