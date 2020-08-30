# -*- coding: utf-8 -*-
"""
Created on Sat Jun 27 16:19:04 2020

@author: rohan
"""
import utils
from utils import frameStack, functionNames, getData, enumNames, isPrimitive
from utils import typeNames, structNames, patternMatch
from HFunction import HFunction, Composition, Function, Lambda, Func
from List import List, Nil, Cons, Iterator, head, tail, Array
from Tuple import Tuple
from Types import (Int, Float, Bool, Variable, Alias, Enum, EnumValue, Struct,
                   Class, Interface, Char, Module, Object, String)
from Expression import BinaryExpr
from math import *

def assign(a, b, state = None):
    var, value = a, b
    if isPrimitive(var) or isinstance(var, Nil):
        return 
 
    if isinstance(var, Variable):
        if var.name == '_ ...': return
        
        value = b.simplify()
        if utils.functional_mode:
            if var.name in state.keys():
                raise Exception('Cannot assign variable',
                                var.name, 'in FUNCTIONAL-MODE.')
        if utils.static_mode:
            if var.name in state.keys():
                varType = type(state[var.name])
                valType = type(value)
                if varType != valType:
                    raise Exception('Cannot assign variable', var.name,
                                    'of type',
                                    str(varType), 'with value of type',
                                    str(valType),
                                    'in STATIC-MODE.') 
        if state == None:
            for curr in frameStack[::-1]: 
                if var.name in curr.keys():
                    curr[var.name] = value 
                    return
            state = frameStack[-1]
        state[var.name] = value
        return value
    
    if state == None:
        state = frameStack[-1]
        
    if isinstance(var, (Tuple, Array)):
        value = value.simplify()
        for i in range(len(var.items)): 
            assign(var.items[i], value.items[i], state) 
        return value

    elif isinstance(var, Cons):
        assign(head(var), head(value), state)
        assign(tail(var), tail(value), state)
        return value
        
    elif isinstance(var, BinaryExpr):
        if var.operator.name == '@':
            assign(var.leftExpr, value, state)
            assign(var.rightExpr, value, state)
            
        if var.operator.name == '!!':
            array = var.leftExpr.simplify()
            value = value.simplify()
            array.items[head(var.rightExpr).simplify().value] = value 

        if var.operator.name == ':':
            value = value.simplify()
            assign(var.leftExpr, head(value), state) 
            assign(var.rightExpr, tail(value), state)
            return Int(0)
        
        elif var.operator.name == '.':
            obj = var.leftExpr.simplify()
            obj.state[var.rightExpr.name] = value.simplify()
            
        elif var.operator.name == ' ':
            arguments = []
            args = var 
            while True:
                arg = args.rightExpr 
                arguments.insert(0, arg)
                args = args.leftExpr
                if (isinstance(args, (Variable, Nil, Cons, Tuple, Array, Class)) or 
                    utils.null(args)):
                    arguments.insert(0, args)
                    break
                
            if (isinstance(arguments[0], Variable) 
                and arguments[0].name in structNames):
                if isinstance(arguments[1], Tuple):
                    assign(arguments[1], Tuple(value.values), state) 
                else:
                    assign(arguments[1], value, state)
                return value
            
            if (utils.null(arguments[0].simplify()) or 
                isinstance(arguments[0], (Nil, Cons, Tuple, Array)) or 
                arguments[0].name in typeNames):
                assign(arguments[1], value, state)
                return value
            
            elif arguments[0].name in 'def':
                name = arguments[1].name
                
                arguments = arguments[2:]
                
                for i in range(len(arguments)):
                    if not (isinstance(arguments[i], BinaryExpr) and 
                            arguments[i].operator.name in ' :'):
                        arguments[i] = arguments[i].simplify()
                
                case = Lambda(name, arguments = arguments, expr = value)
                if name != None:
                    if utils.in_class:
                        if name in state.keys():
                            func = state[name]
                            func.cases.append(case)
                            return case 
                        else:
                            func = Function(name, [case])
                            state[name] = func
                            functionNames.append(name) 
                    else:
                        for state in frameStack[::-1]:
                            if name in state.keys():
                                func = state[name]
                                func.cases.append(case)
                                return case 
                        func = Function(name, [case])
                        state[name] = func
                        functionNames.append(name) 
                return case

    return value
    
def application(a, b):
    func, arg = (a, b)
    if not (issubclass(type(func), Func) 
        and func.name.split(' ')[0] in utils.lazy_eval):
        arg = arg.simplify()
    return func.apply(arg)

def compose(a, b):
    (second, first) = (a, b)
    return Composition(second, first)

def index(a, b):
    from List import head, tail
    if isinstance(b, Int):
        n = b.value
        if n < 0 or isinstance(a, Nil):
            return None
        if utils.isList(a):
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

