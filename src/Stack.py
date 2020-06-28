# -*- coding: utf-8 -*-
"""
Created on Tue Jun 23 09:30:32 2020

@author: rohan
"""

class Stack:
    def __init__(self):
        self.arr = []
    
    def push(self, item):
        self.arr.append(item)
    
    def pop(self):
        item = None
        if (len(self.arr) > 0):
            item = self.arr[-1]
            del self.arr[-1]
        return item
    
    def peek(self):
        if (len(self.arr) == 0):
            return None
        return self.arr[-1]
   
    