# -*- coding: utf-8 -*-
"""
Created on Mon Jun 29 11:20:51 2020

@author: rohan
"""
from List import mapHaskell

functionNamesIO = ['getChar', 'getLine', 'putChar', 'putStr', 'putStrLn', 'print']

WORLD = ['','']# (input, out)

def getChar():
    getLine()
                
def putChar(a):
    putStr(a)

def getLine():
    from utils import stringToList
    
    string = input()
    WORLD[0] = string
    
def putStr(a):
    from Operators import Operator
    
    string = printHaskell(a)
    print(string, end = '')
    WORLD[1] += string

def putStrLn(a):
    putStr(a)
    putStr("\n")

def printHaskell(a):
    from utils import isPrimitive
    
    if (isPrimitive(a)):
        return str(a)
    return a.toString()