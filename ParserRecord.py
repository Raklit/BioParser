# -*- coding: utf-8 -*-

import sys
import re
import json
from selenium import webdriver
from selenium.common.exceptions import NoSuchElementException

class ParserRecord():
    
    name : str
    genes : list
    
    def __init__(self, name : str = None, genes : list = []):
        self.name = name
        self.genes = genes
    
    def load_from_json(self, json_string : str):
        temp = json.loads(json_string)
        self.name = temp["name"]
        self.genes = temp["genes"]
    
    def load_from_url(self, browser : object, url : str):
        browser.get(url)
        elem = browser.find_element_by_css_selector("table:nth-of-type(3)")
        i = 2
        name, genes = None, []
        pat = r"[\s\n]*[\u25B6\u25C0\|][\s\n]*|[\s\n]+"
        re_sep = re.compile(pat)
        while (True):
            try:
                row = elem.find_element_by_css_selector("tr:nth-of-type({})".format(i))
                if name is None:
                    name = row.find_element_by_css_selector("td:nth-of-type(1)").text
                temp_genes = row.find_element_by_css_selector("td:nth-of-type(3)").text
                temp_genes = list(filter(lambda x: x, re_sep.split(temp_genes)))
                if temp_genes[0] == "":
                    temp_genes = temp_genes[1::]
                if temp_genes[-1] == "":
                    temp_genes = temp_genes[:-1:]
                genes.extend(temp_genes)
            except NoSuchElementException:
                break
            i += 1
        self.name = name
        self.genes = genes

    def get_dict_with_count_of_genes(self):
        d = dict()
        for gen in self.genes:
            if gen in d: d[gen] += 1
            else: d[gen] = 1
        return d

    def unique_genes(self):
        return list(sorted(set(self.genes)))

    def generate_features(self, feature_vec):
        n = len(feature_vec)
        uni = self.unique_genes()
        result = [0] * n
        for i in range(n):
            if feature_vec[i] in uni: result[i] = 1
        return result



    def __repr__(self):
        return json.dumps({"name" : self.name, "genes" : self.genes})
    
    def __str__(self):
        return json.dumps({"name" : self.name, "genes" : self.genes})