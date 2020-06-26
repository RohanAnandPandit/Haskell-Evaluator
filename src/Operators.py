# -*- coding: utf-8 -*-
"""
Created on Tue Jun 23 09:24:41 2020

@author: rohan
"""
from enum import Enum
from HFunction import HFunction
from Haskell_Functions import *
from utils import *

operatorSymbols = [' ', '/', '*', '+', '-', '^', '==', '<', '<=', '>', '>=', 
                   '&&', '||', '(', ')',',', '[', ']', ':' , '++', '..','fst',
                   'map', 'succ', 'length', 'pred', 'take', 'drop', 'even', 'odd',
                   'maximum', 'minimum', 'elem', 'notElem', 'zip', 'div', 'mod']

operatorStrings = ['SPACE' 'SLASH', 'ASTERISK', 'PLUS', 'MINUS', 'CARET',
                   'DOUBLE_EQUAL', 'LESS_THAN', 'LESS_THAN_OR_EQUAL',
                   'GREATER_THAN', 'GREATER_THAN_OR_EQUAL', 'DOUBLE_AMPERSAND',
                   'DOUBLE_BAR', 'LEFT_PARENTHESES', 'RIGHT_PARENTHESES', 'COMMA',
                   'LEFT_BRACKET', 'RIGHT_BRACKET', 'COLON', 'DOUBLE_PLUS', 'DOUBLE_PERIOD'
                    'FST', 'MAP', 'SUCC', 'LENGTH', 'PRED', 'TAKE', 'DROP', 'EVEN',
                    'ODD', 'MAXIMUM', 'MINIMUM', 'ELEM', 'NOT_ELEM', 'ZIP', 'DIV', 'MOD']

class Associativity(Enum):
    LEFT = 0
    RIGHT = 1
    NONE = 2

apply = HFunction(10, Associativity.LEFT, space, 2, ' ')
division = HFunction(7, Associativity.LEFT, divide, 2, '/')
multiply = HFunction(7, Associativity.LEFT, multiply, 2, '*')
add = HFunction(6, Associativity.LEFT, add, 2, '+')
subtract = HFunction(6, Associativity.LEFT, subtract, 2, '-')
power = HFunction(8, Associativity.RIGHT, power, 2, '^')
equality = HFunction(4, Associativity.LEFT, equals, 2, '==')
less_than = HFunction(4, Associativity.NONE, lessThan, 2, '<')
greater_than = HFunction(4, Associativity.NONE, greaterThan, 2, '>')
less_than_or_equal = HFunction(4, Associativity.NONE, lessThanOrEqual, 2, '<=')
greater_than_or_equal = HFunction(4, Associativity.NONE, greaterThanOrEqual, 2, '>=')
colon = HFunction(5, Associativity.RIGHT, cons, 2, ':')
logical_and = HFunction(3, Associativity.RIGHT, AND, 2, '&&')
logical_or = HFunction(3, Associativity.RIGHT, OR, 2, '||')
left_parentheses = HFunction(4, Associativity.RIGHT, None, 1, '(')
right_parentheses = HFunction(4, Associativity.LEFT, None, 1, ')')
create_tuple = HFunction(4, Associativity.LEFT, comma, 2, ',')
left_bracket = HFunction(4, Associativity.RIGHT, None, 1, '[')
right_bracket = HFunction(4, Associativity.LEFT, None, 1, ']')
func_concatenate = HFunction(5, Associativity.LEFT, concatenate, 2, '++')
func_comprehension = HFunction(5, Associativity.LEFT, comprehension, 2, '..')
func_fst = HFunction(8, Associativity.LEFT, fst, 1, 'fst')
func_map = HFunction(8, Associativity.LEFT, mapHaskell, 2, 'map')
func_succ = HFunction(8, Associativity.LEFT, succ, 1, 'succ')
func_length = HFunction(8, Associativity.LEFT, length, 1, 'length')
func_pred = HFunction(8, Associativity.LEFT, pred, 1, 'pred')
func_take = HFunction(8, Associativity.LEFT, take, 2, 'take')
func_drop = HFunction(8, Associativity.LEFT, drop, 2, 'drop')
func_even = HFunction(8, Associativity.LEFT, take, 1, 'even')
func_odd = HFunction(8, Associativity.LEFT, drop, 1, 'odd')
func_max = HFunction(8, Associativity.LEFT, maximum, 1, 'maximum')
func_min = HFunction(8, Associativity.LEFT, minimum, 1, 'minimum')
func_elem = HFunction(8, Associativity.LEFT, elem, 2, 'elem')
func_notelem = HFunction(8, Associativity.LEFT, notElem, 2, 'notElem')
func_zip = HFunction(8, Associativity.LEFT, zipHaskell, 2, 'zip')
func_div = HFunction(8, Associativity.LEFT, div, 2, 'div')
func_mod = HFunction(8, Associativity.LEFT, mod, 2, 'mod')

