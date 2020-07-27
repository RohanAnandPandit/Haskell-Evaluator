# -*- coding: utf-8 -*-
"""
Created on Sat Jun 27 16:19:04 2020

@author: rohan
"""
from utils import frameStack, builtInState, functionNames, getData, enumNames, isPrimitive, typeNames, structNames
from HFunction import HFunction, Composition, Function, Lambda
from List import List, Nil, Cons, Iterator, head, tail
from Tuple import Tuple, fst, snd
from Types import Int, Float, Bool, Variable, Alias, Enum, EnumValue, Struct, Class, Interface
from Expression import BinaryExpr

def assign(a, b, state = None):
    if (state == None):
        state = frameStack[-1]
    var, value = a, b

    if isPrimitive(var) or isinstance(var, Nil):
        return 
    elif isinstance(var, Variable):
        state[var.name] = b.simplify()
    elif isinstance(var, Alias):
        assign(var.var, value, state)
        assign(var.expr, value, state)
    elif isinstance(var, Tuple):
        varTup = var.tup
        valTup =  value.tup
        for i in range(len(varTup)): 
            assign(varTup[i], valTup[i], state)
        return value
    elif isinstance(var, Cons) and isinstance(value, Cons):
        assign(head(var), head(value), state)
        assign(tail(var), tail(value))
        return value
    elif isinstance(var, BinaryExpr):
        if var.operator.name == ' ':
            arguments = []
            args = var 
            while True:
                arg = args.rightExpr
                arguments.insert(0, arg)
                args = args.leftExpr
                if isinstance(args, Variable):
                    arguments.insert(0, args)
                    break
            if arguments[0].name == 'def':
                name = arguments[1].name
                arguments = arguments[2:]
                case = Lambda(name, arguments = arguments, expr = value)
                if name != None:
                    if name in state.keys():
                        func = state[name]
                        func.cases.append(case)
                    else:
                        func = Function(name, len(arguments), [case])
                        state[name] = func
                        functionNames.append(name) 
                return case
            elif arguments[0].name in typeNames:
                assign(arguments[1], value, state)
                return value 
            elif arguments[0].name in structNames:
                assign(arguments[1], Tuple(value.values), state)
                return value
        elif var.operator.name == '.':
            obj = var.leftExpr.simplify()
            obj.state[var.rightExpr.name] = value.simplify()
    return value
    
def space(a, b):
    func, arg = (a, b)
    if isinstance(func, Variable):
        func = func.simplify()
    return func.apply(arg)

def compose(a, b):
    (second, first) = (a, b)
    return Composition(second, first)

def index(a, b):
    from List import head, tail
    n = b.value
    if n < 0 or isinstance(a, Nil):
        return None
    if isinstance(a, Cons):
        x, xs = head(a), tail(a) 
        if n == 0:
            return x
        return getData(index(xs, Int(n - 1)))
    elif isinstance(a, Enum):
        return builtInState[a.values[n]].simplify()
    elif isinstance(a, Tuple):
        return a.tup[n]

def power(a, b):
    (a, b) = (a.value, b.value)
    return getData(a ** b)

def divide(a, b):
    (a, b) = (a.value, b.value)
    return getData(a / b)

def multiply(a, b):
    (a, b) = (a.value, b.value)
    return getData(a * b)

def add(a, b):
    (a, b) = (a.value, b.value)
    return getData(a + b)

def subtract(a, b):
    (a, b) = (a.value, b.value)
    return getData(a - b)
   
def lessThan(a, b):
    (a, b) = (a.value, b.value)
    return Bool(a < b)

def lessThanOrEqual(a, b):
    (a, b) = (a.value, b.value)
    return Bool(a <= b)

def greaterThan(a, b):
    (a, b) = (a.value, b.value)
    return Bool(a > b)

def greaterThanOrEqual(a, b):
    a, b = a.value, b.value
    return Bool(a >= b)

def equals(a, b):
    a,b = a.simplify(), b.simplify()
    if a == None or b == None:
        return Bool(False)
    if isinstance(a, (Variable, BinaryExpr)) or isinstance(b, (Variable, BinaryExpr)):
        return Bool(False)
    if issubclass(type(a), List) and issubclass(type(b), List):
        if isinstance(a, Nil) and isinstance(b, Nil):
            return Bool(True)
        if isinstance(a, Cons) and isinstance(b, Cons):
            x, xs = head(a), tail(a)
            y, ys = head(b), tail(b)
            return equals(x, y) and equals(xs, ys)
        return Bool(False)
    if isinstance(a, Tuple) and isinstance(b, Tuple):
        if (len(a.tup) != len(b.tup)):
            return Bool(False)
        for i in range(len(a.tup)):
            if not equals(a.tup[0], b.tup[0]):
                return Bool(False)
        return Bool(True)
    if isPrimitive(a) and isPrimitive(b):
        return Bool(a.value == b.value)
    return Bool(False)

