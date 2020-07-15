# -*- coding: utf-8 -*-
"""
Created on Mon Jun 22 11:24:28 2020

@author: rohan
"""
import List, Maybe, Char, Tuple, IO
import Prelude

state = {}

builtInState = {'True' : True, 'False' : False, 'otherwise' : True, 'None' : None}

operators = [' ', '/', '*', '+', '-', '^', '==', '<', '<=', '>', '>=', '&&', 
             '||', '(', ')', ',', '[', ']', ':', '++', '..', '/=', '!!', '`',
             '$', '.', '>>', '>>=', '=', '->', '--', '\\', 'where']

functionNames = Prelude.functionNamesPrelude 
functionNames += List.functionNamesList 
functionNames += Maybe.functionNamesMaybe 
functionNames += Char.functionNamesChar
functionNames += Tuple.functionNamesTuple
functionNames += IO.functionNamesIO

closer = {'[' : ']', '(' : ')'}

brackets = ['[', ']','(', ')']

class Variable:
    def __init__(self, name):
        self.name = name
    
    def simplify(self, state, simplifyVariables):
        if (self.name in builtInState.keys()):
            return builtInState[self.name]
        if (simplifyVariables):
            return state[self.name]
        return self
    
    def __str__(self):
        return self.name
    
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

def stringToList(string):
    from List import List, Nil
    from Operators import Operator
    from Expression import Data
    from Shunting_Yard_Algorithm import addBinaryExpr
    from Stack import Stack
    
    chars = Stack()
    operators = Stack()
    for char in string:
        chars.push(Data(char))
        operators.push(Operator.COLON.value)
    chars.push(Data(Nil()))
    while (operators.peek() != None):
        addBinaryExpr(operators, chars)
    return List(chars.pop())
        
    
    
def getData(exp, variables = None): # withVar tells whether variables should be replaced
    if (exp == ''):
        return None
    elif (isPrimitive(exp) and type(exp) != str):
        return exp
    try: 
        return int(exp)
    except:
        try: 
            return float(exp)
        except:
            return Variable(exp)

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
    return type(expr) in [int, float, bool, str, tuple, None]

def specialMin(a, b):
    if (a == None):
        return b
    if (b == None):
        return a
    return min(a, b)

def haskellEval(exp, state):  
    from Parser import Lexer
    from Shunting_Yard_Algorithm import generateExpr    
    lexer = Lexer(exp, state, operators, functionNames)
    print("tokens : ", end = '')
    lexer.printTokens() 
    (binExp, returnType) = generateExpr(lexer)
    print("expression : ", str(binExp))     
    print("result : ", end = '')
    return binExp.simplify(state, True) 
