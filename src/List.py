# -*- coding: utf-8 -*-
"""
Created on Tue Jun 23 20:381 2020

@author: rohan
"""
from Types import Object, Null

class List:
    pass
      
class Nil(List):
    def __init__(self, listType = None):
        self.type = listType
        
    def __str__(self):
        return '[]'
    
    def simplify(self, program_state):
        return self
        
class Cons(List):
    def __init__(self, itemExpr, listExpr, program_state):
        self.item = itemExpr
        self.tail = listExpr 
        self.program_state = program_state
        
    def __str__(self):
        tail = str(self.tail)
        sep = ', '
        if (tail == '[]'):
            sep = ''
        value = str(self.item.simplify(self.program_state))
        return '[' + value + sep + tail[1 : -1] + ']' 
    
    def simplify(self, program_state):
        return self

class Iterator(List):
    def __init__(self, var, collection, program_state):
        self.var = var
        self.collection = collection.simplify(program_state)
            
    def simplify(self, program_state):
        return self

    def __str__(self):
        return '(' + str(self.var) + ' in ' + str(self.collection) + ')'

class Array:
    def __init__(self, items = []):
        self.items = items
        
    def simplify(self, program_state):
        return self
    
    def __str__(self):
        items = []
        for item in self.items:
            items.append(str(item))
        return '{' + ', '.join(items) + '}'
 
def head(a, program_state):    
    if isinstance(a.simplify(program_state), Object):
         a = a.simplify(program_state)
         func = a.class_.state['head'].apply(a, program_state = program_state)
         return func.simplify(program_state)
    if isinstance(a, Nil):
        return Null()
    if isinstance(a, Cons):
        return a.item


def tail(a, program_state):
    if isinstance(a.simplify(program_state), Object):
         a = a.simplify(program_state)
         func = a.class_.state['tail'].apply(a, program_state = program_state)
         return func.simplify(program_state)
    if isinstance(a, Nil):
        return Null()
    if isinstance(a, Cons):
        return a.tail
