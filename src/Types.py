# -*- coding: utf-8 -*-
"""
Created on Sat Jul 18 14:51:39 2020

@author: rohan
"""
from Tuple import Tuple
from HFunction import Function, Lambda, Func

class Variable:
    def __init__(self, name):
        self.name = name
    
    def simplify(self):
        if self.name == '_ ...':
            return self
        from utils import frameStack
        for curr in frameStack[::-1]:
            if self.name in curr.keys():
                return curr[self.name].simplify()
        #raise Exception('Variable', self.name, 'is not defined') 
        return self
    
    def __str__(self):
        return self.name

    
class Int:
    def __init__(self, value):
        self.type = 'int'
        self.value = value
    
    def simplify(self):
        return self
    
    def __str__(self):
        if (self.value == None):
            return '?'
        return str(self.value)

class Float:
    def __init__(self, value):
        self.type = 'float'
        self.value = value
    
    def simplify(self):
        return self
    
    def __str__(self):
        return str(self.value)


class Bool:
    def __init__(self, value):
        self.type = 'bool'
        self.value = value
    
    def simplify(self):
        return self
    
    def __str__(self):
        values = ['False', 'True']
        return values[self.value]


class Char:
    def __init__(self, value):
        self.type = 'char'
        self.value = value
    
    def simplify(self):
        return self
    
    def __str__(self):
        return "'" + str(self.value) + "'"

class String:
    def __init__(self, value):
        self.type = 'string'
        self.value = value
    
    def simplify(self):
        return self
    
    def __str__(self):
        return self.value

class Alias:
    def __init__(self, var, expr):
        self.var = var
        self.expr = expr
    
    def __str__(self):
        return str(self.var) + '@' + str(self.expr)
    
    def simplify(self, simplifyVariables = True):
        return self

class Collection:
    def __init__(self, items = [], operator = None):
        self.items = items
        self.operator = operator
    
    def simplify(self):
        if self.operator.name == ',':
            return Tuple(list(filter(lambda item: item != None, self.items)))
        if len(self.items) == 2:
            left = self.items[0] 
            if left: left = left.simplify()
            right = self.items[1]
            if right: right = right.simplify()
            return self.operator.apply(left, right)
        for i in range(len(self.items) - 1): 
            if (not self.operator.apply(self.items[i].simplify(),
                                        self.items[i + 1].simplify()).value):
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
    
    def simplify(self):
        return self 
    
    def __str__(self):
        return self.name

class Enum:
    def __init__(self, name, values):
        self.name = name
        self.values = values
    
    def simplify(self):
        return self
    
    def __str__(self):
        return ' | '.join(self.values)

class Struct(Func):
    def __init__(self, name, fields):
        self.name = name
        self.fields = fields
    
    def simplify(self):
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
            
    def simplify(self):
        return self
    
    def __str__(self):
        return ('(' + self.type.name + ' ' 
                  + ' '.join(list(map(str, self.values))) + ')')

class Class(Func):
    def __init__(self, name):
        self.name = 'class ' + name
        self.state = {'this' : self}
        self.parent_classes = []
        self.interfaces = []
        self.private = self.public = self.hidden = []
        self.isConstructor = False

    def apply(self, expr):
        import utils
        if not self.isConstructor:
            methods = expr
            self.isConstructor = True
            self.name = self.name.split(' ')[1]
            utils.frameStack.append(self.state)
            utils.in_class = True
            methods.simplify()
            utils.in_class = False
            utils.frameStack.pop(-1)
            utils.typeNames.append(self.name)
            utils.functionNames.append(self.name)
            return self
        else:
            values = expr
            obj = Object(self)
            for name in self.state.keys():
                if isinstance(self.state[name], (Function, Lambda)):
                    obj.state[name] = Method(obj, self.state[name])
                else:
                    obj.state[name] = self.state[name]  
                    
            obj.state['this'] = obj 

            if 'init' in self.state.keys():
                obj.state['init'].apply(values)
            
            return obj
        
    def __str__(self):
        return self.name
    
    def simplify(self):
        return self
        
class Method(Func):
    def __init__(self, obj, func):
        self.name = func.name
        self.obj = obj
        self.func = func
    
    def apply(self, arg1 = None, arg2 = None):
        from utils import frameStack
        frameStack.append(self.obj.state)
        value = self.func.apply(arg1, arg2)
        frameStack.pop(-1)
        if issubclass(type(value), Func):
            return Method(self.obj, value) 
        return value

    def simplify(self):
        from utils import frameStack
        state = self.obj.state
        frameStack.append(state)
        value = self.func.simplify()
        frameStack.pop(-1) 
        if issubclass(type(value), Func):
            return Method(self.obj, value) 
        return value
    
    def __str__(self):
        return str(self.obj) + ' ' + str(self.func)

class Object:
    def __init__(self, class_):
        self.class_ = class_
        self.state = {'this' : self}
        
    def simplify(self):
        return self
    
    def __str__(self):
        if 'toString' in self.state.keys():
            return str(self.state['toString'].simplify())
        return self.class_.name + ' object' 
    
    
class Interface:
    def __init__(self, name, declarationExpr):
        self.name = name
        state = {}
        from utils import frameStack
        import utils
        frameStack.append(state)
        utils.in_class = True
        declarationExpr.simplify()
        utils.in_class = False
        frameStack.pop(-1) 
        self.methods = state.keys()
    
    def simplify(self):
        return self

    def __str__(self):
        return self.name + ' ' + ' '.join(self.methods)

class Module:
    def __init__(self, name, code):
        self.name = name
        self.state = {}
        import utils
        utils.frameStack.append(self.state)
        utils.evaluate(code) 
        utils.frameStack.pop(-1)
        utils.frameStack[-1].update(self.state)
    
    def simplify(self):
        return self
    
    def __str__(self):
        return self.name
        

class Type:
    def __init__(self, name, expr = None):
        self.name = name
        self.expr = expr
    
    def simplify(self):
        return self
    
    def apply(self, var):
        from Operator_Functions import (defaultInt, defaultFloat, defaultBool,
                                        defaultChar)
        if self.name == 'int':
            return defaultInt(var)
        elif self.name == 'float':
            return defaultFloat(var)
        elif self.name == 'bool':
            return defaultBool(var)
        elif self.name == 'char':
            return defaultChar(var)
        
        return Int(None)
    
    def __str__(self):
        return str(self.expr)
    
class Union:
    def __init__(self, types):
        self.types = types.tup
        
    def __str__(self):
        return str(Tuple(self.types))
    
    def simplify(self):
        return self