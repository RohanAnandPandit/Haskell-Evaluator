# -*- coding: utf-8 -*-
"""
Created on Mon Jun 22 10:20:56 2020

@author: rohan
"""

from utils import *
from Operators import operatorFromString, operatorSymbols
from HFunction import HFunction 

class Lexer:
    def __init__(self, exp):
        self.tokens = self.parse(list(exp), operators)
        self.index = 0
    
    def nextToken(self):
        if (self.index >= len(self.tokens)):
            return None
        value = self.tokens[self.index]
        self.index += 1
        return value
    
    def printTokens(self):
        tokens = []
        for token in self.tokens:
            if (isinstance(token, HFunction)):
                print(token.name, end = ' ')
            else:
                print(token, end = ' ')
    
    # NOTE: Pass a list of characters for exp
    # separators is a list of strings of at most length 2   
    def parse(self, exp, operators):
        tokens = []
        current = ''
        i = len(exp) - 1
        maxLength = max(list(map(len, operatorSymbols)))
        
        while (i >= 0):
            #print(tokens)
            add = 0
            char = exp[i] # current character
            
            if (char == "\""):
                j = i - 1
                while (exp[j] != "\""):
                    j -= 1
                tokens.insert(0, ''.join(exp[j + 1 : i]))
                i = j - 1
                continue
            
            for length in range(maxLength, 0, -1):
                if (0 <= i - length + 1):
                    substring = ''.join(exp[i - length + 1 : i + 1])
                    if (substring in operatorSymbols): # Checks two consecutive chars
                        if (current != ''):
                            tokens.insert(0, getData(current))
                            current = ''
                            
                        if (substring not in functions.keys() and substring not in  [')', ']']):
                            if (len(tokens) > 0):
                                if (isinstance(tokens[0], HFunction)):
                                    if (tokens[0].name == ' '):
                                        del tokens[0]    
                                        
                        if (length == 1): # Now checks the single character                    
                            if (char == ' '):
                                if (len(tokens) > 0):
                                    if (isinstance(tokens[0], HFunction) and tokens[0].name not in ['(', '[']):
                                        add = 1
                                        break
                                else:
                                    add = 1
                                    break
                                
                        op = operatorFromString(substring)
                        tokens.insert(0, op.value)
                        add = length
                        break
                    
            if (add == 0):
                current = char + current # it is concatenated to the previous element
                add = 1
                
            i -= add
            
        if (current != ''):
            tokens.insert(0, getData(current))
            
        i = 0
        # Remove white spaces at front
        while (i < len(tokens)):
            if (isinstance(tokens[i], HFunction)):
                if (tokens[i].name == ' '):
                    i += 1
                else:
                    break
            else:
                break
            
        return tokens[i :]
'''
elif (char in ['[', '(']):
    end = indexOfClosing(char, exp[i:]) -
    tokens.append(operatorFromString(char)) 
    tokens.append(''.join(exp[i + 1 : i + end]))
    tokens.append(operatorFromString(closer[char])) 
    i += end + 1
'''

#p = Lexer("\"Rohan\" ++ \" Pandit\"")
#p.printTokens()