import json
import re
from time import sleep
from typing import Union

from bs4 import BeautifulSoup
import requests
from tqdm import tqdm


class Scraper:
    def __init__(self, root_uri: str):
        """Initialize Scraper object."""
        self.root_uri: str = root_uri
        self.robots_uri: str = root_uri + "robots.txt"
        self.faculty_uri: str = root_uri + "directory/faculty"
        self.delay: Union[int, None] = self.check_robots()

    def health_check(self) -> bool:
        """Simple check to see if UNCC is still live and accessible."""
        r: requests.Response = requests.get(url=self.root_uri)

        if r.ok:
            return True
        else:
            return False

    def check_robots(self) -> Union[int, None]:
        """Extracts the specified time to wait before making subsequent requests."""
        r: requests.Response = requests.get(url=self.robots_uri)

        if r.ok:
            if "Crawl-delay" in r.text:
                # find line starting with "crawl delay" and return all digits until line end
                return int(
                    re.findall(pattern="(?<=Crawl-delay: )(.*)", string=r.text)[0]
                )
        else:
            return None

    def scrape(self) -> None:
        """Scrapes the UNCC DSBA faculty directory."""
        if self.health_check():
            r: requests.Response = requests.get(url=self.faculty_uri).text
            soup = BeautifulSoup(r, features="lxml")

            directory: list = []
            for tile in tqdm(
                soup.find_all("div", {"class": "col-xs-6 col-sm-6 col-md-6 col-lg-4"})
            ):
                for a in tile.find_all("a", {"class": "thumbnail-link"}):
                    link: str = a.get("href")
                    for thumbnail in a.find_all("div", {"class": "thumbnail"}):
                        thumbnail_link: str = thumbnail.img.get("src")
                        for caption in thumbnail.find_all("div", {"class": "caption"}):
                            name: str = caption.h3.text
                            title: str = caption.h4.text
                if self.check_robots() is not None:
                    sleep(self.check_robots())
                faculty_page: requests.Response = requests.get(link).text
                faculty_soup = BeautifulSoup(faculty_page, features="lxml")
                for email_field in faculty_soup.find_all(
                    "div",
                    {
                        "class": "field field-name-field-directory-email field-type-email field-label-hidden"
                    },
                ):
                    for field_item in email_field.find_all(
                        "div", {"class": "field-items"}
                    ):
                        for sub_item in field_item.find_all("div", {"field-item even"}):
                            email: str = sub_item.a.text
                for bio_field in faculty_soup.find_all(
                    "div",
                    {
                        "class": "field field-name-field-directory-biography field-type-text-with-summary field-label-hidden"
                    },
                ):
                    for bio_field_item in bio_field.find_all(
                        "div", {"class": "field-items"}
                    ):
                        for sub_bio_item in bio_field_item.find_all(
                            "div", {"class": "field-item even"}
                        ):
                            bio: str = ""
                            for p in sub_bio_item.find_all("p"):
                                bio += p.text
                if self.check_robots() is not None:
                    sleep(self.check_robots())

                payload: dict = {
                    "name": name,
                    "title": title,
                    "email": email,
                    "link": link,
                    "thumbnail": thumbnail_link,
                    "bio": bio,
                }

                directory.append(payload)

            with open("directory.json", "w", encoding="utf-8") as f:
                json.dump(directory, f, ensure_ascii=False, indent=4)


if __name__ == "__main__":
    scraper: Scraper = Scraper(root_uri="https://dsba.charlotte.edu/")
    scraper.scrape()
