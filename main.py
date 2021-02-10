import sys
import re

from selenium import webdriver
from selenium.common.exceptions import NoSuchElementException
from selenium.webdriver.common.keys import Keys


import ParserRecord as pr
import xml.dom.minidom

# test of correct sync

def main():
    args = sys.argv
    browser = webdriver.Firefox()
    browser.get('http://www.cazy.org/PULDB/index.php?sp_name=Flavobacterium+sp.+SLB02')

    elem = browser.find_element_by_css_selector('table:nth-of-type(3)')
    
    i = 2
    name = None
    gens = []
    pat = r'\s*[\u25B6\u25C0]\s*|\s+'
    re_sep = re.compile(pat)
    while (True):
        try:
            row = elem.find_element_by_css_selector('tr:nth-of-type({})'.format(i))
            if name is None:
                name = row.find_element_by_css_selector('td:nth-of-type(1)').text
            temp_gens = row.find_element_by_css_selector('td:nth-of-type(3)').text
            temp_gens = re_sep.split(temp_gens)
            if temp_gens[0] == '':
                temp_gens = temp_gens[1::]
            if temp_gens[-1] == '':
                temp_gens = temp_gens[:-1:]
            gens.extend(temp_gens)
        except NoSuchElementException:
            break
        i += 1
    print(name)
    print(gens)
    browser.quit()

if __name__ == '__main__':
    main()