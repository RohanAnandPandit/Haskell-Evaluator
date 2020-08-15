# -*- coding: utf-8 -*-
"""
Created on Mon Jun 22 11:24:28 2020

@author: rohan
"""
import List, Maybe, IO
import Prelude
from Types import Variable, Int, Float, Bool, EnumValue, Object, Structure, Char
from List import Nil, Cons, head, tail, Range
from Tuple import functionNamesTuple, Tuple
'''
global builtInState, static_mode, functional_mode, frameStack, enumNames
global typeNames, structNames, operators, keywords, continueLoop, breakLoop 
global return_value, functionNames
'''
builtInState = {}
static_mode = False
functional_mode = False
frameStack = [builtInState]
enumNames = []
typeNames = ['int', 'float', 'char', 'bool', 'var', 'list', 'tuple', 'string',
             'Num']
structNames = []
operators = [' ', '/', '*', '+', '-', '^', '==', '<', '<=', '>', '>=', '&&', 
             '||', '(', ')', ',', '[', ']', ':', '++', '..', '/=', '!!', '`',
             '$', ';', '>>', '>>=', '=', '->', '--', '\\',  ' where ', '|', '@',
             '<-', '<<', '&', '}', '¦', ' then ', ' else ', '#', '{', '=>', '~',
             ',,', '\n', '.', ' extends ', ' implements ', '!=', ' in ',
             '+=', '-=', '*=', '/=', '^=']

keywords = ('class', 'def', 'struct', 'interface', 'extends',
            'where', 'implements', 'while', 'for', 'case', 'default',
            'if', 'else', 'then', 'enum', 'oper', 'break', 'continue',
            'cascade', 'in', 'True', 'False', 'let', 'import', 'return',
            'int', 'float', 'bool', 'char', 'var', 'do', '?', 'list', 'tuple',
            'string', 'Num', 'from', 'type', 'union', 'breakout', 'skipout') 

continueLoop = 0
breakLoop = 0
return_value = None
functionNames = Prelude.functionNamesPrelude
functionNames += List.functionNamesList 
functionNames += Maybe.functionNamesMaybe 
#functionNames += Char.functionNamesChar
functionNames += functionNamesTuple
functionNames += IO.functionNamesIO
functionNames += ['eval', 'read', 'range', 'toInt', 'toBool', 'toChar', 'toFloat']

def reset_state():
    import utils
    utils.builtInState = {}
    utils.static_mode = False
    utils.functional_mode = False 
    utils.frameStack = [builtInState]
    utils.enumNames = []
    utils.typeNames = ['Int', 'Float', 'Char', 'Bool']
    utils.structNames = []
    utils.operators = [' ', '/', '*', '+', '-', '^', '==', '<', '<=', '>', '>=', '&&', 
                 '||', '(', ')', ',', '[', ']', ':', '++', '..', '/=', '!!', '`',
                 '$', ';', '>>', '>>=', '=', '->', '--', '\\',  ' where ', '|', '@',
                 '<-', '<<', '&', '}', '¦', ' then ', ' else ', '#', '{', '=>', '~',
                 ',,', '\n', '.', ' extends ', ';;', ' implements ', '!=', ' in ']
    
    utils.keywords = ('class', 'def', 'struct', 'interface', 'extends',
                'where', 'implements', 'while', 'for', 'case', 'default',
                'if', 'else', 'then', 'enum', 'oper', 'break', 'continue',
                'cascade', 'in', 'True', 'False', 'let', 'import', 'return', 'do')
    
    utils.continueLoop = False
    utils.breakLoop = False
    utils.return_value = None
    utils.functionNames = Prelude.functionNamesPrelude
    utils.functionNames += List.functionNamesList 
    utils.functionNames += Maybe.functionNamesMaybe 
    utils.functionNames += Char.functionNamesChar
    utils.functionNames += functionNamesTuple
    utils.functionNames += IO.functionNamesIO
    utils.functionNames += ['eval', 'read', 'range', 'toInt', 'toBool', 'toChar', 'toFloat']


closer = {'[' : ']', '(' : ')'}

brackets = ['[', ']','(', ')']