def power(a, b):
    if isinstance(a, Object):
        if 'pow' in a.state.keys():
            return a.state['pow'].apply(b) 
        
    (a, b) = (a.value, b.value)
    return getData(a ** b)

def divide(a, b):
    if isinstance(a, Object):
        if 'div' in a.state.keys():
            return a.state['div'].apply(b)
        
    (a, b) = (a.value, b.value)
    return getData(a / b)

def multiply(a, b):
    if isinstance(a, Object):
        if 'mul' in a.state.keys():
            return a.state['mul'].apply(b) 
    elif isinstance(b, Object):
        if 'mul' in b.state.keys():
            return b.state['mul'].apply(a)
        
    (a, b) = (a.value, b.value)
    return getData(a * b)

def add(a, b):
    if isinstance(a, Object):
        if 'add' in a.state.keys():
            return a.state['add'].apply(b) 
    elif isinstance(b, Object):
        if 'add' in b.state.keys():
            return b.state['add'].apply(a)
        
    (a, b) = (a.value, b.value)
    return getData(a + b)

def subtract(a, b):
    if isinstance(a, Object):
        if 'sub' in a.state.keys():
            return a.state['sub'].apply(b)
        
    (a, b) = (a.value, b.value)
    return getData(a - b)

def lessThan(a, b):
    if isinstance(a, Object):
        if 'lessThan' in a.state.keys():
            return a.state['lessThan'].apply(b)
        return Bool(False)
    
    return Bool(a.value < b.value)

def lessThanOrEqual(a, b):
    return Bool(lessThan(a, b).value or equals(a, b).value)

def greaterThan(a, b):
    return Bool(not lessThanOrEqual(a, b).value)

def greaterThanOrEqual(a, b):
    return Bool(greaterThan(a, b).value or equals(a, b).value)

def rem(a, b):
    return Int(a.value % b.value)

