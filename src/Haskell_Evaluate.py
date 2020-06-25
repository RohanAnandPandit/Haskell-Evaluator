# -*- coding: utf-8 -*-
from Haskell_Functions import *
"""
Created on Mon Oct 28 11:50:01 2019

@author: rohan
"""
from functools import partial
from utils import *

FUNCTION_NUMBER = 0
def isInt(exp):
    try:        
        value = int(removeSpaces("".join(exp)))
        return True
    except:
        return False

def isFloat(exp):
    if ('.' not in exp):
        return False
    try:
        value = float(removeSpaces("".join(exp)))
        return True
    except:
        return False

def isTuple(exp):
    brackets = 0
    for char in exp:
        if (char == ','):
            if (brackets == 0):
                return True
        if (char in ['[', '(']):
            brackets += 1
        elif (char in [']', ')']):
            brackets -= 1
    return False
            

def constructList(exp, variables):
    from String_Formatting import tokenize, splitAtCommas

    l = splitAtCommas(exp)

    if (l == ['']):
        return []
    
    l2 = []
    for elem in l:
        l2.append(haskellEval(tokenize(elem, operators + brackets), variables))
    return l2

def constructTuple(exp, variables):
    return tuple(constructList(exp, variables))

def listComprehension(exp, variables):
    from String_Formatting import tokenize
    
    l = []
    (start, end) = exp.split('..')
    start = haskellEval(tokenize(start, operators), variables)
    end = haskellEval(tokenize(end, operators), variables)
    if (start <= end):
        while  (start <= end):
            l.append(start)
            start += 1
    return l

def evalBrackets(exp):
    exp = list(exp)
    i = 0
    while (i < len(exp)):
        c = exp[i]
        if (c == '(' ):
            insidebrackets = exp[i:indexOfClosing('(', exp[i:])]
            del exp[i:indexOfClosing('(', exp[i:])]
            exp.insert(i, haskellEval(insidebrackets))
            return exp[0:i]
        i += 1
             
        
'''
def applyFunction(exp, variables):
    func = "partial"+str(FUNCTION_NUMBER)
    FUNCTION_NUMBER += 1
    i = 1
    noOfArgs = 0
    while (i < len(exp)):
        if (exp[i] == " "):
            noOfArgs += 1
            if (noOfArgs == 1):
                eval(func +"= partial("+exp[0]+','+ str(getData(exp[i + 1])+')')
            else:
                eval(func +"= partial("+func+','+ str(getData(exp[i + 1])+')')
            i += 2
        else:
            break
    return func
'''
#exp is a list of strings starting with the name of the function
def functionCallString(exp, variables):
    string = getData(exp[0]) + '('
    i = 1
    noOfArgs = 0
    while (i < len(exp)):
        if (exp[i] == " "):
            noOfArgs += 1
            string += str(getData(exp[i + 1], variables))
            string += ','
            i += 2
        else:
            break
    return (string[: len(string) - 1] + ')', noOfArgs)
        
        
def simplifyBrackets(exp, variables):
    from String_Formatting import tokenize
    
    i = 0
    l = len(exp)
    while (i < l):
        string = exp[i]
        if (string == '('):
            if (isTuple(exp[i + 1])):
                result = constructTuple(exp[i + 1], variables)
            else:
                result = haskellEval(tokenize(exp[i + 1], operators+brackets), variables)
            del exp[i : i + 3]
            exp.insert(i, result)
            l -= 2
        i += 1
        
def simplifySquareBrackets(exp, variables):
    i = 0
    l = len(exp)
    while (i < l):
        string = exp[i]
        if (string == '['):
            result = constructList(exp[i + 1], variables)
            del exp[i : i + 3]
            exp.insert(i, result)
            l -= 2
        i += 1

def simplifyFunctions(exp, variables):
    i = 0
    l = len(exp)
    while (i < l):
        if (type(exp[i]) != str):
            i += 1
            continue
        string = exp[i]
        if (string in functions.keys()):
            (functionString, noOfArgs) = functionCallString(exp[i:], variables)
            del exp[i : i + 2 * noOfArgs + 1]
            exp.insert(i, eval(functionString))
            l -= 2 * noOfArgs
            
        elif (string == '`'):
            functionName = exp[i + 1]
            del exp[i : i + 3]
            exp.insert(i - 1, functionName)
            exp.insert(i, " ")
            exp.insert(i + 2, " ")
            i -= 1
            l -= 2
            continue
        i += 1

def simplifyAssignments(exp, variables):
    i = 0
    l = len(exp)
    while (i < l):
        chars = exp[i]
        if (chars == '='):
            value = haskellEval(exp[i + 1:], variables)
            variables[exp[i - 1]] = value
            return value
        i += 1

