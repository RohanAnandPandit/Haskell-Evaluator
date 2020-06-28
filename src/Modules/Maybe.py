# -*- coding: utf-8 -*-
"""
Created on Sat Jun 27 13:25:30 2020

@author: rohan
"""
functionNames = ['fromJust', 'fromMaybe', 'isNothing']

class Maybe:
    pass

class Nothing(Maybe):
    def toString(self):
        return 'Nothing'

class Just(Maybe):
    def __init__(self, value):
        self.value = value
    
    def toString(self):
        return 'Just ' + str(self.value)  

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