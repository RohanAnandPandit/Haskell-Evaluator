# -*- coding: utf-8 -*-
"""
Created on Sat Jun 27 16:34:38 2020

@author: rohan
"""
functionNames = ['isUpper', 'isDigit']

def isUpper(a):
    c = a
    return ord('A') <= ord(a) <= ord('Z')

def isDigit(a):
    c = a
    return ord('0') <= ord(a) <= ord('9')
