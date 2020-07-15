# -*- coding: utf-8 -*-
"""
Created on Mon Jun 22 10:24:50 2020

@author: rohan
"""

from IO import printHaskell
from utils import builtInState, haskellEval
from Operators import initialiseFunctions

initialiseFunctions(builtInState)

while (True):
    string = input("Prelude> ") 
    if (string == ''):
        continue
    elif (string == "quit"):
        break
    print(printHaskell(haskellEval(string, builtInState)))