def quot(a, b):
    return Int(a.value // b.value)

def equals(a, b):
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
    if isinstance(a, Tuple) and isinstance(b, Tuple):
        if (len(a.tup) != len(b.tup)):
            return Bool(False)
        for i in range(len(a.tup)):
            if not equals(a.tup[0], b.tup[0]):
                return Bool(False)
        return Bool(True)
    if isPrimitive(a) and isPrimitive(b):
        return Bool(a.value == b.value)
    
    if isinstance(a, Object) and isinstance(b, Object):
        if 'equals' in a.state.keys():
            return a.state['equals'].apply(b)
        return Bool(a == b)
    
    return Bool(False)

def notEqual(a, b):
    return Bool(not equals(a, b).value)

def AND(a, b):
    if not a.simplify().value: 
        return Bool(False)
    return b.simplify()

def OR(a, b):
    if a.simplify().value: 
        return Bool(True)
    return b.simplify()

def comma(a, b):
    if isinstance(a, Tuple):
        return Tuple(a.tup.append(b))
    return Tuple([a, b])
    
def cons(a, b):
    from utils import replaceVariables
    x, xs = a, b
    return Cons(replaceVariables(x), xs.simplify())    

def concatenate(a, b): 
    from List import head, tail
    left, right = a, b
    if isinstance(left, String):
        return String(left.value + right.value)
    if isinstance(left, Nil):
        return right
    elif isinstance(right, Nil):
        return left
    x, xs = head(left), tail(left)
    return Cons(x, concatenate(xs, right))
 
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

def sequence(a, b):
    import utils
    if not (utils.breakLoop > 0 or utils.continueLoop > 0):
        a.simplify()
        if utils.return_value != None:
            return utils.return_value
        if not (utils.breakLoop > 0 or utils.continueLoop > 0):
            return b.simplify()
    return Int(None)
    
def chain(a, b):
    return b.apply(a.simplify())

def createLambda(args, expr):
    from utils import replaceVariables
    arguments = []
    while True:
        if isinstance(args, (Variable, HFunction)):
            name = args.name
            break
        arguments.insert(0, args.rightExpr)
        args = args.leftExpr
    case = Lambda(name, arguments = arguments, expr = replaceVariables(expr))
    return case

def createEnum(name, values):
    state = frameStack[-1]
    values = values.tup
    names = list(map(str, values))
    name = name.name
    typeNames.append(name)
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
    typeNames.append(name)
    structNames.append(name)
    struct = Struct(name, fields)
    state[name] = struct
    functionNames.append(name)
    return struct

def createOperator(symbol, precedence, associativity, func):
    from utils import operators
    from Operators import operatorsDict, Op, Associativity
    associativityMap = {'left' : Associativity.LEFT,
                        'right' : Associativity.LEFT,
                        'none' : Associativity.NONE}
    precedence = precedence.value
    associativity = associativityMap[associativity.name]
    symbol = str(symbol)[1:-1]
    operators.append(symbol) 
    func = func.simplify().apply(None, None)
    func.name = symbol
    func.precedence = precedence
    func.associativity = associativity
    if func.noOfArgs == 1:
        func.precedence = 10
    operatorsDict[symbol] = Op(func)
    return func

def createClass(nameVar):
    name = nameVar.name
    cls = Class(name)
    assign(nameVar, cls)
    return cls

def createInterface(name, declarationsExpr):
    state = frameStack[-1]
    name = name.name
    typeNames.append(name)
    interface = Interface(name, declarationsExpr)
    state[name] = interface
    functionNames.append(name)
    return interface
        
def where(expr1, expr2):
    frameStack.append({})
    expr2.simplify()
    value = expr1.simplify()
    frameStack.pop(-1)
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

def access(a, b):
    obj, field = a.simplify(), b
    try:
        return obj.state[field.name].simplify()
    except:
        print(0)

def forLoop(n, expr):
    import utils
    from List import List
    if isinstance(n, Tuple):
        generators = n.tup       
        frameStack.append({})
        curr = generators[0].simplify() 
        var, collection = curr.var, curr.collection.simplify()
        while not isinstance(collection, Nil):
            assign(var, head(collection))
            if len(generators) == 1:
                expr.simplify()
            else:
                forLoop(Tuple(generators[1:]), expr)
            if utils.breakLoop > 0 or utils.return_value != None:
                utils.breakLoop -= 1
                break
            if utils.continueLoop > 0:
                utils.continueLoop -= 1
            collection = tail(collection)
        frameStack.pop(-1)
        
    elif isinstance(n, BinaryExpr):
        if n.operator.name == ';':
            init, n = n.leftExpr, n.rightExpr
            cond, after = n.leftExpr, n.rightExpr
            state = {}
            frameStack.append(state)
            init.simplify()
            while cond.simplify().value:
                expr.simplify()
                import utils
                if utils.continueLoop > 0:
                    utils.continueLoop -= 1
                if utils.breakLoop > 0 or utils.return_value != None:
                    utils.breakLoop -= 1
                    break
                after.simplify()
            frameStack.pop(-1)
            
        elif n.operator.name == 'in':
            n = n.simplify()
            frameStack.append({})
            var, collection = n.var, n.collection.simplify()
            if issubclass(type(collection), List):
                while not isinstance(collection, Nil):
                    assign(var, head(collection)) 
                    expr.simplify()
                    if utils.breakLoop > 0 or utils.return_value != None:
                        utils.breakLoop -= 1
                        break
                    if utils.continueLoop > 0:
                        utils.continueLoop -= 1
                    collection = tail(collection)
                    
            elif isinstance(collection, (Tuple, Array)):
                for item in collection.items:
                    assign(var, item) 
                    expr.simplify()
                    if utils.breakLoop > 0 or utils.return_value != None:
                        utils.breakLoop -= 1
                        break
                    if utils.continueLoop > 0:
                        utils.continueLoop -= 1
            frameStack.pop(-1)
            
        else:
            n = n.simplify()
            for i in range(n.value):
                expr.simplify()
                if utils.continueLoop > 0:
                    utils.continueLoop -= 1
                if utils.breakLoop > 0:
                    utils.breakLoop -= 1
                    break
                
    else:
        n = n.simplify()
        for i in range(n.value):
            expr.simplify()
            if utils.continueLoop > 0:
                utils.continueLoop -= 1
            if utils.breakLoop > 0:
                utils.breakLoop -= 1

    return Int(0)

def whileLoop(cond, expr):
    while cond.simplify().value:
        expr.simplify()
        import utils
        if utils.continueLoop > 0:
            utils.continueLoop -= 1
        if utils.breakLoop > 0 or utils.return_value != None:
            utils.breakLoop -= 1
            break
    return Int(0)

def breakCurrentLoop():
    import utils
    utils.breakLoop = 1
    return Int(0)

def continue_loop():
    import utils
    utils.continueLoop = 1
    return Int(0)

def breakout(n):
    import utils
    utils.breakLoop += n.value
    return Int(0)

def skipout(n):
    import utils
    utils.continueLoop += n.value
    return Int(0)
    
def ifStatement(cond, expr):
    if cond.simplify().value:
        return expr.simplify()
    return Int(None)

def extends(subclass, superclass):
     subclass.state['super'] = superclass
     for name in superclass.state.keys():
         subclass.state[name] = superclass.state[name]
     return subclass

def implements(class_, interface):
    class_.interfaces.append(interface)
    return class_

def definition(name_var, args_tup, expr):
    name = name_var.name
    state = frameStack[-1]
    case = Lambda(name, arguments = [args_tup], expr = expr)
    if name != None:
        if name in state.keys():
            func = state[name]
            func.cases.append(case)
        else:
            func = Function(name, 1, [case])
            state[name] = func
            functionNames.append(name) 
    return case
        
def switch(value, expr):
    cases = []
    while True:
        if not (isinstance(expr, BinaryExpr) and expr.operator.name == ';'):
            cases.append(expr)
            break
        cases.append(expr.leftExpr)
        expr = expr.rightExpr
    followThrough = False
    for case in cases:
        if (isinstance(case.leftExpr, Variable) 
            and case.leftExpr.name == 'otherwise' 
            or patternMatch(case.leftExpr.simplify(), value.simplify())
            or followThrough):
            
            value = case.rightExpr.simplify()
            followThrough = True
            if case.operator.name == '=>':
                return value
    return Int(None)

def let(assign, expr):
    state = {}
    frameStack.append(state)
    assign.simplify()
    variables = list(state.keys())
    expr.simplify()
    for var in variables:
        state.pop(var)
    frameStack[-2].update(state)
    frameStack.pop(-1)

def import_module(nameVar):
    name = nameVar.name
    file = open('Modules/' + name + '.txt', 'r')
    code = file.read()
    assign(nameVar, Module(name, code))
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
    
def return_statement(value):
    import utils
    utils.return_value = value
    return value

def toInt(expr):
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

def toFloat(expr):
    if isinstance(expr, (Int, Float)):
        return Float(float(expr.value))
    if isinstance(expr, Cons):
        return toFloat(getData(str(expr)))
    if isinstance(expr, Bool):
        if expr.value:
            return Float(1.0)
        return Float(0.0)
    return Float(0)

def toBool(expr):
    if isinstance(expr, (Int, Float)):
        if expr.value > 0:
            return Bool(True)
        return Bool(False)
    if isinstance(expr, Nil):
        return Bool(False)
    if isinstance(expr, Cons):
        return Bool(True)
    return Bool(False)

def toChar(expr):
    if isinstance(expr, Int):
        return Char(chr(expr.value))
    return Char(chr(0))

def doLoop(expr, loop, cond):
    expr.simplify()
    if loop.name == 'while':
        return whileLoop(cond, expr)
    if loop.name == 'for':
        return forLoop(cond, expr)
        
def incrementBy(var, val): 
    value = var.simplify()
    assign(var, add(value, val.simplify()))
    return value

def decrementBy(var, val):
    value = var.simplify()
    assign(var, subtract(var.simplify(), val.simplify()))
    return value

def multiplyBy(var, val):
    value = var.simplify()
    assign(var, multiply(var.simplify(), val.simplify()))
    return value

def divideBy(var, val):
    value = var.simplify()
    assign(var, divide(var.simplify(), val.simplify()))
    return value

def raiseTo(var, val):
    value = var.simplify()
    assign(var, power(var.simplify(), val.simplify()))
    return value

def defaultInt(var):
    if isinstance(var.simplify(), Tuple):
        for name in var.simplify().tup:
            defaultInt(name)
    else:
        frameStack[-1][var.name] = Int(0)
    return var

def defaultFloat(var):
    if isinstance(var, Tuple):
        for name in var.simplify().tup:
            defaultFloat(name)
    else:
        frameStack[-1][var.name] = Float(0)
    return var

def defaultBool(var):
    if isinstance(var, Tuple):
        for name in var.simplify().tup:
            defaultBool(name)
    else:
        frameStack[-1][var.name] = Bool(False)
    return var

def defaultChar(var):
    if isinstance(var, Tuple):
        for name in var.simplify().tup:
            defaultChar(name)
    else:
        frameStack[-1][var.name] = toChar(Int(97))
    return var
    
def defaultList(var):
    frameStack[-1][var.name] = Nil()
    return Nil()

def type_synonym(typeVar, typeExpr):
    from Types import Type
    type_ = Type(typeVar.name, typeExpr)
    assign(typeVar, type_) 
    typeNames.append(typeVar.name)
    return type_

def types_union(typeVar, types):
    from Types import Union
    union = Union(types)
    assign(typeVar, union)
    typeNames.append(typeVar.name)
    return union

def then_clause(cond, expr): 
    if cond.simplify().value:
        return expr.simplify()
    return Int(None)

def else_clause(if_stat, expr):
    if if_stat.leftExpr.rightExpr.simplify().value:
        return if_stat.simplify()
    return expr.simplify()

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

def match(a, b):
    from utils import patternMatch
    return Bool(patternMatch(a, b))   

def append(a, b):
    if isinstance(a.simplify(), Object):
        a.simplify().state['append'].apply(b)
        return a.simplify()
    if isinstance(a, (Tuple, Array)):
        a.items.append(b)
    return a

def python_eval(code):
    return getData(str(eval(code.value)))