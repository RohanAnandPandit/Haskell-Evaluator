# -*- coding: utf-8 -*-
"""
Created on Tue Jun 23 20:381 2020

@author: rohan
"""
from Maybe import Just, Nothing
from Tuple import Tuple

functionNamesList = ['length', 'head', 'tail', 'last', 'concat', 'init', 'maximum',
                 'minimum', 'elem', 'notElem', 'reverse', 'take', 'drop', 'map',
                 'words', 'unwords', 'takeWhile', 'dropWhile', 'zip', 'unzip',
                 'foldl', 'foldr', 'foldl1', 'foldr1', 'and', 'or', 'any', 'all', 'filter', 'sum',
                 'product', 'lookup', 'concatMap', 'splitAt', 'span', 'replicate',
                 'iterate', 'repeat', 'zipWith', 'zip3', 'zipWith3', 'cycle']
class List:
    pass
      
class Nil(List):
    def __init__(self, listType = None):
        self.type = listType
        
    def __str__(self):
        return '[]'
    
    def simplify(self, a, b):
        return self
        
class Cons(List):
    def __init__(self, itemExpr, listExpr, listType = None):
        self.item = itemExpr
        self.tail = listExpr 
        self.type = listType
        
    def __str__(self):
        if (type(self.item) == str):
            tail = str(self.tail)
            return '\"' + self.item + tail[1 : -1] + '\"'
    
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
    
    def simplify(self, state, simplifyVariables):
        from utils import isPrimitive
        
        if (not isPrimitive(self.item)):
            self.item = self.item.simplify(state, simplifyVariables)
        return self

class Iterator(List):
    def __init__(self, cycleList = None, func = None, item = None, iterations = None,
                 iteratorType = None, step = None, end = None, mapFunc = None, current = None):
        self.type = iteratorType
        self.func = func
        self.item = item
        self.iterations = iterations
        self.list = cycleList
        self.current = current
        if (current == None):
            self.current = self.list
        self.step = step
        self.end = end
        self.mapFunc = mapFunc
        if (mapFunc == None):
            from utils import state
            func_id = state['id']
            self.mapFunc = func_id
    
    def getHead(self):
        if (self.type in ('comprehension', 'general')):
            return self.mapFunc.apply(self.item)
        else:
            return self.mapFunc.apply(self.current.item)
               
    def getTail(self):
        if (self.iterations == 0):
            return Nil()
        iterations = None
        if (self.iterations != None):
            iterations = self.iterations - 1
        if (self.type == 'comprehension'):
            return Iterator(item = self.func.apply(self.item), iteratorType = self.type, step = self.step,
                            func = self.func, iterations = iterations, mapFunc = self.mapFunc)
        elif (self.type == 'general'):
            return Iterator(item = self.func.apply(self.item), iteratorType = self.type, 
                            func = self.func, iterations = iterations, mapFunc = self.mapFunc)
        elif (self.type == 'cycle'):
            current = tail(self.current)
            if isinstance(current, Nil):
                current = self.list
            return Iterator(mapFunc = self.mapFunc, cycleList = self.list,
                            current = current, iteratorType = self.type, iterations = iterations)
            
    def simplify(self, a, b):
        return self

    def apply(self, arg1 = None, arg2 = None):
        if (arg1 != None):
            self.start = arg1
        if (arg2 != None):
            self.end = arg2
            self.iterations = int(abs((self.end - self.item) / self.step))
        return self

    def setRange(self, n):
        self.iterations = n
    
    def __str__(self):
        if (self.iterations != None):
            tail = str(self.getTail())[1 : -1]
            sep = ', '
            if (tail == ''):
                sep = ''
            return '[' + str(self.getHead()) + sep + tail + ']'
        if (self.type in ('comprehension', 'general')):
            return '[' + str(self.getHead()) + '..' + ']'   
        if (self.type == 'cycle'):
            return str(self.list)[ : -1] + '...]'
        
def length(a, l = 0):
    xs = tail(a)
    if (isinstance(a, Nil)):
        return l
    elif (isinstance(a, Cons)):
        if (isinstance(a.item, Iterator)):
            return length(xs, l + a.item.iterations)
        return length(xs, l + 1)

def head(a):    
    if (isinstance(a, Nil)):
        return None
    if (isinstance(a, Cons)):
        if (isinstance(a.item, Iterator)):
            return a.item.getHead()
        return a.item

def tail(a):
    if (isinstance(a, Nil)):
        return None
    if (isinstance(a, Cons)):  
        if (isinstance(a.item, Iterator)):
            iterator = a.item.getTail()
            if (isinstance(iterator, Nil)):
                return a.tail
            return Cons(iterator, a.tail)
        return a.tail

def last(a):    
    (x, xs) = (head(a), tail(a)) 
    if (isinstance(a, Nil)):
        return None
    if (isinstance(xs, Nil)):
        return x 
    return last(xs)

def concat(a):
    from Operators import operatorFromString

    return foldl(operatorFromString('++').value, Nil(), a)

