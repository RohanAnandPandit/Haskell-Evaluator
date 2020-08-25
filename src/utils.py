# -*- coding: utf-8 -*-
"""
Created on Mon Jun 22 11:24:28 2020

@author: rohan
"""
import List, IO
import Prelude
from Types import (Variable, Int, Float, Bool, EnumValue, Object, Structure,
                   Char)
from List import Nil, Cons, head, tail, Range, Array
from Tuple import functionNamesTuple, Tuple
from HFunction import Func
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
typeNames = ['int', 'float', 'char', 'bool', 'var', 'Num', 'global', 'local',
             'hidden', 'Func']
structNames = []
operators = [' ', '/', '*', '+', '-', '^', '==', '<', '<=', '>', '>=', '&&', 
             '||', '(', ')', ',', '[', ']', ':', '++', '..', '/=', '!!', '`',
             '$', ';', '>>', '>>=', '=', '->', '--', '\\',  ' where ', '|',
             '@', '<-', '<<', '&', '}', '¦', ' then ', ' else ', '\t', '{',
             '=>', '~', ',,', '\n', '.', ' inherits ', ' implements ', '!=',
             ' in ', '+=', '-=', '*=', '/=', '^=', '//', '%', '::', '...'] 

keywords = ('class', 'def', 'struct', 'interface', 'inherits', 'where',
            'implements', 'while', 'for', 'switch', 'default', 'if', 'else',
            'then', 'enum', 'oper', 'break', 'continue', 'in', 'True', 
            'False', 'let', 'import', 'return', 'int', 'float', 'bool',
            'char', 'var', 'do', '?', 'Num', 'from', 'type', 'union', 
            'stop', 'skip', 'global', 'local', 'hidden', 'Func')  

continueLoop = 0
breakLoop = 0
return_value = None
functionNames = Prelude.functionNamesPrelude
functionNames += List.functionNamesList 
#functionNames += Char.functionNamesChar
functionNames += functionNamesTuple
functionNames += IO.functionNamesIO
functionNames += ['eval', 'read', 'range', 'toInt', 'toBool', 'toChar',
                  'toFloat', 'match']

lazy_eval = ('=', '->', 'where', '|', '.', '\n', ';', '+=', '-=', '*=', '/=',
             '^=', '=>', ':', '::',  'while', 'for', 'struct', 'enum', 'oper', 
             'class', 'interface', 'def', 'switch', 'if', 'let', 'import',
             'do', 'int', 'float', 'char', 'bool', 'from', 'type', 'union',
             'where', 'in', 'global', 'local', 'hidden', 'match', '||', '&&')

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
    #print("tokens : ", end = '')
    #lexer.printTokens() 
    expr = parse(lexer)
    #expr = optimise(expr)
    #print("expression : ", str(expr)) 
    #print("result : ", end = '')
    #try:
    return expr.simplify()
    #except Exception as error:
        #print(' '.join(error.args))

def patternMatch(expr1, expr2):
    from Operator_Functions import equals
    from Expression import BinaryExpr
    if expr1 == None:
        return True
    
    if isinstance(expr1, Variable):
        return True
    
    if isinstance(expr1, BinaryExpr) and expr1.operator.name == '@':
        return patternMatch(expr1.expr, expr2)
    
    if isPrimitive(expr1) and isPrimitive(expr2):
        return equals(expr1, expr2).value
    
    if isinstance(expr1, Nil) and isinstance(expr2, Nil):
        return True
    
    if isinstance(expr1, (Cons, Range)):
            return (patternMatch(head(expr1), head(expr2).simplify()) 
                    and patternMatch(tail(expr1), tail(expr2)))
            
    if isinstance(expr1, BinaryExpr) and expr1.operator.name == ':':
            return (patternMatch(expr1.leftExpr, head(expr2).simplify()) 
                    and patternMatch(expr1.rightExpr, tail(expr2)))    
    
    if type(expr1) == type(expr2) and type(expr1) in (Tuple, Array):
        if len(expr1.items) == 0:
            return True
        if len(expr1.items) != len(expr2.items):
            if (isinstance(expr1.items[-1], Variable) and 
                expr1.items[-1].name == '...'):
                if len(expr1.items) - 1 > len(expr2.items):
                    return False
            else:
                return False
            
        if (len(expr1.items) > 0 and isinstance(expr1.items[0], Variable) and 
              expr1.items[0].name == '...'):
            return True
        
        return (patternMatch(expr1.items[0], expr2.items[0].simplify()) and
                patternMatch(Tuple(expr1.items[1:]), Tuple(expr2.items[1:]))) 

    if isinstance(expr1, BinaryExpr): 
        if typeMatch(expr1.leftExpr, expr2):
            if isinstance(expr2, Structure):
                return patternMatch(expr1.rightExpr, Tuple(expr2.values))
            else:
                return patternMatch(expr1.rightExpr, expr2)
    return False

def typeMatch(type_, expr):
    from Types import Type, Union
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
            return type_.name == expr.class_.name
        elif isPrimitive(expr):
            return type_.name == expr.type
        elif issubclass(type(expr), Func):
            return type_.name == 'Func'

    elif isinstance(type_, Nil) and isinstance(expr, (Nil, Cons)):
        return True
    
    elif isinstance(type_, Cons) and isinstance(expr, Cons):
        return (typeMatch(head(type_), head(expr)) 
                and typeMatch(tail(type_), tail(expr)))

    if (type(expr) in (Tuple, Array) and isinstance(type_, Variable) and
        type_.name == '...'): 
        return True
    
    elif type(type_) == type(expr) and type(type_) in (Tuple, Array):
        if len(type_.items) == 0:
            return True
        elif (isinstance(type_.items[0], Variable) and 
              type_.items[0].name == '...'):
            return True
        elif len(type_.items) != len(expr.items):
            if (isinstance(type_.items[-1], Variable) and 
                type_.items[-1].name == '...'):
                if len(type_.items) - 1 > len(expr.items):
                    return False
            else:
                return False
        return (typeMatch(type_.items[0], expr.items[0]) and
                typeMatch(Tuple(type_.items[1:]), Tuple(expr.items[1:])))
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
        if expr.name not in typeNames:
            expr = expr.simplify()
    elif isinstance(expr, BinaryExpr):
        if expr.operator.name == '.':
            try:
                return expr.simplify()
            except:
                pass
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
        expr = Collection(list(map(lambda exp: replaceVariables(exp),
                                   expr.items)), expr.operator)        
    return expr

def convertToList(expr):
    # If None is returned means there was no operand or 
    # operator which means it is an empty list
    xs = Nil()
    for i in range(len(expr) - 1, -1, -1):
        xs = Cons(expr[i], xs)
    return xs