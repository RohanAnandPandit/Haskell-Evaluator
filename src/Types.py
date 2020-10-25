# -*- coding: utf-8 -*-
"""
Created on Sat Jul 18 14:51:39 2020

@author: rohan
"""
from Tuple import Tuple
from HFunction import Function, Func

class Variable:
    def __init__(self, name):
        self.name = name
    
    def simplify(self, program_state):
        if self.name == '_ ...':
            return self
        
        frameStack = program_state.frameStack
        for curr in frameStack[::-1]:
            if self.name in list(curr.keys()):
                return curr[self.name].simplify(program_state)

        #raise Exception('Variable', self.name, 'is not defined') 
        #print(self.name)
        return self
    
    def __str__(self):
        return self.name

class Type(Func):
    def __init__(self, name, expr = None, program_state = None):
        self.name = name
        self.expr = expr
        self.lazy = True
        self.program_state = program_state
    
    def simplify(self, program_state): 
        return self
    
    def apply(self, var, program_state = None):
        from Operator_Functions import (defaultInt, defaultFloat, defaultBool,
                                        defaultChar)
        if self.name == 'int':
            return defaultInt(var, self.program_state)
        elif self.name == 'float':
            return defaultFloat(var, self.program_state)
        elif self.name == 'bool':
            return defaultBool(var, self.program_state)
        elif self.name == 'char':
            return defaultChar(var, self.program_state)
        
        return Null()
    
    def __str__(self):
        return str(self.expr)
    
class Null:
    def __init__(self):
        self.value = None
        
    def __str__(self):
        return '?'
    
    def simplify(self, program_state):
        return self

class Int:
    def __init__(self, value):
        self.type = 'int'
        self.value = value
    
    def simplify(self, program_state):
        return self
    
    def __str__(self):
        return str(self.value)

class Float:
    def __init__(self, value):
        self.type = 'float'
        self.value = value
    
    def simplify(self, program_state):
        return self
    
    def __str__(self):
        return str(self.value)


class Bool:
    def __init__(self, value):
        self.type = 'bool'
        self.value = value
    
    def simplify(self, program_state):
        return self
    
    def __str__(self):
        values = ['False', 'True']
        return values[self.value]


class Char:
    def __init__(self, value):
        self.type = 'char'
        self.value = value
    
    def simplify(self, program_state):
        return self
    
    def __str__(self):
        return "'" + self.value + "'"

class String:
    def __init__(self, value):
        self.type = 'string'
        self.value = value
    
    def simplify(self, program_state):
        return self
    
    def __str__(self):
        return '"' + str(self.value) + '"'

class Alias:
    def __init__(self, var, expr):
        self.var = var
        self.expr = expr
    
    def __str__(self):
        return str(self.var) + '@' + str(self.expr)
    
    def simplify(self, program_state):
        return self

class Collection:
    def __init__(self, items = [], operator = None):
        self.items = items
        self.operator = operator
    
    def simplify(self, program_state):
        if self.operator.name == ',':
            return Tuple(list(filter(lambda item: item != None, self.items)),
                         program_state)
        
        if len(self.items) == 2:
            left = self.items[0] 
            if left: left = left.simplify(program_state)
            right = self.items[1]
            if right: right = right.simplify(program_state)
            return self.operator.apply(left, right, program_state)
        for i in range(len(self.items) - 1): 
            if (not self.operator.apply(self.items[i].simplify(program_state),
             self.items[i + 1].simplify(program_state), program_state).value):
                return Bool(False)
        return Bool(True)
    
    def __str__(self):
        string = list(map(str,self.items))
        return '(' + (' '+ self.operator.name + ' ').join(string) + ')'


class EnumValue:
    def __init__(self, enum, name, value):
        self.type = enum.name
        self.enum = enum
        self.name = name
        self.value = value
    
    def simplify(self, program_state):
        return self 
    
    def __str__(self):
        return self.name

class Enum:
    def __init__(self, name, values):
        self.name = name
        self.values = values
    
    def simplify(self, program_state):
        return self
    
    def __str__(self):
        return ' | '.join(self.values)

