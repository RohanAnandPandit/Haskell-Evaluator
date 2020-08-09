# -*- coding: utf-8 -*-
"""
Created on Sat Jun 27 16:19:04 2020

@author: rohan
"""
import utils
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
        value = b.simplify()
        if utils.functional_mode:
            if var.name in state.keys():
                raise Exception('Cannot assign variable', var.name, 'in FUNCTIONAL-MODE.')
        if utils.static_mode:
            if var.name in state.keys():
                varType = type(state[var.name])
                valType = type(value)
                if varType != valType:
                    raise Exception('Cannot assign variable', var.name, 'of type',
                                    str(varType), 'with value of type',  str(valType),
                                    'in STATIC-MODE.')

        state[var.name] = value
    elif isinstance(var, Alias):
        assign(var.var, value, state)
        assign(var.expr, value, state)
    elif isinstance(var, Tuple):
        varTup = var.tup
        valTup =  value.simplify().tup
        for i in range(len(varTup)): 
            assign(varTup[i], valTup[i], state)
        return value
    elif isinstance(var, Cons) and isinstance(value, Cons):
        assign(head(var), head(value), state)
        assign(tail(var), tail(value), state)
        return value
    elif isinstance(var, BinaryExpr):
        if var.operator.name == ' ':
            arguments = []
            args = var 
            while True:
                arg = args.rightExpr
                if not isinstance(arg, BinaryExpr) or arg.operator.name != ' ':
                    arg = arg.simplify(False)
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
                if isinstance(arguments[1], Tuple):
                    assign(arguments[1], Tuple(value.values), state)
                else:
                    assign(arguments[1], value, state)
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
    a.simplify()
    import utils
    if utils.return_value != None:
        return utils.return_value
    if not (utils.breakLoop or utils.continueLoop):
        return b.simplify()
    return Int(None)
    
def chain(a, b):
    return b.apply(a.simplify())

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
    typeNames.append(name)
    structNames.append(name)
    struct = Struct(name, fields)
    state[name] = struct
    functionNames.append(name)
    return struct

def createOperator(symbol, precedence, associativity, func):
    from utils import operators
    from Operators import operatorsDict, Op, Associativity
    associativityMap = {'left' : Associativity.LEFT, 'right' : Associativity.LEFT,
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

def createClass(name, methodsExpr):
    state = frameStack[-1]
    name = name.name
    typeNames.append(name)
    cls = Class(name, methodsExpr)
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
    obj, field = a, b       
    return obj.state[field.name].simplify()

def forLoop(n, expr):
    import utils
    if isinstance(n, Iterator):
        frameStack.append({})
        var, collection = n.var, n.collection.simplify()
        while not isinstance(collection, Nil):
            assign(var, head(collection))
            expr.simplify()
            if utils.breakLoop or utils.return_value != None:
                utils.breakLoop = False
                break
            if utils.continueLoop:
                utils.continueLoop = False
            collection = tail(collection)
        from utils import unassignVariables
        unassignVariables(n.var)
        frameStack[-2].update(frameStack[-1])
        frameStack.pop(-1)
    elif isinstance(n, BinaryExpr):
        if n.operator.name != ';':
            n = n.simplify()
            for i in range(n.value):
                expr.simplify()
                if utils.continueLoop:
                    utils.continueLoop = False
                if utils.breakLoop:
                    utils.breakLoop = False
                    break
        else:
            init, n = n.leftExpr, n.rightExpr
            cond, after = n.leftExpr, n.rightExpr
            state = {}
            frameStack.append(state)
            init.simplify()
            variables = list(state.keys())
            while cond.simplify().value:
                expr.simplify()
                import utils
                if utils.continueLoop:
                    utils.continueLoop = False
                if utils.breakLoop or utils.return_value != None:
                    utils.breakLoop = False
                    break
                after.simplify()
            from utils import unassignVariables
            for var in variables:
                frameStack[-1].pop(var)
            frameStack[-2].update(frameStack[-1])
            frameStack.pop(-1)
    else:
        n = n.simplify()
        for i in range(n.value):
            expr.simplify()
            if utils.continueLoop:
                utils.continueLoop = False
            if utils.breakLoop:
                utils.breakLoop = False
    return Int(0)

def whileLoop(cond, expr):
    while cond.simplify().value:
        expr.simplify()
        import utils
        if utils.continueLoop:
            utils.continueLoop = False
        if utils.breakLoop or utils.return_value != None:
            utils.breakLoop = False
            break
    return Int(0)

def breakCurrentLoop():
    import utils
    utils.breakLoop = True
    return Int(0)

def continueCurrentLoop():
    import utils
    utils.continueLoop = True
    return Int(0)
    
def ifStatement(cond, expr):
    if cond.simplify().value:
        return expr.simplify()
    return Int(None)

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

def definition(name_var, args_tup, expr):
    name = name_var.name
    state = frameStack[-1]
    state[name] = func = Lambda(name, arguments = [args_tup], expr = expr)
    return func


def switch(value, expr):
    cases = []
    while True:
        if not ((isinstance(expr, BinaryExpr) and expr.operator.name == ';')):
            cases.append(expr)
            break
        cases.insert(0, expr.leftExpr)
        expr = expr.rightExpr
    for case in cases:
        if (isinstance(case.cond, Variable) and case.cond.name == 'default' 
            or equals(value.simplify(), case.cond.simplify()).value):
            return case.ret.simplify()
    return Int(None)
        
def cascade(value, expr):
    cases = []
    while True:
        if not (isinstance(expr, BinaryExpr) and expr.operator.name == ';'):
            cases.append(expr)
            break
        cases.append(expr.leftExpr)
        expr = expr.rightExpr
    followThrough = False
    for case in cases:
        if (isinstance(case.cond, Variable) and case.cond.name == 'default' 
            or equals(value.simplify(), case.cond.simplify()).value
            or followThrough):
            case.ret.simplify()
            followThrough = True
            import utils
            if utils.breakLoop:
                utils.breakLoop = False 
                break
    return Int(0)

def evaluate_in_scope(assign, expr):
    state = {}
    frameStack.append(state)
    assign.simplify()
    variables = list(state.keys())
    expr.simplify()
    for var in variables:
        state.pop(var)
    frameStack[-2].update(state)
    frameStack.pop(-1)

def import_module(name):
    name = name.name
    file = open('Modules/' + name + '.txt', 'r')
    code = file.read()
    from utils import evaluate
    evaluate(code)
    return Int(0)
    
def return_statement(value):
    import utils
    utils.return_value = value
    return value