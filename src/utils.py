# -*- coding: utf-8 -*-
"""
Created on Mon Jun 22 11:24:28 2020

@author: rohan
"""

def indexOfClosing(c, exp):
    closer = {'[' : ']', '(' : ')'}
    index = 0
    count = 0
    for char in exp:
        if (char == c):
            count += 1
        elif (char == closer[c]):
            count -= 1
            if (count == 0):
                return index
        index += 1
    return None
