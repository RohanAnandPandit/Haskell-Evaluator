from StringFormatting.py import *
result = ""
while (True):
    exp = input("Prelude> ")
    if (exp == ''):
        pass
    elif (exp == '$quit'):
        break
    elif (exp == "$reset"):
        ##print('*')
        variables.clear()
    else:
        #exp = removeUnwantedSpaces(exp)
        exp = separateText(list(exp))
        ##print(exp)
        result = haskellEval2(exp)
        print(result)
