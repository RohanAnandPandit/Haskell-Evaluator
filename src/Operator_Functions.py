# -*- coding: utf-8 -*-
"""
Created on Sat Jun 27 16:19:04 2020

@author: rohan
"""
from utils import is_primitive
from utils import pattern_match
from HFunction import Composition, Function, Lambda, Func
from List import Nil, Cons, Iterator, head, tail, Array
from Tuple import Tuple
from Types import (Int, Float, Bool, Variable, Alias, Char, Module, String, Null,
                   Collection)
from Class import Class, Object, Interface
from Struct import Struct
from Enum import EnumValue, Enum
from Expression import BinaryExpr
from Modules import *
from math import *


def assign(a, b, program_state, state=None):
    var, value = a, b

    if is_primitive(var) or isinstance(var, Nil):
        return

    if isinstance(var, Variable):
        if var.name == '_ ...':
            return var

        value = b.simplify(program_state)

        if state is None:
            for curr in program_state.frame_stack[::-1]:
                if var.name in list(curr.keys()):
                    curr[var.name] = value
                    return value

            state = program_state.frame_stack[-1]

        state[var.name] = value
        return value

    if state is None:
        state = program_state.frame_stack[-1]

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
            assign(var.left_expr, value, program_state, state)
            assign(var.right_expr, value, program_state, state)

        # Modifying
        elif var.operator.name == '!!':
            array = var.left_expr.simplify(program_state)
            value = value.simplify(program_state)
            i = head(var.right_expr, program_state).simplify(program_state).value

            array.items[i] = value

        # Assigning to a list
        elif var.operator.name == ':':
            value = value.simplify(program_state)

            assign(var.left_expr, head(value, program_state),
                   program_state, state)
            assign(var.right_expr, tail(value, program_state),
                   program_state, state)

            return value

        # Modifying field
        elif var.operator.name == '.':
            obj = var.left_expr.simplify(program_state)
            obj.state[var.right_expr.name] = value.simplify(program_state)

        # Function declaration
        elif var.operator.name == ' ':
            arguments = []
            args = var
            while isinstance(args, BinaryExpr):
                arg = args.right_expr
                arguments.insert(0, arg)
                args = args.left_expr

            arguments.insert(0, args)

            # Directly extract values in a structure using a tuple
            if (isinstance(arguments[0], Variable) and
                    isinstance(arguments[0].simplify(program_state), Struct) and
                    isinstance(arguments[1], Tuple)):
                value = value.simplify(program_state)
                assign(arguments[1], Tuple(value.values, program_state),
                       program_state, state)
                return value

            # Typed variable
            if (len(arguments) == 2 and
                    program_state.is_type(arguments[0].simplify(program_state))):
                assign(arguments[1], value, program_state, state)
                return value

            # Function definition
            return_type = None
            # Find position of 'def' keyword
            if arguments[0].name == 'def':
                name = arguments[1].name
                arguments = arguments[2:]

            elif arguments[1].name == 'def':
                return_type = arguments[0].simplify(program_state)
                name = arguments[2].name
                arguments = arguments[3:]

            # For def func() { ... } notation
            if isinstance(value, Array):
                value = value.items[0]

            for i in range(len(arguments)):
                if not (isinstance(arguments[i], BinaryExpr) and
                        arguments[i].operator.name in '   :'):
                    arguments[i] = arguments[i].simplify(program_state)

            # Convert function to method
            if program_state.in_class > 0:
                case = Lambda(name, arguments=arguments, expr=value,
                              return_type=return_type)

                if name in list(state.keys()):
                    func = state[name]
                    func.cases.append(case)
                    return case
                else:
                    func = Function(name, [case])
                    state[name] = func
                    program_state.function_names.append(name)
            else:
                # Add current definition as additional case in pre-existing function
                case = Lambda(name, arguments=arguments, expr=value)
                for state in program_state.frame_stack[::-1]:
                    if name in list(state.keys()):
                        func = state[name]
                        func.cases.append(case)
                        return case

                # Create new function
                func = Function(name, [case])
                state[name] = func
                program_state.function_names.append(name)

            return case
        else:
            var, value = assign_arithmetic(var, value)
            return assign(var, value, program_state, state)

    return value


def assign_arithmetic(expr, value):
    return 0, 0


