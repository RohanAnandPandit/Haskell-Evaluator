# -*- coding: utf-8 -*-
"""
Created on Mon Jun 29 10:19:03 2020

@author: rohan
"""
from IO import printHaskell

functionNamesTuple = ['fst', 'snd', 'swap']

class Tuple:
    def __init__(self, tup):
        self.tup = tup
       
    def simplify(self, state, simplifyVariables):
        from utils import isPrimitive
        for i in range(len(self.tup)):
            if (not isPrimitive(self.tup[i])):
                self.tup[i] = self.tup[i].simplify(state, simplifyVariables)
        return self
    
    def __str__(self):
        from utils import isPrimitive
        
        string = ''
        for item in self.tup:
            value = item
            char = ''
            if (type(value) == str):
                char = "\""
            string += char + str(value) + char 
            string += ', '

        return '(' + string[ : -2] + ')'

def fst(tup):
    if (type(tup) != tuple):
        tup = tup.tup
    return tup[0]

def snd(tup):
    if (type(tup) != tuple):
        tup = tup.tup
    return tup[1]

def swap(a):
    tup = a
    tup.tup = (tup.tup[1], tup.tup[0])
    return tup