# -*- coding: utf-8 -*-
"""
Created on Tue Jun 23 20:38:21 2020

@author: rohan
"""

class HList:
    def __init__(self):
        pass
    
    def init_with_exp(self, exp):
        self.items = splitAtCommas(exp)
        self.evaluated = []
        for item in items:
            evaluated.append(False)
    
    def init_list_comp(self, start, end = None):
        self.start = start
        self.end = end
        
    def get(index):
        if (not evaluated[index]):
            items[index] = haskellEval(items[index])
            evaluated[index] = True
        return items[index]
    
    def nextItem(self):
        value = self.start
        self.start += 1
        return value
        
            
