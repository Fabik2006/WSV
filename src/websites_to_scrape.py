from dataclasses import dataclass


@dataclass
class ScrapeOption:
    tag: str
    attrs: dict


def scrape_options():
    websites = {
        "Bertrandt": "https://bertrandtgroup.onlyfy.jobs/",
        "AtlasCopco": "https://www.atlascopco.com/de-de/jobs/job-overview?function=Research%20and%20Development",
        "Deutz": "https://career.deutz.com/search/?createNewAlert=false&q=&locationsearch=K%C3%B6ln&optionsFacetsDD_department=Forschung+und+Entwicklung&optionsFacetsDD_location=&optionsFacetsDD_country=",
        "DLR": "https://jobs.dlr.de/go/Alle-Stellen/9261201/?markerViewed=&carouselIndex=&facetFilters=%7B%22filter1%22%3A%5B%22Ingenieurwissenschaften+%28F%26E%29%22%5D%2C%22mfield1%22%3A%5B%22Absolventinnen+%26+Absolventen%22%5D%2C%22mfield3%22%3A%5B%22Maschinenbau%22%2C%22Luft-+und+Raumfahrttechnik%22%2C%22Ingenieurwissenschaften%22%5D%7D&pageNumber=0",
        "Igus": "https://karriere.igus.de/search?department=Forschung%20%26%20Entwicklung"
    }

    scrapeOptionsBertrandt = [
        ScrapeOption("div", {"class_": ["row row-table row-24 collapsed row-table-condensed",
                             "row row-table row-24 collapsed even row-table-condensed"]}),
        ScrapeOption("a", {"href": True}),
        ScrapeOption(
            "div", {
                "class_": "inner", "style": "white-space: normal;"})
    ]

    scrapeOptionsAtlasCopco = [
        ScrapeOption("article", {"class_": "o-grid o-grid--small u-stb"}),
        ScrapeOption("a", {"href": True}),
        ScrapeOption("p", {"class_": "c-caption u-mb-alpha"})
    ]
    scrapeOptionsDeutz = [
        ScrapeOption("tr", {"class_": "data-row"}),
        ScrapeOption("a", {"href": True}),
        ScrapeOption("span", {"class_": "jobLocation"})
    ]
    scrapeOptionsDLR = [
        ScrapeOption("li", {"class_": "JobsList_jobCard__8wE-Z"}),
        ScrapeOption("a", {"href": True}),
        ScrapeOption("div", {"class_": "JobsList_jobCardLocation__oMpM+"})
    ]
    scrapeOptionsIgus = [
        ScrapeOption("li", {"class_": "ais-InfiniteHits-item"}),
        ScrapeOption("a", {"href": True}),
        ScrapeOption("li", {"class_": "location"})
    ]
    return [scrapeOptionsBertrandt,
            scrapeOptionsAtlasCopco,
            scrapeOptionsDeutz,
            scrapeOptionsDLR,
            scrapeOptionsIgus], websites