class Operator(Enum):
    SPACE = apply
    SLASH = division
    ASTERISK = multiply
    PLUS = add
    MINUS = subtract
    CARET = power
    DOUBLE_EQUAL = equality
    LESS_THAN = less_than
    LESS_THAN_OR_EQUAL= less_than_or_equal
    GREATER_THAN = greater_than
    GREATER_THAN_OR_EQUAL = greater_than_or_equal
    DOUBLE_AMPERSAND = logical_and
    DOUBLE_BAR = logical_or
    LEFT_PARENTHESES = left_parentheses
    RIGHT_PARENTHESES = right_parentheses
    COMMA = create_tuple
    LEFT_BRACKET = left_bracket
    RIGHT_BRACKET = right_bracket
    DOUBLE_PLUS = func_concatenate
    DOUBLE_PERIOD = func_comprehension
    COLON = colon
    FST = func_fst
    MAP = func_map
    SUCC = func_succ
    LENGTH = func_length
    PRED = func_pred
    TAKE = func_take
    DROP = func_drop
    EVEN = func_even
    ODD = func_odd
    MAXIMUM = func_max
    MINIMUM = func_min
    ELEM = func_elem
    NOT_ELEM = func_notelem
    ZIP = func_zip
    DIV = func_div
    MOD = func_mod
    EQUAL = None 
    DOLLAR = None
    UNDERSCORE = None
    DOT = None
    EXCLAMATION = None
    REM= None
    QUOT= None

    
operators = [Operator.SPACE, Operator.SLASH, Operator.ASTERISK, Operator.PLUS,
             Operator.MINUS, Operator.CARET, Operator.DOUBLE_EQUAL, Operator.LESS_THAN,
             Operator.LESS_THAN_OR_EQUAL, Operator.GREATER_THAN, Operator.GREATER_THAN_OR_EQUAL,
             Operator.DOUBLE_AMPERSAND, Operator.DOUBLE_BAR, Operator.LEFT_PARENTHESES,
             Operator.RIGHT_PARENTHESES, Operator.COMMA, Operator.LEFT_BRACKET,
             Operator.RIGHT_BRACKET, Operator.COLON, Operator.DOUBLE_PLUS, Operator.DOUBLE_PERIOD,
             Operator.FST, Operator.MAP, Operator.SUCC, Operator.LENGTH, 
             Operator.PRED, Operator.TAKE, Operator.DROP, Operator.EVEN, Operator.ODD,
             Operator.MAXIMUM, Operator.MINIMUM, Operator.ELEM, Operator.NOT_ELEM,
             Operator.ZIP, Operator.DIV, Operator.MOD]

def operatorIndex(op):
    for i in range(len(operators)):
        if (op == operators[i]):
            return i
    return None
    
def operatorFromString(op):
    for i in range(len(operatorSymbols)):
        if (operatorSymbols[i] == op):
            return operators[i]
    return None

def operatorToString(op):
    return operatorSymbols[operatorIndex(op)]


def getData(exp, variables = None): # withVar tells whether variables should be replaced
    functionMap = {'map':'map2', '&&' : 'AND', '||' : 'OR'}
    
    if (type(exp) in [list, tuple, int, float, bool]):
        return exp
    #elif (exp in operatorSymbols):
        #return operatorFromString(exp).value
    elif (exp in functions.keys()):
        if (exp in functionMap.keys()):
            return functionMap[exp]
        return exp
    elif (exp in ['True', 'False']): # Checks if input is a bool
        return bool(exp)
    elif (variables != None and exp in variables.keys()):
        return variables[exp] # Returns value of variable

    elif (exp[0] in ["'", "\""] and exp[len(exp) - 1] in ["'", "\""]):
        return exp
    try: 
        return int(exp)
    except:
        try: 
            return float(exp)
        except:
            return exp
        
    
    