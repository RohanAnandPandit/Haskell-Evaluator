# -*- coding: utf-8 -*-
"""
Created on Tue Jun 23 09:24:41 2020

@author: rohan
"""
from enum import Enum
from HFunction import HFunction
import Prelude
import Operator_Functions

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
concatenate = HFunction(5, Associativity.LEFT, Operator_Functions.concatenate, 2, '++')
comprehension = HFunction(5, Associativity.LEFT, Operator_Functions.comprehension, 2, '..')
notequal = HFunction(4, Associativity.LEFT, Operator_Functions.notEqual, 2, '/=')
logical_or = HFunction(3, Associativity.RIGHT, Operator_Functions.OR, 2, '||')
left_parentheses = HFunction(8, Associativity.RIGHT, None, 1, '(')
right_parentheses = HFunction(8, Associativity.LEFT, None, 1, ')')
comma = HFunction(5, Associativity.LEFT, Operator_Functions.comma, 2, ',')
left_bracket = HFunction(8, Associativity.RIGHT, None, 1, '[')
right_bracket = HFunction(8, Associativity.LEFT, None, 1, ']')
dollar = HFunction(0, Associativity.RIGHT, Operator_Functions.space, 2, '$')
dot = HFunction(9, Associativity.RIGHT, Operator_Functions.dot, 2, '.')
index = HFunction(9, Associativity.LEFT, Operator_Functions.index, 2, '!!')
sequence = HFunction(1, Associativity.RIGHT, Operator_Functions.sequence, 2, '>>')
chain = HFunction(1, Associativity.LEFT, Operator_Functions.chain, 2, '>>=')
infix = HFunction(5, Associativity.LEFT, None, 1, '`')
equals = HFunction(2, Associativity.RIGHT, Operator_Functions.assign, 2, '=')
lambda_func = HFunction(8, Associativity.NONE, Operator_Functions.collect, -1, '\\')
func_assign = HFunction(1, Associativity.RIGHT, Operator_Functions.createLambda, 2, '->')
where = HFunction(0, Associativity.RIGHT, Operator_Functions.where, 2, 'where')

class Operator(Enum):
    EQUAL = equals
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
    DOUBLE_PLUS = concatenate
    DOUBLE_PERIOD = comprehension
    COLON = colon
    NOT_EQUAL = notequal
    BACKTICK = infix
    BACKSLASH = lambda_func
    ARROW = func_assign
    DOUBLE_EXCLAMATION = index
    DOLLAR = dollar
    PERIOD = dot
    WHERE = where
    DOUBLE_GREATER_THAN = sequence

