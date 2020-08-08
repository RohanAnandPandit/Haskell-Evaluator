# -*- coding: utf-8 -*-
"""
Created on Tue Jun 23 20:381 2020

@author: rohan
"""
from Maybe import Just, Nothing
from Tuple import Tuple
from Types import Int, Char, Bool

functionNamesList = ['length', 'head', 'tail', 'last', 'concat', 'init', 'maximum',
                 'minimum', 'elem', 'notElem', 'reverse', 'take', 'drop', 'map',
                 'words', 'unwords', 'takeWhile', 'dropWhile', 'zip', 'unzip',
                 'foldl', 'foldr', 'foldl1', 'foldr1', 'and', 'or', 'any', 'all', 'filter', 'sum',
                 'product', 'lookup', 'concatMap', 'splitAt', 'span', 'replicate',
                 'iterate', 'repeat', 'zipWith', 'zip3', 'zipWith3', 'cycle', 'append']
class List:
    pass
      
class Nil(List):
    def __init__(self, listType = None):
        self.type = listType
        
    def __str__(self):
        return '[]'
    
    def simplify(self, simplifyVariables = True):
        return self
        
class Cons(List):
    def __init__(self, itemExpr, listExpr, listType = None):
        self.item = itemExpr
        self.tail = listExpr 
        self.type = listType
        
    def __str__(self):
        if (type(self.item) == Char):
            tail = str(self.tail)
            return '\"' + str(self.item)[1:-1] + tail[1:-1] + '\"'
    
        tail = str(self.tail)
        sep = ', '
        if (tail == '[]'):
            sep = ''
        value = str(self.item)
        if (isinstance(self.item, Iterator)):
            value = value[1 : -1]
            if (tail != '[]'):
                value += ','
        return '[' + value + sep + tail[1 : -1] + ']'

    def apply(self, arg1 = None, arg2 = None):
        if (isinstance(self.item, Iterator)):
            self.item.apply(arg1, arg2)
        return self
    
    def simplify(self, simplifyVariables = True):
        from Expression import BinaryExpr
        hd = self.item
        if simplifyVariables:
            hd = hd.simplify()
        if isinstance(hd, BinaryExpr) and hd.operator.name == ' ':
            hd = BinaryExpr(hd.operator, hd.leftExpr,
                            hd.rightExpr.simplify(False))
        return Cons(hd, self.tail.simplify(simplifyVariables))

class Iterator(List):
    def __init__(self, var, collection):
        self.var = var
        self.collection = collection.simplify()
            
    def simplify(self, simplifyVariables = True):
        return self

    def __str__(self):
        return '(' + str(self.var) + ' in ' + str(self.collection) + ')'

class Range:
    def __init__(self, start, end, step):
        self.curr = start
        self.end = end
        self.step = step
        self.stop = False
    
    def next(self):
        return self.curr
    
    def apply(self, end):
        self.end = end.simplify()
        return self
    
    def simplify(self):
        if self.stop:
            return Nil()
        return self
    
    def __str__(self):
        string = '[' + str(self.curr) + ', ' + str(self.curr.value + self.step.value)
        string += '..'
        string += str(self.end) + ']'
        return string
        
def length(a, l = 0):
    xs = tail(a)
    if (isinstance(a, Nil)):
        return l
    elif (isinstance(a, Cons)):
        if (isinstance(a.item, Iterator)):
            return length(xs, l + a.item.iterations)
        return length(xs, l + 1)

def head(a):    
    if isinstance(a, Nil):
        return None
    if isinstance(a, Cons):
        return a.item
    elif isinstance(a, Range):
        return a.next()

def tail(a):
    if (isinstance(a, Nil)):
        return None
    if (isinstance(a, Cons)):
        return a.tail
    elif isinstance(a, Range):
        from Operator_Functions import add, greaterThan
        start = add(a.curr, a.step)
        if a.end != None and greaterThan(start, a.end.simplify()).value:
            return Nil()
        end = a.end
        if end != None:
            end = end.simplify()
        return Range(start, end, a.step)

