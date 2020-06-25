# -*- coding: utf-8 -*-
"""
Created on Tue Jun 23 13:38:23 2020

@author: rohan
"""
from Operators import Operator, operatorToString
from HFunction import HFunction

class Data:
    def __init__(self, value):
        self.value = value
    
    def simplify(self):
        return self.value
    
    def toString(self):
        return str(self.value)
        
class BinaryExpr:
    def __init__(self, operator, left, right):
        self.operator = operator
        self.leftExpr = left
        self.rightExpr = right
        
    def toString(self):
        buf = '( '
            
        if (self.leftExpr == None):
            buf += 'None'
        else:
            buf += str(self.leftExpr.toString()) + ' '
            
        if (self.operator == None):
            buf += 'None'
        else:
            char = str(self.operator.toString())
            buf += char
            if (char != ' '):
                buf += ' '
            
        if (self.rightExpr == None):
            buf += 'None'
        else:
            buf += str(self.rightExpr.toString()) + ' '


        buf += ')'
            
        return buf

    def simplify(self):
        operator = self.operator
        if (self.leftExpr != None):
            operator = operator.apply(arg1 = self.leftExpr.simplify(), arg2 = None)
        if (self.rightExpr != None):
            operator = operator.apply(arg1 = None, arg2 = self.rightExpr.simplify())
        return operator
    
    