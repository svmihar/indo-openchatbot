from pathlib import Path
from dataclasses import dataclass
from selenium.webdriver import Chrome
import pandas
from selenium.webdriver.chrome.options import Options
from tqdm import tqdm
from bs4 import BeautifulSoup
from gensim.utils import simple_preprocess
import pandas as pd
import requests


def get_download_link(url):
    req = requests.get(url)
    soup = BeautifulSoup(req.content, 'lxml')
    raw_div = soup.find('div', {'class': 'btn-download'})
    download_link = raw_div.a['href']
    r_download = requests.get(download_link, stream=True)
    z = zipfile.ZipFile(StringIO(r_download.content))
    z.extractall('./')
    return download_link


def get_page(page, url='https://subs.dog/subtitles/id/Movies/uploaded_at:desc/'):
    r = requests.get(url+str(page))
    soup = BeautifulSoup(r.content, 'lxml')
    titles = soup.find_all('td', {'class': 'releases'})
    titles_raw = [simple_preprocess(a.text) for a in titles]
    hasil = [{'titles': ' '.join(title_raw), 'link': 'https://subs.dog'+title.a['href']}
             for title_raw, title in zip(titles_raw, titles)]
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
    chrome_options.add_argument("--headless")
    driver = Chrome(executable_path='../../chromedriver',
                    options=chrome_options)
    url: str
    page_length: int


if __name__ == "__main__":
    page_range = range(1, 1143)
    for i in tqdm(page_range):
        page = get_page(page=i)
        page.to_csv(f'./data/{i}.csv', index=False)