def application(func, arg, program_state):
    # For if (...) { ... } syntax
    if (((issubclass(type(func), Func) and func.name in program_state.keywords) or
         isinstance(func, Class)) and isinstance(arg, Array)):
        arg = arg.items[0]

    value = func.apply(arg, program_state=program_state)
    return value


def compose(second, first, program_state):
    return Composition(second, first)


def index(a, b, program_state):
    from List import head, tail
    # specific index
    if isinstance(b, Int):
        n = b.value
        if n < 0 or isinstance(a, Nil):
            return None

        if program_state.is_list(a):
            x, xs = head(a, program_state), tail(a, program_state)
            if n == 0:
                return x
            return index(xs, Int(n - 1), program_state)

        elif isinstance(a, Enum):
            return a.values[n]

        elif isinstance(a, (Tuple, Array)):
            return a.items[n]

    # slice
    elif isinstance(b, Cons):
        start = head(b, program_state).simplify(program_state)
        b = tail(b, program_state)

        if isinstance(b, Nil):
            return index(a, start, program_state)
        else:
            end = head(b, program_state).simplify(program_state)
            if isinstance(a, String):
                if isinstance(end, Variable) and end.name == '...':
                    return String(a.value[start.value:])
                return String(a.value[start.value: end.value])

            if isinstance(end, Variable) and end.name == '...':
                return Array(a.items[start.value:])
            return Array(a.items[start.value: end.value])

    # dictionary lookup
    elif isinstance(b, Array):
        key = b.items[0].simplify(program_state)
        for pair in a.items:
            if equals(pair.items[0], key, program_state).value:
                return pair.items[1]
        return Null()


def power(a, b, program_state):
    if isinstance(a, Object):
        if 'pow' in list(a.state.keys()):
            return a.state['pow'].apply(b, program_state=program_state)
    if isinstance(b, Object):
        if 'raise' in list(b.state.keys()):
            return b.state['raise'].apply(a, program_state=program_state)

    a, b = a.value, b.value
    return program_state.get_data(a ** b)


def divide(a, b, program_state):
    if isinstance(a, Object):
        if 'div' in list(a.state.keys()):
            return a.state['div'].apply(b, program_state=program_state)

    (a, b) = (a.value, b.value)
    return program_state.get_data(a / b)


def multiply(a, b, program_state):
    if isinstance(a, Object):
        if 'mul' in list(a.state.keys()):
            return a.state['mul'].apply(b, program_state=program_state)
    elif isinstance(b, Object):
        if 'mul' in list(b.state.keys()):
            return b.state['mul'].apply(a, program_state=program_state)

    a, b = a.value, b.value
    return program_state.get_data(a * b)


def add(a, b, program_state):
    if isinstance(a, String) and isinstance(b, String):
        return String(a.value + b.value)
    if isinstance(a, Object):
        if 'add' in list(a.state.keys()):
            return a.state['add'].apply(b, program_state=program_state)
    elif isinstance(b, Object):
        if 'add' in list(b.state.keys()):
            return b.state['add'].apply(a, program_state=program_state)

    a, b = a.value, b.value
    return program_state.get_data(a + b)


def subtract(a, b, program_state):
    if isinstance(a, Object):
        if 'sub' in list(a.state.keys()):
            return a.state['sub'].apply(b, program_state=program_state)
    if isinstance(b, Object):
        if 'subfrom' in list(b.state.keys()):
            return b.state['subfrom'].apply(a, program_state=program_state)

    return program_state.get_data(a.value - b.value)


def lessThan(a, b, program_state):
    if isinstance(a, Object):
        if 'lessThan' in list(a.state.keys()):
            return a.state['lessThan'].apply(b, program_state=program_state)
        return Bool(False)
    elif isinstance(b, Object):
        if 'greaterThan' in list(b.state.keys()):
            return b.state['greaterThan'].apply(a, program_state=program_state)
        return Bool(False)
    a, b = a.simplify(program_state), b.simplify(program_state)
    print(a.)
    return Bool(a.value < b.value)


def lessThanOrEqual(a, b, program_state):
    return Bool(lessThan(a, b, program_state).value or
                equals(a, b, program_state).value)


