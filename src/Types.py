# -*- coding: utf-8 -*-
"""
Created on Sat Jul 18 14:51:39 2020

@author: rohan
"""
from Tuple import Tuple
from HFunction import Function, Lambda

class Variable:
    def __init__(self, name):
        self.name = name
    
    def simplify(self, simplifyVariable = True):
        from utils import frameStack
        if (simplifyVariable):
            curr = len(frameStack) - 1
            while (curr >= 0):
                frame = frameStack[curr]
                if (self.name in frame.keys()):
                    value = frame[self.name]
                    return value.simplify()
                curr -= 1
        #raise Exception('Variable', self.name, 'is not defined') 
        return self
    
    def __str__(self):
        return self.name

class Constant:
    def __init__(self, name):
        self.name = name
        self.value = None
    
    def simplify(self, a = True):
        return self.value
    
    def __str__(self):
        if self.value != None:
            return str(self.value)
        return self.name
    
class Int:
    def __init__(self, value):
        self.type = 'Int'
        self.value = value
    
    def simplify(self, simplifyVariable = True):
        return self
    
    def __str__(self):
        if (self.value == None):
            return '?'
        return str(self.value)

class Float:
    def __init__(self, value):
        self.type = 'Float'
        self.value = value
    
    def simplify(self, simplifyVariable = True):
        return self
    
    def __str__(self):
        return str(self.value)


class Bool:
    def __init__(self, value):
        self.type = 'Bool'
        self.value = value
    
    def simplify(self, simplifyVariable = True):
        return self
    
    def __str__(self):
        values = ['False', 'True']
        return values[self.value]


class Char:
    def __init__(self, value):
        self.type = 'Char'
        self.value = value
    
    def simplify(self, simplifyVariable = True):
        return self
    
    def __str__(self):
        return "'" + str(self.value) + "'"

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
    
    def simplify(self, simplifyVariables = True):
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
        string = (' '+ self.operator.name + ' ').join(list(map(str, self.items)))
        if self.operator.name == ':':
            string += ' : []'
        return '(' + string + ')'

class Conditional:
    def __init__(self, cond, ret):
        self.cond = cond
        self.ret = ret 
    
    def simplify(self, simplifyVariables = True):
        if self.cond.simplify().value:
            return self.ret.simplify()
        return Int(None)

    def __str__(self):
        return '(' + str(self.cond) + ' => ' + str(self.ret) + ')'
    
class Else:
    def __init__(self, conditional, right):
        self.conditional = conditional
        self.right = right
    
    def simplify(self, simplifyVariables = True):
        value = self.conditional.simplify()
        from Operator_Functions import equals
        if equals(value, Int(None)):
            return self.right.simplify()
        return value
    
    def __str__(self):
        return '(' + str(self.conditional) + ' | ' + str(self.right) + ')'


class EnumValue:
    def __init__(self, enum, name, value):
        self.enum = enum
        self.name = name
        self.value = value
    
    def simplify(self, a = True):
        return self 
    
    def __str__(self):
        return self.name

class Enum:
    def __init__(self, name, values):
        self.name = name
        self.values = values
    
    def simplify(self, a = True):
        return self
    
    def __str__(self):
        return ' | '.join(self.values)

class Struct:
    def __init__(self, name, fields):
        self.name = name
        self.fields = fields
    
    def simplify(self, a = True):
        return self
    
    def apply(self, values):
        if (isinstance(values, Tuple)):
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
            
    def simplify(self, a = True):
        return self
    
    def __str__(self):
        return '(' + self.type.name + ' ' + ' '.join(list(map(str, self.values))) + ')'

class Class:
    def __init__(self, name, methodsExpr):
        self.name = name
        self.state = {} 
        from utils import frameStack
        frameStack.append(self.state)
        methodsExpr.simplify()
        frameStack.pop(-1) 
    
    def apply(self, values):
        obj = Object(self)
        for name in self.state.keys():
            if isinstance(self.state[name], (Function, Lambda)):
                obj.state[name] = Method(obj, self.state[name])
            else:
                obj.state[name] = self.state[name]
        if 'init' in self.state.keys():
            obj.state['init'].apply(values)
        return obj
    
    def __str__(self):
        return self.name + ' {' + ' '.join(self.fields) + '} ' + ' '.join(self.state.keys())
    
    def simplify(self):
        return self
        
class Method:
    def __init__(self, obj, func):
        self.obj = obj
        self.func = func
    
    def apply(self, arg1 = None, arg2 = None):
        from utils import frameStack
        if self.func.noOfArgs == 1 and arg1 != None or self.func.noOfArgs == 0:
            state = self.obj.state
            frameStack.append(state)
            value = self.func.apply(arg1, arg2)
            frameStack.pop(-1)
            return value
        func = self.func.apply(arg1, arg2)
        return Method(self.obj, func) 

    def simplify(self):
        from utils import frameStack
        if self.func.noOfArgs == 0:
            state = self.obj.state
            frameStack.append(state)
            value = self.func.simplify()
            frameStack.pop(-1)
            return value
        return self
    
    def __str__(self):
        return str(self.obj) + ' ' + str(self.func)

class Object:
    def __init__(self, classType):
        self.classType = classType
        self.state = {'this' : self}
        
    def simplify(self, a = True):
        return self
    
    def __str__(self):
        if 'toString' in self.state.keys():
            return str(self.state['toString'].simplify())
        return self.classType.name + ' object' 
    
    
class Interface:
    def __init__(self, name, declarationExpr):
        self.name = name
        state = {}
        from utils import frameStack
        frameStack.append(state)
        declarationExpr.simplify()
        frameStack.pop(-1) 
        self.methods = state.keys()
    
    def simplify(self):
        return self

    def __str__(self):
        return self.name + ' ' + ' '.join(self.methods)        