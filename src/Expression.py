# -*- coding: utf-8 -*-
"""
Created on Tue Jun 23 13:38:23 2020

@author: rohan
"""
from utils import functionNames
from HFunction import HFunction

class Expression:
    pass

class BinaryExpr(Expression):
    def __init__(self, operator, left, right): 
        self.operator = operator
        self.leftExpr = left
        self.rightExpr = right
        
    def __str__(self):        
        if (self.operator.name in functionNames or self.operator.name == '\\'):
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
        if self.leftExpr == None:
            buf += '?'
        else:
            buf += str(self.leftExpr)
        string = self.operator.name
        buf += ' ' + string
        if string != ' ':
            buf += ' '
        if self.rightExpr == None:
            buf += '?'
        else:
            buf += str(self.rightExpr)
        buf += ')'
        return buf

    def simplifyRightExpr(self, leftExpr):
        return not (self.operator.name in ('=', '->', 'where', '|', '.', '\n', ';', '+=', '-=', '*=', '/=', '^=') 
                    or self.operator.name == ' ' 
                    and isinstance(leftExpr, HFunction) 
                    and leftExpr.name in ('while', 'for', 'struct', 'enum', 
                                          'oper', 'class', 'interface', 'def',
                                          'case', 'if', 'cascade', 'let',
                                          'import', 'do', 'int', 'float', 'char',
                                          'bool', 'string', 'list', 'from',
                                          'type', 'union'))

    def simplify(self, simplifyVariables = True):
        simplifyRightVariables = simplifyLeftVariables = simplifyVariables
        if (self.operator.name in ('=', 'where', '|')):
            simplifyRightVariables = simplifyLeftVariables = False

        operator = self.operator
        if operator.noOfArgs == 0:
            operator.apply()
        if self.leftExpr != None:
            leftExpr = self.leftExpr
            if (self.operator.name not in (':', '->', '=', '\n', ';', 'in', 
                                           'where', '+=', '-=', '*=', '/=', '^=')):
                leftExpr = leftExpr.simplify(simplifyLeftVariables)
            operator = operator.apply(leftExpr)
            if (self.rightExpr != None):
                rightExpr = self.rightExpr
                if self.simplifyRightExpr(leftExpr):
                    rightExpr = self.rightExpr.simplify(simplifyRightVariables)
                operator = operator.apply(rightExpr)       
                return operator
        if self.rightExpr != None:
            rightExpr = self.rightExpr
            if self.simplifyRightExpr(self.leftExpr):
                rightExpr = rightExpr.simplify(simplifyRightVariables)
            operator = operator.apply(arg1 = None, arg2 = rightExpr)  
        return operator
    
    