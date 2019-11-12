def getData(exp, withVar = True): # withVar tells whether variables should be 
                                  # replaced
    if (exp in variables.keys() and withVar == True):
        return variables[exp] # Returns value of variable
    
    if (exp in ['True','False']): # Checks if input is a bool
        return bool(exp)
    try:
        if (exp[0] == "[" and exp[len(exp)-1] == "]"):
            l = constructList(exp[1:len(exp)-1])
            return l
        if (exp[0] == "(" and exp[len(exp)-1] == ")"):
            l = tuple(exp)
            return l
        if (exp[0] in ["'", "\""] and exp[len(exp)-1] in ["'", "\""]):
                    return exp
    except:
        pass
    try: 
        return int(exp)
    except:
        try: 
            return float(exp)
        except:
            return None
def replaceData(exp):
    #if (type(exp) != list):
    #    return exp
    i = 0
    while (i < len(exp)):
        b = True
        if (i < len(exp) - 1):
            if (exp[i+1] == '='):
                b = False
        value = getData(exp[i], b)
        if (value != None):
            exp[i] = value
        i += 1
    return exp

def constructList(exp):
    l = exp.split(',')
    if (l == ['']):
        return []
    l2 = []
    for elem in l:
        l2.append(haskellEval(elem))
    return l2
