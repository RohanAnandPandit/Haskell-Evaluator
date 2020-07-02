# -*- coding: utf-8 -*-
"""
Created on Mon Jun 22 10:20:56 2020

@author: rohan
"""

from utils import operators, functionNames, getData
import Operators
from Operators import operatorFromString
from HFunction import HFunction 

class Lexer:
    def __init__(self, exp, state):
        self.tokens = self.parse(list(exp), state)
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
                tokens.append(token.name)
            else:
                tokens.append(token)
        print(tokens)
    
    # NOTE: Pass a list of characters for exp
    # separators is a list of strings of at most length 2   
    def parse(self, exp, state):
        from Shunting_Yard_Algorithm import convertToList
        
        operatorSymbols = functionNames + operators
        tokens = []
        current = ''
        i = len(exp) - 1
        maxLength = max(list(map(len, operatorSymbols)))
        isAssignment = False
        # String is iterated from right to left
        while (i >= 0):
            self.tokens = tokens
            operator = None
            char = exp[i]
            
            # If the current character is a double quote the corresponding quote is 
            # found and the string between them is added as a token
            if (char in ["\""] and not isAssignment):
                j = i - 1
                while (exp[j] != char):
                    j -= 1
                string = convertToList(exp[j + 1 : i])
                string.type = 'string'
                tokens.insert(0, string)
                i = j - 1
                continue
                
                
            # The substrings up to this index are checked to see if this is an 
            # operator or function name
            operator = self.searchOperator(exp, i, maxLength, operatorSymbols)
            if (operator == '='):
                isAssignment = True
                
            if (operator != None):  
                isFunction = operator in functionNames
                putParentheses = isFunction
                isCloseBracket = operator in [')', ']']
    
                # The backtick is not included as a token but it will 
                # cause white space to be removed around a function name                
                if (len(tokens) > 0 and isinstance(tokens[0], HFunction) 
                    and tokens[0].name == '`'): 
                    putParentheses = False
                    del tokens[0] 
                    
                # When an operator is encountered the previously accumulating
                # value is added as a token after converting to its actual type 
                if (current != ''):
                    tokens.insert(0, getData(current, state))
                    current = ''           
                    
                # A space cannot be put before an operator except 
                # for open brackets
                if (operator == ' '):
                    if (len(tokens) > 0): 
                        if (isinstance(tokens[0], HFunction) 
                        and tokens[0].name not in ['(', '[']):
                            if (tokens[0].name == '`'):
                                del tokens[0]
                            i -= 1
                            continue
                    else:
                        i -= 1
                        continue  
              
                # If current operator is a symbol there shouldn't be a space after it
                if (not isFunction and not isCloseBracket):
                    if (len(tokens) > 0):
                        if (isinstance(tokens[0], HFunction) and tokens[0].name == ' '):
                            del tokens[0]
                
                # A function is naturally enclosed in brackets as an
                # argument to the SPACE operator 
                if (isFunction and putParentheses):
                    putParentheses = True
                    tokens.insert(0, operatorFromString(')').value)
                
                # The corresponding HFunction of the operator is added as a token
                op = operatorFromString(operator)
                tokens.insert(0, op.value)
                
                if (isFunction and putParentheses):
                    tokens.insert(0, operatorFromString('(').value)
                    
            else:
                # If there is no operator up to the current index then the current
                # char is concatenated to the accumulating data
                current = char + current
                
            # Index is shifted back
            if (operator != None):
                i -= len(operator)
            else:
                i -= 1
                
            #self.printTokens()  
            
        # Remaining value of data is added
        if (current != ''):
            tokens.insert(0, getData(current, state))
            
        # Remove white space at front
        if (i >= 0 and isinstance(tokens[i], HFunction) and tokens[i].name == ' '):
            return tokens[1 : ]
            
        return tokens
    
    def searchOperator(self, exp, i, maxLength, operatorSymbols):
        for length in range(maxLength, 0, -1):
            if (0 <= i - length + 1):
                substring = ''.join(exp[i - length + 1 : i + 1])
                if (substring in operatorSymbols):
                    return substring
        return None
