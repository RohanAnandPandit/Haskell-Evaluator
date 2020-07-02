# -*- coding: utf-8 -*-
"""
Created on Mon Jun 22 10:24:50 2020

@author: rohan
"""

from Shunting_Yard_Algorithm import Lexer, generateExpr
from IO import printHaskell
from utils import state

while (True):
    exp = input("Prelude> ") 
    if (exp == "quit"):
        break
    elif (exp == 'state'):
        print(state)
        continue
    lexer = Lexer(exp, state)
    print("tokens : ", end = '')
    lexer.printTokens()
    (binExp, returnType) = generateExpr(lexer)
    print("expression : ", binExp.toString())
    
    print("result : ", end = '')
    binExp = binExp.simplify()
    if (returnType != 'io'):
        print(printHaskell(binExp))

    