def stringToList(string):
    from List import List, Nil
    from Operators import Operator
    from Expression import Data
    from Parser import addBinaryExpr
    from Stack import Stack
    chars = Stack()
    operators = Stack()
    for char in string:
        chars.push(Data(char))
        operators.push(Operator.COLON.value)
    chars.push(Data(Nil()))
    while operators.peek() != None:
        addBinaryExpr(operators, chars)
    return List(chars.pop())
        

def getData(exp):
    if isPrimitive(exp):
        return exp

    if '.' in str(exp):
        return Float(float(exp))
    try: 
        return Int(int(exp))
    except:
        pass

    if exp == 'True':
        return Bool(True)
    elif exp == 'False':
        return Bool(False)
    if exp in '?':
        return Int(None)
    
    from Types import Variable
    return Variable(exp)

def isPrimitive(expr):
    return type(expr) in [Int, Float, Bool, Char, EnumValue]

def evaluate(exp):  
    from Lexer import Lexer
    from Parser import parse  
    if isinstance(exp, Cons):
        exp = str(exp)[1:-1]
    lexer = Lexer(exp)
    print("tokens : ", end = '')
    lexer.printTokens() 
    expr = parse(lexer)
    #expr = optimise(expr)
    print("expression : ", str(expr)) 
    print("result : ", end = '')
    #try:
    return expr.simplify()
    #except Exception as error:
        #print(' '.join(error.args))

def patternMatch(expr1, expr2):
    from Operator_Functions import equals
    from Expression import BinaryExpr #hello bye hi shy
    if expr1 == expr2 == None:
        return True
    if isinstance(expr1, Variable):
        return True
    if isinstance(expr1, BinaryExpr) and expr1.operator.name == '@':
        return patternMatch(expr1.expr, expr2)
    if isPrimitive(expr1) and isPrimitive(expr2):
        return equals(expr1, expr2).value
    if isinstance(expr1, Nil) and isinstance(expr2, Nil):
        return True
    if isinstance(expr1, Range) and isinstance(expr2, Range):
        return (patternMatch(head(expr1), head(expr2)) 
                and patternMatch(tail(expr1), tail(expr2)))
    if isinstance(expr1, Cons):
            return (patternMatch(head(expr1), head(expr2)) 
                    and patternMatch(tail(expr1), tail(expr2)))
    if isinstance(expr1, Tuple) and isinstance(expr2, Tuple):
        if len(expr1.tup) != len(expr2.tup):
            return False
        for i in range(len(expr1.tup)):
            if not patternMatch(expr1.tup[i], expr2.tup[i]):
                return False
        return True
    if isinstance(expr1, BinaryExpr): 
        if typeMatch(expr1.leftExpr, expr2):
            if isinstance(expr2, Structure):
                return patternMatch(expr1.rightExpr, Tuple(expr2.values))
            else:
                return patternMatch(expr1.rightExpr, expr2)
    return False


def typeMatch(type_, expr):
    from Types import Type, Union
    from Expression import BinaryExpr
    if isinstance(type_,  Variable):
        if isinstance(type_.simplify(), Type):
            return typeMatch(type_.simplify().expr, expr)
        elif isinstance(type_.simplify(), Union):
            type_ = type_.simplify()
            for t in type_.types:
                if typeMatch(t, expr):
                    return True
        elif isinstance(expr, Structure):
            return type_.name == expr.type.name
        elif isinstance(expr, Object):
            return type_.name == expr.classType.name
        elif isPrimitive(expr):
            if type_.name == 'Num' and isinstance(expr, (Int, Float)):
                return True
            return type_.name == expr.type
        elif type_.name == 'list' and isinstance(expr, (Nil, Cons)):
            return True
        elif type_.name == 'tuple' and isinstance(expr, Tuple):
            return True
        elif (type_.name == 'string' 
              and (isinstance(expr, Nil) or isinstance(expr, BinaryExpr) 
              and expr.operator.name == ':' 
              and isinstance(expr.leftExpr, Char))):
            return True
    elif isinstance(type_, Nil) and (isinstance(expr, (Nil, Cons))):
        return True
    elif isinstance(type_, Cons) and isinstance(expr, Cons):
        return typeMatch(head(type_), head(expr)) and typeMatch(tail(type_), tail(expr))
    elif isinstance(type_, Tuple) and isinstance(expr, Tuple):
        if len(type_.tup) != len(expr.tup):
            return False
        for i in range(len(type_.tup)):
            if not typeMatch(type_.tup[i], expr.tup[i]):
                return False
        return True
    return False
    