def simplifyExponents(exp, variables):
    i = len(exp) - 1
    while (i >= 0):
        chars = exp[i]
        if (chars == '^'):
            value = getData(exp[i-1], variables) ** getData(exp[i+1], variables)
            del exp[(i-1): i+2]
            exp.insert(i-1, value)
        i -= 1

def simplifyDivision(exp, variables):
    i = 0
    l = len(exp)
    while (i < l):
        chars = exp[i]
        if (chars == '/'):
            value = getData(exp[i-1], variables) / getData(exp[i+1], variables)
            del exp[(i-1): i+2]
            exp.insert(i-1, value)
            l -= 2
            i -= 1
        i += 1

def simplifyMultiplication(exp, variables):
    i = 0
    l = len(exp)
    while (i < l):
        chars = exp[i]
        if (chars == '*'):
            value = getData(exp[i-1], variables) * getData(exp[i+1], variables)
            del exp[(i-1): i+2]
            exp.insert(i-1, value)
            l -= 2
            i -= 1
        i += 1

def simplifyAddition(exp, variables):
    i = 0
    l = len(exp)
    while (i < l):
        chars = exp[i]         
        if (chars == '+'):
            value = getData(exp[i-1], variables) + getData(exp[i+1], variables)
            del exp[i-1: i+2]
            exp.insert(i-1, value)
            l -= 2
            i -= 1
        i += 1


def simplifySubtraction(exp, variables):
    i = 0
    l = len(exp)
    while (i < l):
        chars = exp[i]
        if (chars == '-'):
            value = getData(exp[i-1], variables) - getData(exp[i+1], variables)
            del exp[(i-1): i+2]
            exp.insert(i-1, value)
            l -= 2
            i -= 1
        i += 1 


def simplifyCons(exp, variables):
    i = len(exp)-1
    while (i >= 0):
        chars = exp[i]
        if (chars == ':'):
            value = [getData(exp[i-1], variables)] + getData(exp[i+1], variables)
            ##print(value)
            del exp[(i-1): i+2]
            exp.insert(i-1, value)
        i -= 1

def simplifyConcat(exp, variables):
    i = 0
    l = len(exp)
    while (i < l):
        chars = exp[i]
        if (chars == '++'):
            left = getData(exp[i-1], variables)
            right = getData(exp[i+1], variables)
            value = left[1 : len(left) - 1] + right[1 : len(right) - 1]
            if (type(value) == str):
                value = "\"" + value + "\"" 
            ##print(value)
            del exp[i - 1 : i + 2]
            exp.insert(i - 1, value)
            l -= 2
            i -= 1
        i += 1

def simplifyEquality(exp, variables):
    i = 0
    l = len(exp)
    while (i < l):
        chars = exp[i]
        if (chars == '=='):
            value = getData(exp[i-1], variables) == getData(exp[i+1], variables)
            ##print(value)
            del exp[(i-1): i+2]
            exp.insert(i-1, value)
            ##print(exp)
            l -= 2
        i += 1

def simplifyAnd(exp, variables):
    i = 0
    l = len(exp)
    while (i < l):
        chars = exp[i]
        if (chars == '&&'):
            value = getData(exp[i-1], variables) and getData(exp[i+1], variables)
            ##print(value)
            del exp[(i-1): i+2]
            exp.insert(i-1, value)
            ##print(exp)
            l -= 2
        i += 1

def simplifyOr(exp, variables):
    i = 0
    l = len(exp)
    while (i < l):
        chars = exp[i]
        if (chars == '||'):
            value = getData(exp[i - 1], variables) or getData(exp[i + 1], variables)
            del exp[i - 1 : i + 2]
            exp.insert(i-1, value)
            l -= 2
        i += 1

def simplifyListComprehension(exp, variables):
    i = 0
    l = len(exp)
    while (i < l):
        if (exp[i] == ".."):
            value = listComprehension(''.join(exp[i - 1 : i + 2]), variables)
            del exp[i - 2 : i + 3]
            exp.insert(i - 2, value)
            i -= 2
            l -= 4
        i += 1

# exp should be a list of tokens
def haskellEval(exp, variables):
    if (exp == []):
        return None
    '''
    if ("=" in exp):
        value = simplifyAssignments(exp, variables)
        return value
    '''
    simplifyAssignments(exp, variables)
    simplifyBrackets(exp, variables)
    simplifySquareBrackets(exp, variables)
    simplifyFunctions(exp, variables)
    simplifyExponents(exp, variables)
    simplifyDivision(exp, variables)
    simplifyMultiplication(exp, variables)
    simplifyAddition(exp, variables)
    simplifySubtraction(exp, variables)
    simplifyCons(exp, variables)
    simplifyConcat(exp, variables)
    simplifyEquality(exp, variables)
    simplifyAnd(exp, variables)
    simplifyOr(exp, variables)
    simplifyListComprehension(exp, variables)

    return getData(exp[0], variables)


