import bs4 as bs
import urllib.request
import pandas as pd
import typing
import os
import pathlib
import logging
import time

from constants import NAMES

logging.basicConfig(level=logging.INFO)


def scrape_page(name: NAMES, page: int) -> None:
    folder = pathlib.Path(name)
    os.makedirs(folder, exist_ok=True)
    url = f"https://doon.se/ordtyp/{name}?page={page}"
    source = urllib.request.urlopen(url).read()
    soup = bs.BeautifulSoup(source, "lxml")
    words = pd.Series([x.string for x in soup.find_all("a", attrs={"class": "slider"})])
    if words.empty:
        raise EOFError(f"No words on this page. {url = }")
    words.to_csv(folder / f"{page}.csv", index=False, header=False)


def main() -> None:
    for name in typing.get_args(NAMES):
        page = 1
        while True:
            logging.info(f"Scraping {name} page {page}")
            try:
                scrape_page(name, page)
            except EOFError:
                logging.info(f"Reached the end. Exiting.")
                break
            page += 1
            time.sleep(0.1)


if __name__ == "__main__":
    main()
