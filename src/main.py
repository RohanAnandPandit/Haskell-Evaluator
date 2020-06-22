# -*- coding: utf-8 -*-
"""
Created on Mon Jun 22 10:24:50 2020

@author: rohan
"""
from Haskell_Evaluate import operators, brackets, haskellEval
from String_Formatting import tokenize

def haskellIO():
    variables = {}
    result = ""
    while (True):
        exp = input("Prelude> ")
        if (exp == ''):
            pass
        elif (exp == '$quit'):
            return
        elif (exp == "$reset"):
            variables.clear()
        else:
            exp = tokenize(exp, operators + brackets)
            result = haskellEval(exp, variables)
            if (result != None):
                print(result)
haskellIO()    

