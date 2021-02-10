# -*- coding: utf-8 -*-
"""
Created on Wed Feb 10 14:24:11 2021

@author: gorlo
"""

import json

class ParserRecord():
    
    name : str
    gens : list
    
    def __init__(self, name : str, gens : list):
        self.name = name
        self.gens = gens
    
    def load_from_json(self, json_string : str):
        temp = json.loads(json_string)
        self.name = temp['name']
        self.gens = temp['gens']
    
    def __repr__(self):
        return json.dumps({'name' : self.name, 'gens' : self.gens})