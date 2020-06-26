# -*- coding: utf-8 -*-
"""
Created on Mon Nov 18 15:43:13 2019

@author: rohan
"""
from functools import partial
from utils import dimensionOf

def id(x):
    return x

def const(x, y):
    return x

def space(func, arg):
    return func.apply(arg)

def index(a, b):
    (arr, index) = (a, b)
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

def notEqual(a, b):
    return a != b

def AND(a, b):
    return (a and b)

def OR(a, b):
    return (a or b)


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
'''=============================================='''

def cons(a, b):
    (x, xs) = (a, b)
    return [x] + xs

def concatenate(a, b):
    return a + b

def null(l):
    return l == []

def head(l):
    if (len(l) == 0):
        return None
    return l[0]

def last(l):
    if (len(l) == 0):
        return None
    return l[-1]

def tail(l):
    if (len(l) == 0):
        return None
    return l[1:]

def length(l):
    return len(l)

def comma(a, b):
    diff = dimensionOf(b) - dimensionOf(a)
    if (diff == 1):
        b = list(b)
        b = [a] + b
        return tuple(b)
    elif (diff == 0):
        return (a, b)

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
   
def concat(lists):
    if (lists == []):
        return []
    if (type(lists[0]) == list):
        final = []
    elif (type(lists[0]) == str):
        final = ''
        
    final = []
    for l in lists:
        final += l
        
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
'''
def map2(func, l):
    return list(map(func, list(l)))
'''
def map(func, l):
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
    res = []
    for item in l:
        if (func.apply(item)):
            res.append(item)
        else:
            break
    return res

def dropWhile(func, l):
    i = 0
    for item in l:
        if (func.apply(item)):
            i += 1
        else:
            break
    return l[i:]


def zip(xs, ys):
    res = []
    for i in range(min(len(xs), len(ys))):
        res.append((xs[i], ys[i]))
    return res

def zipWith(a, b, c):
    (func, xs, ys) = (a, b, c)
    res = []
    for i in range(min(len(xs), len(ys))):
        res.append(func.apply(xs[i], ys[i]))
    return res
    
def foldr(func, u, xs):
    if (xs == []):
        return u
    else:
        return func.apply(head(xs), foldr(func, u, tail(xs)))

def foldl(func, u, xs):
    if (xs == []):
        return u
    else:
        return foldl(func, func.apply(u, head(xs)), tail(xs))

def andHk(bools):
    for b in bools:
        if (not b):
            return False
    return True

def orHk(bools):
    for b in bools:
        if (b):
            return True
    return False

def any(bools):
    for b in bools:
        if (func.apply(b)):
            return True
    return False

def all(func, bools):
    for b in bools:
        if (not func.apply(b)):
            return False
    return True

def filter(pred, xs):
    res = []
    for x in xs:
        if (pred.apply(x)):
            res.append(x)
    return res
