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


greater_than = HFunction(4, Associativity.NONE,
                         op_func.greaterThan, 2, '>')

less_than_or_equal = HFunction(4, Associativity.NONE,
                               op_func.lessThanOrEqual, 2, '<=')

greater_than_or_equal = HFunction(4, Associativity.NONE,
                                  op_func.greaterThanOrEqual,
                                  2, '>=')

int_div = HFunction(4, Associativity.NONE, op_func.quot, 2, '//')

remainder = HFunction(4, Associativity.NONE, op_func.rem, 2, '%')

colon = HFunction(5, Associativity.RIGHT, op_func.cons, 2, ':')

logical_and = HFunction(3, Associativity.RIGHT,
                        op_func.AND, 2, '&&')

concatenate = HFunction(5, Associativity.LEFT,
                        op_func.concatenate, 2, '++')

iterator = HFunction(10, Associativity.LEFT,
                     op_func.create_iterator, 2, 'in')

notequal = HFunction(4, Associativity.NONE, 
                     op_func.notEqual, 2, '!=')

logical_or = HFunction(3, Associativity.RIGHT, op_func.OR, 2, '||')

left_parentheses = HFunction(8, Associativity.RIGHT, None, 1, '(')

right_parentheses = HFunction(8, Associativity.LEFT, None, 1, ')')

comma = HFunction(2, Associativity.NONE, op_func.comma, 2, ',')

tuple_cons = HFunction(2.6, Associativity.LEFT,
                       op_func.comma, 2, ',,')

left_bracket = HFunction(8, Associativity.RIGHT, None, 1, '[')

right_bracket = HFunction(8, Associativity.LEFT, None, 1, ']')

dollar = HFunction(0, Associativity.RIGHT, op_func.application, 2, '$')

composition = HFunction(9, Associativity.RIGHT,
                        op_func.compose, 2, '~')

index = HFunction(9, Associativity.LEFT, op_func.index, 2, '!!')

newline = HFunction(-1, Associativity.RIGHT,
                    op_func.sequence, 2, ';')
chain = HFunction(2, Associativity.LEFT, op_func.chain, 2, '>>=')

infix = HFunction(5, Associativity.LEFT, None, 1, '`')

equals = HFunction(2.5, Associativity.RIGHT,
                   op_func.assign, 2, '=')

returns = HFunction(2, Associativity.RIGHT,
                    op_func.createLambda, 2, '->')

whereclause = HFunction(2.6, Associativity.LEFT,
                        op_func.where, 2, 'where')

append_tail = HFunction(3, Associativity.LEFT, Prelude.append, 2, '<-')

inheritance = HFunction(9, Associativity.LEFT,
                        op_func.extends, 2, 'extends')

implements = HFunction(9, Associativity.LEFT,
                       op_func.implements, 2, 'implements')

bitwise_or = HFunction(1, Associativity.LEFT,
                       op_func.bitwise_or, 2, '¦')

bitwise_and = HFunction(1, Associativity.LEFT,
                        op_func.bitwise_and, 2, '&')

alias = HFunction(9.1, Associativity.LEFT, op_func.alias, 2, '@')

shiftleft = HFunction(5, Associativity.LEFT,
                      op_func.shiftLeft, 2, '<<')

shiftright = HFunction(5, Associativity.LEFT,
                       op_func.shiftRight, 2, '>>')

then = HFunction(2.6, Associativity.RIGHT, 
                 op_func.then_clause, 2, '=>')

left_curly = HFunction(8, Associativity.RIGHT, None, 1, '{')

right_curly = HFunction(8, Associativity.LEFT, None, 1, '}')

else_clause = HFunction(2.5, Associativity.RIGHT,
                        op_func.else_clause, 2, '|')

access = HFunction(9.1, Associativity.LEFT, op_func.access, 2, '.')

comprehension = HFunction(11, Associativity.LEFT,
                          op_func.comprehension, 2, '..')

increment_by = HFunction(2.5, Associativity.RIGHT, 
                         op_func.incrementBy, 2, '+=')

