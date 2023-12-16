import requests
from bs4 import BeautifulSoup

CS_PROFESSORS_URL = "http://informatik.jku.at/research/faculty.phtml"


def scrape_jku_cs_profs() -> list[str]:
    print("Scraping JKU CS professors...")

    page = requests.get(CS_PROFESSORS_URL)
    soup = BeautifulSoup(page.content, "html.parser", from_encoding="utf-8")

    profs = soup.find_all("div", class_="team_employee")

    prof_names = []

    for prof in profs:
        name = (prof.find_next("p")
                .find_next("a")
                .find_next("em")
                .text)
        prof_names.append(name)

    print("Scraped %s professors" % len(prof_names))

    return prof_names
