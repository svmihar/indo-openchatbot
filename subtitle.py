from pathlib import Path
import time
from dataclasses import dataclass
from selenium.webdriver import Chrome
import pandas
from selenium.webdriver.chrome.options import Options
from tqdm import tqdm
from bs4 import BeautifulSoup
from gensim.utils import simple_preprocess
import pandas as pd
import requests

# TODO: bikin supaya txt biasa bisa jadi formatted dataset
# TODO: apache_arrow + beam buat preprocess csv dialog format


def get_page(page, url="https://subs.dog/subtitles/id/Movies/uploaded_at:desc/"):
    r = requests.get(url + str(page))
    soup = BeautifulSoup(r.content, "lxml")
    titles = soup.find_all("td", {"class": "releases"})
    titles_raw = [simple_preprocess(a.text) for a in titles]
    hasil = [
        {"titles": " ".join(title_raw), "link": "https://subs.dog" + title.a["href"]}
        for title_raw, title in zip(titles_raw, titles)
    ]
    return pd.DataFrame(hasil)


@dataclass
class scraper:
    prefs = {}
    chrome_options = Options()
    chrome_options.experimental_options["prefs"] = prefs
    prefs["profile.default_content_settings"] = {"images": 2}
    prefs["profile.managed_default_content_settings"] = {"images": 2}
    chrome_options.add_argument("--disable-popup-blocking")
    chrome_options.add_argument("--start-maximized")
    # chrome_options.add_argument("--headless")
    driver = Chrome(executable_path="../../chromedriver", options=chrome_options)
    csv: str

    def __post_init__(self):
        self.contoh_df = pd.read_csv(self.csv)  # ['link'].values
        self.hasil = [
            self.contoh_df["link"][i]
            for i, title in enumerate(self.contoh_df.titles)
            if "yts" in title or "yify" in title
        ]

    def set_url(self, link):
        self.url = link
        self.driver.get(self.url)
        self.driver.find_element_by_xpath(
            '//*[@id="subtitle-info"]/div/div[2]/a/i'
        ).click()

    def run(self):
        for link in tqdm(self.hasil):
            try:
                self.set_url(link)
            except Exception as e:
                print(e)
                pass
        time.sleep(5)
        self.driver.quit()


if __name__ == "__main__":
    c = scraper("./data/gabungan.csv")
    c.run()
    # for i in tqdm(page_range):
    #     page = get_page(page=i)
    #     page.to_csv(f'./data/{i}.csv', index=False)
