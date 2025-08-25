import os
import json
import threading
import urllib.request

from tqdm import tqdm


INPUT_JSON = "pdf_urls.json"
OUTPUT_DIR = "pdfs"
MAX_THREADS = 8

def getter(url, dest):
    urllib.request.urlretrieve(url, dest)


if __name__ == "__main__":
    with open(INPUT_JSON) as f:
        data = json.load(f)

    threads = []
    for year, links in tqdm(data.items()):
        year_output_dir = os.path.join(OUTPUT_DIR, str(year))
        os.makedirs(year_output_dir, exist_ok=True)
        for link in tqdm(links):
            base_pdf_filename = os.path.basename(link)
            output_path = os.path.join(year_output_dir, base_pdf_filename)
            if os.path.exists(output_path):
                print(f"Skipping {output_path}, already exists.")
                continue

            if len(threads) == MAX_THREADS:
                for thread in threads:
                    thread.join()
                threads = []

            t = threading.Thread(target=getter, args=(link, output_path))
            t.start()
            threads.append(t)
            # urllib.request.urlretrieve(link, output_path)

