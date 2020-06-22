# -*- coding: utf-8 -*-
"""
Created on Mon Nov 18 15:43:13 2019

@author: rohan
"""
def AND(a, b):
    return (a and b)

def OR(a, b):
    return (a or b)

def head(l):
    if (len(l) == 0):
        return None
    else:
        return l[0]
        
def tail(l):
    if (len(l) == 0):
        return None
    else:
        return l[1:]
        
def length(l):
    return len(l)

def concat(*lists):
    final = lists[0]
    for l in lists[1:]:
        final += l
    return final

def init(l):
    if (len(l) == 0):
        return None
    else:
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

def take(n, l):
    if (n > len(l)):
        return None
    else: 
        return l[:n] 

def drop(n, l):
    if (n > len(l)):
        return None
    else: 
        return l[n:]

def map2(func, l):
    return list(map(func,l))

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
    return x+1

def pred(x):
    return x-1

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
    