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
        item = self.peek()
        if (len(self.arr) > 0):
            del self.arr[-1]
        return item
    
    def peek(self):
        if (len(self.arr) == 0):
            return None
        item = self.arr[-1]
        return item
    
    def enQueue(self, item):
        self.arr.append(item)
    
    def deQueue(self):
        if (len(self.arr) > 0):
            item = self.arr[0]
            del self.arr[0]
            return item
        return None
    