# -*- coding: utf-8 -*-
"""
Created on Tue Jun 23 09:35:26 2020

@author: rohan
"""
from StackQueue import StackQueue
from HFunction import HFunction
from Operators import Operator, Associativity, operatorFromString, operatorToString
from Haskell_Functions import *
from Haskell_Evaluate import operators
from Expression import Data, BinaryExpr
from Parser import Lexer

def addBinaryExpr(operators, operands):
    (right, left) = (operands.pop(), operands.pop())
    '''
    if (left == None):
        left = right
        right = None
    '''
    operands.push(BinaryExpr(operators.pop(), left, right))
    
def checkOperators(current, operands, operators):
    topOperator = operators.peek()
    if (topOperator != None):
        if (topOperator.precedence > current.precedence
            or (topOperator.precedence == current.precedence 
                and topOperator.associativity == Associativity.LEFT)):
            addBinaryExpr(operators, operands)
            return False
    operators.push(current)
    return True

def printState(operands, operators):
    print("=================")
    print("OPERANDS")
    for operand in operands.arr:
        print(operand.toString())
    print("=================")
    print("OPERATORS")
    for op in operators.arr:
        print("\"" + op.toString() + "\"")
    print("=================")
    print()

def generateExpr(parser):
    operands = StackQueue()
    operators = StackQueue()
    token = parser.nextToken()
    while (token != None):
        if (isinstance(token, HFunction)):
            if (token.name == '('):
                operands.push(generateExpr(parser))
            elif (token.name == '['):
                exp = generateExpr(parser)
                operands.push(exp)
            elif (token.name == ')' or token.name == ']'):
                while (operators.peek() != None):
                    addBinaryExpr(operators, operands)
                return operands.pop()
            else:
                done = False
                while (not done):
                    done = checkOperators(token, operands, operators)
        else:
            operands.push(Data(token))

        #printState(operands, operators)
        token = parser.nextToken()
    
    while (operators.peek() != None):
        addBinaryExpr(operators, operands)
    
    return operands.pop()


exp = ''
while (True):
    exp = input(">>")
    if (exp == "quit"):
        break
    lexer = Lexer(exp)
    lexer.printTokens()
    binExp = generateExpr(lexer)
    print("as string =", binExp.toString())
    print("result =", binExp.simplify())

            
    