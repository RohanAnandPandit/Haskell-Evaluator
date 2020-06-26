# -*- coding: utf-8 -*-
"""
Created on Mon Nov 18 15:43:13 2019

@author: rohan
"""
from functools import partial
from utils import dimensionOfList
def space(func, arg):
    return func.apply(arg)

def index(arr, index):
    return arr[index]

def power(a, b):
    return a ** b

def divide(a, b):
    return a / b

def multiply(a, b):
    return a * b

def add(a, b):
    return a + b

def subtract(a, b):
    return a - b

def modulo(a, b):
    return a % b

def remainder(a, b):
    return a % b

def quotient(a, b):
    return a // b

def cons(a, b):
    return tuple([a] + list(b))

def concatenate(a, b):
    return a + b

def comprehension(a, b):
    lis = []
    if (type(a) == int):
        if (a <= b):
            end = b + 1
            step = 1
        else:
            end = b - 1
            step = -1
        for i in range(a, end, step):
            lis.append(i)
    elif (type(a) == bool):
        pass
    return lis
    
def lessThan(a, b):
    return a < b

def lessThanOrEqual(a, b):
    return a <= b

def greaterThan(a, b):
    return a > b

def greaterThanOrEqual(a, b):
    return a >= b

def equals(a, b):
    return a == b

def AND(a, b):
    return (a and b)

def OR(a, b):
    return (a or b)

def head(l):
    if (len(l) == 0):
        return None
    return l[0]

        
def tail(l):
    if (len(l) == 0):
        return None
    return l[1:]
        
def length(l):
    return len(l)

def comma(a, b):
    if (dimensionOfList(a) - 1 == dimensionOfList(b)):
        a.append(b)
        return a
    else:
        return [a, b]
        
    
def concat(lists):
    if (lists == []):
        return []
    if (type(lists[0]) == list):
        final = []
        for l in lists:
            final += l
    elif (type(lists[0]) == str):
        final = ''
        for l in lists:
            final += l[1 : len(l) - 1]
        return final 
        #return "\"" + final + "\""

    return final

def init(l):
    if (len(l) == 0):
        return None
    return l[0:len(l)-1]

def maximum(l):
    return max(l)

def minimum(l):
    return min(l)

def even(n):
    return n & 1 == 0

def odd(n):
    return n & 1 == 1

def elem(item, l):
    return item in l

def notElem(item, l):
    return not elem(item, l)

def reverse(l):
    return l[::-1]

def take(a, b):
    if (a > len(b)):
        return None
    return b[:a] 

def drop(a, b):
    if (a > len(b)):
        return None
    return b[a:]

def map2(func, l):
    return list(map(func, list(l)))

def mapHaskell(func, l):
    l = list(l)
    res = []
    for item in l:
        res.append(func.apply(item))
    return res

def words(string):
    return string.split(' ')

def unwords(string):
    s = ""
    for word in string:
        s += word + ' '
    return s

def takeWhile(func, l):
    i = 0
    for item in l:
        if (func(item)):
            i += 1
        else:
            break
    return l[0:i]

def dropWhile(func, l):
    i = 0
    for item in l:
        if (func(item)):
            i += 1
        else:
            break
    return l[i:]

def fst(tup):
    return tup[0]

def snd(tup):
    return tup[1]

def div(a, b):
    return a // b

def mod(a, b):
    return a % b

def succ(x):
    return x + 1

def pred(x):
    return x - 1

def zipHaskell(a, b):
    res = []
    for i in range(min(len(a), len(b))):
        res.append((a[i], b[i]))
    return res

def foldr(func, u, xs):
    if (xs == []):
        return u
    else:
        return func(head(xs), foldr(func, u, tail(xs)))

def foldl(func, u, xs):
    if (xs == []):
        return u
    else:
        return foldl(func, func(u, head(xs)), tail(xs))
    