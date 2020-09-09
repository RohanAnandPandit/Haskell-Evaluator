# -*- coding: utf-8 -*-
"""
Created on Mon Jun 29 11:20:51 2020

@author: rohan
"""
from Types import Char, String
functionNamesIO = ['input', 'printLn', 'print']

def printLn(a, program_state):
    a = str(a.simplify(program_state))
    if (len(a) > 0 and a[0] == '"'):
        a = a[1:-1]
    print(a)
    return String(a)

def printHaskell(a, program_state):
    a = str(a.simplify(program_state))
    if len(a) > 0 and a[0] == '"':
        a = a[1:-1]
    print(a, end = '')
    return String(a)

def show(a, program_state):
    return String(str(a))

def inputHaskell(question):
    inp = input(question.value)
    return String(inp)