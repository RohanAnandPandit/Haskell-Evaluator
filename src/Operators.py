# -*- coding: utf-8 -*-
"""
Created on Tue Jun 23 09:24:41 2020

@author: rohan
"""
from enum import Enum
from HFunction import HFunction
import Prelude
import Operator_Functions
from utils import operators, functionNames

class Associativity(Enum):
    LEFT = 0
    RIGHT = 1
    NONE = 2

apply = HFunction(9, Associativity.LEFT, Operator_Functions.space, 2, ' ')
division = HFunction(7, Associativity.LEFT, Operator_Functions.divide, 2, '/')
multiply = HFunction(7, Associativity.LEFT, Operator_Functions.multiply, 2, '*')
add = HFunction(6, Associativity.LEFT, Operator_Functions.add, 2, '+')
subtract = HFunction(6, Associativity.LEFT, Operator_Functions.subtract, 2, '-')
power = HFunction(8, Associativity.RIGHT, Operator_Functions.power, 2, '^')
equality = HFunction(4, Associativity.LEFT, Operator_Functions.equals, 2, '==')
less_than = HFunction(4, Associativity.NONE, Operator_Functions.lessThan, 2, '<')
greater_than = HFunction(4, Associativity.NONE, Operator_Functions.greaterThan, 2, '>')
less_than_or_equal = HFunction(4, Associativity.NONE, Operator_Functions.lessThanOrEqual, 2, '<=')
greater_than_or_equal = HFunction(4, Associativity.NONE, Operator_Functions.greaterThanOrEqual, 2, '>=')
colon = HFunction(5, Associativity.RIGHT, Operator_Functions.cons, 2, ':')
logical_and = HFunction(3, Associativity.RIGHT, Operator_Functions.AND, 2, '&&')
func_concatenate = HFunction(5, Associativity.LEFT, Operator_Functions.concatenate, 2, '++')
func_comprehension = HFunction(5, Associativity.LEFT, Operator_Functions.comprehension, 2, '..')
func_notequal = HFunction(4, Associativity.LEFT, Operator_Functions.notEqual, 2, '/=')
logical_or = HFunction(3, Associativity.RIGHT, Operator_Functions.OR, 2, '||')
left_parentheses = HFunction(8, Associativity.RIGHT, None, 1, '(')
right_parentheses = HFunction(8, Associativity.LEFT, None, 1, ')')
comma = HFunction(4, Associativity.RIGHT, Operator_Functions.cons, 2, ',')
left_bracket = HFunction(8, Associativity.RIGHT, None, 1, '[')
right_bracket = HFunction(8, Associativity.LEFT, None, 1, ']')
func_dollar = HFunction(0, Associativity.RIGHT, Operator_Functions.space, 2, '$')
func_dot = HFunction(9, Associativity.RIGHT, Operator_Functions.dot, 2, '.')

func_fst = HFunction(8, Associativity.LEFT, Prelude.fst, 1, 'fst')
func_snd = HFunction(8, Associativity.LEFT, Prelude.snd, 1, 'snd')
func_not = HFunction(8, Associativity.LEFT, Prelude.notHaskell, 1, 'not')
func_swap = HFunction(8, Associativity.LEFT, Prelude.swap, 1, 'swap')
func_map = HFunction(8, Associativity.LEFT, Prelude.mapHaskell, 2, 'map')
func_succ = HFunction(8, Associativity.LEFT, Prelude.succ, 1, 'succ')
func_length = HFunction(8, Associativity.LEFT, Prelude.length, 1, 'length')
func_pred = HFunction(8, Associativity.LEFT, Prelude.pred, 1, 'pred')
func_take = HFunction(8, Associativity.LEFT, Prelude.take, 2, 'take')
func_drop = HFunction(8, Associativity.LEFT, Prelude.drop, 2, 'drop')
func_even = HFunction(8, Associativity.LEFT, Prelude.even, 1, 'even')
func_odd = HFunction(8, Associativity.LEFT, Prelude.odd, 1, 'odd')
func_max = HFunction(8, Associativity.LEFT, Prelude.maximum, 1, 'maximum')
func_min = HFunction(8, Associativity.LEFT, Prelude.minimum, 1, 'minimum')
func_elem = HFunction(8, Associativity.LEFT, Prelude.elem, 2, 'elem')
func_notelem = HFunction(8, Associativity.LEFT, Prelude.notElem, 2, 'notElem')
func_zip = HFunction(8, Associativity.LEFT, Prelude.zip, 2, 'zip')
func_div = HFunction(8, Associativity.LEFT, Prelude.div, 2, 'div')
func_mod = HFunction(8, Associativity.LEFT, Prelude.mod, 2, 'mod')
func_zipwith = HFunction(8, Associativity.LEFT, Prelude.zipWith, 3, 'zipWith')
func_takewhile = HFunction(8, Associativity.LEFT, Prelude.takeWhile, 2, 'takeWhile')
func_dropwhile = HFunction(8, Associativity.LEFT, Prelude.dropWhile, 2, 'dropWhile')
func_list = HFunction(8, Associativity.LEFT, list, 1, 'list')
func_id = HFunction(8, Associativity.LEFT, Prelude.id, 1, 'id')
func_const = HFunction(8, Associativity.LEFT, Prelude.const, 2, 'const')
func_index = HFunction(8, Associativity.LEFT, Operator_Functions.index, 2, '!!')
func_lookup = HFunction(8, Associativity.LEFT, Prelude.lookup, 2, 'lookup')
func_concatmap = HFunction(8, Associativity.LEFT, Prelude.concatMap, 2, 'concatMap')
func_splitat = HFunction(8, Associativity.LEFT, Prelude.splitAt, 2, 'splitAt')
func_replicate = HFunction(8, Associativity.LEFT, Prelude.replicate, 2, 'replicate')
func_span = HFunction(8, Associativity.LEFT, Prelude.span, 2, 'span')
func_backtick = HFunction(5, Associativity.LEFT, None, 1, '`')
func_head = HFunction(8, Associativity.LEFT, Prelude.head, 1, 'head')
func_tail = HFunction(8, Associativity.LEFT, Prelude.tail, 1, 'tail')
func_concat = HFunction(8, Associativity.LEFT, Prelude.concat, 1, 'concat')
func_sum = HFunction(8, Associativity.LEFT, Prelude.sum, 1, 'sum')
func_product = HFunction(8, Associativity.LEFT, Prelude.product, 1, 'product')
func_flip = HFunction(8, Associativity.LEFT, Prelude.flip, 1, 'flip')
func_last = HFunction(8, Associativity.LEFT, Prelude.last, 1, 'last')
func_just = HFunction(8, Associativity.LEFT, Prelude.just, 1, 'Just')
func_fromjust = HFunction(8, Associativity.LEFT, Prelude.fromJust, 1, 'fromJust')

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
    COMMA = comma
    LEFT_BRACKET = left_bracket
    RIGHT_BRACKET = right_bracket
    DOUBLE_PLUS = func_concatenate
    DOUBLE_PERIOD = func_comprehension
    COLON = colon
    NOT_EQUAL = func_notequal
    BACKTICK = func_backtick
    FST = func_fst
    SND = func_snd
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
    ZIP_WITH = func_zipwith
    TAKE_WHILE = func_takewhile
    DROP_WHILE = func_dropwhile
    LIST = func_list
    ID = func_id
    CONST = func_const
    DOUBLE_EXCLAMATION = func_index
    LOOKUP = func_lookup
    SPLIT_AT = func_splitat
    CONCAT_MAP = func_concatmap
    SPAN = func_span
    REPLICATE = func_replicate
    HEAD = func_head
    TAIL = func_tail
    CONCAT = func_concat
    DOLLAR = func_dollar
    PERIOD = func_dot
    SUM = func_sum
    PRODUCT = func_product
    FLIP = func_flip
    LAST = func_last
    SWAP = func_swap
    JUST = func_just
    FROM_JUST = func_fromjust
    NOT = func_not