def notEqual(a, b):
    return Bool(not equals(a, b).value)

def AND(a, b):
    a, b = a.value, b.value
    return Bool(a and b)

def OR(a, b):
    a, b = a.value, b.value
    return Bool(a or b)

def comma(a, b): 
    return Tuple([a, b])
    
def cons(a, b):
    x, xs = a, b
    x = x.simplify()
    return Cons(x, xs, type(a))    

def concatenate(a, b): 
    from List import head, tail
    (left, right) = (a, b)
    if isinstance(left, Nil):
        return right
    elif isinstance(right, Nil):
        return left
    x, xs = head(left), tail(left)
    return Cons(x, concatenate(xs, right))
 
def comprehension(a, b):    
    if type(a) in [Int, Float, Tuple]:
        step = 1
        if isinstance(a, Tuple):
            a.tup = a.tup[1 : ]
            if len(a.tup) == 1:
                start = fst(a)
            else:
                first, second = fst(a), snd(a)
                start = first
                step = second - first
        else:            
            start = a
        end = b
        func_succ = builtInState['succ']
        hfunc = func_succ.clone()
        hfunc.func = lambda x: x + step
        iterations = None
        if (end != None):
            iterations =  int(abs((end - start) / step))
        iterator = Iterator(func = hfunc, item = start, iterations = iterations, 
                        iteratorType = 'comprehension', step = step, end = end)
        return Cons(iterator, Nil()) 
 
    elif type(a) == Bool:
        pass

def sequence(a, b): 
    return Int(0)
    
def chain(a, b):
    return b.apply(a.simplify())

def collect(*args):
    return args

def createLambda(args, expr):
    arguments = []
    while True:
        if isinstance(args, (Variable, HFunction)):
            name = args.name
            break
        arguments.insert(0, args.rightExpr.simplify(False))
        args = args.leftExpr
    case = Lambda(name, arguments = arguments, expr = expr)
    return case

def createEnum(name, values):
    state = frameStack[-1]
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
 
def createStruct(name, fields):
    state = frameStack[-1]
    fields = list(map(lambda var: var.name, fields.tup))
    name = name.name
    structNames.append(name)
    struct = Struct(name, fields)
    state[name] = struct
    functionNames.append(name)
    return struct

def createOperator(symbol, tup):
    from utils import operators
    from Operators import operatorsDict, Op, Associativity
    associativityMap = {'left' : Associativity.LEFT, 'right' : Associativity.LEFT,
                'none' : Associativity.NONE}
    expr = tup.tup[0]
    precedence = tup.tup[1].value
    associativity = associativityMap[tup.tup[2].name]
    symbol = str(symbol)[1:-1]
    operators.append(symbol) 
    func = expr.simplify().apply(None, None)
    func.name = symbol
    func.precedence = precedence
    func.associativity = associativity
    if func.noOfArgs == 1:
        func.precedence = 10
    operatorsDict[symbol] = Op(func)
    return func

def createClass(name, fields, methodsExpr):
    state = frameStack[-1]
    name = name.name
    typeNames.append(name)
    fields = list(map(str, fields.tup))
    cls = Class(name, fields, methodsExpr)
    state[name] = cls
    functionNames.append(name)
    return cls

def createInterface(name, declarationsExpr):
    state = frameStack[-1]
    name = name.name
    typeNames.append(name)
    interface = Interface(name, declarationsExpr)
    state[name] = interface
    functionNames.append(name)
    return interface
        
def where(func, exp):
    func.whereClause = exp
    return func

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

def access(obj, field):       
    return obj.state[field.name].simplify()

def forLoop(n, expr):
    for i in range(n.simplify().value):
        expr.simplify()
    return Int(0)

def whileLoop(cond, expr):
    while cond.simplify().value:
        expr.simplify()
    return Int(0)

def inherits(subclass, superclass):
     subclass.state['super'] = superclass
     for name in superclass.state.keys():
         if name not in subclass.state.keys():
             subclass.state[name] = superclass.state[name]
     return subclass

def checkImplements(subclass, interface):
    for methodName in interface.methods:
        if methodName not in subclass.state.keys():
            print("Missing definition for " + methodName)
    return subclass

def definition(name):
    name = name.name
    state = frameStack[-1]
    state[name] = None

def switch(value, expr):
    from Types import Conditional
    cases = []
    while True:
        if not isinstance(expr, BinaryExpr):
            cases.insert(0, expr)
            break
        cases.insert(0, expr.rightExpr)
        expr = expr.leftExpr
    for i in range(len(cases)):
        case = cases[i]
        if i == len(cases) - 1 or equals(value.simplify(), case.cond.simplify()).value:
            case.ret.simplify()
            break
    return Int(0)
        
        