decrement_by = HFunction(2.5, Associativity.RIGHT,
                         op_func.decrementBy, 2, '-=')

multiply_by = HFunction(2.5, Associativity.RIGHT,
                        op_func.multiplyBy, 2, '*=')

divide_by = HFunction(2.5, Associativity.RIGHT,
                      op_func.divideBy, 2, '/=')

raise_to = HFunction(2.5, Associativity.RIGHT,
                     op_func.raiseTo, 2, '^=')

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
    BACK_ARROW = append_tail
    DOUBLE_PERIOD = comprehension
    INCREMENT_BY = increment_by
    DECREMENT_BY = decrement_by
    MULTIPLY_BY = multiply_by
    DIVIDE_BY = divide_by
    RAISE_TO = raise_to
    DOUBLE_SLASH = int_div
    PERCENT = remainder
    DOUBLE_COLON = HFunction(5, Associativity.LEFT, op_func.pass_arg, 2, '::')
    
def initialiseFunctions(state):
    state['fst'] = HFunction(8, Associativity.LEFT, Prelude.fst, 1, 'fst')
    state['snd'] = HFunction(8, Associativity.LEFT, Prelude.snd, 1, 'snd')
    state['not'] = HFunction(8, Associativity.LEFT, Prelude.notHaskell,
         1, 'not')
    state['swap'] = HFunction(8, Associativity.LEFT, Prelude.swap, 1, 'swap')
    state['map'] = HFunction(8, Associativity.LEFT, Prelude.map_, 2, 'map')
    state['succ'] = HFunction(8, Associativity.LEFT, Prelude.succ, 1, 'succ')
    state['length'] = HFunction(8, Associativity.LEFT,
                                 Prelude.length, 1, 'length')
    state['pred'] = HFunction(8, Associativity.LEFT, Prelude.pred, 1, 'pred')
    state['take'] = HFunction(8, Associativity.LEFT, Prelude.take, 2, 'take')
    state['drop'] = HFunction(8, Associativity.LEFT, Prelude.drop, 2, 'drop')
    state['even'] = HFunction(8, Associativity.LEFT, Prelude.even, 1, 'even')
    state['odd'] = HFunction(8, Associativity.LEFT, Prelude.odd, 1, 'odd')
    state['maximum'] = HFunction(8, Associativity.LEFT,
                                 Prelude.maximum, 1, 'maximum')
    state['minimum'] = HFunction(8, Associativity.LEFT,
                                 Prelude.minimum, 1, 'minimum')
    state['elem'] = HFunction(8, Associativity.LEFT, Prelude.elem, 2, 'elem')
    state['notElem'] = HFunction(8, Associativity.LEFT,
                                 Prelude.empty, 1, 'notElem')
    state['empty'] = HFunction(8, Associativity.LEFT,
                                 Prelude.empty, 1, 'notElem')
    state['null'] = HFunction(8, Associativity.LEFT, Prelude.null, 1, 'null')
    state['zip'] = HFunction(8, Associativity.LEFT,
                             Prelude.zipHaskell, 2, 'zip')
    state['div'] = HFunction(8, Associativity.LEFT, Prelude.div, 2, 'div')
    state['mod'] = HFunction(8, Associativity.LEFT, Prelude.mod, 2, 'mod')
    state['zipWith'] = HFunction(8, Associativity.LEFT, 
                                 Prelude.zipWith, 3, 'zipWith')
    state['takeWhile'] = HFunction(8, Associativity.LEFT, Prelude.takeWhile,
         2, 'takeWhile')
    state['dropWhile'] = HFunction(8, Associativity.LEFT, Prelude.dropWhile,
         2, 'dropWhile')
    state['id'] = HFunction(8, Associativity.LEFT, Prelude.idHaskell, 1, 'id')
    state['const'] = HFunction(8, Associativity.LEFT,
                                Prelude.const, 2, 'const')
    state['for'] = HFunction(8, Associativity.LEFT,
                             Prelude.forHaskell, 5, 'for')
    state['concatMap'] = HFunction(8, Associativity.LEFT, Prelude.concatMap,
         2, 'concatMap')
    state['splitAt'] = HFunction(8, Associativity.LEFT, Prelude.splitAt, 2,
         'splitAt')
    state['replicate'] = HFunction(8, Associativity.LEFT, Prelude.replicate,
         2, 'replicate')
    state['span'] = HFunction(8, Associativity.LEFT, Prelude.span, 2, 'span')
    state['head'] = HFunction(8, Associativity.LEFT, Prelude.head, 1, 'head')
    state['tail'] = HFunction(8, Associativity.LEFT, Prelude.tail, 1, 'tail')
    state['concat'] = HFunction(8, Associativity.LEFT, Prelude.concat, 1,
         'concat')
    state['sum'] = HFunction(8, Associativity.LEFT,
                             Prelude.sumHaskell, 1, 'sum')
    state['product'] = HFunction(8, Associativity.LEFT, Prelude.product, 1,
         'product')
    state['flip'] = HFunction(8, Associativity.LEFT, Prelude.flip, 1, 'flip')
    state['last'] = HFunction(8, Associativity.LEFT, Prelude.last, 1, 'last')
    state['printLn'] = HFunction(8, Associativity.LEFT,
                                 Prelude.printLn, 1, 'printLn')
    state['print'] = HFunction(8, Associativity.LEFT, 
                                 Prelude.printHaskell, 1, 'print')
    state['show'] = HFunction(8, Associativity.LEFT, Prelude.show, 1, 'show')
    state['input'] = HFunction(8, Associativity.LEFT,
                                 Prelude.inputHaskell, 1, 'input')
    state['init'] = HFunction(8, Associativity.LEFT, Prelude.init, 1, 'init')
    state['unzip'] = HFunction(8, Associativity.LEFT,
                             Prelude.unzip, 1, 'unzip')
    state['uncurry'] = HFunction(8, Associativity.LEFT,
                                 Prelude.uncurry, 1, 'uncurry')
    state['curry'] = HFunction(8, Associativity.LEFT,
                                 Prelude.curry, 1, 'curry')
    state['foldl'] = HFunction(8, Associativity.LEFT,
                                 Prelude.foldl, 3, 'foldl')
    state['foldr'] = HFunction(8, Associativity.LEFT,
                                 Prelude.foldr, 3, 'foldr')
    state['foldl1'] = HFunction(8, Associativity.LEFT,
                                 Prelude.foldl1, 2, 'foldl1')
    state['foldr1'] = HFunction(8, Associativity.LEFT,
                                 Prelude.foldr1, 2, 'foldr1')
    state['reverse'] = HFunction(8, Associativity.LEFT,
                                 Prelude.reverse, 1, 'reverse')
    state['words'] = HFunction(8, Associativity.LEFT,
                                 Prelude.words, 1, 'words')
    state['unwords'] = HFunction(8, Associativity.LEFT,
                                 Prelude.unwords, 1, 'unwords')
    state['and'] = HFunction(8, Associativity.LEFT,
                             Prelude.andHaskell, 1, 'and')
    state['or'] = HFunction(8, Associativity.LEFT,
                             Prelude.orHaskell, 1, 'or')
    state['any'] = HFunction(8, Associativity.LEFT,
                             Prelude.anyHaskell, 2, 'any')
    state['all'] = HFunction(8, Associativity.LEFT,
                             Prelude.allHaskell, 2, 'all')
    state['filter'] = HFunction(8, Associativity.LEFT,
                                 Prelude.filterHaskell, 2, 'filter')
    state['zip3'] = HFunction(8, Associativity.LEFT, Prelude.zip3, 3, 'zip3')
    state['zipWith3'] = HFunction(8, Associativity.LEFT,
                                     Prelude.zipWith3, 4, 'zipWith3')
    state['eval'] = HFunction(8, Associativity.LEFT, 
                             lambda exp: utils.evaluate(str(exp)), 1, 'eval')
    state['read'] = HFunction(8, Associativity.LEFT,
                             lambda exp: utils.getData(str(exp)), 1, 'read')
    state['for'] = HFunction(8, Associativity.LEFT,
                             op_func.forLoop, 2, 'for')
    state['while'] = HFunction(8, Associativity.LEFT,
                                 op_func.whileLoop, 2, 'while')
    state['if'] = HFunction(8, Associativity.LEFT, 
         op_func.ifStatement, 2, 'if')
    state['struct'] = HFunction(8, Associativity.LEFT, 
                                 op_func.createStruct, 2, 'struct')
    state['enum'] = HFunction(8, Associativity.LEFT,
                             op_func.createEnum, 2, 'enum')
    state['oper'] = HFunction(8, Associativity.LEFT, 
                             op_func.createOperator, 4, 'oper')
    state['class'] = HFunction(8, Associativity.LEFT, 
                             op_func.createClass, 1, 'class')
    state['interface'] = HFunction(8, Associativity.LEFT,
                             op_func.createInterface, 2, 'interface')
    state['def'] = HFunction(8, Associativity.LEFT, 
                             op_func.definition, 3, 'def')
    state['switch'] = HFunction(8, Associativity.LEFT, 
                             op_func.switch, 2, 'switch')
    state['continue'] = HFunction(8, Associativity.LEFT,
                             op_func.continue_loop, 0, 'continue')
    state['break'] = HFunction(8, Associativity.LEFT, 
                             op_func.breakCurrentLoop, 0, 'break')
    state['let'] = HFunction(8, Associativity.LEFT, 
                             op_func.let, 2, 'let')
    state['range'] = HFunction(8, Associativity.LEFT, 
                     op_func.range_specifier, 1, 'range')
    state['import'] = HFunction(8, Associativity.LEFT,
                         op_func.import_module, 1, 'import')
    state['from'] = HFunction(8, Associativity.LEFT, 
                             op_func.from_import, 3, 'from')
    state['return'] = HFunction(8, Associativity.LEFT,
                             op_func.return_statement, 1, 'return')
    state['toInt'] = HFunction(8, Associativity.LEFT, 
                             op_func.toInt, 1, 'roInt')
    state['toFloat'] = HFunction(8, Associativity.LEFT, 
                             op_func.toFloat, 1, 'toFloat')
    state['toBool'] = HFunction(8, Associativity.LEFT,
                             op_func.toBool, 1, 'toBool')
    state['toChar'] = HFunction(8, Associativity.LEFT, 
                                 op_func.toChar, 1, 'toChar')
    state['do'] = HFunction(8, Associativity.LEFT, 
                             op_func.doLoop, 3, 'do')
    state['int'] = HFunction(8, Associativity.LEFT,
                             op_func.defaultInt, 1, 'int') 
    state['float'] = HFunction(8, Associativity.LEFT,
                             op_func.defaultFloat, 1, 'float')
    state['bool'] = HFunction(8, Associativity.LEFT, 
                             op_func.defaultBool, 1, 'bool')
    state['char'] = HFunction(8, Associativity.LEFT, 
                             op_func.defaultChar, 1, 'char')
    state['list'] = HFunction(8, Associativity.LEFT,
                             op_func.defaultList, 1, 'list')
    state['string'] = HFunction(8, Associativity.LEFT,
                             op_func.defaultList, 1, 'string') 
    state['type'] = HFunction(8, Associativity.LEFT,
                             op_func.type_synonym, 2, 'type') 
    state['union'] = HFunction(8, Associativity.LEFT,
                                 op_func.types_union, 2, 'union') 
    state['breakout'] = HFunction(8, Associativity.LEFT,
                                 op_func.breakout, 1, 'breakout') 
    state['skipout'] = HFunction(8, Associativity.LEFT,
                                 op_func.skipout, 1, 'skipout') 
    state['global'] = HFunction(8, Associativity.LEFT,
                                 op_func.make_public, 1, 'global') 
    state['local'] = HFunction(8, Associativity.LEFT,
                                 op_func.make_private, 1, 'local') 
    state['hidden'] = HFunction(8, Associativity.LEFT,
                                 op_func.make_hidden, 1, 'hidden') 
    
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