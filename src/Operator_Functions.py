# -*- coding: utf-8 -*-
"""
Created on Sat Jun 27 16:19:04 2020

@author: rohan
"""
from utils import frameStack, functionNames, getData, enumNames, isPrimitive
from utils import patternMatch
from HFunction import HFunction, Composition, Function, Lambda
from List import List, Nil, Cons, Iterator, head, tail, Array
from Tuple import Tuple
from Types import (Int, Float, Bool, Variable, Alias, Enum, EnumValue, Struct,
                   Class, Interface, Char, Module, Object, String, Null, 
                   Collection, Type)
from Expression import BinaryExpr
from math import *

def assign(a, b, program_state, state = None):
    var, value = a, b
    if isPrimitive(var) or isinstance(var, Nil):
        return 
 
    if isinstance(var, Variable):
        if var.name == '_ ...': return var

        if b == None:
            print(0)
        value = b.simplify(program_state)

        if program_state.functional_mode:
            if var.name in list(state.keys()):
                raise Exception('Cannot assign variable',
                                var.name, 'in FUNCTIONAL-MODE.')
        if program_state.static_mode:
            if var.name in list(state.keys()):
                varType = type(state[var.name])
                valType = type(value)
                if varType != valType:
                    raise Exception('Cannot assign variable', var.name,
                                    'of type',
                                    str(varType), 'with value of type',
                                    str(valType),
                                    'in STATIC-MODE.') 

        if state == None:
            for curr in program_state.frameStack[::-1]:
                if var.name in list(curr.keys()):
                    curr[var.name] = value 
                    return value
            state = program_state.frameStack[-1] 
        state[var.name] = value
        return value
    
    if state == None:
        state = program_state.frameStack[-1]
        
    if (isinstance(var, (Tuple, Array)) or 
        isinstance(var, Collection) and var.operator.name == ','):
        value = value.simplify(program_state)
        
        for i in range(len(var.items)): 
            assign(var.items[i], value.items[i], program_state, state) 
            
        return value

    elif isinstance(var, Cons):
        assign(head(var), head(value), program_state, state)
        assign(tail(var), tail(value), program_state, state)
        return value
        
    elif isinstance(var, BinaryExpr):
        if var.operator.name == '@':
            assign(var.leftExpr, value, program_state, state)
            assign(var.rightExpr, value, program_state, state)
            
        if var.operator.name == '!!':
            array = var.leftExpr.simplify(program_state)
            value = value.simplify(program_state)
            index = head(var.rightExpr).simplify(program_state).value
            if len(array.items) == index:
                array.items.append(value)
            else:
                array.items[index] = value 

        if var.operator.name == ':':
            value = value.simplify(program_state)
            assign(var.leftExpr, head(value, program_state),
                   program_state, state) 
            assign(var.rightExpr, tail(value, program_state),
                   program_state, state)
            return value
        
        elif var.operator.name == '.':
            obj = var.leftExpr.simplify(program_state)
            obj.state[var.rightExpr.name] = value.simplify(program_state)
            
        elif var.operator.name == ' ':
            arguments = []
            args = var 
            while True:
                arg = args.rightExpr 
                arguments.insert(0, arg)
                args = args.leftExpr
                if (isinstance(args, (Variable,Nil,Cons,Tuple,Array,Class,Type)) or 
                    program_state.null(args)):
                    arguments.insert(0, args)
                    break 
                
            if (isinstance(arguments[0], Variable) and
                isinstance(arguments[0].simplify(program_state), Struct) and
                isinstance(arguments[1], Tuple)):
                    assign(arguments[1], Tuple(value.values, program_state), 
                           program_state, state) 
                    return value

            
            if program_state.isType(arguments[0].simplify(program_state)):
                assign(arguments[1], value, program_state, state)
                return value 
            
            elif arguments[0].name == 'def':
                name = arguments[1].name
                arguments = arguments[2:] 
                
                for i in range(len(arguments)):
                    if not (isinstance(arguments[i], BinaryExpr) and 
                            arguments[i].operator.name in ' :'):
                        arguments[i] = arguments[i].simplify(program_state)
                
                case = Lambda(name, arguments = arguments, expr = value)
                if name:
                    if program_state.in_class:
                        if name in list(state.keys()):
                            func = state[name]
                            func.cases.append(case)
                            return case 
                        else:
                            func = Function(name, [case])
                            state[name] = func
                            program_state.functionNames.append(name) 
                    else:
                        for state in program_state.frameStack[::-1]:
                            if name in list(state.keys()):
                                func = state[name]
                                func.cases.append(case)
                                return case 
                        func = Function(name, [case])
                        state[name] = func
                        program_state.functionNames.append(name) 
                return case

    return value
    
