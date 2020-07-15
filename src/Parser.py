# -*- coding: utf-8 -*-
"""
Created on Mon Jun 22 10:20:56 2020

@author: rohan
"""
import utils
from utils import getData, Variable
from Operators import operatorFromString
from HFunction import HFunction 

class Lexer:
    def __init__(self, string, state, operators, functionNames):
        self.tokens = []
        self.string = string
        self.state = state
        self.index = 0
        self.operators = operators
        self.functionNames = functionNames
        #self.parse(list(string), state)
        self.curr = 0
        #self.operatorSymbols =  functionNames + operators
        self.acc = ''
        self.isFunction = False
        self.isAssignment = False
        self.inWhereClause = False
        self.parse(string, state)
        
    def nextToken(self):
        if (self.index >= len(self.tokens)):
            return None
        value = self.tokens[self.index]
        self.index += 1
        return value
    
    def printTokens(self):
        tokens = []
        for token in self.tokens:
            tokens.append(str(token))
        print(tokens)
        
    def addSpace(self):
        if (len(self.tokens) > 0):
            lastToken = self.tokens[-1]
            if (not isinstance(lastToken, HFunction) or not lastToken.name in self.operators
                or lastToken.name in (')', ']')):
                self.tokens.append(operatorFromString(' ').value)  
                if (not self.isAssignment):
                    self.isFunction = True
                        
    def addString(self):
        from Shunting_Yard_Algorithm import convertToList
        string = ''
        start = self.curr
        while (True):
            char = self.string[self.curr]
            if (char == '"' and string[-1] != '\\'):
                break
            string += char
            if (len(string) > 1):
                if (string[-2 : ] == '\\n'):
                    string = string[ : -2] + '\n'
                elif (string[-2 : ] == '\\"'):
                    string = string[ : -2] + '"'
                elif (string[-2 : ] == '\\\\'):
                    string = string[ : -2] + '\\'  
            self.curr += 1

            
        charList = convertToList(self.string[start : self.curr]).simplify({}, False)
        self.tokens.append(charList)
        self.curr += 1
    
    def addOperator(self, op):
        if (op == ' '):
            self.addSpace()
            return
        elif (op == '\\'):
            self.addFunction('\\')
            return

        if (op not in ['[', '(']):
            if (len(self.tokens) > 0 and isinstance(self.tokens[-1], HFunction) 
                and self.tokens[-1].name == ' '):
                del self.tokens[-1]
                
        if (op == '='):
            if (operatorFromString(' ').value in self.tokens and not self.inWhereClause):
                self.isAssignment = True
                self.isFunction = True
                op = '->'
                self.tokens.insert(0, operatorFromString(' ').value)
                self.tokens.insert(0, operatorFromString(')').value)
                self.tokens.insert(0, operatorFromString('\\').value)
                self.tokens.insert(0, operatorFromString('(').value) 
                
        if (op != '`'):
            self.tokens.append(operatorFromString(op).value)
    
    def addFunction(self, func):
        self.tokens.append(operatorFromString('(').value)
        self.tokens.append(operatorFromString(func).value)
        self.tokens.append(operatorFromString(')').value)
        if (func == '\\'):
            self.addSpace()
            self.tokens.append(Variable('None'))
            self.addSpace()
    
    def addData(self):
        if (self.acc != ''):
            self.tokens.append(getData(self.acc, self.state))            
            self.acc = ''
        
    def parse(self, string, state):
        while (self.curr < len(self.string)):
            if (len(self.tokens) > 0 and self.tokens[-1] == '--'):
                del self.tokens[-1]
                return
                
            op = self.searchOperator(utils.operators)
            if (op != None):
                if (op == 'where'):
                    self.inWhereClause = True
                if (op == '.' and '0' <= string[self.curr] <= '9'):
                    self.acc += '.'
                else:
                    self.addData()
                    self.addOperator(op)
                continue
                    
            if (string[self.curr] == '"'):
                self.curr += 1
                self.addString()
            else:
                self.acc += string[self.curr]
                self.curr += 1
      
        self.addData()
            
    def searchOperator(self, operators):
        for length in range(5, 0, -1):
            if (self.curr + length - 1 < len(self.string)):
                substring = self.string[self.curr : self.curr + length]
                if (substring in operators): 
                    self.curr += length
                    return substring
        return None
