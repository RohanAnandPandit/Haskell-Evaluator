# -*- coding: utf-8 -*-
"""
Created on Sat Jun 27 13:25:30 2020

@author: rohan
"""

functionNamesMaybe = ['Just', 'fromJust', 'fromMaybe', 'isNothing']

class Maybe:
    pass

class Nothing(Maybe):
    def toString(self):
        return 'Nothing'

class Just(Maybe):
    def __init__(self, value):
        self.value = value
    
    def toString(self):
        from utils import isPrimitive

        value = self.value
        if (not isPrimitive(value)):
            value = value.simplify()
        if (not isPrimitive(value)):
            string = value.toString()
        else:
            string = str(value)
        return 'Just ' + string

def just(value):
    return Just(value)

def fromJust(maybe):
    if (isinstance(maybe, Just)):
        return maybe.value
    print('Program error: Maybe.fromJust: Nothing')

def fromMaybe(default, maybe):
    if (isinstance(maybe, Just)):
        return maybe.value
    return default

def isNothing(maybe):
    return isinstance(maybe, Nothing)