def last(a):    
    (x, xs) = (head(a), tail(a)) 
    if isinstance(a, Nil):
        return None
    if isinstance(xs, Nil):
        return x 
    return last(xs)

def append(a, b):    
    (x, xs) = (head(a), tail(a)) 
    item = b
    if isinstance(a, Nil):
        return Cons(item, Nil())
    return Cons(x, append(xs, item))

def concat(a):
    from Operators import operatorFromString
    return foldl(operatorFromString('++'), Nil(), a)

def init(a):
    (x, xs) = (head(a), tail(a)) 
    if isinstance(a, Nil):
        return None
    elif isinstance(a, Cons):
        if isinstance(xs, Nil):
            return Nil()
        return Cons(x, init(xs))  

def maximum(a, m = None):
    (x, xs) = (head(a), tail(a))
    if (isinstance(a, Nil)):
        return m
    if (isinstance(a, Cons)):
        if (m == None):
            m = x
        return maximum(xs, max(x, m))

def minimum(a, m = None):
    from utils import isPrimitive
    (x, xs) = (head(a), tail(a))
    if (isinstance(a, Nil)):
        return m
    if (not isPrimitive(x)):
        x = x.simplify()
    if (isinstance(a, Cons)):
        if (m == None):
            m = x
        return minimum(xs, min(x, m))


def elem(a, b):  
    from Operator_Functions import equals
    value = a
    (x, xs) = (head(b), tail(b))
    if (isinstance(b, Nil)):
        return False
    elif (isinstance(b, Cons)):
        return Bool(equals(x, value).value or elem(value, xs).value)


def notElem(a, b): 
    return Bool(not elem(a, b).value)

def reverse(a, l = Nil()):
    if (isinstance(a, Nil)):
        return l
    (x, xs) = (head(a), tail(a))
    return reverse(xs, Cons(x, l))
    

def take(a, b):
    n = a
    x, xs = head(b), tail(b)
    if (n.value <= 0 or isinstance(b, Nil)):
        return Nil()
    return Cons(x, take(Int(n.value - 1), xs))
        

def drop(a, b):    
    n = a
    if (n.value <= 0 or isinstance(b, Nil)):
        return b
    return drop(Int(n.value - 1), tail(b))

def mapHaskell(a, b):    
    func = a
    x, xs = head(b), tail(b)
    if (isinstance(b, Nil)):
        return b
    return Cons(func.apply(x), mapHaskell(func, xs))
        

def words(a):
    if (isinstance(a, Nil)):
        return Cons(Nil(), Nil())
    x,xs = head(a), tail(a)
    if (x == ' '):
        return Cons(Nil(), words(xs))
    w = words(xs)
    y, ys = head(w), tail(w)
    return Cons(Cons(x, y), ys)
    

def unwords(a):
    from Operator_Functions import concatenate
    if (isinstance(a, Nil)):
        return None
    x,xs = head(a), tail(a)
    if isinstance(xs, Nil):
        return x
    return concatenate(x, Cons(' ', unwords(xs)))

def takeWhile(a, b):
    func = a
    if (isinstance(b, Nil)):
        return Nil()
    (x, xs) = (head(b), tail(b))
    if func.apply(x).value:
        return Cons(x, takeWhile(func, xs))
    return Nil()

def dropWhile(a, b):
    (func, xs) = (a, b)
    if isinstance(xs, Nil):
        return Nil()
    if func.apply(head(xs)).value:
        return dropWhile(func, tail(xs))
    return xs 


def zipHaskell(a, b):
    from Operators import operatorFromString
    return zipWith(operatorFromString(',,'), a, b)
   
def zip3(a, b, c):
    if isinstance(a, Nil) or isinstance(b, Nil) or isinstance(c, Nil):
        return Nil()
    x, xs = head(a), tail(a)
    y, ys = head(b), tail(b)
    z, zs = head(c), tail(c)
    return Cons(Tuple((x, y, z)), zip3(xs, ys, zs))    
    
