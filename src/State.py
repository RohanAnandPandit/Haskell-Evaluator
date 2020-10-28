# -*- coding: utf-8 -*-
"""
Created on Mon Sep  7 09:32:31 2020

@author: rohan
"""
from HFunction import HFunction
from Operators import Associativity
import Operator_Functions as op_func
import Prelude
from Parser import Parser
from Lexer import Lexer

class State:
    def __init__(self):
        self.reset()
    
    def reset(self):
        self.operators = [' ', '/', '*', '+', '-', '^', '==', '<', '<=', '>', 
            '>=', '&&', '||', '(', ')', ',', '[', ']', ':',  '+', '...', 
            '/=', '!!', '`', '$', ';', '>>', '>>=', '=', '->', '--', '\\', 
            ' where ', '|', '@',  '<-', '<<', '&', '}', '|||', ' then ',
            ' else ', '\t', '{','=>', '~', ',,', '\n', '.', ' extends ',
            ' implements ', '!=', ' in ', '+=', '-=', '*=',
            '/=', '^=', '//', '%', '::'] 
    
        self.keywords = ['class', 'def', 'struct', 'interface', 'extends',
            'implements', 'while', 'for', 'switch', 'default', 'if', 'else',
            'then', 'enum', 'oper', 'break', 'continue', 'in', 'True', 
            'False', 'let', 'import', 'return', 'int', 'float', 'bool',
            'char', 'var', 'do', '?', 'Num', 'from', 'type', 'union', 
            'stop', 'skip', 'global', 'local', 'hidden', 'Func', 'where']
        
        self.functional_mode = self.static_mode = False
        self.builtInState = {}
        self.frameStack = [self.builtInState]
        self.functionNames = []
        self.in_class = 0
        self.breakLoop = 0
        self.continueLoop = 0
        self.return_value = None
        self.initialiseFunctions()

        
    def initialiseFunctions(self):
        from Types import Type       
        self.builtInState['println'] = HFunction(8, Associativity.LEFT,
                                         Prelude.printLn, 1, 'println')
        
        self.builtInState['print'] = HFunction(8, Associativity.LEFT, 
                                     Prelude.print_, 1, 'print')
        
        self.builtInState['show'] = HFunction(8, Associativity.LEFT, 
                                     Prelude.show, 1, 'show')
        
        self.builtInState['tostr'] = HFunction(8, Associativity.LEFT, 
                                     op_func.toString, 1, 'tostr')
        
        self.builtInState['input'] = HFunction(8, Associativity.LEFT,
                                     Prelude.input_, 1, 'input')
    
        self.builtInState['eval'] = HFunction(8, Associativity.LEFT,  
                                             op_func.eval_, 1, 'eval')
        
        self.builtInState['for'] = HFunction(8, Associativity.LEFT,
                                 op_func.forLoop, 2, 'for', lazy = True)
        
        self.builtInState['while'] = HFunction(8, Associativity.LEFT,
                                     op_func.whileLoop, 2, 'while',
                                     lazy = True)
        
        self.builtInState['if'] = HFunction(8, Associativity.LEFT, 
                                 op_func.ifStatement, 2, 'if', lazy = True)
        
        self.builtInState['struct'] = HFunction(8, Associativity.LEFT, 
                                     op_func.createStruct, 2, 'struct', 
                                     lazy = True)
        
        self.builtInState['enum'] = HFunction(8, Associativity.LEFT,
                                 op_func.createEnum, 2, 'enum', lazy = True)
        
        self.builtInState['oper'] = HFunction(8, Associativity.LEFT, 
                                 op_func.createOperator, 4, 'oper', 
                                 lazy = True)
        
        self.builtInState['class'] = HFunction(8, Associativity.LEFT, 
                                 op_func.createClass, 1, 'class', lazy = True)
        
        self.builtInState['interface'] = HFunction(8, Associativity.LEFT,
                                 op_func.createInterface, 2, 'interface', 
                                 lazy = True)
        
        self.builtInState['def'] = HFunction(8, Associativity.LEFT, 
                                 op_func.definition, 3, 'def', lazy = True)
        
        self.builtInState['switch'] = HFunction(8, Associativity.LEFT, 
                                 op_func.switch, 2, 'switch', lazy = True)
        
        self.builtInState['continue'] = HFunction(8, Associativity.LEFT,
                                 op_func.continue_loop, 0, 'continue')
        
        self.builtInState['break'] = HFunction(8, Associativity.LEFT, 
                                 op_func.breakCurrentLoop, 0, 'break')
        
        self.builtInState['let'] = HFunction(8, Associativity.LEFT, 
                                 op_func.let, 2, 'let', lazy = True)
        
        self.builtInState['import'] = HFunction(8, Associativity.LEFT,
                             op_func.import_module, 1, 'import', lazy = True)
        
        self.builtInState['from'] = HFunction(8, Associativity.LEFT, 
                                 op_func.from_import, 3, 'from', lazy = True)
        
        self.builtInState['return'] = HFunction(8, Associativity.LEFT,
                                 op_func.return_statement, 1, 'return')
        
        self.builtInState['toint'] = HFunction(8, Associativity.LEFT, 
                                 op_func.toInt, 1, 'toint')
        
        self.builtInState['tofloat'] = HFunction(8, Associativity.LEFT, 
                                 op_func.toFloat, 1, 'tofloat')
        
        self.builtInState['tobool'] = HFunction(8, Associativity.LEFT,
                                 op_func.toBool, 1, 'tobool')
        
        self.builtInState['tochar'] = HFunction(8, Associativity.LEFT, 
                                     op_func.toChar, 1, 'tochar')
        
        self.builtInState['do'] = HFunction(8, Associativity.LEFT, 
                                 op_func.doLoop, 3, 'do', lazy = True) 

        self.builtInState['var'] = Type('var', program_state = self)         
        self.builtInState['int'] = Type('int', program_state = self) 
        self.builtInState['float'] = Type('float', program_state = self) 
        self.builtInState['bool'] = Type('bool', program_state = self) 
        self.builtInState['char'] = Type('char', program_state = self) 
        self.builtInState['string'] = Type('string', program_state = self)
        self.builtInState['Object'] = Type('Object', program_state = self) 
        self.builtInState['Func'] = Type('Func', program_state = self) 
        self.builtInState['Type'] = Type('Type', program_state = self) 
        
        self.builtInState['type'] = HFunction(8, Associativity.LEFT,
                                 op_func.type_synonym, 2, 'type', lazy = True)
        
        self.builtInState['union'] = HFunction(8, Associativity.LEFT,
                                     op_func.types_union, 2, 'union',
                                     lazy = True) 
        
        self.builtInState['stop'] = HFunction(8, Associativity.LEFT,
                                     op_func.breakout, 1, 'stop') 
        self.builtInState['skip'] = HFunction(8, Associativity.LEFT,
                                     op_func.skipout, 1, 'skip') 
        self.builtInState['global'] = HFunction(8, Associativity.LEFT,
                                     op_func.make_public, 1, 'global') 
        self.builtInState['local'] = HFunction(8, Associativity.LEFT,
                                     op_func.make_private, 1, 'local') 
        self.builtInState['hidden'] = HFunction(8, Associativity.LEFT,
                                     op_func.make_hidden, 1, 'hidden') 
        self.builtInState['match'] = HFunction(8, Associativity.LEFT,
                                     op_func.match, 2, 'match', lazy = True) 
        self.builtInState['py'] = HFunction(8, Associativity.LEFT,
                                     op_func.python_eval, 1, 'py') 
        self.evaluate('import Prelude')

    
    def evaluate(self, source, reset_state = False):
        value = None
        if "#STATIC-MODE#\n" in source:
            self.static_mode = True
        if "#FUNCTIONAL-MODE#\n" in source:
            self.functional_mode = True
        for section in source.split('#EVAL#\n'):                
            lexer = Lexer(source, self)
            #print("tokens : ", end = '')
            #lexer.printTokens() 
            expr = Parser(lexer, self).expr
            #expr = optimise(expr)
            #print("expression : ", str(expr)) 
            #print("result : ", end = '')
            #try:
            value = expr.simplify(self)
            #except Exception as error:
                #print(' '.join(error.args))
        if reset_state:
            self.reset()
        return value

    def isPrimitive(self, expr):
        from Types import Int, Float, Bool, Char, String, EnumValue, Null
        return isinstance(expr, (Int, Float, Bool, Char, String, EnumValue,
                                 Null))
    
    def null(self, expr):
        from Types import Null
        return isinstance(expr, Null)
    
    def isType(self, expr):
        from List import Nil, Array
        from Types import Type, Class, Struct, Null, Union
        from Tuple import Tuple
        return isinstance(expr, (Nil, Null, Type, Class, Struct, Tuple, 
                                 Array, Union)) 
    
    def isList(self, expr):
        from List import List
        from Types import Object
        if issubclass(type(expr), List):
            return True
        if isinstance(expr, Object):
            for interface in expr.class_.interfaces:
                if interface.name == 'List':
                    return True
        return False   

    def getData(self, exp):
        from Types import Bool, Null, Variable, Int, Float 
        
        if self.isPrimitive(exp): 
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
