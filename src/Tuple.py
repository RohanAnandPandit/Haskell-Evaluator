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
        return self
    
    def __str__(self):
        return '{' + ', '.join(list(map(str, self.tup))) + '}'

def fst(tup):
    return tup.tup[0]

def snd(tup):
    return tup.tup[1]

def swap(a):
    tup = a
    tup.tup = (tup.tup[1], tup.tup[0])
    return tup