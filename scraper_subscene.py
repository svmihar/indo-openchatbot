from tqdm import tqdm
from bs4 import BeautifulSoup
from gensim.utils import simple_preprocess
import pandas as pd
import requests

def get_download_link(url):
    req = requests.get(url)
    soup = BeautifulSoup(req.content, 'lxml')
    raw_div = soup.find('div', {'class':'btn-download'})
    download_link = raw_div.a['href']
    return download_link

def get_page(page,url='https://subs.dog/subtitles/id/Movies/uploaded_at:desc/'):
    r = requests.get(url+str(page))
    soup = BeautifulSoup(r.content, 'lxml')
    titles = soup.find_all('td', {'class':'releases'})
    titles_raw = [simple_preprocess(a.text) for a in titles]
    hasil = []
    for i in tqdm(range(len(titles))):
        link = 'https://subs.dog'+titles[i].a['href']
        download_link = get_download_link(link)

        hasil.append({
            'titles':' '.join(titles_raw[i]),
            'link':link,
            'download_link': download_link
        })
    a = pd.DataFrame(hasil)
    return a

if __name__ == "__main__":
    page_range = range(1, 1143)
    for i in tqdm(page_range):
        page = get_page(page=i)
        page.to_csv(f'{i}.csv', index=False)