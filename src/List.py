# -*- coding: utf-8 -*-
"""
Created on Tue Jun 23 20:381 2020

@author: rohan
"""
from Maybe import Just, Nothing

functionNamesList = ['length', 'head', 'tail', 'last', 'concat', 'init', 'maximum',
                 'minimum', 'elem', 'notElem', 'reverse', 'take', 'drop', 'map',
                 'words', 'unwords', 'takeWhile', 'dropWhile', 'zip', 'unzip',
                 'foldl', 'foldr', 'and', 'or', 'any', 'all', 'filter', 'sum',
                 'product', 'lookup', 'concatMap', 'splitAt', 'span', 'replicate'] 
class List:
    def __init__(self, expr, listType = None):
        self.expr = expr
        self.type = listType
       
    def simplify(self):
        self.expr = self.expr.simplify()
        return self
    
    def toString(self):
        return listString(self.type, self.expr.simplify(), '[')

      
class Nil:
    
    def toString(self):
        return '[]'
    
    def simplify(self):
        return self
        
class Cons:
    def __init__(self, itemExpr, listExpr):
        self.item = itemExpr
        self.list = listExpr
        
    def toString(self):
        string = self.list.toString()
        sep = ', '
        if (string == '[]'):
            sep = ''
        try:
            value = self.item.toString()
        except:
            value = str(self.item)
        return '[' + value + sep + self.list.toString()[1 : -1] + ']'
    
    def simplify(self):
        return self

        
def listString(listType, expr, char):
    from utils import isPrimitive, closer
    from IO import printHaskell
    
    string = ''
    while (not isinstance(expr, Nil)):
        value = expr.item
        if (not isPrimitive(expr.item)):
            value = expr.item.simplify()
        string += printHaskell(value)
        if (listType != 'string'):
            string += ', '
        expr = expr.list
    if (listType == 'string'):
        return "\"" + string + "\""
    return char + string[ : -2] + closer[char]
 
def length(a):
    xs = a
    xs = xs.simplify().expr
    if (isinstance(xs, Nil)):
        return 0
    elif (isinstance(xs, Cons)):
        return 1 + length(xs.list)
    
def head(l):
    from utils import isPrimitive
    
    xs = l
    xs = xs.simplify().expr
    if (isinstance(xs, Nil)): 
        return None
    if (isPrimitive(xs.item)):
        return xs.item
    return xs.item.simplify()


def tail(l):
    xs = l
    xs.simplify().expr
    if (isinstance(xs, Nil)):
        return None
    
    return List(l.list)

def last(a):
    from utils import isPrimitive
    
    xs = a
    xs = xs.simplify().expr
    if (isinstance(xs, Nil)):
        return None
    while (not isinstance(xs.list, Nil)):
        xs = xs.list
    if (isPrimitive(xs.item)):
        return xs.item
    return xs.item.simplify()

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
    return l[0:-1]

def maximum(l):
    return max(l)

def minimum(l):
    return min(l)

def elem(a, b):
    from utils import isPrimitive
    
    (value, xs) = (a, b)
    xs = xs.simplify()
    while (not isinstance(xs, Nil)):
        item = xs.item
        if (not isPrimitive(item)):
            item = item.simplify()
        if (item == value):
            return True
        xs = xs.list
    return False

def notElem(a, b):
    (value, l) = (a, b)
    while (not isinstance(l, Nil)):
        if (not isinstance(l, Cons)):
            l = l.simplify()
        item = l.item
        if (type(item) not in [int, float, bool, str]):
            item = item.simplify()
        if (item == value):
            return False
        l = l.list
    return True

def reverse(a):
    return a[::-1]

def take(a, b):
    (n, l) = (a, b)
    listType = l.type
    xs = l.simplify().expr
    initialList = xs
    while (n > 1 and not isinstance(xs, Nil)):
        item = xs.item
        xs = xs.list
        n -= 1
    if (not isinstance(xs, Nil)):
        xs.list = Nil()
    return List(initialList, listType)

def drop(a, b):
    from Expression import Data
    
    (n, xs) = (a, b)
    listType = xs.type
    xs = xs.simplify().expr
    
    while (n > 0 and not isinstance(xs, Nil)):
        item = xs.item
        xs = xs.list
        n -= 1

    return List(xs, listType)

def mapHaskell(a, b):
    from Operators import Operator
    from Expression import BinaryExpr
    from utils import isPrimitive
    
    (func, xs) = (a, b)
    
    xs = xs.simplify().expr
    initialList = xs

    while (not isinstance(xs, Nil)):
        if (not isPrimitive(xs.item)):
            xs.item = xs.item.simplify()
        xs.item = func.apply(xs.item) 
        xs = xs.list
        
    return List(initialList)

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


def zipHaskell(a, b):
    from Shunting_Yard_Algorithm import convertToList
    from Tuple import Tuple
    
    (xs, ys) = (a, b)
    xs = xs.simplify().expr
    ys = ys.simplify().expr
    if (isinstance(xs, Nil)):
        return ys
    elif (isinstance(ys, Nil)):
        return xs
    pairs = []
    while (not isinstance(xs, Nil) and not isinstance(ys, Nil)):
        pairs.append(Tuple((xs.item, ys.item))) 
        xs = xs.list
        ys = ys.list
    return convertToList(pairs)

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

def sumHaskell(a):
    from utils import isPrimitive
    
    xs = a
    xs = xs.simplify()
    total = 0
    while (not isinstance(xs, Nil)):
        item = xs.item
        if (not isPrimitive(item)):
            item = item.simplify()
        total += item
        xs = xs.list
    return total

def product(a):
    from utils import isPrimitive
    
    xs = a
    xs = xs.simplify()
    prod = 1
    while (not isinstance(xs, Nil)):
        item = xs.item
        if (not isPrimitive(item)):
            item = item.simplify()
        prod *= item  
        xs = xs.list
    return total

def lookup(a, b):
    from utils import isPrimitive
    from Prelude import fst, snd
    
    (key, pairs) = (a, b)
    pairs = pairs.simplify()
    if (not isPrimitive(key)):
        key = key.simplify()
    while (not isinstance(pairs, Nil)):
        tup = pairs.item
        (first, second) = (fst(tup), snd(tup))
        if (not isPrimitive(first)):
            first = first.simplify()
        if (first == key):
            return Just(second)
        pairs = pairs.list
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
