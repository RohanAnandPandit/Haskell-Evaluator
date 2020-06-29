# -*- coding: utf-8 -*-
"""
Created on Mon Jun 22 10:24:50 2020

@author: rohan
"""
from Shunting_Yard_Algorithm import Lexer, generateExpr

while (True):
    exp = input(">>")
    if (exp == "quit"):
        break
    lexer = Lexer(exp)
    lexer.printTokens()
    (binExp,_) = generateExpr(lexer)
    print(binExp.toString())
    try:
        print("=", binExp.simplify().toString())
    except:
        print("=", binExp.simplify())

