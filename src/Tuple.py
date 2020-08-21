# -*- coding: utf-8 -*-
"""
Created on Mon Jun 29 10:19:03 2020

@author: rohan\
"""
functionNamesTuple = ['fst', 'snd', 'swap']

class Tuple:
    def __init__(self, tup):
        self.tup = tup
       
    def simplify(self, simplifyVariables = True): 
        from utils import replaceVariables
        return Tuple(list(map(lambda expr: replaceVariables(expr), self.tup)))
    
    def __str__(self):
        tup = []
        for item in self.tup:
            if item == None:
                tup.append('')
            else:
                try:
                    tup.append(str(item.simplify()))
                except:
                    tup.append(str(item))
        return '(' + ', '.join(tup) + ')'

def fst(tup):
    return tup.tup[0]

def snd(tup):
    return tup.tup[1]

def swap(a):
    tup = a
    tup.tup = (tup.tup[1], tup.tup[0])
    return tup