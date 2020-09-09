# -*- coding: utf-8 -*-
"""
Created on Tue Jun 23 13:38:23 2020

@author: rohan
"""
class BinaryExpr:
    def __init__(self, operator, left, right): 
        self.operator = operator
        self.leftExpr = left
        self.rightExpr = right
        
    def __str__(self):        
        buf = '('
        if not self.leftExpr:
            buf += '?'
        else:
            try:
                buf += str(self.leftExpr)
            except:
                print(self.leftExpr)
        string = self.operator.name
        buf += ' ' + string
        if string != ' ':
            buf += ' '
        if not self.rightExpr:
            buf += '?'
        else:
            buf += str(self.rightExpr)
        buf += ')'
        return buf

    def simplify(self, program_state):
        operator = self.operator
        if self.leftExpr:
            leftExpr = self.leftExpr
            if not self.operator.lazy:  
                leftExpr = leftExpr.simplify(program_state)
            operator = operator.apply(leftExpr, program_state = program_state)
            if self.rightExpr:
                rightExpr = self.rightExpr
                if not (self.operator.lazy or
                        self.operator.name == ' ' and leftExpr.lazy):
                        rightExpr = self.rightExpr.simplify(program_state)
                operator = operator.apply(rightExpr,
                                          program_state = program_state)       
                return operator
            
        if self.rightExpr:
            rightExpr = self.rightExpr
            if not self.operator.lazy:
                rightExpr = rightExpr.simplify(program_state)
            operator = operator.apply(arg1 = None, arg2 = rightExpr,
                                      program_state = program_state) 
            
        return operator
    
    