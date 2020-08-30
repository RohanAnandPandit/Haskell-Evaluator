# -*- coding: utf-8 -*-
"""
Created on Mon Jun 29 11:20:51 2020

@author: rohan
"""
from Types import Char, Int, String
functionNamesIO = ['input', 'printLn', 'print']

def printLn(a):
    a = str(a.simplify())
    if (len(a) > 0 and a[0] == '"'):
        a = a[1:-1]
    print(a)
    return Int(None)

def printHaskell(a):
    a = str(a.simplify())
    if len(a) > 0 and a[0] == '"':
        a = a[1:-1]
    print(a, end = '')
    return Int(None)

def show(a):
    return String(str(a))

def inputHaskell(question):
    from utils import convertToList
    inp = input(str(question))
    return  convertToList(list(map(Char, str(inp)))).simplify()