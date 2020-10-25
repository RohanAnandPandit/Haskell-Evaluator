# -*- coding: utf-8 -*-
"""
Created on Tue Jun 23 09:24:41 2020

@author: rohan
"""
from enum import Enum
from HFunction import HFunction
import Prelude
import Operator_Functions as op_func
import utils

class Associativity(Enum):
    LEFT = 0
    RIGHT = 1
    NONE = 2


greater_than = HFunction(4, Associativity.NONE, op_func.greaterThan, 2, '>')

less_than_or_equal = HFunction(4, Associativity.NONE,
                               op_func.lessThanOrEqual, 2, '<=')

greater_than_or_equal = HFunction(4, Associativity.NONE,
                                  op_func.greaterThanOrEqual,
                                  2, '>=')

int_div = HFunction(4, Associativity.NONE, op_func.quot, 2, '//')

remainder = HFunction(4, Associativity.NONE, op_func.rem, 2, '%')

colon = HFunction(5, Associativity.RIGHT, op_func.cons, 2, ':', lazy = True)

logical_and = HFunction(3, Associativity.RIGHT, op_func.AND, 2, '&&')

concatenate = HFunction(5, Associativity.LEFT, op_func.concatenate, 2, '++')

iterator = HFunction(10, Associativity.LEFT, op_func.create_iterator, 2, 'in')

notequal = HFunction(4, Associativity.NONE, op_func.notEqual, 2, '!=')

logical_or = HFunction(3, Associativity.RIGHT, op_func.OR, 2, '||')

left_parentheses = HFunction(8, Associativity.RIGHT, None, 1, '(')

right_parentheses = HFunction(8, Associativity.LEFT, None, 1, ')')

comma = HFunction(3, Associativity.NONE, op_func.comma, 2, ',')

tuple_cons = HFunction(2.6, Associativity.LEFT, op_func.comma, 2, ',,')

left_bracket = HFunction(8, Associativity.RIGHT, None, 1, '[')

right_bracket = HFunction(8, Associativity.LEFT, None, 1, ']')

dollar = HFunction(2.6, Associativity.RIGHT, op_func.application, 2, '$')

composition = HFunction(9, Associativity.RIGHT, op_func.compose, 2, '~')

index = HFunction(9, Associativity.LEFT, op_func.index, 2, '!!')

newline = HFunction(-1, Associativity.RIGHT, op_func.sequence, 2, ';', lazy = True)
chain = HFunction(2, Associativity.LEFT, op_func.chain, 2, '>>=')

infix = HFunction(5, Associativity.LEFT, None, 1, '`')

equals = HFunction(2.5, Associativity.RIGHT, op_func.assign, 2, '=', lazy = True)

returns = HFunction(2, Associativity.RIGHT, op_func.createLambda, 2, '->', lazy = True)

whereclause = HFunction(2.6, Associativity.LEFT, op_func.where, 2, 'where', lazy = True)

inheritance = HFunction(9, Associativity.LEFT, op_func.extends, 2, 'extends')

implements = HFunction(9, Associativity.LEFT,
                       op_func.implements, 2, 'implements')

bitwise_or = HFunction(5, Associativity.LEFT, op_func.bitwise_or, 2, '¦')

bitwise_and = HFunction(1, Associativity.LEFT, op_func.bitwise_and, 2, '&')

alias = HFunction(9.1, Associativity.LEFT, op_func.alias, 2, '@')

shiftleft = HFunction(5, Associativity.LEFT, op_func.shiftLeft, 2, '<<')

shiftright = HFunction(5, Associativity.LEFT, op_func.shiftRight, 2, '>>')

then = HFunction(2.6, Associativity.RIGHT, op_func.then_clause, 2, '=>',
                 lazy = True)

left_curly = HFunction(8, Associativity.RIGHT, None, 1, '{')

right_curly = HFunction(8, Associativity.LEFT, None, 1, '}')

else_clause = HFunction(2.5, Associativity.RIGHT, op_func.else_clause, 2, '|',
                        lazy = True)

access = HFunction(10, Associativity.LEFT, op_func.access, 2, '.',
                   lazy = True)

comprehension = HFunction(11, Associativity.LEFT, op_func.comprehension, 2,
                          '..')

increment_by = HFunction(2.5, Associativity.RIGHT, op_func.incrementBy, 2,
                         '+=', lazy = True)

decrement_by = HFunction(2.5, Associativity.RIGHT, op_func.decrementBy, 2,
                         '-=', lazy = True)

