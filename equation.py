#-------------------------------------------------------------------------------
# Name:        module2
#-------------------------------------------------------------------------------
import string, re

def isValidTerm(term):
    # assume it is term and all checks are already done like in form 5x
    pass

##def splitEq(equation):
##    return [ item.strip() for item in  re.split(r',|\+|\.|\-|\*|/', equation) ]
operators  = ('+','-','/','*', '=')

def splitEq(eq):
    global operators
    c = ''
    s = [c for c in eq if c != ' ' ]
##    s = ''.join(s)
##    print(s)
    term = []
    equation = []
    operators  = ['+','-','/','*', '=']
    for item in s:
        term.append(item)
        if item in operators:
##            print(item)
            term.pop()
            s = ''.join(term)
            equation.append(s)
            equation.append(item)
            term = []

    equation.append(''.join(term))
    return equation



def cof(term):
    # to get coefficient
    # check term has a variable i.e any [a-z][A-Z]
    if isinstance(term, (int,)) or term is None:
        return term
    if term.isdigit():
        try:
            num = int(term)
            return num
        except ValueError:
            print("Error in converting str to int")
            return None

    if isinstance(term, str) and term[-1] in string.ascii_letters: # ends with any
        term = term.strip()

        if len(term) == 1 and term.isalpha():
            return 1 # to handle special case when we have coefficient 1 i.e. x only

        # check if term contain multiple alphabets
        if sum(1 for c in term if c.isalpha())  >1 :
            print("Invalid Term: %s" % term)
            return None
        else:
            # split
            last = term[-1]
            q = term.split(last)
##            print(q)
            return(q[0])
    else:
        operator = term[0]
        try:
            num = int(term[1:])
            if operator == '+':
                return num
            elif operator == '-':
                return num * -1
        except ValueError:
            print("Error in converting str to int")
            return None


##print (cof(5) )
##print (cof('10') )
##print (cof('25x') )
##print (cof('25yy') )
##print (cof('30y') )
##print (cof('x30') )
##print (cof('3t0') )
##print (cof('xx30') )
##print (cof('3tx0') )


def joinSymbols(splitEquation):
    global operators
    term = []
    newEquation = []
    newEquation.append(splitEquation[0])
    for item in splitEquation[1:]:
        if item in operators:
            lastOperator = item
            continue
        item = lastOperator + item
        newEquation.append(item)

    return newEquation

def solveEquation(equation):
    splitEquation = splitEq(equation)
    print("Split: ", splitEquation)
    newEquation = joinSymbols(splitEquation)
    print(newEquation)

    xterm = []
    cterm = []
    for item in newEquation:
        if item.isupper() or item.islower():
            xterm.append(item)
        else:
            cterm.append(item)

    print (cterm)
    print (xterm)
    sumcterm = sum([int (cof( item)) for item in cterm])
    sumxterm = sum([int (cof( item)) for item in xterm])
    print('%s%s' % (''.join(xterm), ''.join(cterm)))
    print('%sx %s' % (sumxterm, ('+ ' + str(sumcterm)) if sumcterm>0 else  sumcterm))
    print('x = %s/%s' % (sumcterm, sumxterm))
    ##item = '+20'
    ##print(cof(item))


e1 = '5x - 7x - 200-10 - 27x'
##e1 = '5x + 7x + 20-10 / 30x * 50 * 40-39*x*20 / 30t+40x/40'
solveEquation(e1)
e2 = '5x + 7x + 20-100- 30x + 50x +40-39'
solveEquation(e2)


def main():
    pass

if __name__ == '__main__':
    main()
