# -*- coding: utf-8 -*-
"""
Created on Tue Jun 23 20:381 2020

@author: rohan
"""
from Modules.Maybe import Just, Nothing

functionNames = ['length', 'head', 'tail', 'last', 'concat', 'init', 'maximum',
                 'minimum', 'elem', 'notElem', 'reverse', 'take', 'drop', 'map',
                 'words', 'unwords', 'takeWhile', 'dropWhile', 'zip', 'unzip',
                 'foldl', 'foldr', 'and', 'or', 'any', 'all', 'filter', 'sum',
                 'product', 'lookup', 'concatMap', 'splitAt', 'span', 'replicate'] 
class List:
    pass

class Nil(List):
    pass
        
class Cons(List):
    def __init__(self, valueExpr, listExpr):
        self.valueExpr = valueExpr
        self.list = listExpr

def length(l):
    return len(l)
    
def head(l):
    if (len(l) == 0):
        return None
    return l[0]

def tail(l):
    if (len(l) == 0):
        return None
    return l[1:]

def last(l):
    if (len(l) == 0):
        return None
    return l[-1]

def concat(lists):
    if (lists == []):
        return []
    if (type(lists[0]) == list):
        res = []
    elif (type(lists[0]) == str):
        res = ''
        
    for l in lists:
        res += l
        
    return res

def init(l):
    if (len(l) == 0):
        return None
    return l[0:len(l)-1]

def maximum(l):
    return max(l)

def minimum(l):
    return min(l)

def elem(a, b):
    (item, l)= (a, b)
    return item in l

def notElem(item, l):
    return not elem(item, l)

def reverse(a):
    return a[::-1]

def take(a, b):
    (n, xs) = (a, b)
    if (n < 0):
        return None
    return xs[:n] 

def drop(a, b):
    (n, xs) = (a, b)
    if (n < 0):
        return xs
    return xs[n :] 

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

def takeWhile(a, b):
    (func, l) = (a, b)
    res = []
    for item in l:
        if (func.apply(item)):
            res.append(item)
        else:
            break
    return res

def dropWhile(a, b):
    (func, l) = (a, b)
    i = 0
    for item in l:
        if (func.apply(item)):
            i += 1
        else:
            break
    return l[i:]


def zip(a, b):
    (xs, ys) = (a, b)
    res = []
    for i in range(min(len(xs), len(ys))):
        res.append((xs[i], ys[i]))
    return res

def unzip(a):
    pairs = a
    xs = ys = []
    for (x, y) in pairs:
        xs.append(x)
        ys.append(y)
    return (xs, ys)
    
    
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

def andHaskell(a): 
    bools = a
    for b in bools:
        if (not b):
            return False
    return True

def orHaskell(a):
    bools = a
    for b in bools:
        if (b):
            return True
    return False

def any(a):
    bools = a
    for b in bools:
        if (func.apply(b)):
            return True
    return False

def all(a, b):
    (func, bools) = (a, b)
    for b in bools:
        if (not func.apply(b)):
            return False
    return True

def filter(a, b):
    (pred, xs) = (a, b)
    res = []
    for x in xs:
        if (pred.apply(x)):
            res.append(x)
    return res

def sum(a):
    xs = a
    total = 0
    for x in xs:
        total += x
    return total

def product(a):
    xs = a
    res = 1
    for x in xs:
        res *= x
    return res

def lookup(a, b):
    (key, pairs) = (a, b)
    for (k, v) in pairs:
        if (k == key):
            return Just(v) 
    return Nothing()

def concatMap(a, b):
    return concat(map(a, b))

def splitAt(a, b):
    (n, xs) = (a, b)
    return (xs[ : n], xs[n : ])

def span(a, b):
    (p, xs) = (a, b)
    left = right = []
    i = 0
    while (p.apply(xs[i])):
        i += 1
    return (xs[ : i], xs[i : ])

def replicate(a, b):
    (n, x) = (a, b)
    res = []
    for i in range(n):
        res.append(x)
    return res
