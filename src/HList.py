# -*- coding: utf-8 -*-
"""
Created on Tue Jun 23 20:38:21 2020

@author: rohan
"""
class HList:
    pass

class Nil(HList):
    def __init__(self):
        self.value = None
        self.list = []
        
        
class Cons(HList):
    def __init__(self, value, hlist):
        self.value = value
        self.list = hlist
            

def listFromTuple(expr):
    pass