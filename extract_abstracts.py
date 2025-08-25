import os
import glob

import pypdf
from tqdm import tqdm


PDFS_ROOT = "pdfs"
OUTPUT_DIR = "abstracts"
YEARS = ["2020", "2021", "2022", "2023", "2024"]


if __name__ == "__main__":
    os.makedirs(OUTPUT_DIR, exist_ok=True)

    skips_for_years: dict = {
        "2020": 0,
        "2021": 0,
        "2022": 0,
        "2023": 0,
        "2024": 0
    }

    for year in tqdm(YEARS):
        year_dir = os.path.join(PDFS_ROOT, year)
        pdf_paths = glob.glob(os.path.join(year_dir, "*.pdf"))
        for pdf_path in tqdm(pdf_paths):
            abs_path = os.path.splitext(os.path.basename(pdf_path))[0] + ".txt"
            abs_path = os.path.join(OUTPUT_DIR, abs_path)
            if os.path.exists(abs_path):
                print(f"Skipping {abs_path}.")
                continue
            reader = pypdf.PdfReader(pdf_path)
            # abstract is probably on first page
            first_page = reader.pages[0]
            try:
                text = first_page.extract_text()
            except Exception as e:
                print(e)
                skips_for_years[year] += 1
                continue
            pre_abs = text.split("Abstract") 
            if len(pre_abs) == 2:
                abs_intr = pre_abs[1].split("1. Introduction")
                if len(abs_intr) == 2:
                    abstract = abs_intr[0]
                    abstract = abstract.replace("-\n", "").replace("\n", " ")
                    with open(abs_path, 'w') as f:
                        f.write(abstract)
                else:
                    skips_for_years[year] += 1
            else:
                skips_for_years[year] += 1
    
    print("Skips for years:")
    for year, skips in skips_for_years.items():
        print(f"{year}: {skips}")