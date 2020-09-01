# -*- coding: utf-8 -*-
"""
Created on Tue Jun 23 20:381 2020

@author: rohan
"""
from Tuple import Tuple
from Types import Int, Bool, Object, Null

functionNamesList = ['length', 'head', 'tail', 'last', 'concat', 'init',
                     'maximum', 'minimum', 'elem', 'notElem', 'reverse',
                     'take', 'drop', 'map', 'words', 'unwords', 'takeWhile',
                     'dropWhile', 'zip', 'unzip', 'foldl', 'foldr', 'foldl1',
                     'foldr1', 'and', 'or', 'any', 'all', 'filter', 'sum',
                     'product', 'lookup', 'concatMap', 'splitAt', 'span',
                     'replicate', 'zipWith', 'zip3', 'zipWith3', 'append']
class List:
    pass
      
class Nil(List):
    def __init__(self, listType = None):
        self.type = listType
        
    def __str__(self):
        return '[]'
    
    def simplify(self):
        return self
        
class Cons(List):
    def __init__(self, itemExpr, listExpr):
        self.item = itemExpr
        self.tail = listExpr 
        
    def __str__(self):
        tail = str(self.tail)
        sep = ', '
        if (tail == '[]'):
            sep = ''
        value = str(self.item)
        try:
            value = str(self.item.simplify())
        except:
            value = str(self.item)
        return '[' + value + sep + tail[1 : -1] + ']' 
    
    def simplify(self):
        return self

class Iterator(List):
    def __init__(self, var, collection):
        self.var = var
        self.collection = collection.simplify()
            
    def simplify(self):
        return self

    def __str__(self):
        return '(' + str(self.var) + ' in ' + str(self.collection) + ')'

class Range(List):
    def __init__(self, start, end, step):
        self.curr = start
        self.end = end
        self.step = step
        self.stop = False
    
    def next(self):
        return self.curr
    
    def apply(self, end):
        self.end = end.simplify()
        if self.curr.value > self.end.value:
            self.step = Int(-1)
        return self
    
    def simplify(self):
        if self.stop:
            return Nil()
        return self
    
    def __str__(self):
        string = '[' + str(self.curr) + ', ' 
        string += str(self.curr.value + self.step.value)
        string += '..'
        string += str(self.end) + ']'
        return string


class Array:
    def __init__(self, items = []):
        self.items = items
        
    def simplify(self):
        return self
    
    def __str__(self):
        tup = []
        for item in self.items:
            if item == None:
                tup.append('')
            else:
                tup.append(str(item.simplify()))
        return '{' + ', '.join(tup) + '}'
        
def length(a):
    xs = tail(a)
    if isinstance(a, Nil):
        return Int(0)
    return Int(length(xs).value + 1)

def head(a):    
    if isinstance(a.simplify(), Object):
         value = a.simplify().state['head'].simplify()
         return value
    if isinstance(a, Nil):
        return Null()
    if isinstance(a, Cons):
        return a.item
    elif isinstance(a, Range):
        return a.next()

def tail(a):
    if isinstance(a.simplify(), Object):
         return a.simplify().state['tail'].simplify()
    if isinstance(a, Nil):
        return Null()
    if isinstance(a, Cons):
        return a.tail
    elif isinstance(a, Range):
        from Operator_Functions import add
        start = add(a.curr, a.step)
        if (a.end != None and (
                a.step.value > 0 and start.value > a.end.simplify().value
                or a.step.value < 0 and start.value < a.end.simplify().value)):
            return Nil()
        end = a.end
        if end != None:
            end = end.simplify()
        return Range(start, end, a.step)

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