def init(a):
    (x, xs) = (head(a), tail(a)) 
    if (isinstance(a, Nil)):
        return None
    elif (isinstance(a, Cons)):
        if (isinstance(xs, Nil)):
            return Nil()
        return Cons(x, init(xs))  

def maximum(a, m = None):
    from utils import isPrimitive
    
    (x, xs) = (head(a), tail(a))

    if (isinstance(a, Nil)):
        return m
    if (not isPrimitive(x)):
        x = x.simplify()
    if (isinstance(a, Cons)):
        if (m == None):
            m = x
        return maximum(xs, max(x, m))
    elif (isinstance(a, Iterator)):
        if (m == None):
            m = x
        if (a.iterations == None):
            if (a.type == 'comprehension' and a.step <= 0):
                return maximum(a.tail, max(x, m))
            return None
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
    elif (isinstance(a, Iterator)):
        if (m == None):
            m = x
        if (a.iterations == None):
            if (a.type == 'comprehension' and a.step >= 0):
                return minimum(a.tail, max(x, m))
            return None
        return minimum(xs, min(x, m))

def elem(a, b):    
    value = a
    (x, xs) = (head(b), tail(b))
    if (isinstance(b, Nil)):
        return False
    elif (isinstance(b, Cons)):
        if (isinstance(b.item, Iterator)):
            if (b.item.iterations == None and b.item.type == 'general'):
                return None
            check = ((value - x) % b.item.step == 0 and x <= value 
                     and (b.item.end == None or value <= b.item.end))
            return check or elem(value, b.tail)
        
        return x == value or elem(value, xs)


def notElem(a, b): 
    return not elem(a, b)

def reverse(a, l = Nil()):
    if (isinstance(a, Nil)):
        return l
    (x, xs) = (head(a), tail(a))
    return reverse(xs, Cons(x, l))
    

def take(a, b):
    n = a
    (x, xs) = (head(b), tail(b))
    if (n <= 0 or isinstance(b, Nil)):
        return Nil()
    if (isinstance(b, Cons)):
        return Cons(x, take(n - 1, xs))
        

def drop(a, b):    
    n = a
    if (n <= 0 or isinstance(b, Nil)):
        return b
    return drop(n - 1, tail(b))

def mapHaskell(a, b):
    from Operator_Functions import dot
    
    func = a
    (x, xs) = (head(b), tail(b))
    if (isinstance(b, Nil)):
        return b
    if (isinstance(b, Cons)):
        if (isinstance(b.item, Iterator)):
            b.item.mapFunc = dot(func, b.item.mapFunc)
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
    if (isinstance(xs, Nil)):
        return x
    return concatenate(x, Cons(' ', unwords(xs)))

def takeWhile(a, b):
    from utils import isPrimitive
    
    func = a
    if (isinstance(b, Nil)):
        return Nil()
    (x, xs) = (head(b), tail(b))
    if (not isPrimitive(x)):
        x = x.simplify()
    if (isinstance(b, Cons)):
        if (func.apply(x)):
            return Cons(x, takeWhile(func, xs))
        return Nil()

def dropWhile(a, b):
    (func, xs) = (a, b)
    if (isinstance(xs, Nil)):
        return Nil()
    elif (isinstance(xs, Cons)):
        if (func.apply(xs.item)):
            return dropWhile(func, tail(xs))
        return xs 


def zipHaskell(a, b):
    from Operators import operatorFromString
    return zipWith(operatorFromString(',').value, a, b)
   
def zip3(a, b, c):
    if (isinstance(a, Nil) or isinstance(b, Nil) or isinstance(c, Nil)):
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
    elif (isinstance(pairs, Cons)):
        tup = unzip(tail(pairs))
        (left, right) = pairs.item.tup
        return Tuple((Cons(left, fst(tup)), Cons(right, snd(tup)))) 
    
    
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
    return foldl(operatorFromString('&&').value, True, a)

def orHaskell(a):
    from Operators import operatorFromString
    return foldl(operatorFromString('||').value, False, a)

def anyHaskell(a, b):
    func = a
    if isinstance(b, Nil):
        return False
    x, xs = head(b), tail(b)
    if (func.apply(x)):
        return True
    return allHaskell(func, xs)

def allHaskell(a, b):
    func = a
    if isinstance(b, Nil):
        return True
    x, xs = head(b), tail(b)
    if (not func.apply(x)):
        return False
    return allHaskell(func, xs)

def filterHaskell(a, b):
    func = a
    if isinstance(b, Nil):
        return b
    x, xs = head(b), tail(b)
    if (func.apply(x)):
        return Cons(x, filterHaskell(func, xs))
    return filterHaskell(func, xs)

def sumHaskell(a):
    from Operators import operatorFromString
    return foldl(operatorFromString('+').value, 0, a)

def product(a):
    from Operators import operatorFromString
    return foldl(operatorFromString('*').value, 0, a)

def lookup(a, b):
    from Prelude import fst, snd
    if isinstance(b, Nil):
        return Nothing()
    tup, pairs = head(b), tail(b)
    if (fst(tup) == a):
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