operatorSymbols = operators + functionNames
operators = {' ' : Operator.SPACE,
             '/' : Operator.SLASH,
             '*' : Operator.ASTERISK,
             '+' : Operator.PLUS,
             '-' : Operator.MINUS,
             '^' : Operator.CARET,
             '==': Operator.DOUBLE_EQUAL,
             '<' : Operator.LESS_THAN,
             '<=': Operator.LESS_THAN_OR_EQUAL,
             '>' : Operator.GREATER_THAN,
             '>=': Operator.GREATER_THAN_OR_EQUAL, 
             '&&': Operator.DOUBLE_AMPERSAND,
             '||': Operator.DOUBLE_BAR,
             '(' : Operator.LEFT_PARENTHESES,
             ')' : Operator.RIGHT_PARENTHESES,
             ',' : Operator.COMMA,
             '[' : Operator.LEFT_BRACKET,
             ']' : Operator.RIGHT_BRACKET,
             ':' : Operator.COLON,
             '++': Operator.DOUBLE_PLUS,
             '..': Operator.DOUBLE_PERIOD,
             '/=': Operator.NOT_EQUAL, 
             '!!': Operator.DOUBLE_EXCLAMATION,
             '`' : Operator.BACKTICK,
             '$' : Operator.DOLLAR,
             '.' : Operator.PERIOD,
             'id' : Operator.ID,
             'const' : Operator.CONST,
             'mod' : Operator.MOD,
             'rem' : None,
             'not' : Operator.NOT,
             'fst' : Operator.FST,
             'snd' : Operator.SND,
             'swap' : Operator.SWAP,
             'div' : Operator.DIV,
             'succ' : Operator.SUCC,
             'pred' : Operator.PRED,
             'null' : None,
             'even' : Operator.EVEN,
             'odd' : Operator.ODD,
             'flip' : Operator.FLIP,
             'length' : Operator.LENGTH,
             'head' : Operator.HEAD,
             'tail' : Operator.TAIL,
             'last' : Operator.LAST,
             'concat' : Operator.CONCAT,
             'init' : None,
             'maximum' : Operator.MAXIMUM,
             'minimum' : Operator.MINIMUM,
             'elem' : Operator.ELEM,
             'notElem' : Operator.NOT_ELEM, 
             'reverse' : None,
             'take' : Operator.TAKE,
             'drop' : Operator.DROP,
             'map' : Operator.MAP,
             'words' : None, 
             'unwords' : None,
             'takeWhile' : Operator.TAKE_WHILE,
             'dropWhile' : Operator.DROP_WHILE,
             'zip' : Operator.ZIP,
             'unzip' : None,
             'foldl' : None,
             'foldr' : None,
             'and' : None,
             'or' : None,
             'any' : None,
             'all' : None,
             'filter' : None,
             'sum' : Operator.SUM,
             'product' : Operator.PRODUCT,
             'lookup' : Operator.LOOKUP,
             'concatMap' : Operator.CONCAT_MAP,
             'splitAt' : Operator.SPLIT_AT,
             'span' : None,
             'replicate' : Operator.REPLICATE,
             'fromJust' : Operator.FROM_JUST,
             'Just' : Operator.JUST}


def operatorIndex(op):
    for i in range(len(operators)):
        if (op == operators[i]):
            return i
    return None
    
def operatorFromString(string):
    return operators[string]

def operatorToString(op):
    return operatorSymbols[operatorIndex(op)]

    