import json
from urllib.parse import urlparse

from tqdm import tqdm
import requests
from bs4 import BeautifulSoup


CVPR_PAGES_BY_YEAR = [
    ("2020", ["https://openaccess.thecvf.com/CVPR2020.py?day=2020-06-16", "https://openaccess.thecvf.com/CVPR2020.py?day=2020-06-17", "https://openaccess.thecvf.com/CVPR2020.py?day=2020-06-18"]),
    ("2021", ["https://openaccess.thecvf.com/CVPR2021?day=all"]),
    ("2022", ["https://openaccess.thecvf.com/CVPR2022?day=all"]),
    ("2023", ["https://openaccess.thecvf.com/CVPR2023?day=all"]),
    ("2024", ["https://openaccess.thecvf.com/CVPR2024?day=all"])
]

OUTPUT_PATH = "pdf_urls.json"

if __name__ == "__main__":
    # get links to pdfs
    pdf_urls: dict[int, list] = {}

    for year, pages in tqdm(CVPR_PAGES_BY_YEAR):
        urls_for_year: list = []
        for page_url in tqdm(pages):
            base_page_url = urlparse(page_url)._replace(query="").geturl()
            page = requests.get(page_url)
            soup = BeautifulSoup(page.text, "html.parser")
            for link in soup.findAll('a', href=True, string="pdf"):
                pdf_url = urlparse(base_page_url)._replace(path=link["href"]).geturl()
                urls_for_year.append(pdf_url)
        pdf_urls[year] = urls_for_year

    with open(OUTPUT_PATH, 'w') as f:
        json.dump(pdf_urls, f)
