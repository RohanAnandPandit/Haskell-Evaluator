# -*- coding: utf-8 -*-
"""
Created on Mon Jun 22 11:24:28 2020

@author: rohan
"""
import Io
import Prelude
from Types import (Variable, Int, Float, Bool, Char, Type, String, Null)
from Class import Class, Object
from Struct import Struct, Structure
from Enum import EnumValue
from List import Nil, Cons, head, tail, Array, List
from Tuple import function_names_tuple, Tuple
from Function import Func

LIBRARY_PATH = 'Modules/'


def is_primitive(expr):
    return type(expr) in [Int, Float, Bool, Char, String, EnumValue, Null]


def null(expr):
    return isinstance(expr, Null)


def is_list(expr):
    if issubclass(type(expr), List):
        return True
    if isinstance(expr, Object):
        for interface in expr.class_.interfaces:
            if interface.name == 'List':
                return True
    return False


def pattern_match(expr1, expr2, program_state):
    from Operator_Functions import equals
    from Expression import BinaryExpression

    expr2 = expr2.simplify(program_state)

    if is_primitive(expr1) and is_primitive(expr2):
        return equals(expr1.simplify(program_state), expr2, program_state).value

    if isinstance(expr1, Variable):
        if isinstance(expr1.simplify(program_state), Type):
            return (isinstance(expr2, (Type, Class, Struct)) and
                    expr1.simplify(program_state).name == expr2.name)
        return True

    if isinstance(expr1, BinaryExpression) and expr1.operator.name == '@':
        return pattern_match(expr1.right_expr, expr2, program_state)

    if isinstance(expr1, Nil) and isinstance(expr2, Nil):
        return True

    if isinstance(expr1, Cons):
        if isinstance(expr2, Nil):
            return False
        return (pattern_match(head(expr1), head(expr2).simplify(program_state), program_state)
                and pattern_match(tail(expr1), tail(expr2), program_state))

    if (isinstance(expr1, BinaryExpression) and
            expr1.operator.name == ':' and
            is_list(expr2)):
        if isinstance(expr2, Nil):
            return False
        return (pattern_match(expr1.left_expr,
                              head(expr2, program_state).simplify(program_state),
                              program_state)
                and pattern_match(expr1.right_expr, tail(expr2, program_state),
                                  program_state))

    if type(expr1) == type(expr2) and type(expr1) in (Tuple, Array):
        if len(expr1.items) == len(expr2.items) == 0:
            return True

        if len(expr1.items) != len(expr2.items):
            if len(expr1.items) == 0:
                return False
            if (isinstance(expr1.items[-1], Variable) and
                    expr1.items[-1].name == '...'):
                if len(expr1.items) - 1 > len(expr2.items):
                    return False
            else:
                return False

        if (len(expr1.items) > 0 and isinstance(expr1.items[0], Variable) and
                expr1.items[0].name == '...'):
            return True

        return (pattern_match(expr1.items[0],
                              expr2.items[0].simplify(program_state),
                              program_state) and
                pattern_match(Tuple(expr1.items[1:], program_state),
                              Tuple(expr2.items[1:], program_state),
                              program_state))

    if isinstance(expr1, BinaryExpression) and expr1.operator.name == " ":
        if type_match(expr1.left_expr, expr2, program_state):
            if isinstance(expr2, Structure):
                return pattern_match(expr1.right_expr, Tuple(expr2.values, program_state),
                                     program_state)
            else:
                return pattern_match(expr1.right_expr, expr2, program_state)
    else:
        return equals(expr1.simplify(program_state), expr2, program_state).value

    return False


def type_match(type_, expr, program_state):
    from Types import Type
    from Union import Union
    if (null(type_.simplify(program_state)) or
            null(expr.simplify(program_state))):
        return True

    if isinstance(type_, (Variable, Struct)) or isinstance(type_, Type):
        if type_.name == 'var':
            return True

        if type_.name == 'Type':
            return program_state.is_type(expr)

        elif type_.name == 'Object':
            return isinstance(expr, Object)

        elif isinstance(expr, Object):
            return type_.simplify(program_state).name == expr.class_.name

        elif type_.name == 'Func':
            return issubclass(type(expr), Func)

        elif isinstance(type_.simplify(program_state), Type):
            if is_primitive(expr):
                return type_.simplify(program_state).name == expr.type
            if type_.simplify(program_state).name in ('int', 'float', 'char',
                                                      'string', 'bool'):
                return False
            return type_match(type_.simplify(program_state).expr, expr,
                              program_state)

        elif isinstance(type_.simplify(program_state), Union):
            type_ = type_.simplify(program_state)
            for t in type_.types:
                if type_match(t, expr, program_state):
                    return True

        elif isinstance(expr, (Structure, Struct)):
            return type_.name == expr.type.name

    elif isinstance(type_, Nil) and is_list(expr):
        return True

    elif (isinstance(type_, (Tuple, Array)) and len(type_.items) == 0
          and type(type_) in (Tuple, Array)):
        return True

    elif isinstance(type_, Cons) and is_list(expr):
        return (type_match(head(type_, program_state),
                           head(expr, program_state),
                           program_state)
                and type_match(tail(type_, program_state),
                               tail(expr, program_state),
                               program_state))

    if (type(expr) in (Tuple, Array) and isinstance(type_, Variable) and
            type_.name == '...'):
        return True

    elif type(type_) == type(expr) and type(type_) in (Tuple, Array):
        if len(type_.items) == 0:
            return True

        elif (isinstance(type_.items[0], Variable) and
              type_.items[0].name == '...'):
            return True

        elif len(type_.items) != len(expr.items):
            if (isinstance(type_.items[-1], Variable) and
                    type_.items[-1].name == '...'):
                if len(type_.items) - 1 > len(expr.items):
                    return False
            else:
                return False

        return (type_match(type_.items[0], expr.items[0], program_state) and
                type_match(Tuple(type_.items[1:], program_state),
                           Tuple(expr.items[1:], program_state)))

    return False