def optimise(expr):
    from Expression import BinaryExpr
    from Operator_Functions import equals
    if isinstance(expr, BinaryExpr):
        expr.leftExpr = optimise(expr.leftExpr)
        expr.rightExpr = optimise(expr.rightExpr)
        if expr.operator.name in ('+', '||'):
            if equals(expr.leftExpr, Int(0)).value:
                if expr.rightExpr != None:
                    return expr.rightExpr
            elif equals(expr.rightExpr, Int(0)).value:
                if expr.leftExpr != None:
                    return expr.leftExpr
        elif expr.operator.name == '-':
                if equals(expr.rightExpr, Int(0)).value:
                    if (expr.leftExpr != None):
                        return expr.leftExpr
        elif expr.operator.name == '*':
            if equals(expr.leftExpr, Int(0)).value:
                if expr.rightExpr != None:
                    return Int(0) 
            elif equals(expr.rightExpr, Int(0)).value:
                if expr.leftExpr != None:
                    return Int(0)
            elif equals(expr.leftExpr, Int(1)).value:
                if expr.rightExpr != None:
                    return expr.rightExpr
            elif equals(expr.rightExpr, Int(1)).value:
                if expr.leftExpr != None:
                    return expr.leftExpr
        elif expr.operator.name == '&&':
            if equals(expr.leftExpr, Int(0)).value:
                if expr.rightExpr != None:
                    return Bool(False)
            elif equals(expr.rightExpr, Int(0)).value:
                if expr.leftExpr != None:
                    return Bool(False)
        elif expr.operator.name == '/':
            if equals(expr.leftExpr, Int(0)).value:
                if expr.rightExpr != None:
                    return Int(0)
            elif equals(expr.rightExpr, Int(1)).value:
                if expr.leftExpr != None:
                    return expr.leftExpr
        elif expr.operator.name == '^':
            if equals(expr.leftExpr, Int(1)).value:
                if expr.rightExpr != None:
                    return Int(1)
            elif equals(expr.leftExpr, Int(0)).value:
                if expr.rightExpr != None:
                    return Int(0)
            elif equals(expr.rightExpr, Int(1)).value:
                if expr.leftExpr != None:
                    return expr.leftExpr
            elif equals(expr.rightExpr, Int(0)).value:
                if expr.leftExpr != None:
                    return Int(1)
        elif expr.operator.name == '++':
            if isinstance(expr.leftExpr, Nil):
                if expr.rightExpr != None:
                    return expr.rightExpr
            elif isinstance(expr.rightExpr, Nil):
                if expr.leftExpr != None:
                    return expr.leftExpr

    return expr

def replaceVariables(expr):
    from Expression import BinaryExpr
    from Types import Collection
    if isinstance(expr, Variable):
        expr = expr.simplify()
    elif isinstance(expr, BinaryExpr):
        left = expr.leftExpr
        if expr.operator.name not in ('=', 'where'):
            left = replaceVariables(expr.leftExpr)
        right = replaceVariables(expr.rightExpr)
        expr = BinaryExpr(expr.operator, left, right)
    elif isinstance(expr, Cons):
        expr = Cons(replaceVariables(expr.item), replaceVariables(expr.tail))
    elif isinstance(expr, Tuple):
        expr = Tuple(list(map(lambda exp: replaceVariables(exp), expr.tup)))
    elif isinstance(expr, Collection):
        expr = Collection(list(map(lambda exp: replaceVariables(exp), expr.items)), expr.operator)        
    return expr

def convertToList(expr):
    # If None is returned means there was no operand or 
    # operator which means it is an empty list
    xs = Nil()
    for i in range(len(expr) - 1, -1, -1):
        xs = Cons(expr[i], xs)
    return xs
    
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


def specialMin(a, b):
    if (a == None):
        return b
    if (b == None):
        return a
    return min(a, b)

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