def greaterThan(a, b, program_state):
    if isinstance(a, Object):
        if 'greaterThan' in list(a.state.keys()):
            return a.state['greaterThan'].apply(b,
                                                program_state=program_state)
        return Bool(False)

    return Bool(not lessThanOrEqual(a, b, program_state).value)


def greaterThanOrEqual(a, b, program_state):
    return Bool(greaterThan(a, b, program_state).value or
                equals(a, b, program_state).value)


def rem(a, b, program_state):
    return Int(a.value % b.value)


def quot(a, b, program_state):
    return Int(a.value // b.value)


def equals(a, b, program_state):
    if a is None and b is None:
        return Bool(True)

    if a is None or b is None:
        return Bool(False)

    if program_state.is_primitive(a) and program_state.is_primitive(b):
        return Bool(a.value == b.value)

    if program_state.is_list(a) and program_state.is_list(b):
        if isinstance(a, Nil) and isinstance(b, Nil):
            return Bool(True)
        x, xs = head(a, program_state), tail(a, program_state)
        y, ys = head(b, program_state), tail(b, program_state)
        return equals(x, y, program_state) and equals(xs, ys, program_state)

    if isinstance(a, (Array, Tuple)) and isinstance(b, (Array, Tuple)):
        if len(a.items) != len(b.items):
            return Bool(False)
        for i in range(len(a.items)):
            if not equals(a.items[i], b.items[i], program_state).value:
                return Bool(False)
        return Bool(True)

    if isinstance(a, Object):
        if 'equals' in list(a.state.keys()):
            return a.state['equals'].apply(b, program_state=program_state)
        return Bool(a == b)

    if issubclass(type(a), Func) and issubclass(type(b), Func):
        if a.name == b.name:
            return equals(Tuple(a.inputs, program_state),
                          Tuple(b.inputs, program_state), program_state)

    return Bool(False)


def not_equal(a, b, program_state):
    return Bool(not equals(a, b, program_state).value)


def logical_and(a, b, program_state):
    if not a.simplify(program_state).value:
        return Bool(False)
    return b.simplify(program_state)


def logical_or(a, b, program_state):
    if a.simplify(program_state).value:
        return Bool(True)
    return b.simplify(program_state)


def comma(a, b, program_state):
    if isinstance(a, Tuple):
        return Tuple(a.items.append(b), program_state)
    return Tuple([a, b], program_state)


def cons(a, b, program_state):
    from utils import replaceVariables
    if isinstance(b.simplify(program_state), Object):
        b = b.simplify(program_state)
        if 'cons' in list(b.state.keys()):
            return b.state['cons'].apply(a, program_state=program_state)

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


def sequence(a, b, program_state):
    if not (program_state.break_loop > 0 or program_state.continue_loop > 0):
        a.simplify(program_state)

        # if return value is set or the first line is a break or continue
        # then execution must be stopped
        if program_state.return_value:
            return program_state.return_value

        if not (program_state.break_loop > 0 or program_state.continue_loop > 0):
            return b.simplify(program_state)

    return Null()


def chain(a, b, program_state):
    return b.apply(a.simplify(program_state), program_state=program_state)


def create_lambda(args, expr, program_state):
    arguments = []
    while isinstance(args, BinaryExpr):
        arguments.insert(0, args.right_expr)
        args = args.left_expr
    arguments.insert(0, args)

    case = Lambda('\\', expr, arguments=arguments)
    return case


def create_enum(name, values, program_state):
    state = program_state.frame_stack[-1]
    names = list(map(lambda var: var.name, values.items))
    name = name.name
    enum = Enum(name, names)
    state[name] = enum
    i = 0
    for val in values.items:
        assign(val, EnumValue(enum, val.name, i), program_state)
        i += 1
    return enum


def create_struct(name, fields, program_state):
    state = program_state.frame_stack[-1]
    fields = list(map(lambda var: var.name, fields.items))
    name = name.name
    struct = Struct(name, fields)
    state[name] = struct
    program_state.function_names.append(name)
    return struct


def create_operator(symbol, precedence, associativity, func, program_state):
    from Operators import operatorsDict, Op, Associativity
    associativity_map = {'left': Associativity.LEFT,
                         'right': Associativity.LEFT,
                         'none': Associativity.NONE}

    precedence = precedence.value
    associativity = associativity_map[associativity.name]
    symbol = str(symbol)[1:-1]
    program_state.operators.append(symbol)

    func = func.simplify(program_state).apply(program_state=program_state)
    func.name = symbol
    func.precedence = precedence
    func.associativity = associativity

    operatorsDict[symbol] = Op(hfunc=func)

    return func


def create_class(nameVar, program_state):
    name = nameVar.name
    class_ = Class(name)
    assign(nameVar, class_, program_state)
    return class_


def create_interface(name, declarationsExpr, program_state):
    state = program_state.frame_stack[-1]
    name = name.name
    interface = Interface(name, declarationsExpr, program_state)
    state[name] = interface
    program_state.function_names.append(name)
    return interface


def where(expr1, expr2, program_state):
    program_state.frame_stack.append({})
    expr2.simplify(program_state)
    value = expr1.simplify(program_state)
    program_state.frame_stack.pop(-1)
    return value


def alias(var, expr):
    return Alias(var, expr)


def shift_left(num, n, program_state):
    return Int(num.value << n.value)


def shift_right(num, n, program_state):
    return Int(num.value >> n.value)


def bitwise_or(x, y, program_state):
    return Int(x.value | y.value)


def bitwise_and(x, y, program_state):
    return Int(x.value & y.value)


def access(obj, field, program_state):
    obj = obj.simplify(program_state)
    try:
        return obj.state[field.name].simplify(program_state)
    except:
        print('operator_functions > access(...):', obj, field)
        # print(program_state.frame_stack)


def for_loop(n, expr, program_state):
    val = Null()
    state = {}
    #
    if isinstance(n, Tuple):
        generators = n.items
        program_state.frame_stack.append(state)
        curr = generators[0].simplify(program_state)
        var, collection = curr.var, curr.collection.simplify(program_state)
        # List comprehension
        while not isinstance(collection, Nil):
            assign(var, head(collection, program_state), program_state)
            if len(generators) == 1:
                val = expr.simplify(program_state)
            else:
                val = for_loop(Tuple(generators[1:], program_state), expr,
                               program_state)

            if program_state.break_loop > 0 or program_state.return_value:
                program_state.break_loop -= 1
                break

            if program_state.continue_loop > 0:
                program_state.continue_loop -= 1

            collection = tail(collection, program_state)

        program_state.frame_stack.pop(-1)

    elif isinstance(n, BinaryExpr):
        # Traditional for-lop
        if n.operator.name == ';':
            init, n = n.left_expr, n.right_expr
            cond, after = n.left_expr, n.right_expr
            program_state.frame_stack.append(state)
            init.simplify(program_state)
            while cond.simplify(program_state).value:
                val = expr.simplify(program_state)
                if program_state.continue_loop > 0:
                    program_state.continue_loop -= 1
                if program_state.break_loop > 0 or program_state.return_value:
                    program_state.break_loop -= 1
                    break
                after.simplify(program_state)
            program_state.frame_stack.pop(-1)

        elif n.operator.name == 'in':
            n = n.simplify(program_state)
            program_state.frame_stack.append(state)
            var, collection = n.var, n.collection.simplify(program_state)
            # Iterates over elements in list
            if program_state.is_list(collection):
                while not isinstance(collection, Nil):
                    assign(var, head(collection, program_state),
                           program_state, state)
                    val = expr.simplify(program_state)
                    if (program_state.break_loop > 0 or
                            program_state.return_value):
                        program_state.break_loop -= 1
                        break
                    if program_state.continue_loop > 0:
                        program_state.continue_loop -= 1
                    collection = tail(collection, program_state)

            # Iterate over items in tuples or array
            elif isinstance(collection, (Tuple, Array)):
                for item in collection.items:
                    assign(var, item, program_state, state)
                    val = expr.simplify(program_state)
                    if (program_state.break_loop > 0 or
                            program_state.return_value):
                        program_state.break_loop -= 1
                        break

                    if program_state.continue_loop > 0:
                        program_state.continue_loop -= 1

            program_state.frame_stack.pop(-1)

        else:
            # n loops
            n = n.simplify(program_state)
            for i in range(n.value):
                val = expr.simplify(program_state)
                if program_state.continue_loop > 0:
                    program_state.continue_loop -= 1
                if program_state.break_loop > 0:
                    program_state.break_loop -= 1
                    break
    else:
        n = n.simplify(program_state)
        for i in range(n.value):
            val = expr.simplify(program_state)
            if program_state.continue_loop > 0:
                program_state.continue_loop -= 1
            if program_state.break_loop > 0:
                program_state.break_loop -= 1

    return val


def while_loop(cond, expr, program_state):
    value = Null()
    while cond.simplify(program_state).value:
        value = expr.simplify(program_state)

        #
        if program_state.continue_loop > 0:
            program_state.continue_loop -= 1

        if program_state.break_loop > 0 or program_state.return_value:
            program_state.break_loop -= 1
            break

    return value


def break_current_loop(program_state):
    program_state.break_loop = 1
    return Int(0)


def continue_loop(program_state):
    program_state.continue_loop = 1
    return Int(0)


def breakout(n, program_state):
    program_state.break_loop += n.value
    return Int(0)


def skipout(n, program_state):
    program_state.continue_loop += n.value
    return Int(0)


def if_statement(cond, expr, program_state):
    try:
        if cond.simplify(program_state).value:
            return expr.simplify(program_state)
    except:
        # print(cond)
        pass
    return Null()


def extends(subclass, superclass, program_state):
    subclass.state['super'] = superclass
    for name in list(superclass.state.keys()):
        subclass.state[name] = superclass.state[name]
    return subclass


def implements(class_, interface, program_state):
    class_.interfaces.append(interface)
    return class_


def definition(name_var, args_tup, expr, program_state):
    name = name_var.name
    state = program_state.frame_stack[-1]
    case = Lambda(name, arguments=[args_tup], expr=expr)
    if name in state.keys():
        func = state[name]
        func.cases.append(case)
    else:
        func = Function(name, cases=[case])
        state[name] = func
        program_state.function_names.append(name)
    return case


def switch(value, expr, program_state):
    cases = []
    while isinstance(expr, BinaryExpr) and expr.operator.name == ';':
        cases.append(expr.left_expr)
        expr = expr.right_expr

    cases.append(expr)

    follow_through = False
    for case in cases:
        if (follow_through or
                isinstance(case.leftExpr, Variable) and
                case.leftExpr.name == 'otherwise' or
                pattern_match(case.leftExpr.simplify(program_state),
                              value.simplify(program_state), program_state)):
            val = case.rightExpr.simplify(program_state)
            follow_through = True

            # No follow through
            if case.operator.name == '=>':
                return val

    return Null()


def let(assign_stat, expr, program_state):
    state = {}
    program_state.frame_stack.append(state)
    assign_stat.simplify(program_state)
    variables = list(state.keys())
    expr.simplify(program_state)
    for var in variables:
        state.pop(var)
    program_state.frame_stack[-2].update(state)
    program_state.frame_stack.pop(-1)


def import_module(nameVar, program_state):
    name = nameVar.name
    try:
        file = open('Modules/' + name + '.txt', 'r')
    except:
        file = open('src/Modules/' + name + '.txt', 'r')

    code = file.read()
    return Module(name, code, program_state)


def from_import(moduleVar, stat, names):
    if isinstance(names, Tuple):
        names = list(map(str, names.tup))
    elif isinstance(names, Variable):
        names = [names.name]

    module_name = moduleVar.name
    file = open('Modules/' + module_name + '.txt', 'r')
    code = file.read()
    module = Module(module_name, code)
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


def to_int(expr, program_state):
    if isinstance(expr, (Int, Float, String)):
        return Int(int(float(expr.value)))
    if isinstance(expr, Bool):
        if expr.value:
            return Int(1)
        return Int(0)
    if isinstance(expr, Char):
        return Int(ord(expr.value))
    return Int(0)


def to_float(expr, program_state):
    if isinstance(expr, (Int, Float, String)):
        return Float(float(expr.value))
    if isinstance(expr, Bool):
        if expr.value:
            return Float(1.0)
        return Float(0.0)
    return Float(0)


def to_bool(expr, program_state):
    if isinstance(expr, (Int, Float)):
        if expr.value > 0:
            return Bool(True)
        return Bool(False)
    if isinstance(expr, Nil):
        return Bool(False)
    if isinstance(expr, Cons):
        return Bool(True)
    return Bool(False)


def to_char(expr, program_state):
    if isinstance(expr, Int):
        return Char(chr(expr.value))
    return Char(chr(0))


def to_string(expr, program_state):
    if isinstance(expr, Char):
        return String(expr.value)
    elif isinstance(expr, String):
        return expr
    return String(str(expr))


def do_loop(expr, loop, cond, program_state):
    expr.simplify(program_state)
    if loop.name == 'while':
        return while_loop(cond, expr, program_state)
    if loop.name == 'for':
        return for_loop(cond, expr, program_state)


def increment_by(var, val, program_state):
    value = var.simplify(program_state)
    assign(var, add(value, val.simplify(program_state), program_state),
           program_state)
    return value


def decrement_by(var, val, program_state):
    value = var.simplify(program_state)
    assign(var, subtract(val.simplify(program_state), value, program_state),
           program_state)
    return value


def multiply_by(var, val, program_state):
    value = var.simplify(program_state)
    assign(var, multiply(val.simplify(program_state), value, program_state),
           program_state)
    return value


def divide_by(var, val, program_state):
    value = var.simplify(program_state)
    assign(var, divide(val.simplify(program_state), value, program_state),
           program_state)
    return value


def raise_to(var, val, program_state):
    value = var.simplify(program_state)
    assign(var, power(val.simplify(program_state), value, program_state),
           program_state)
    return value


def default_int(var, program_state):
    if isinstance(var.simplify(program_state), Tuple):
        for name in var.simplify(program_state).items:
            default_int(name, program_state)
    else:
        program_state.frame_stack[-1][var.name] = Int(0)
    return var


def default_float(var, program_state):
    if isinstance(var, Tuple):
        for name in var.simplify().tup:
            default_float(name)
    else:
        program_state.frame_stack[-1][var.name] = Float(0)
    return var


def default_bool(var, program_state):
    if isinstance(var, Tuple):
        for name in var.simplify().tup:
            default_bool(name)
    else:
        program_state.frame_stack[-1][var.name] = Bool(False)
    return var


def default_char(var, program_state):
    if isinstance(var, Tuple):
        for name in var.simplify().tup:
            default_char(name)
    else:
        program_state.frame_stack[-1][var.name] = to_char(Int(97))
    return var


def type_synonym(typeVar, typeExpr, program_state):
    from Types import Type
    type_ = Type(typeVar.name, typeExpr)
    assign(typeVar, type_, program_state)
    return type_


def types_union(var, types, program_state):
    from Types import Union

    for i in range(len(types.items)):
        types.items[i] = types.items[i].simplify(program_state)

    union = Union(var.name, types)
    assign(var, union, program_state)
    return union


def then_clause(cond, expr, program_state):
    if cond.simplify(program_state).value:
        return expr.simplify(program_state)
    return Null()


def else_clause(if_stat, expr, program_state):
    if if_stat.left_expr.right_expr.simplify(program_state).value:
        return if_stat.simplify(program_state)
    return expr.simplify(program_state)


def read_as(var, struct, program_state):
    return Alias(var, struct)


def create_iterator(var, xs, program_state):
    return Iterator(var, xs, program_state)


def make_public(var, program_state):
    program_state.frame_stack[-1]['this'].public.append(var.name)
    return var


def make_private(var, program_state):
    program_state.frame_stack[-1]['this'].private.append(var.name)
    return var


def make_hidden(var, program_state):
    program_state.frame_stack[-1]['this'].hidden.append(var.name)
    return var


def pass_arg(arg, funcs, program_state):
    if isinstance(funcs.simplify(program_state), Tuple):
        items = []
        for func in funcs.simplify(program_state).tup:
            items.append(pass_arg(arg, func, program_state))
        return Tuple(items, program_state)
    if not isinstance(arg, Variable):
        arg = arg.simplify(program_state)
    return application(funcs.simplify(program_state), arg, program_state)


def match(a, b, program_state):
    from utils import pattern_match
    return Bool(pattern_match(a, b, program_state))


def append(a, b, program_state):
    if isinstance(a, (Tuple, Array)):
        a.items.append(b)

    return a


def python_eval(code, program_state):
    return program_state.get_data(str(eval(code.value)))


def eval_(code, program_state):
    return program_state.evaluate(code.value)