def application(func, arg, program_state):
    #try:
    if isinstance(func, Class) and isinstance(arg, Tuple):
        #print(0)
        pass
    value = func.apply(arg, program_state = program_state) 
    return value
    #except:
        #print(0)

def compose(second, first, program_state):
    return Composition(second, first)

def index(a, b, program_state):
    from List import head, tail
    if isinstance(b, Int):
        n = b.value
        if n < 0 or isinstance(a, Nil):
            return None
        if program_state.isList(a):
            x, xs = head(a), tail(a) 
            if n == 0:
                return x
            return index(xs, Int(n - 1))
        elif isinstance(a, Enum):
            return a.values[n]
        elif isinstance(a, (Tuple, Array)):
            return a.items[n]
        
    elif isinstance(b, Cons):
        start, b = head(b).simplify(), tail(b)
        if isinstance(b, Nil):
            return index(a, start)
        else:
            end = head(b).simplify()
            if isinstance(a, String):
                return String(a.value[start.value : end.value])

            return Array(a.items[start.value : end.value])

def power(a, b, program_state):
    if isinstance(a, Object):
        if 'pow' in list(a.state.keys()):
            return a.state['pow'].apply(b, program_state = program_state) 
        
    a, b = a.value, b.value
    return getData(a ** b)

def divide(a, b, program_state):
    if isinstance(a, Object):
        if 'div' in list(a.state.keys()):
            return a.state['div'].apply(b, program_state = program_state)
        
    (a, b) = (a.value, b.value)
    return getData(a / b)

def multiply(a, b, program_state):
    if isinstance(a, Object):
        if 'mul' in list(a.state.keys()):
            return a.state['mul'].apply(b, program_state = program_state) 
    elif isinstance(b, Object):
        if 'mul' in list(b.state.keys()):
            return b.state['mul'].apply(a, program_state = program_state)
        
    a, b = a.value, b.value
    return getData(a * b)

def add(a, b, program_state):
    if isinstance(a, Object):
        if 'add' in list(a.state.keys()):
            return a.state['add'].apply(b, program_state = program_state) 
    elif isinstance(b, Object):
        if 'add' in list(b.state.keys()):
            return b.state['add'].apply(a, program_state = program_state)
        
    a, b = a.value, b.value
    return getData(a + b)

def subtract(a, b, program_state):
    if isinstance(a, Object):
        if 'sub' in list(a.state.keys()):
            return a.state['sub'].apply(b, program_state = program_state)
    if isinstance(b, Object):
        if 'subfrom' in list(b.state.keys()):
            return b.state['subfrom'].apply(a, program_state = program_state)
        
    a, b = a.value, b.value
    return getData(a - b)

def lessThan(a, b, program_state):
    if isinstance(a, Object):
        if 'lessThan' in list(a.state.keys()):
            return a.state['lessThan'].apply(b, 
                          program_state = program_state)
        return Bool(False)
    elif isinstance(b, Object):
        if 'greaterThan' in list(b.state.keys()):
            return b.state['greaterThan'].apply(a, 
                          program_state = program_state)
        return Bool(False)
    
    return Bool(a.value < b.value)

def lessThanOrEqual(a, b, program_state):
    return Bool(lessThan(a, b, program_state).value or 
                equals(a, b, program_state).value)

def greaterThan(a, b, program_state):
    if isinstance(a, Object):
        if 'greaterThan' in list(a.state.keys()):
            return a.state['greaterThan'].apply(b, 
                          program_state = program_state)
        return Bool(False)
    
    return Bool(not lessThanOrEqual(a, b, program_state).value)

def greaterThanOrEqual(a, b, program_state):
    return Bool(greaterThan(a, b, program_state).value or 
                equals(a, b, program_state).value)

def rem(a, b, program_state):
    return Int(a.value % b.value)

