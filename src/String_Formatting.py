# -*- coding: utf-8 -*-
"""
Created on Mon Jun 22 10:20:56 2020

@author: rohan
"""

from utils import *

digitChar = ['0','1','2','3','4','5', '6', '7', '8','9'] 
closer = {'[' : ']', '(' : ')'}
brackets = ['[', ']','(', ')']


def splitAtCommas(exp):
    brackets = 0
    for i in range(0, len(exp)):
        char = exp[i]
        if (char in ["[", '(']):
            brackets += 1
        elif (char in [']', ')']):
            brackets -= 1
        elif (char == ',' and brackets == 0):
            return [exp[0:i]] + splitAtCommas(exp[i + 1:])
    return [exp]
    
    
def removeSpaces(exp):
    l = []
    for char in exp:
        if (char != " "):
            l.append(char)
    return "".join(l)


def balancedBrackets(c, exp):
    count = 0
    for char in exp:
        if (char == c):
            count += 1
        elif (char == closer[c]):
            if (count == 0):
                return False
            else:
                count -= 1
    return count == 0
            
def getString(c, exp):
    index = 0
    count = -1
    for char in exp:
        if (char == c and count == 0):
            return index
        if (char == c):
            count += 1
        index += 1
            
     
def removeUnwantedSpaces(exp):
    exp = list(exp)
    i = 0
    prev = ""
    l = len(exp)
    while (i < l):
        current = exp[i]
        if (current == " " and prev in [" ", ',']):
            del exp[i]
            l -= 1
            pass
        else:
            prev = current
            i += 1
    return "".join(exp)
        
def getParameters(exp, n):
    return (exp.split(' ')[0:n], exp.split(' ')[n:])

def checkOperators(exp):
    operators = ['|','+', '*', '@', '&', '|', '-', ':', '<', '>', '=','/', '^','(',')']
    for char in exp:
        if (char in operators):
            return True
        else:
            continue
    return False

# NOTE: Pass a list of characters for exp
# separators is a list of strings of at most length 2    
def separateText(exp, separators):
    i = 0
    while (i < len(exp)):
        char = exp[i] # current character
        if (''.join(exp[i : i + 2]) in separators): # Checks two consecutive chars
            # Concatenates three sections by recursively calling on remaining
            return exp[0:i] + [''.join(exp[i : i + 2])] + separateText(exp[i + 2 :], separators)
        
        elif (char in separators): # Now checks the single character
            if (char == "\""):
                end = closingQuote(exp[i:]) 
                return exp[0 : i] + [''.join(exp[i : i + end + 1])] + separateText(exp[i + end + 1 :], separators)
            elif (char in ['[', '(']):
                end = indexOfClosing(char, exp[i:]) 
                return exp[0:i] + [char] + [''.join(exp[i + 1 : i + end])] + [closer[char]] + separateText(exp[i + end + 1 :], separators)
            else:
                return exp[0:i] + [char] + separateText(exp[i + 1 :], separators)

        
        if (i > 0): # If char is not a symbol then
            exp[i - 1] += char # it is concatenated to the previous element
            del exp[i] # and the char is deleted from the list
            return separateText(exp, separators) # Function called on this new list
        i += 1
    return exp

def removeSpaceAroundOperators(exp):
    from Haskell_Evaluate import operators
    i = 0
    l = len(exp)
    while (i < l):
        string = exp[i]
        if string in operators:
            if (i > 0):
                if (exp[i - 1] == " "):
                    del exp[i - 1]
                    i -= 1
                    l -= 1
            if (i < l - 1):
                if (exp[i + 1] == " "):
                    del exp[i + 1]
                    i -= 1
                    l -= 1
        i += 1
        
def tokenize(exp, separators):
    exp = removeUnwantedSpaces(exp)
    exp = separateText(list(exp), separators)
    removeSpaceAroundOperators(exp)
    return exp

