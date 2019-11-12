def separateText(exp):
    separators = ['&&', '||',' ','++' ,'+', '*', '|', '-', ':', '<', '>','<=',
                  '>=','/','=', '==', '^', '/='] # Haskell symbols
    i = 0
    while (i < len(exp)):
        char = exp[i] # current character
        if (''.join(exp[i:i+2]) in separators): # Checks two consecutive chars
            # Concatenates three sections by recursively calling on remaining
            return exp[0:i] + [''.join(exp[i:i+2])] + separateText(exp[i+2:])
        
        elif (char in separators): # Now checks the single character
            
            if (char == ' '):
                sep = [] # Spaces are not included in final list
            else:
                sep = [char] # The operator/symbol
                
            return exp[0:i] + sep + separateText(exp[i+1:])
        
        else:
            if (i > 0): # If char is not a symbol then
                exp[i-1] += char # it is concatenated to the previous element
                del exp[i] # and the char is deleted from the list
                return separateText(exp) # Function called on this new list
        i += 1
    return exp