def quot(a, b):
    return Int(a.value // b.value)

def equals(a, b, program_state):
    if a == None or b == None:
        return Bool(False)
    if (isinstance(a, (Variable, BinaryExpr)) 
        or isinstance(b, (Variable, BinaryExpr))):
        return Bool(False)
    if issubclass(type(a), List) and issubclass(type(b), List):
        if isinstance(a, Nil) and isinstance(b, Nil):
            return Bool(True)
        if isinstance(a, Cons) and isinstance(b, Cons):
            x, xs = head(a), tail(a)
            y, ys = head(b), tail(b)
            return equals(x, y) and equals(xs, ys)
        return Bool(False)
    if isinstance(a, (Array, Tuple)) and isinstance(b, (Array, Tuple)):
        if len(a.items) != len(b.items):
            return Bool(False)
        for i in range(len(a.items)):
            if not equals(a.items[i], b.items[i], program_state).value:
                return Bool(False)
        return Bool(True)
    if isPrimitive(a) and isPrimitive(b):
        return Bool(a.value == b.value)
    
    if isinstance(a, Object):
        if 'equals' in list(a.state.keys()):
            return a.state['equals'].apply(b, program_state = program_state)
        return Bool(a == b)
    
    return Bool(False)

def notEqual(a, b, program_state):
    return Bool(not equals(a, b, program_state).value)

def AND(a, b, program_state):
    if not a.simplify(program_state).value: 
        return Bool(False)
    return b.simplify(program_state)

def OR(a, b, program_state):
    if a.simplify(program_state).value: 
        return Bool(True)
    return b.simplify(program_state)

def comma(a, b):
    if isinstance(a, Tuple):
        return Tuple(a.items.append(b))
    return Tuple([a, b])

def cons(a, b, program_state):
    from utils import replaceVariables
    x, xs = a, b
    return Cons(replaceVariables(x, program_state),
                xs.simplify(program_state), program_state)

def concatenate(a, b, program_state): 
    from List import head, tail
    left, right = a, b
    if isinstance(left, String):
        return String(left.value + right.value)
    if isinstance(left, Nil):
        return right
    elif isinstance(right, Nil):
        return left
    x, xs = head(left, program_state), tail(left, program_state)
    return Cons(x, concatenate(xs, right, program_state))
 
def iterator(a, b):
    var, collection = a, b
    return Iterator(var, collection)

def range_specifier(a):
    from List import Range
    options = a.tup
    if len(options) == 1:
        start = Int(0)
        end = options[0]
        step = Int(1)
    elif len(options) == 2:
        start = options[0]
        end = options[1]
        step = Int(1)
    elif len(options) == 3:
        start = options[0]
        end = options[1]
        step = options[2]
    return Range(start, end, step)
        
        
def comprehension(a, b):
    from List import Range
    start, end = a, b
    return Range(start, end, Int(1))

def sequence(a, b, program_state):
    if not (program_state.breakLoop > 0 or program_state.continueLoop > 0):
        a.simplify(program_state)
        
        if program_state.return_value:
            return program_state.return_value
        
        if not (program_state.breakLoop > 0 or program_state.continueLoop >0):
            return b.simplify(program_state)
        
    return Null()
    
def chain(a, b):
    return b.apply(a.simplify())

def createLambda(args, expr, program_state):
    arguments = []
    while True:
        if isinstance(args, (Variable, HFunction)):
            name = args.name
            break
        arguments.insert(0, args.rightExpr)
        args = args.leftExpr
    case = Lambda(name, expr, arguments = arguments)
    return case

def createEnum(name, values, program_state):
    state = program_state.frameStack[-1]
    values = values.tup
    names = list(map(str, values))
    name = name.name
    enum = Enum(name, names)
    state[name] = enum
    i = 0
    for val in values:
        enumNames.append(val.name)
        assign(val, EnumValue(enum, val.name, i))
        i += 1
    return enum
 
def createStruct(name, fields, program_state):
    state = program_state.frameStack[-1]
    fields = list(map(lambda var: var.name, fields.tup))
    name = name.name
    struct = Struct(name, fields)
    state[name] = struct
    program_state.functionNames.append(name)
    return struct

def createOperator(symbol, precedence, associativity, func, program_state):
    from utils import operators
    from Operators import operatorsDict, Op, Associativity
    associativityMap = {'left' : Associativity.LEFT,
                        'right' : Associativity.LEFT,
                        'none' : Associativity.NONE}
    
    precedence = precedence.value
    associativity = associativityMap[associativity.name]
    symbol = str(symbol)
    program_state.operators.append(symbol) 
    
    func = func.simplify(program_state).apply(program_state = program_state)
    func.name = symbol
    func.precedence = precedence
    func.associativity = associativity
    
    operatorsDict[symbol] = Op(func)
    
    return func

def createClass(nameVar, program_state):
    name = nameVar.name
    class_ = Class(name)
    assign(nameVar, class_, program_state)
    return class_

def createInterface(name, declarationsExpr, program_state):
    state = program_state.frameStack[-1]
    name = name.name
    interface = Interface(name, declarationsExpr, program_state)
    state[name] = interface
    program_state.functionNames.append(name)
    return interface
        
def where(expr1, expr2, program_state):
    program_state.frameStack.append({})
    expr2.simplify()
    value = expr1.simplify()
    program_state.frameStack.pop(-1)
    return value

def alias(var, expr):
    return Alias(var, expr)

def shiftLeft(num, n):
    return Int(num.value << n.value)

def shiftRight(num, n):
    return Int(num.value >> n.value)

def bitwise_or(x, y):
    return Int(x.value | y.value)

def bitwise_and(x, y):
    return Int(x.value & y.value)

def access(obj, field, program_state):
    obj = obj.simplify(program_state)
    return obj.state[field.name].simplify(program_state)


def forLoop(n, expr, program_state):
    if isinstance(n, Tuple):
        generators = n.items
        program_state.frameStack.append({})
        curr = generators[0].simplify(program_state) 
        var, collection = curr.var, curr.collection.simplify(program_state)
        while not isinstance(collection, Nil): 
            assign(var, head(collection), program_state)
            if len(generators) == 1:
                expr.simplify(program_state)
            else:
                forLoop(Tuple(generators[1:]), expr, program_state)
            if program_state.breakLoop > 0 or program_state.return_value:
                program_state.breakLoop -= 1
                break
            if program_state.continueLoop > 0:
                program_state.continueLoop -= 1
            collection = tail(collection, program_state)
        program_state.frameStack.pop(-1)
        
    elif isinstance(n, BinaryExpr):
        if n.operator.name == ';':
            init, n = n.leftExpr, n.rightExpr
            cond, after = n.leftExpr, n.rightExpr
            state = {}
            program_state.frameStack.append(state)
            init.simplify(program_state)
            while cond.simplify(program_state).value:
                expr.simplify(program_state)
                if program_state.continueLoop > 0:
                    program_state.continueLoop -= 1
                if program_state.breakLoop > 0 or program_state.return_value:
                    program_state.breakLoop -= 1
                    break
                after.simplify(program_state)
            program_state.frameStack.pop(-1)
            
        elif n.operator.name == 'in':
            n = n.simplify(program_state)
            program_state.frameStack.append({})
            var, collection = n.var, n.collection.simplify(program_state)
            if program_state.isList(collection):
                while not isinstance(collection, Nil):
                    assign(var, head(collection)) 
                    expr.simplify(program_state)
                    if (program_state.breakLoop > 0 or 
                        program_state.return_value):
                        program_state.breakLoop -= 1
                        break
                    if program_state.continueLoop > 0:
                        program_state.continueLoop -= 1
                    collection = tail(collection, program_state)
                    
            elif isinstance(collection, (Tuple, Array)):
                for item in collection.items:
                    assign(var, item, program_state, ) 
                    expr.simplify(program_state)
                    if (program_state.breakLoop > 0 or 
                        program_state.return_value):
                        program_state.breakLoop -= 1
                        break
                    if program_state.continueLoop > 0:
                        program_state.continueLoop -= 1
            frameStack.pop(-1)
            
        else:
            n = n.simplify(program_state)
            for i in range(n.value):
                expr.simplify(program_state)
                if program_state.continueLoop > 0:
                    program_state.continueLoop -= 1
                if program_state.breakLoop > 0:
                    program_state.breakLoop -= 1
                    break
                
    else:
        n = n.simplify(program_state)
        for i in range(n.value):
            expr.simplify(program_state)
            if program_state.continueLoop > 0:
                program_state.continueLoop -= 1
            if program_state.breakLoop > 0:
                program_state.breakLoop -= 1

    return Int(0)

def whileLoop(cond, expr, program_state):
    while cond.simplify(program_state).value:
        value = expr.simplify(program_state)
        if program_state.continueLoop > 0:
            program_state.continueLoop -= 1
        if program_state.breakLoop > 0 or program_state.return_value:
            program_state.breakLoop -= 1
            break
    return value

def breakCurrentLoop(program_state):
    program_state.breakLoop = 1
    return Int(0)

def continue_loop(program_state):
    program_state.continueLoop = 1
    return Int(0)

def breakout(n, program_state):
    program_state.breakLoop += n.value
    return Int(0)

def skipout(n, program_state):
    program_state.continueLoop += n.value
    return Int(0)
    
def ifStatement(cond, expr, program_state):
    if cond.simplify(program_state).value:
        return expr.simplify(program_state)
    return Null()

def extends(subclass, superclass, program_state):
     subclass.state['super'] = superclass
     for name in superclass.state.keys():
         subclass.state[name] = superclass.state[name]
     return subclass

def implements(class_, interface, program_state):
    class_.interfaces.append(interface)
    return class_

def definition(name_var, args_tup, expr, program_state):
    name = name_var.name
    state = program_state.frameStack[-1]
    case = Lambda(program_state, name, arguments = [args_tup], expr = expr)
    if name != None:
        if name in state.keys():
            func = state[name]
            func.cases.append(case)
        else:
            func = Function(name, 1, [case])
            state[name] = func
            functionNames.append(name) 
    return case
        
def switch(value, expr, program_state):
    cases = []
    while True:
        if not (isinstance(expr, BinaryExpr) and expr.operator.name == ';'):
            cases.append(expr)
            break
        cases.append(expr.leftExpr)
        expr = expr.rightExpr
    followThrough = False
    for case in cases:
        if (followThrough or 
            isinstance(case.leftExpr, Variable) and 
            case.leftExpr.name == 'otherwise' or 
            patternMatch(case.leftExpr.simplify(program_state),
                         value.simplify(program_state), program_state)):
            val = case.rightExpr.simplify(program_state)
            followThrough = True
            if case.operator.name == '=>':
                return val 
    return Null()

def let(assign, expr, program_state):
    state = {}
    frameStack.append(state)
    assign.simplify(program_state)
    variables = list(state.keys())
    expr.simplify(program_state)
    for var in variables:
        state.pop(var)
    frameStack[-2].update(state)
    frameStack.pop(-1)

def import_module(nameVar, program_state):
    name = nameVar.name
    file = open('Modules/' + name + '.txt', 'r')
    code = file.read()
    Module(name, code, program_state)
    #assign(nameVar, Module(name, code, program_state), program_state)
    return Int(0)

def from_import(moduleVar, stat, names):
    if isinstance(names, Tuple):
        names = list(map(str, names.tup))
    elif isinstance(names, Variable):
        names = [names.name]
    moduleName = moduleVar.name
    file = open('Modules/' + moduleName + '.txt', 'r')
    code = file.read()
    module = Module(moduleName, code)
    state = module.state
    module.state = module.state.copy()
    keys = list(state.keys())
    for name in keys:
        if name not in names:
            state.pop(name)
    assign(moduleVar, module)
    return Int(0)
    
def return_statement(value, program_state):
    program_state.return_value = value
    return value

def toInt(expr, program_state):
    if isinstance(expr, (Int, Float)):
        return Int(int(expr.value))
    if isinstance(expr, Cons):
        return toInt(getData(str(expr)))
    if isinstance(expr, Bool):
        if expr.value:
            return Int(1)
        return Int(0)
    if isinstance(expr, Char):
        return Int(ord(expr.value))
    return Int(0)

def toFloat(expr, program_state):
    if isinstance(expr, (Int, Float)):
        return Float(float(expr.value))
    if isinstance(expr, Cons):
        return toFloat(getData(str(expr)))
    if isinstance(expr, Bool):
        if expr.value:
            return Float(1.0)
        return Float(0.0)
    return Float(0)

def toBool(expr, program_state):
    if isinstance(expr, (Int, Float)):
        if expr.value > 0:
            return Bool(True)
        return Bool(False)
    if isinstance(expr, Nil):
        return Bool(False)
    if isinstance(expr, Cons):
        return Bool(True)
    return Bool(False)

def toChar(expr, program_state):
    if isinstance(expr, Int):
        return Char(chr(expr.value))
    return Char(chr(0))

def doLoop(expr, loop, cond, program_state):
    expr.simplify(program_state)
    if loop.name == 'while':
        return whileLoop(cond, expr)
    if loop.name == 'for':
        return forLoop(cond, expr)
        
def incrementBy(var, val, program_state): 
    value = var.simplify(program_state)
    assign(var, add(val.simplify(program_state), value, program_state),
           program_state)
    return value

def decrementBy(var, val, program_state):
    value = var.simplify(program_state)
    assign(var, subtract(val.simplify(program_state), value, program_state),
           program_state)
    return value

def multiplyBy(var, val, program_state):
    value = var.simplify(program_state)
    assign(var, multiply(val.simplify(program_state), value, program_state),
           program_state)
    return value

def divideBy(var, val, program_state):
    value = var.simplify(program_state)
    assign(var, divide(val.simplify(program_state), value, program_state),
           program_state)
    return value

def raiseTo(var, val, program_state):
    value = var.simplify(program_state)
    assign(var, power(val.simplify(program_state), value, program_state), 
           program_state)
    return value

def defaultInt(var, program_state):
    if isinstance(var.simplify(program_state), Tuple):
        for name in var.simplify(program_state).items:
            defaultInt(name, program_state)
    else:
        program_state.frameStack[-1][var.name] = Int(0)
    return var

def defaultFloat(var, program_state):
    if isinstance(var, Tuple):
        for name in var.simplify().tup:
            defaultFloat(name)
    else:
        program_state.frameStack[-1][var.name] = Float(0)
    return var

def defaultBool(var, program_state):
    if isinstance(var, Tuple):
        for name in var.simplify().tup:
            defaultBool(name)
    else:
        program_state.frameStack[-1][var.name] = Bool(False)
    return var

def defaultChar(var, program_state):
    if isinstance(var, Tuple):
        for name in var.simplify().tup:
            defaultChar(name)
    else:
        program_state.frameStack[-1][var.name] = toChar(Int(97))
    return var
    
def defaultList(var):
    frameStack[-1][var.name] = Nil()
    return Nil()

def type_synonym(typeVar, typeExpr, program_state):
    from Types import Type
    type_ = Type(typeVar.name, typeExpr)
    assign(typeVar, type_, program_state) 
    return type_

def types_union(var, types, program_state):
    from Types import Union
    union = Union(var.name, types)
    assign(var, union, program_state)
    return union

def then_clause(cond, expr): 
    if cond.simplify().value:
        return expr.simplify()
    return Int(None)

def else_clause(if_stat, expr, program_state):
    if if_stat.leftExpr.rightExpr.simplify(program_state).value:
        return if_stat.simplify(program_state)
    return expr.simplify(program_state)

def read_as(var, struct):
    return Alias(var, struct)

def create_iterator(var, xs):
    return Iterator(var, xs)

def make_public(var):
    frameStack[-1]['this'].public.append(var.name)
    return var

def make_private(var):
    frameStack[-1]['this'].private.append(var.name)
    return var

def make_hidden(var):
    frameStack[-1]['this'].hidden.append(var.name)
    return var

def pass_arg(arg, funcs):
    if isinstance(funcs.simplify(), Tuple):
        items = []
        for func in funcs.simplify().tup:
            items.append(pass_arg(arg, func))
        return Tuple(items)
    if not isinstance(arg, Variable):
        arg = arg.simplify()
    return application(funcs.simplify(), arg)

def match(a, b, program_state):
    from utils import patternMatch
    return Bool(patternMatch(a, b, program_state))   

def append(a, b):
    if isinstance(a.simplify(), Object):
        a.simplify().state['append'].apply(b)
        return a.simplify()
    if isinstance(a, (Tuple, Array)):
        a.items.append(b)
    return a

def python_eval(code, program_state):
    return getData(str(eval(code.value)))