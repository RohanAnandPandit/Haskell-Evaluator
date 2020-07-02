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
       
    def simplify(self):
        return self
    
    def toString(self):
        from utils import isPrimitive, closer
        from IO import printHaskell
        
        string = '('
        for item in self.tup:
            value = item
            if (not isPrimitive(value)):
                value = value.simplify()
            char = ''
            if (type(value) == str):
                char = "\""
            string += char + printHaskell(value) + char
            string += ', '

        return string[ : -2] + ')'

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