multiply_by = HFunction(2.5, Associativity.RIGHT, op_func.multiplyBy, 2, '*=',
                        lazy = True)

divide_by = HFunction(2.5, Associativity.RIGHT, op_func.divideBy, 2, '/=', 
                      lazy = True)

raise_to = HFunction(2.5, Associativity.RIGHT, op_func.raiseTo, 2, '^=', 
                     lazy = True)

class Operator(Enum):
    EQUAL = equals
    SPACE = HFunction(9, Associativity.LEFT, op_func.application, 2, ' ')
    SLASH = HFunction(7, Associativity.LEFT, op_func.divide, 2, '/')
    ASTERISK = HFunction(7, Associativity.LEFT, op_func.multiply, 2, '*')
    PLUS = HFunction(6, Associativity.LEFT, op_func.add, 2, '+')
    MINUS = HFunction(6, Associativity.LEFT, op_func.subtract, 2, '-')
    CARET = HFunction(8, Associativity.RIGHT, op_func.power, 2, '^')
    DOUBLE_EQUAL = HFunction(4, Associativity.NONE, op_func.equals, 2, '==')
    LESS_THAN = HFunction(4, Associativity.NONE, op_func.lessThan, 2, '<')
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
    ITERATION = iterator
    COLON = colon
    NOT_EQUAL = notequal
    BACKTICK = infix
    BACKSLASH = None
    ARROW = returns
    DOUBLE_EXCLAMATION = index
    DOLLAR = dollar
    WHERE = whereclause
    BAR = else_clause
    CHAIN = chain 
    TILDE = composition
    AT = alias
    SHIFT_LEFT = shiftleft
    SHIFT_RIGHT = shiftright
    AMPERSAND = bitwise_and
    RIGHT_CURLY = right_curly
    LEFT_CURLY = left_curly
    BROKEN_BAR = bitwise_or
    PERIOD = access
    THEN = then
    DOUBLE_COMMA = tuple_cons
    NEWLINE = newline
    INHERITANCE = inheritance
    IMPLEMENTS = implements
    BACK_ARROW = HFunction(3, Associativity.LEFT, op_func.append, 2, '<-')
    DOUBLE_PERIOD = comprehension
    INCREMENT_BY = increment_by
    DECREMENT_BY = decrement_by
    MULTIPLY_BY = multiply_by
    DIVIDE_BY = divide_by
    RAISE_TO = raise_to
    DOUBLE_SLASH = int_div
    PERCENT = remainder
    DOUBLE_COLON = HFunction(1, Associativity.LEFT, op_func.pass_arg, 2, '::',
                             lazy = True)
    
    
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
                 '//': Operator.DOUBLE_SLASH,
                 '%' : Operator.PERCENT,
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
                 ' in ': Operator.ITERATION,
                 '!=': Operator.NOT_EQUAL, 
                 '!!': Operator.DOUBLE_EXCLAMATION,
                 '`' : Operator.BACKTICK,
                 '$' : Operator.DOLLAR,
                 '\\': Operator.BACKSLASH,
                 '->': Operator.ARROW,
                 '¦' : Operator.BROKEN_BAR,
                 '>>=' : Operator.CHAIN,
                 ' where ' : Operator.WHERE,
                 '@' : Operator.AT,
                 '<<' : Operator.SHIFT_LEFT,
                 '>>' : Operator.SHIFT_RIGHT,
                 '&' : Operator.AMPERSAND,
                 '{' : Operator.LEFT_CURLY,
                 '}' : Operator.RIGHT_CURLY,
                 '=>' : Operator.THEN,
                 '|' : Operator.BAR,
                 ' then ' : Operator.THEN,
                 ' else ' : Operator.BAR,
                 '.' : Operator.PERIOD,
                 ',,' : Operator.DOUBLE_COMMA,
                 '\n' : Operator.NEWLINE,
                 '~' : Operator.TILDE,
                 ' extends ' : Operator.INHERITANCE,
                 ';' : Operator.NEWLINE,
                 ' implements ' : Operator.IMPLEMENTS,
                 '<-' : Operator.BACK_ARROW,
                 '..' : Operator.DOUBLE_PERIOD,
                 '+=' : Operator.INCREMENT_BY,
                 '-=' : Operator.DECREMENT_BY,
                 '*=' : Operator.MULTIPLY_BY,
                 '/=' : Operator.DIVIDE_BY,
                 '^=' : Operator.RAISE_TO,
                 '::' : Operator.DOUBLE_COLON}
    
def operatorFromString(string):
    return operatorsDict[string].value   