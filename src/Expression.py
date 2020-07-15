# -*- coding: utf-8 -*-
"""
Created on Tue Jun 23 13:38:23 2020

@author: rohan
"""
from utils import functionNames, isPrimitive, Variable
from IO import printHaskell

class Expression:
    pass

class Data(Expression):
    def __init__(self, value):
        self.value = value
    
    def simplify(self, state, simplifyVariables):
        if (isPrimitive(self.value)):           
            return self.value
        return self.value.simplify(state, simplifyVariables)
    
    def __str__(self):
        return str(self.value)
        
class BinaryExpr(Expression):
    def __init__(self, operator, left, right): 
        self.operator = operator
        self.leftExpr = left
        self.rightExpr = right
        
    def __str__(self):        
        if (self.operator.name in functionNames):
            buf = '(' + self.operator.name
            for i in range(self.operator.noOfArgs):
                buf += ' '
                if (i == 0 and self.leftExpr != None):
                    buf += str(self.leftExpr)
                elif (i == 1 and self.rightExpr != None):
                    buf += str(self.rightExpr)
                else:
                    buf += '?'
            return buf + ')'
                
        buf = '('
        if (self.leftExpr == None):
            buf += '?'
        else:
            buf += printHaskell(self.leftExpr)
            
        string = self.operator.name
        buf += ' ' + string
        if (string != ' '):
            buf += ' '
            
        if (self.rightExpr == None):
            buf += '?'
        else:
            buf += printHaskell(self.rightExpr)
        buf += ')'
            
        return buf

    def simplify(self, state, simplifyVariables):
        simplifyLeftVariables = simplifyRightVariables = simplifyVariables
        if (self.operator.name in ('=', '->', 'where')):
            simplifyRightVariables = simplifyLeftVariables = False
            
            
        operator = self.operator
        if (operator.noOfArgs == 0):
            operator.apply()
            
        if (self.leftExpr != None):
            if (self.operator.name == ':' and not isinstance(self.leftExpr, Variable)):
                leftExpr = self.leftExpr
            else:
                leftExpr = self.leftExpr.simplify(state, simplifyLeftVariables)
                 
            operator = operator.apply(arg1 = leftExpr, arg2 = None)

            if (self.rightExpr != None):
                if (self.operator.name in ('->', 'where')):
                    rightExpr = self.rightExpr
                else:
                    rightExpr = self.rightExpr.simplify(state, simplifyRightVariables)
                operator = operator.apply(arg2 = rightExpr)   
                
                return operator
            
        if (self.rightExpr != None):
            if (self.operator.name in ('->', 'where')):
                rightExpr = self.rightExpr
            else:
                rightExpr = self.rightExpr.simplify(state, simplifyRightVariables)
            operator = operator.apply(arg1 = None, arg2 = rightExpr)
            
        return operator
    
    