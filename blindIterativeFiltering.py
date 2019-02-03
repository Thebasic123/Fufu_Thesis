import math

IFthreshold = 0.1
def changeThreshold(newThreshold):
    IFthreshold = newThreshold
def initialiseVar(dataMatrix):
    m = len(dataMatrix)     # Number of time intervals
    n = len(dataMatrix[0])  # Number of stock analysts
    initVarSum = 0
    for j in range(n):
        for t in range(m):
            innerSum = 0
            for k in range(n):
                innerSum += dataMatrix[t][k]
            initVarSum += (dataMatrix[t][j] - innerSum/n)**2
    initVar = initVarSum/(m*(n-1))
    return [initVar for i in range(n)]

def initialiseRep(dataMatrix):
    m = len(dataMatrix)     # Number of time intervals
    n = len(dataMatrix[0])  # Number of stock analysts
    return [sum(dataMatrix[t])/n for t in range(m)]

def crFirstIter(dataMatrix, rep, var):
    m = len(dataMatrix)     # Number of time intervals
    n = len(dataMatrix[0])  # Number of stock analysts

    cr = []
    for i in range(n):
        product = 1
        for j in range(n):
            if i == j:
                continue
            innerSum = 0
            for t in range(m):
                innerSum += (dataMatrix[t][i] - rep[t])**2
            product *= math.exp((-innerSum/m)/(2*var[j]))/math.sqrt(2*math.pi*var[j])
        cr.append(product**(1/(n-1)))
    return cr

def crOtherIter(dataMatrix, var):
    m = len(dataMatrix)     # Number of time intervals
    n = len(dataMatrix[0])  # Number of stock analysts

    cr = []
    for i in range(n):
        prod = 1
        for j in range(n):
            if i != j:
                prod *= math.exp(-var[i]/(2*var[j]))/(math.sqrt(2*math.pi*var[j]))
        cr.append(prod)
    return cr


def nextRep(dataMatrix, cr):
    m = len(dataMatrix)     # Number of time intervals
    n = len(dataMatrix[0])  # Number of stock analysts

    rep = []
    crSum = sum(cr)
    for t in range(m):
        s = 0
        for i in range(n):
            s += dataMatrix[t][i]*cr[i]/crSum
        rep.append(s)
    return rep

def nextVar(dataMatrix, rep):
    m = len(dataMatrix)     # Number of time intervals
    n = len(dataMatrix[0])  # Number of stock analysts

    var = []
    for i in range(n):
        s = 0
        for t in range(m):
            s += (dataMatrix[t][i] - rep[t])**2
        var.append(s/m)

    return var



def iterativeFiltering(dataMatrix):
    m = len(dataMatrix)     # Number of time intervals
    n = len(dataMatrix[0])  # Number of stock analysts

    var = initialiseVar(dataMatrix)
    rep = initialiseRep(dataMatrix)
    l = 0

    previousAvgVar = 10000
    currAvgVar = 1000

    while (abs(previousAvgVar - currAvgVar) > IFthreshold):
        previousAvgVar = currAvgVar

        if l == 0:
            cr = crFirstIter(dataMatrix, rep, var)
        else:
            cr = crOtherIter(dataMatrix, var)
        rep = nextRep(dataMatrix, cr)
        var = nextVar(dataMatrix, rep)

        currAvgVar = 0
        for i in var:
            currAvgVar += i/m
        
        newCr = []
        newVar = []
        for i in range(n):
            newCr.append(cr[i]/sum(cr))
            newVar.append(var[i]/sum(var))
        cr = newCr
        var = newVar

        newRep = []
        for t in range(m):
            newRep.append(rep[t]/sum(rep))
        rep = newRep
        #print('i {}: {}, {}, {}'.format(l, cr, rep, var))
        l += 1
    #print('number of iterations: ',l, previousAvgVar, currAvgVar)
    return cr