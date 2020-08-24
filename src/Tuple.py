# -*- coding: utf-8 -*-
"""
Created on Mon Jun 29 10:19:03 2020

@author: rohan\
"""
functionNamesTuple = ['fst', 'snd', 'swap']

class Tuple:
    def __init__(self, tup):
        self.tup = tup
        self.items = tup
       
    def simplify(self, simplifyVariables = True): 
        from utils import replaceVariables
        return Tuple(list(map(lambda expr: replaceVariables(expr), self.tup)))
    
    def __str__(self):
        tup = []
        for item in self.tup:
            try:
                tup.append(str(item.simplify()))
            except:
                tup.append(str(item))
        string = ', '.join(tup)
        if len(tup) == 1:
            string += ','
        return '(' + string + ')'
