import sys
import re

from selenium import webdriver
from selenium.common.exceptions import NoSuchElementException

import ParserRecord as pr

def main():
    args = sys.argv
    browser = webdriver.Firefox()
    urls = ["http://www.cazy.org/PULDB/index.php?sp_name=Flavobacterium+sp.+SLB02"]
    records, share_vector, features = [], [], []
    for url in urls:
        temp = pr.ParserRecord()
        temp.load_from_url(browser, url)
        records.append(temp)
        share_vector.extend(temp.unique_genes())
    browser.quit()
    share_vector = list(sorted(set(share_vector)))

    for record in records:
        temp = record.generate_features(share_vector)
        features.append(temp)
        print(temp)

if __name__ == "__main__":
    main()