class Struct(Func):
    def __init__(self, name, fields):
        self.name = name
        self.fields = fields
    
    def simplify(self, program_state):
        return self
    
    def apply(self, values):
        if isinstance(values, Tuple):
            values = values.tup
        else:
            values = [values]
        return Structure(self, values)

    def __str__(self):
        return self.name + ' ' + ' '.join(self.fields)

class Structure:
    def __init__(self, struct, values):
        self.type = struct
        self.values = values 
        self.state = dict(zip(self.type.fields, values))
            
    def simplify(self, program_state):
        return self
    
    def __str__(self):
        return ('(' + self.type.name + ' ' 
                  + ' '.join(list(map(str, self.values))) + ')')

class Class(Func):
    def __init__(self, name):
        self.name = 'class ' + name
        self.state = {}
        self.parent_classes = []
        self.interfaces = []
        self.private = self.public = self.hidden = []
        self.isConstructor = False
        self.lazy = True

    def apply(self, expr, program_state = None):
        if not self.isConstructor:
            self.isConstructor = True
            self.name = self.name.split(' ')[1]
            program_state.frameStack.append(self.state)
            program_state.in_class += 1
            expr.simplify(program_state)
            program_state.in_class -= 1
            program_state.frameStack.pop(-1)
            program_state.functionNames.append(self.name)
            return self
        else:
            values = expr
            obj = Object(self, program_state)
            for name in list(self.state.keys()):
                obj.state[name] = self.state[name]
                if isinstance(self.state[name], Function):
                    obj.state[name] = obj.state[name].clone()
                    obj.state[name].inputs.append(obj)
                    
            if 'init' in list(obj.state.keys()):
                obj.state['init'].apply(values, program_state = program_state)
            
            return obj
        
    def __str__(self):
        return self.name
    
    def simplify(self, program_state):
        return self
        
class Method(Func):
    def __init__(self, obj, func, program_state):
        self.name = func.name
        self.obj = obj
        self.func = func
        self.lazy = False
        self.program_state = program_state
    
    def apply(self, arg1 = None, arg2 = None, program_state = None):
        program_state.frameStack.append({'this' : self.obj})
        value = self.func.apply(arg1, arg2, program_state = program_state)
        program_state.frameStack.pop(-1)
        if issubclass(type(value), Func) and value.name == self.name:
            return Method(self.obj, value, program_state) 
        return value

    def simplify(self, program_state):
        self.program_state.frameStack.append({'this' : self.obj})
        value = self.func.simplify(program_state)
        self.program_state.frameStack.pop(-1) 
        if issubclass(type(value), Func) and value.name == self.name:
            return Method(self.obj, value, program_state)
        return value
    
    def __str__(self):
        return str(self.obj) + ' ' + str(self.func)

class Object:
    def __init__(self, class_, program_state):
        self.class_ = class_
        self.state = {'this' : self}
        self.program_state = program_state
        
    def simplify(self, program_state):
        return self
    
    def __str__(self):
        if 'toString' in list(self.state.keys()):
            string = self.state['toString'].simplify(self.program_state).value
            return string
        return self.class_.name + ' object'  
    
class Interface:
    def __init__(self, name, declarationExpr, program_state):
        self.name = name
        state = {}
        program_state.frameStack = program_state.frameStack
        program_state.frameStack.append(state)
        program_state.in_class += 1
        declarationExpr.simplify(program_state)
        program_state.in_class -= 1
        program_state.frameStack.pop(-1) 
        self.methods = state.keys()
    
    def simplify(self, program_state):
        return self

    def __str__(self):
        return self.name + ' ' + ' '.join(self.methods)

class Module:
    def __init__(self, name, code, program_state):
        self.name = name
        self.state = {}
        program_state.frameStack.append(self.state)
        program_state.evaluate(code) 
        program_state.frameStack.pop(-1)
        program_state.frameStack[-1].update(self.state) 
    
    def simplify(self, program_state):
        return self
    
    def __str__(self):
        return self.name
        
    
class Union:
    def __init__(self, name, types):
        self.name = name
        self.types = types.items
        
    def __str__(self):
        return str(Tuple(self.types))
    
    def simplify(self, program_state):
        return self