def initialiseFunctions(state):
    state['fst'] = HFunction(8, Associativity.LEFT, Prelude.fst, 1, 'fst')
    state['snd'] = HFunction(8, Associativity.LEFT, Prelude.snd, 1, 'snd')
    state['not'] = HFunction(8, Associativity.LEFT, Prelude.notHaskell, 1, 'not')
    state['swap'] = HFunction(8, Associativity.LEFT, Prelude.swap, 1, 'swap')
    state['map'] = HFunction(8, Associativity.LEFT, Prelude.mapHaskell, 2, 'map')
    state['succ'] = HFunction(8, Associativity.LEFT, Prelude.succ, 1, 'succ')
    state['length'] = HFunction(8, Associativity.LEFT, Prelude.length, 1, 'length')
    state['pred'] = HFunction(8, Associativity.LEFT, Prelude.pred, 1, 'pred')
    state['take'] = HFunction(8, Associativity.LEFT, Prelude.take, 2, 'take')
    state['drop'] = HFunction(8, Associativity.LEFT, Prelude.drop, 2, 'drop')
    state['even'] = HFunction(8, Associativity.LEFT, Prelude.even, 1, 'even')
    state['odd'] = HFunction(8, Associativity.LEFT, Prelude.odd, 1, 'odd')
    state['max'] = HFunction(8, Associativity.LEFT, Prelude.maximum, 1, 'maximum')
    state['min'] = HFunction(8, Associativity.LEFT, Prelude.minimum, 1, 'minimum')
    state['elem'] = HFunction(8, Associativity.LEFT, Prelude.elem, 2, 'elem')
    state['notElem'] = HFunction(8, Associativity.LEFT, Prelude.notElem, 2, 'notElem')
    state['zip'] = HFunction(8, Associativity.LEFT, Prelude.zipHaskell, 2, 'zip')
    state['div'] = HFunction(8, Associativity.LEFT, Prelude.div, 2, 'div')
    state['mod'] = HFunction(8, Associativity.LEFT, Prelude.mod, 2, 'mod')
    state['zipwith'] = HFunction(8, Associativity.LEFT, Prelude.zipWith, 3, 'zipWith')
    state['takeWhile'] = HFunction(8, Associativity.LEFT, Prelude.takeWhile, 2, 'takeWhile')
    state['dropWhile'] = HFunction(8, Associativity.LEFT, Prelude.dropWhile, 2, 'dropWhile')
    state['id'] = HFunction(8, Associativity.LEFT, Prelude.id, 1, 'id')
    state['const'] = HFunction(8, Associativity.LEFT, Prelude.const, 2, 'const')
    state['lookup'] = HFunction(8, Associativity.LEFT, Prelude.lookup, 2, 'lookup')
    state['concatMap'] = HFunction(8, Associativity.LEFT, Prelude.concatMap, 2, 'concatMap')
    state['splitAt'] = HFunction(8, Associativity.LEFT, Prelude.splitAt, 2, 'splitAt')
    state['replicate'] = HFunction(8, Associativity.LEFT, Prelude.replicate, 2, 'replicate')
    state['span'] = HFunction(8, Associativity.LEFT, Prelude.span, 2, 'span')
    state['head'] = HFunction(8, Associativity.LEFT, Prelude.head, 1, 'head')
    state['tail'] = HFunction(8, Associativity.LEFT, Prelude.tail, 1, 'tail')
    state['concat'] = HFunction(8, Associativity.LEFT, Prelude.concat, 1, 'concat')
    state['sum'] = HFunction(8, Associativity.LEFT, Prelude.sumHaskell, 1, 'sum')
    state['product'] = HFunction(8, Associativity.LEFT, Prelude.product, 1, 'product')
    state['flip'] = HFunction(8, Associativity.LEFT, Prelude.flip, 1, 'flip')
    state['last'] = HFunction(8, Associativity.LEFT, Prelude.last, 1, 'last')
    state['just'] = HFunction(8, Associativity.LEFT, Prelude.just, 1, 'Just')
    state['fromJust'] = HFunction(8, Associativity.LEFT, Prelude.fromJust, 1, 'fromJust')
    state['getchar'] = HFunction(8, Associativity.LEFT, Prelude.getChar, 0, 'getChar')
    state['putchar'] = HFunction(8, Associativity.LEFT, Prelude.putChar, 1, 'putChar')
    state['getline'] = HFunction(8, Associativity.LEFT, Prelude.getLine, 0, 'getLine')
    state['putstr'] = HFunction(8, Associativity.LEFT, Prelude.putStr, 1, 'putStr')
    state['putstrln'] = HFunction(8, Associativity.LEFT, Prelude.putStrLn, 1, 'putStrLn')
    state['print'] = HFunction(8, Associativity.LEFT, Prelude.printHaskell, 1, 'print')
    state['iterate'] = HFunction(8, Associativity.LEFT, Prelude.iterate, 2, 'iterate')
    state['init'] = HFunction(8, Associativity.LEFT, Prelude.init, 1, 'init')
    state['unzip'] = HFunction(8, Associativity.LEFT, Prelude.unzip, 1, 'unzip')
    state['uncurry'] = HFunction(8, Associativity.LEFT, Prelude.uncurry, 1, 'uncurry')
    state['curry'] = HFunction(8, Associativity.LEFT, Prelude.curry, 1, 'curry')
    state['foldl'] = HFunction(8, Associativity.LEFT, Prelude.foldl, 3, 'foldl')
    state['foldr'] = HFunction(8, Associativity.LEFT, Prelude.foldr, 3, 'foldr')
    state['foldl1'] = HFunction(8, Associativity.LEFT, Prelude.foldl1, 2, 'foldl1')
    state['foldr1'] = HFunction(8, Associativity.LEFT, Prelude.foldr1, 2, 'foldr1')
    state['repeat'] = HFunction(8, Associativity.LEFT, Prelude.repeat, 1, 'repeat')
    state['reverse'] = HFunction(8, Associativity.LEFT, Prelude.reverse, 1, 'reverse')
    state['words'] = HFunction(8, Associativity.LEFT, Prelude.words, 1, 'words')
    state['unwords'] = HFunction(8, Associativity.LEFT, Prelude.unwords, 1, 'unwords')
    state['and'] = HFunction(8, Associativity.LEFT, Prelude.andHaskell, 1, 'and')
    state['or'] = HFunction(8, Associativity.LEFT, Prelude.orHaskell, 1, 'or')
    state['any'] = HFunction(8, Associativity.LEFT, Prelude.anyHaskell, 2, 'any')
    state['all'] = HFunction(8, Associativity.LEFT, Prelude.allHaskell, 2, 'all')
    state['filter'] = HFunction(8, Associativity.LEFT, Prelude.filterHaskell, 2, 'filter')
    state['zip3'] = HFunction(8, Associativity.LEFT, Prelude.zip3, 3, 'zip3')
    state['zipWith3'] = HFunction(8, Associativity.LEFT, Prelude.zipWith3, 4, 'zipWith3')
    state['cycle'] = HFunction(8, Associativity.LEFT, Prelude.cycle, 1, 'cycle')


class Op:
    def __init__(self, hfunc):
        self.value = hfunc
    
    def simplify(self, a, b):
        return self.value
    
    def __str__(self):
        return str(self.value)
        
operatorsDict = {'=' : Operator.EQUAL,
                 ' ' : Operator.SPACE,
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
                 '\\': Operator.BACKSLASH,
                 '->': Operator.ARROW,
                 '>>': Operator.DOUBLE_GREATER_THAN,
                 'where' : Operator.WHERE}
    
def operatorFromString(string):
    return operatorsDict[string]    