def unzip(a):
    from Tuple import Tuple, fst, snd
    pairs = a
    if (isinstance(pairs, Nil)):
        return Tuple((Nil(), Nil()))
    p, ps = head(pairs), tail(pairs)
    tup = unzip(ps)
    left, right = fst(p), snd(p)
    return Tuple([Cons(left, fst(tup)), Cons(right, snd(tup))]) 
    
    
def zipWith(a, b, c):
    func = a
    if (isinstance(b, Nil) or isinstance(c, Nil)):
        return Nil()
    x, xs = head(b), tail(b)
    y, ys = head(c), tail(c)
    return Cons(func.apply(x, y), zipWith(func, xs, ys))

def zipWith3(a, b, c, d):
    func = a
    if (isinstance(b, Nil) or isinstance(c, Nil) or isinstance(d, Nil)):
        return Nil()
    x, xs = head(b), tail(b)
    y, ys = head(c), tail(c)
    z, zs = head(d), tail(d)
    return Cons(func.apply(x, y).apply(z), zipWith3(func, xs, ys, zs))    
    
def foldr(a, b, c):
    func, u, xs = a, b, c
    if (isinstance(xs, Nil)):
        return u
    else:
        return func.apply(head(xs), foldr(func, u, tail(xs)))
    
def foldr1(func, xs):
    if (isinstance(xs, Nil)):
        return None
    return foldr(func, head(xs), tail(xs))

def foldl(a, b, c):
    func, u, xs = a, b, c
    if (isinstance(xs, Nil)):
        return u
    return foldl(func, func.apply(u, head(xs)), tail(xs))

def foldl1(func, b):
    if (isinstance(b, Nil)):
        return None
    x, xs = head(b), tail(b)
    return foldl(func, x, xs)

def andHaskell(a): 
    from Operators import operatorFromString
    return foldl(operatorFromString('&&'), Bool(1), a)

def orHaskell(a):
    from Operators import operatorFromString
    return foldl(operatorFromString('||'), Bool(0), a)

def anyHaskell(a, b):
    func = a
    if isinstance(b, Nil):
        return False
    x, xs = head(b), tail(b)
    if (func.apply(x).value):
        return True
    return allHaskell(func, xs)

def allHaskell(a, b):
    func = a
    if isinstance(b, Nil):
        return True
    x, xs = head(b), tail(b)
    if (not func.apply(x).value):
        return False
    return allHaskell(func, xs)

def filterHaskell(a, b):
    func = a
    if isinstance(b, Nil):
        return b
    x, xs = head(b), tail(b)
    if (func.apply(x).value):
        return Cons(x, filterHaskell(func, xs))
    return filterHaskell(func, xs)

def sumHaskell(a):
    from Operators import operatorFromString
    return foldl(operatorFromString('+'), Int(0), a)

def product(a):
    from Operators import operatorFromString
    return foldl(operatorFromString('*'), Int(1), a)

def lookup(a, b):
    from Prelude import fst, snd
    from Operator_Functions import equals
    if isinstance(b, Nil):
        return Nothing()
    tup, pairs = head(b), tail(b)
    if equals(fst(tup), a).value:
        return Just(snd(tup))
    return lookup(a, pairs)

def concatMap(a, b):
    (func, xs) = (a, b)
    return concat(mapHaskell(func, xs))

def splitAt(a, b):
    (n, xs) = (a, b)
    return Tuple((take(n, xs), drop(n, xs)))

def span(a, b):
    (func, xs) = (a, b)
    return Tuple((takeWhile(func, xs), dropWhile(func, xs)))

def replicate(a, b, l = Nil()):
    (n, x) = (a, b)
    if (n == 0):
        return l
    return replicate(n - 1, x, Cons(x, l))

def iterate(a, b):
    (func, value) = (a, b)
    return Cons(Iterator(func = func, item = value, iteratorType = 'general'), Nil())

def repeat(a):
    import Operators
    iterator = Iterator(func = Operators.func_id, item = a, iteratorType = 'general')
    return Cons(iterator, Nil())

def cycle(a):
    iterator = Iterator(cycleList = a, iteratorType = 'cycle')
    return Cons(iterator, Nil())