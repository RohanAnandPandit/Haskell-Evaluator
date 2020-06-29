# -*- coding: utf-8 -*-
"""
Created on Mon Jun 22 11:24:28 2020

@author: rohan
"""
import List, Maybe, Char, Tuple
import Prelude

operators = [' ', '/', '*', '+', '-', '^', '==', '<', '<=', '>', '>=', '&&', 
             '||', '(', ')', ',', '[', ']', ':', '++', '..', '/=', '!!', '`',
             '$', '.']

functionNames = Prelude.functionNamesPrelude 
functionNames += List.functionNamesList 
functionNames += Maybe.functionNamesMaybe 
functionNames += Char.functionNamesChar
functionNames += Tuple.functionNamesTuple

closer = {'[' : ']', '(' : ')'}

brackets = ['[', ']','(', ')']


def indexOfClosing(c, exp):
    closer = {'[' : ']', '(' : ')'}
    index = 0
    count = 0
    for char in exp:
        if (char == c):
            count += 1
        elif (char == closer[c]):
            count -= 1
            if (count == 0):
                return index
        index += 1
    return None

def closingQuote(exp):    
    index = 0
    insideString = False
    for char in exp:
        if (char == "\""):
            if (insideString):
                return index
        if (char == "\""):
            insideString = True
        index += 1
    return None

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
    return ''.join(l)



            
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
    prev = " "
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

def removeSpaceAroundOperators(exp):
    from Haskell_Evaluate import operators
    i = 0
    l = len(exp)
    while (i < l):
        string = exp[i]
        if string in operators:
            if (string not in brackets):
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
    return ''.join(exp)

def getData(exp, variables = None): # withVar tells whether variables should be replaced
    functionMap = {'map' : 'map2'}
    if (exp == ''):
        return None
    if (isPrimitive(exp) and type(exp) != str):
        return exp
    elif (exp in functionNames):
        from Operators import operatorFromString
        return operatorFromString(exp)
    elif (exp in ['True', 'False']): # Checks if input is a bool
        boolMap = {'True' : True, 'False' : False}
        return boolMap[exp]
    try: 
        return int(exp)
    except:
        try: 
            return float(exp)
        except:
            return exp

def dimensionOf(l):
    dim = 0
    initialType = type(l)
    while (type(l) == initialType and initialType in [list, tuple]):
        dim += 1
        if (len(l) > 0):
            l = l[0]
        else:
            break
    return dim

def isPrimitive(expr):
    return type(expr) in [int, float, bool, str]
#print(getData('False'))