# -*- coding: utf-8 -*-
"""
Created on Mon Jun 22 10:20:56 2020

@author: rohan
"""
import utils
from utils import getData, operators
from Types import Variable, Char
from Operators import operatorFromString
from HFunction import HFunction, Function, Lambda

class Lexer:
    def __init__(self, string):
        self.tokens = []
        self.string = string
        self.index = 0
        self.curr = 0
        self.acc = ''
        self.tokenize()
        
    def nextToken(self):
        value = self.peek()
        self.index += 1
        return value
    
    def peek(self): 
        if self.index >= len(self.tokens):
            return None
        value = self.tokens[self.index]
        return value
        
    def printTokens(self):
        tokens = []
        for token in self.tokens:
            tokens.append(str(token))
        print(tokens)
        
    def addSpace(self, op):
        if len(self.tokens) > 0:
            lastToken = self.tokens[-1]
            if (op == '\n' and isinstance(lastToken, HFunction) 
                and lastToken.name == ' '):
                del self.tokens[-1]
            if (not isinstance(lastToken, (HFunction, Function, Lambda)) 
                or not lastToken.name in operators
                or lastToken.name in ')]}'):
                self.tokens.append(operatorFromString(op)) 
                        
    def addString(self):
        from utils import convertToList
        characters = []
        while (True):
            char = self.string[self.curr]
            if (char == '"'):
                if (len(characters) == 0):
                    break
                elif (characters[-1] != '\\'):
                    break
            if (len(characters) > 1):
                if (characters[-1] == '\\'):
                    del characters[-1]
                    if (char == 'n'):
                        char = '\n'
                    elif (char == '"'):
                        char = '"'
                    elif (char == '\\'):
                        char = '\\'
            characters.append(Char(char))
            self.curr += 1            
        charList = convertToList(characters).simplify()
        self.tokens.append(charList)
        self.curr += 1
    
    def addOperator(self, op):
        self.curr += len(op)
        if op in ' \n':
            self.addSpace(op)
            return
        elif op == '\\':
            self.tokens.append(Variable('\\'))
            self.addSpace(' ')
            return

        if op not in '[({':
            if (len(self.tokens) > 0 
                and isinstance(self.tokens[-1], (HFunction, Function)) 
                and self.tokens[-1].name in '; '):
                del self.tokens[-1] 
        
        if op == '(':
            if (len(self.tokens) > 0 
                and (not isinstance(self.tokens[-1], HFunction) 
                or  self.tokens[-1].name == ')')):
                self.tokens.append(operatorFromString('*'))
        self.tokens.append(operatorFromString(op))
    
    def addData(self):
        if self.acc != '':
            i = 0
            while (i < len(self.acc) 
                    and ('0' <= self.acc[i] <= '9' or self.acc[i] in '._')):
                i += 1
            if i == 0 or i == len(self.acc):                
                self.tokens.append(getData(self.acc)) 
            else:
                self.tokens.append(getData(self.acc[:i])) 
                self.tokens.append(operatorFromString('*'))
                self.tokens.append(getData(self.acc[i:])) 
            self.acc = ''
        
    def tokenize(self):
        while self.curr < len(self.string):
            if self.string[self.curr] == '\t':
                self.curr += 1
                continue
            if self.string[self.curr] == '#':
                self.curr += 1
                while self.string[self.curr] not in '#\n':
                    self.curr += 1
                    if self.curr == len(self.string):
                        return
                self.curr += 1
                continue
            op = self.searchOperator(utils.operators)
            if (op != None 
                and not (op == '.' 
                         and '0' <= self.string[self.curr + 1] <= '9')):
                self.addData()
                self.addOperator(op)
                continue
                    
            if self.string[self.curr] == '"':
                self.curr += 1
                self.addString()
                continue
            elif self.string[self.curr] == "'":
                if self.curr + 1 < len(self.string):
                    char = self.string[self.curr + 1]
                    if (self.curr + 2 < len(self.string) 
                        and self.string[self.curr + 2] == "'" and  char != "'" ):
                        self.tokens.append(Char(char))
                        self.curr += 3
                        continue
            self.acc += self.string[self.curr]
            self.curr += 1
      
        self.addData()
        self.addSpace(' ')
        del self.tokens[-1]
            
    def searchOperator(self, operators):
        max_length = max(map(len, operators))
        for length in range(max_length, 0, -1):
            if self.curr + length - 1 < len(self.string):
                substring = self.string[self.curr : self.curr + length]
                if substring in operators: 
                    return substring
        return None
