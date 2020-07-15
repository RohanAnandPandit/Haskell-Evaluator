# -*- coding: utf-8 -*-
"""
Created on Mon Jun 29 11:20:51 2020

@author: rohan
"""

functionNamesIO = ['getChar', 'getLine', 'putChar', 'putStr', 'putStrLn', 'print']

WORLD = ['', '']# (input, out)

def getChar():
    getLine()
                
def putChar(a):
    putStr(a)

def getLine():
    from utils import stringToList
    from Shunting_Yard_Algorithm import convertToList
    
    string = input()
    WORLD[0] = convertToList(string)
    return WORLD[0]
    
def putStr(a):
    from Operator_Functions import concatenate
    
    string = printHaskell(a)
    print(string, end = '')
    WORLD[1] = concatenate(WORLD[1], a)

def putStrLn(a):
    putStr(a)
    putStr("\n")

def printHaskell(a):    
    if (a == None):
        return ''
    #try:
    return str(a)
    #except:
        #print(a.name)