def optimise(expr):
    from Expression import BinaryExpression
    from Operator_Functions import equals
    if isinstance(expr, BinaryExpression):
        expr.left_expr = optimise(expr.left_expr)
        expr.right_expr = optimise(expr.right_expr)
        if expr.operator.name in ('+', '||'):
            if equals(expr.left_expr, Int(0)).value:
                if expr.right_expr is not None:
                    return expr.right_expr
            elif equals(expr.right_expr, Int(0)).value:
                if expr.left_expr is not None:
                    return expr.left_expr
        elif expr.operator.name == '-':
            if equals(expr.right_expr, Int(0)).value:
                if expr.left_expr is not None:
                    return expr.left_expr
        elif expr.operator.name == '*':
            if equals(expr.left_expr, Int(0)).value:
                if expr.right_expr is not None:
                    return Int(0)
            elif equals(expr.right_expr, Int(0)).value:
                if expr.left_expr is not None:
                    return Int(0)
            elif equals(expr.left_expr, Int(1)).value:
                if expr.right_expr is not None:
                    return expr.right_expr
            elif equals(expr.right_expr, Int(1)).value:
                if expr.left_expr is not None:
                    return expr.left_expr
        elif expr.operator.name == '&&':
            if equals(expr.left_expr, Int(0)).value:
                if expr.right_expr is not None:
                    return Bool(False)
            elif equals(expr.right_expr, Int(0)).value:
                if expr.left_expr is not None:
                    return Bool(False)
        elif expr.operator.name == '/':
            if equals(expr.left_expr, Int(0)).value:
                if expr.right_expr is not None:
                    return Int(0)
            elif equals(expr.right_expr, Int(1)).value:
                if expr.left_expr is not None:
                    return expr.left_expr
        elif expr.operator.name == '^':
            if equals(expr.left_expr, Int(1)).value:
                if expr.right_expr is not None:
                    return Int(1)
            elif equals(expr.left_expr, Int(0)).value:
                if expr.right_expr is not None:
                    return Int(0)
            elif equals(expr.right_expr, Int(1)).value:
                if expr.left_expr is not None:
                    return expr.left_expr
            elif equals(expr.right_expr, Int(0)).value:
                if expr.left_expr is not None:
                    return Int(1)
        elif expr.operator.name == '++':
            if isinstance(expr.left_expr, Nil):
                if expr.right_expr is not None:
                    return expr.right_expr
            elif isinstance(expr.right_expr, Nil):
                if expr.left_expr is not None:
                    return expr.left_expr

    return expr


def replace_variables(expr, program_state):
    from Expression import BinaryExpression
    from Collection import Collection
    if isinstance(expr, Variable):
        expr = expr.simplify(program_state)
    elif isinstance(expr, BinaryExpression):
        left = expr.left_expr
        if expr.operator.name not in ('=', 'where'):
            left = replace_variables(expr.left_expr, program_state)
        right = replace_variables(expr.right_expr, program_state)
        expr = BinaryExpression(expr.operator, left, right)
    elif isinstance(expr, Cons):
        expr = Cons(replace_variables(expr.item, program_state),
                    replace_variables(expr.tail, program_state), program_state)
    elif isinstance(expr, Tuple):
        expr = Tuple(list(map(lambda exp: replace_variables(exp, program_state),
                              expr.tup)), program_state)
    elif isinstance(expr, Collection):
        expr = Collection(list(map(lambda exp: replace_variables(exp, program_state),
                                   expr.items)), expr.operator)
    return expr


def convertToList(expr, program_state):
    # If None is returned means there was no operand or 
    # operator which means it is an empty list
    xs = Nil()
    for i in range(len(expr) - 1, -1, -1):
        xs = Cons(expr[i], xs, program_state)
    return xs
