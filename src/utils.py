# -*- coding: utf-8 -*-
"""
Created on Mon Jun 22 11:24:28 2020

@author: rohan
"""
operators = ['&&', '||',' ','++' ,'+', '*', '|', '-', ':', '<', '>','<=',
              '>=','/','=', '==', '^', '/=', '`', '..', "\"", '(', ')', ',', '[', ']', ' '] # Haskell symbols

functions = {'fst' : 1, 'snd' : 1, 'pred' : 1, 'succ' : 1,'length' : 1,'head': 1, 'tail' : 1, 'even' : 1, 'odd' : 1, 'maximum' : 1,
             'minimum' : 1, 'init' : 1, 'words' : 1, 'unwords':1, 'reverse' : 1, 'concat' : 1, 'take': 2, 'drop' : 2, 
             'div' : 2, 'mod' : 2,'take' : 2, 'elem' : 2, 'notElem' : 2, 'takeWhile':2, 'dropWhile':2, 'map':2, '&&' : 2, '||' : 2}

digitChar = ['0','1','2','3','4','5', '6', '7', '8','9'] 
closer = {'[' : ']', '(' : ')'}
brackets = ['[', ']','(', ')']


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

def closingQuote(exp):    
    index = 0
    insideString = False
    for char in exp:
        if (char == "\""):
            if (insideString):
                return index
        if (char == "\""):
            insideString = True
        index += 1
    return None

def balancedBrackets(c, exp):
    count = 0
    for char in exp:
        if (char == c):
            count += 1
        elif (char == closer[c]):
            if (count == 0):
                return False
            else:
                count -= 1
    return count == 0


def splitAtCommas(exp):
    brackets = 0
    for i in range(0, len(exp)):
        char = exp[i]
        if (char in ["[", '(']):
            brackets += 1
        elif (char in [']', ')']):
            brackets -= 1
        elif (char == ',' and brackets == 0):
            return [exp[0:i]] + splitAtCommas(exp[i + 1:])
    return [exp]
    
    
def removeSpaces(exp):
    l = []
    for char in exp:
        if (char != " "):
            l.append(char)
    return ''.join(l)



            
def getString(c, exp):
    index = 0
    count = -1
    for char in exp:
        if (char == c and count == 0):
            return index
        if (char == c):
            count += 1
        index += 1
            
     
def removeUnwantedSpaces(exp):
    exp = list(exp)
    i = 0
    prev = " "
    l = len(exp)
    while (i < l):
        current = exp[i]
        if (current == " " and prev in [" ", ',']):
            del exp[i]
            l -= 1
            pass
        else:
            prev = current
            i += 1
    return "".join(exp)

def removeSpaceAroundOperators(exp):
    from Haskell_Evaluate import operators
    i = 0
    l = len(exp)
    while (i < l):
        string = exp[i]
        if string in operators:
            if (string not in brackets):
                if (i > 0):
                    if (exp[i - 1] == " "):
                        del exp[i - 1]
                        i -= 1
                        l -= 1
                if (i < l - 1):
                    if (exp[i + 1] == " "):
                        del exp[i + 1]
                        i -= 1
                        l -= 1
        i += 1
    return ''.join(exp)

def getData(exp, variables = None): # withVar tells whether variables should be replaced
    functionMap = {'map':'map2', '&&' : 'AND', '||' : 'OR'}
    if (exp == ''):
        return None
    if (type(exp) in [list, tuple, int, float, bool]):
        return exp
    elif (exp in functions.keys()):
        from Operators import operatorFromString
        return operatorFromString(exp)
    elif (exp in ['True', 'False']): # Checks if input is a bool
        return bool(exp)
    elif (variables != None and exp in variables.keys()):
        return variables[exp] # Returns value of variable
    elif (exp[0] == "[" and exp[-1] == "]"):
        l = constructList(exp[1 :-1], variables)
        return l
    elif (exp[0] == "(" and exp[-1] == ")"):
        tup = tuple(exp)
        return exp
    elif (exp[0] in ["'", "\""] and exp[-1] in ["'", "\""]):
        return exp[1 : -1]
    try: 
        return int(exp)
    except:
        try: 
            return float(exp)
        except:
            return exp

    