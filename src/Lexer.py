# -*- coding: utf-8 -*-
"""
Created on Mon Jun 22 10:20:56 2020

@author: rohan
"""
from utils import isPrimitive
from Types import Variable, Char, String
from Operators import operatorFromString
from HFunction import HFunction, Function, Lambda
from Types import Int, Float, Bool, Null

class Lexer:
    def __init__(self, string, program_state):
        self.tokens = []
        self.string = string
        self.index = 0
        self.curr = 0
        self.acc = ''
        self.program_state = program_state
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
        
    def addSpace(self, op = ' '):
        if len(self.tokens) > 0:
            lastToken = self.tokens[-1]
            if (op == '\n' and isinstance(lastToken, HFunction) 
                and lastToken.name == ' '):
                self.tokens.pop(-1)
                lastToken = self.tokens[-1]
            if (not isinstance(lastToken, (HFunction, Function, Lambda)) 
                or not lastToken.name in self.program_state.operators
                or lastToken.name in ')]}'):
                self.tokens.append(operatorFromString(op)) 
                        
    def addString(self):
        start = self.curr
        escape = False
        while not (self.string[self.curr] == '"' and not escape):
            escape = False
            if self.string[self.curr] == '\\':
                escape = True

            self.curr += 1
        string = self.string[start : self.curr].replace('\\n', '\n')
        string = string.replace('\\"', '"') 
        string = string.replace('\\t', '\t')
        self.tokens.append(String(string))
        self.curr += 1
    
    def addOperator(self, op):
        self.curr += len(op)
        if op in ' \n':
            self.addSpace(op)
            return
        elif op == '\\':
            self.tokens.append(Variable('\\'))
            self.addSpace()
            return
        elif op == '...':
            self.tokens.append(Variable('...'))
            return

        if op not in '[({':
            if (len(self.tokens) > 0 
                and isinstance(self.tokens[-1], (HFunction, Function)) 
                and self.tokens[-1].name in '; '):
                del self.tokens[-1] 
        
        if op == '(':
            if len(self.tokens) > 0:
                if (isinstance(self.tokens[-1], Variable) or 
                    self.tokens[-1].name == ')'):
                    self.addSpace()

        if op in '[{':
            if len(self.tokens) > 0:
                if (isinstance(self.tokens[-1], (Variable, String)) or 
                    self.tokens[-1].name in ']})'):
                    self.tokens.append(operatorFromString('!!'))
                    
        self.tokens.append(operatorFromString(op))
    
    def addData(self):
        if self.acc != '':
            i = 0
            while (i < len(self.acc) and 
                   ('0' <= self.acc[i] <= '9' or 
                    self.acc[i] in '._')):
                i += 1
            
            if i == 0 or i == len(self.acc):                
                self.tokens.append(self.getData(self.acc)) 
            else:
                self.tokens.append(self.getData(self.acc[:i])) 
                self.tokens.append(operatorFromString('*'))
                self.tokens.append(self.getData(self.acc[i:])) 
                
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
            
            op = self.searchOperator()
            if (op and not (op == '.' and 
                '0' <= self.string[self.curr + 1] <= '9')):
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
                    if (self.curr + 2 < len(self.string) and 
                        self.string[self.curr + 2] == "'" and  char != "'" ):
                        self.tokens.append(Char(char))
                        self.curr += 3
                        continue
                    
            self.acc += self.string[self.curr]
            self.curr += 1
      
        self.addData()
        self.addSpace(' ')
        if len(self.tokens) > 0:
            del self.tokens[-1]
            
    def searchOperator(self):
        max_length = max(map(len, self.program_state.operators))
        for length in range(max_length, 0, -1):
            if self.curr + length - 1 < len(self.string):
                substring = self.string[self.curr : self.curr + length]
                if substring in self.program_state.operators: 
                    return substring
        return None

    def getData(self, exp):
        if isPrimitive(exp): 
            return exp
    
        if '.' in str(exp):
            if int(float(exp)) == float(exp):
                return Int(int(float(exp)))
            return Float(round(float(exp), 10))
        try: 
            return Int(int(exp))
        except:
            pass
    
        if exp == 'True':
            return Bool(True) 
        elif exp == 'False':
            return Bool(False) 
        if exp == '?':
            return Null() 
        
        from Types import Variable
        return Variable(exp)