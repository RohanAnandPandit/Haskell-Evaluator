# -*- coding: utf-8 -*-
from Haskell_Functions import *
"""
Created on Mon Oct 28 11:50:01 2019

@author: rohan
"""
from functools import partial
from utils import *

operators = ['&&', '||',' ','++' ,'+', '*', '|', '-', ':', '<', '>','<=',
              '>=','/','=', '==', '^', '/=', '`', '..'] # Haskell symbols
brackets = ['[', ']','(', ')']

functions = {'fst' : 1, 'snd' : 1, 'pred' : 1, 'succ' : 1,'length' : 1,'head': 1, 'tail' : 1, 'even' : 1, 'odd' : 1, 'maximum' : 1,
             'minimum' : 1, 'init' : 1, 'words' : 1, 'unwords':1, 'reverse' : 1,'take': 2, 'drop' : 2, 
             'div' : 2, 'mod' : 2,'take' : 2, 'elem' : 2, 'notElem' : 2, 'takeWhile':2, 'dropWhile':2, 'map':2, '&&' : 2, '||' : 2}


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
    lists = 0
    for char in exp:
        if (char == ','):
            if (lists == 0):
                return True
        if (char in ['[', '(']):
            lists += 1
        elif (char in [']', ')']):
            lists -= 1
    return False
            

def constructList(exp, variables):
    from String_Formatting import tokenize, splitAtCommas

    l = splitAtCommas(exp)
    if (len(l) == 1 and ".." in exp):
        return listComprehension(exp, variables)
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
             
def getData(exp, variables = None): # withVar tells whether variables should be replaced
    functionMap = {'map':'map2', '&&' : 'AND', '||' : 'OR'}
    
    if (type(exp) in [list, tuple, int, float, bool]):
        return exp
    elif (exp in functions.keys()):
        if (exp in functionMap.keys()):
            return functionMap[exp]
        return exp
    elif (exp in ['True', 'False']): # Checks if input is a bool
        return bool(exp)
    elif (variables != None and exp in variables.keys()):
        return variables[exp] # Returns value of variable
    elif (exp[0] == "[" and exp[len(exp) - 1] == "]"):
        l = constructList(exp[1 : len(exp) - 1], variables)
        return l
    elif (exp[0] == "(" and exp[len(exp) - 1] == ")"):
        tup = tuple(exp)
        return exp
    elif (exp[0] in ["'", "\""] and exp[len(exp) - 1] in ["'", "\""]):
        return str(exp[1 : len(exp) - 1])
    try: 
        return int(exp)
    except:
        try: 
            return float(exp)
        except:
            return None
        

def replaceData(exp):
    exp = list(exp)
    #if (type(exp) != list):
    #    return exp
    i = 0
    while (i < len(exp)):
        b = True
        if (i < len(exp) - 1):
            if (exp[i+1] == '='):
                b = False
        value = getData(exp[i], b)
        if (value != None):
            exp[i] = value
        i += 1
    return exp

def functionCallString(exp, variables):
    parameters = functions[exp[0]]
    string = getData(exp[0]) + '('
    for i in range(1, parameters + 1):
        string += str(getData(exp[i * 2], variables))
        if (i != parameters):
            string += ','
    return string + ')'
        
        
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
            arguments = functions[string]
            functionString = functionCallString(exp[i:], variables)
            del exp[i:i+arguments+1]
            exp.insert(i, eval(functionString))
            l -= 1 + arguments
            
        elif (string == '`'):
            functionString = functionCallString([exp[i+1],exp[i-1],exp[i+3]], variables)
            del exp[i-1:i+4]
            exp.insert(i-1, eval(functionString))
            i -= 1
            l -= 5
        i += 1

def simplifyAssignments(exp, variables):
    i = 0
    l = len(exp)
    while (i < l):
        chars = exp[i]
        if (chars == '='):
            variables[exp[i-1]] = getData(exp[i+1], variables)
            del exp[(i-1): i+2]
            l -= 2
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
            value = getData(exp[i-1], variables) + getData(exp[i+1], variables)
            ##print(value)
            del exp[(i-1): i+2]
            exp.insert(i-1, value)
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
            value = getData(exp[i-1], variables) or getData(exp[i+1], variables)
            ##print(value)
            del exp[(i-1): i+2]
            exp.insert(i-1, value)
            ##print(exp)
            l -= 2
        i += 1
        
def haskellEval(exp, variables):
    simplifyBrackets(exp, variables)
    simplifySquareBrackets(exp, variables)
    simplifyFunctions(exp, variables)
    simplifyAssignments(exp, variables)
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
        
    if (exp == []):
        return ''
    return getData(exp[0], variables)


