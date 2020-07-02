# -*- coding: utf-8 -*-
"""
Created on Tue Jun 23 13:38:23 2020

@author: rohan
"""
from utils import functionNames


class Expression:
    pass

class Data(Expression):
    def __init__(self, value):
        self.value = value
    
    def simplify(self):
        return self.value
    
    def toString(self):
        try:
            return self.value.toString()
        except:
            return str(self.value)
        
class BinaryExpr(Expression):
    def __init__(self, operator, left, right):
        self.operator = operator
        self.leftExpr = left
        self.rightExpr = right
        
    def toString(self):
        from List import listString
        
        #if (self.operator.name == ':'):
            #return listString(self.simplify())
        
        if (self.operator.name in functionNames):
            buf = '( ' + self.operator.name
            for i in range(self.operator.noOfArgs):
                buf += ' '
                if (i == 0 and self.leftExpr != None):
                    buf += self.leftExpr.toString()
                elif (i == 1 and self.rightExpr != None):
                    buf += self.rightExpr.toString()
                else:
                    buf += '?'
            return buf + ' )'
                
        buf = '( '
        if (self.leftExpr == None):
            buf += '?'
        else:
            buf += str(self.leftExpr.toString())
            
        string = self.operator.name
        buf += ' ' + string
        if (string != ' '):
            buf += ' '
            
        if (self.rightExpr == None):
            buf += '?'
        else:
            buf += str(self.rightExpr.toString())
        buf += ' )'
            
        return buf

    def simplify(self):
        operator = self.operator
        if (operator.noOfArgs == 0):
            operator.apply()
            
        if (self.leftExpr != None):
            if (operator.name == ':'):
                leftExpr = self.leftExpr
            else:
                leftExpr = self.leftExpr.simplify()
                
            operator = operator.apply(arg1 = leftExpr, arg2 = None)
            
            if (self.rightExpr != None):
                rightExpr = self.rightExpr.simplify()
                operator = operator.apply(arg1 = rightExpr)
                return operator
            
        if (self.rightExpr != None):
            operator = operator.apply(arg1 = None, arg2 = self.rightExpr.simplify())
            
        return operator
    
    