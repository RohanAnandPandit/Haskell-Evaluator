# -*- coding: utf-8 -*-
"""
Created on Mon Sep  7 09:32:31 2020

@author: rohan
"""
from function import HFunction
from operators import Associativity
import operator_functions as op_func
import prelude
from parser import Parser
from lexer import Lexer
import list


class State:
    def __init__(self):
        self.reset()

    def reset(self):
        self.operators = [' ', '/', '*', '+', '-', '^', '==', '<', '<=', '>',
                          '>=', '&&', '||', '(', ')', ',', '[', ']', ':', '+', '...',
                          '/=', '!!', '`', '$', ';', '>>', '>>=', '=', '->', '--', '\\',
                          ' where ', '|', '@', '<-', '<<', '&', '}', '|||', 'then',
                          ' else ', '\t', '{', '=>', '~', ',,', '\n', '.', '!=', '<->',
                          '+=', '-=', '*=', '/=', '^=', '//', '%', '::', '!', 'implements',
                          'where', 'in', 'then', 'else', 'extends']

        self.keywords = ['class', 'def', 'struct', 'interface', 'extends',
                         'implements', 'while', 'for', 'switch', 'default', 'if', 'else',
                         'then', 'enum', 'oper', 'break', 'continue', 'in', 'True',
                         'False', 'let', 'import', 'return', 'int', 'float', 'bool',
                         'char', 'var', 'do', '?', 'Num', 'from', 'type', 'union',
                         'stop', 'skip', 'global', 'local', 'hidden', 'Func', 'where',
                         'init']

        self.functional_mode = self.static_mode = False
        self.built_in_state = {}
        self.frame_stack = [self.built_in_state]
        self.in_class = 0
        self.break_loop = 0
        self.continue_loop = 0
        self.return_value = None
        self.function_names = list(self.built_in_state.keys())
        self.initialise_functions()

        # self.evaluate('import Prelude')

    def initialise_functions(self):
        from types import Type
        self.built_in_state['println'] = HFunction(8, Associativity.LEFT,
                                                   prelude.print_ln, 1, 'println')

        self.built_in_state['print'] = HFunction(8, Associativity.LEFT,
                                                 prelude.print_, 1, 'print')

        self.built_in_state['show'] = HFunction(8, Associativity.LEFT,
                                                prelude.show, 1, 'show')

        self.built_in_state['tostr'] = HFunction(8, Associativity.LEFT,
                                                 op_func.to_string, 1, 'tostr')

        self.built_in_state['input'] = HFunction(8, Associativity.LEFT,
                                                 prelude.input_, 1, 'input')

        self.built_in_state['eval'] = HFunction(8, Associativity.LEFT,
                                                op_func.eval_, 1, 'eval')

        self.built_in_state['for'] = HFunction(8, Associativity.LEFT,
                                               op_func.for_loop, 2, 'for', lazy=True)

        self.built_in_state['while'] = HFunction(8, Associativity.LEFT,
                                                 op_func.while_loop, 2, 'while',
                                                 lazy=True)

        self.built_in_state['if'] = HFunction(8, Associativity.LEFT,
                                              op_func.if_statement, 2, 'if', lazy=True)

        self.built_in_state['struct'] = HFunction(8, Associativity.LEFT,
                                                  op_func.create_struct, 2, 'struct',
                                                  lazy=True)

        self.built_in_state['enum'] = HFunction(8, Associativity.LEFT,
                                                op_func.create_enum, 2, 'enum', lazy=True)

        self.built_in_state['oper'] = HFunction(8, Associativity.LEFT,
                                                op_func.create_operator, 4, 'oper',
                                                lazy=True)

        self.built_in_state['class'] = HFunction(8, Associativity.LEFT,
                                                 op_func.create_class, 1, 'class', lazy=True)

        self.built_in_state['interface'] = HFunction(8, Associativity.LEFT,
                                                     op_func.create_interface, 2, 'interface',
                                                     lazy=True)

        self.built_in_state['def'] = HFunction(8, Associativity.LEFT,
                                               op_func.definition, 3, 'def', lazy=True)

        self.built_in_state['switch'] = HFunction(8, Associativity.LEFT,
                                                  op_func.switch, 2, 'switch', lazy=True)

        self.built_in_state['continue'] = HFunction(8, Associativity.LEFT,
                                                    op_func.continue_loop, 0, 'continue')

        self.built_in_state['break'] = HFunction(8, Associativity.LEFT,
                                                 op_func.break_current_loop, 0, 'break')

        self.built_in_state['let'] = HFunction(8, Associativity.LEFT,
                                               op_func.let, 2, 'let', lazy=True)

        self.built_in_state['import'] = HFunction(8, Associativity.LEFT,
                                                  op_func.import_module, 1, 'import', lazy=True)

        self.built_in_state['from'] = HFunction(8, Associativity.LEFT,
                                                op_func.from_import, 3, 'from', lazy=True)

        self.built_in_state['return'] = HFunction(8, Associativity.LEFT,
                                                  op_func.return_statement, 1, 'return')

        self.built_in_state['toint'] = HFunction(8, Associativity.LEFT,
                                                 op_func.to_int, 1, 'toint')

        self.built_in_state['tofloat'] = HFunction(8, Associativity.LEFT,
                                                   op_func.to_float, 1, 'tofloat')

        self.built_in_state['tobool'] = HFunction(8, Associativity.LEFT,
                                                  op_func.to_bool, 1, 'tobool')

        self.built_in_state['tochar'] = HFunction(8, Associativity.LEFT,
                                                  op_func.to_char, 1, 'tochar')

        self.built_in_state['do'] = HFunction(8, Associativity.LEFT,
                                              op_func.do_loop, 3, 'do', lazy=True)

        self.built_in_state['var'] = Type('var', program_state=self)
        self.built_in_state['int'] = Type('int', program_state=self)
        self.built_in_state['float'] = Type('float', program_state=self)
        self.built_in_state['bool'] = Type('bool', program_state=self)
        self.built_in_state['char'] = Type('char', program_state=self)
        self.built_in_state['string'] = Type('string', program_state=self)
        self.built_in_state['Object'] = Type('Object', program_state=self)
        self.built_in_state['Func'] = Type('Func', program_state=self)
        self.built_in_state['Type'] = Type('Type', program_state=self)

        self.built_in_state['type'] = HFunction(8, Associativity.LEFT,
                                                op_func.type_synonym, 2, 'type', lazy=True)

        self.built_in_state['union'] = HFunction(8, Associativity.LEFT,
                                                 op_func.types_union, 2, 'union',
                                                 lazy=True)

        self.built_in_state['stop'] = HFunction(8, Associativity.LEFT,
                                                op_func.breakout, 1, 'stop')
        self.built_in_state['skip'] = HFunction(8, Associativity.LEFT,
                                                op_func.skipout, 1, 'skip')
        self.built_in_state['global'] = HFunction(8, Associativity.LEFT,
                                                  op_func.make_public, 1, 'global')
        self.built_in_state['local'] = HFunction(8, Associativity.LEFT,
                                                 op_func.make_private, 1, 'local')
        self.built_in_state['hidden'] = HFunction(8, Associativity.LEFT,
                                                  op_func.make_hidden, 1, 'hidden')
        self.built_in_state['match'] = HFunction(8, Associativity.LEFT,
                                                 op_func.match, 2, 'match', lazy=True)
        self.built_in_state['py'] = HFunction(8, Associativity.LEFT,
                                              op_func.python_eval, 1, 'py')
        self.built_in_state['head'] = HFunction(8, Associativity.LEFT,
                                                list.head, 1, 'head')
        self.built_in_state['tail'] = HFunction(8, Associativity.LEFT,
                                                list.tail, 1, 'tail')
        self.evaluate('import prelude')

    def evaluate(self, source, reset_state=False):
        value = None

        if "#STATIC-MODE#\n" in source:
            self.static_mode = True

        if "#FUNCTIONAL-MODE#\n" in source:
            self.functional_mode = True

        for section in source.split('#EVAL#\n'):
            lexer = Lexer(section, self)
            expr = Parser(lexer, self).expr
            # print('State evaluate', expr)
            value = expr.simplify(self)

        if reset_state:
            self.reset()

        return value

    def is_primitive(self, expr):
        from types import Int, Float, Bool, Char, String, Null
        from enum import EnumValue
        return isinstance(expr, (Int, Float, Bool, Char, String, EnumValue,
                                 Null))

    def null(self, expr):
        from types import Null
        return isinstance(expr, Null)

    def is_type(self, expr):
        from list import Nil, Array
        from types import Type, Null
        from union import Union
        from Class import Class
        from struct import Struct
        from tuple import Tuple
        return isinstance(expr, (Nil, Null, Type, Class, Struct, Tuple,
                                 Array, Union))

    def is_list(self, expr):
        from list import List
        from Class import Object
        if issubclass(type(expr), List):
            return True
        if isinstance(expr, Object):
            for interface in expr.class_.interfaces:
                if interface.name == 'List':
                    return True
        return False

    def get_data(self, exp):
        from types import Bool, Null, Variable, Int, Float

        if self.is_primitive(exp):
            return exp

        if '.' in str(exp):
            if int(float(exp)) == float(exp):
                return Int(int(float(exp)))
            return Float(round(float(exp), 10))
        try:
            return Int(int(exp))
        except:
            pass

        if exp == 'True':
            return Bool(True)
        elif exp == 'False':
            return Bool(False)

        if exp in '?':
            return Null()

        return Variable(exp)
