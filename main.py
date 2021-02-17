import sys
import re

from selenium import webdriver
from selenium.common.exceptions import NoSuchElementException

import ParserRecord as pr

def main():
    args = sys.argv
    browser = webdriver.Firefox()
    f = open("links.txt", 'r', encoding="utf8")
    urls = []
    for line in f:
        urls.append(line)
    f.close()
    records, share_vector, features = [], [], []
    for url in urls:
        temp = pr.ParserRecord()
        temp.load_from_url(browser, url)
        records.append(temp)
        share_vector.extend(temp.unique_genes())
    browser.quit()
    share_vector = list(sorted(set(share_vector)))

    f = open("vecs.txt", "w+", encoding="utf8")
    f.write(str(share_vector)+"\n")
    for record in records:
        temp = record.generate_features(share_vector)
        features.append(temp)
        f.write(str(temp)+"\n")
    f.close()

if __name__ == "__main__":
    main()