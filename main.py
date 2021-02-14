import sys
import re

from selenium import webdriver
from selenium.common.exceptions import NoSuchElementException
import ParserRecord as pr


import ParserRecord as pr

def main():
    args = sys.argv
    browser = webdriver.Firefox()
    urls = ["http://www.cazy.org/PULDB/index.php?sp_name=Flavobacterium+sp.+SLB02"]
    record = []
    for url in urls:
        temp = pr.ParserRecord()
        temp.load_from_url(browser, url)
        record.append(temp)
        print(temp.get_dict_with_count_of_genes())
    browser.quit()

if __name__ == "__main__":
    main()