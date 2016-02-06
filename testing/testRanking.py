import random, itertools

def order(x):
    """
    returns the order of each element in x as a list.
    """
    L = len(x)
    rangeL = range(L)
    z = itertools.izip(x, rangeL)
    z = itertools.izip(z, rangeL) #avoid problems with duplicates.
    D = sorted(z)
    return [d[1] for d in D]

def rank(x):
    """
    Returns the rankings of elements in x as a list.
    """
    L = len(x)
    ordering = order(x)
    ranks = [0] * len(x)
    for i in range(L):
        ranks[ordering[i]] = i
    return ranks

# for testing
def test():
    L = 4
    x = [random.random() for i in range(L)]
    print(x)
    #x = [7, 6, 19, 10]

    ordering = order(x)
    ranking  = rank(x)
    for i in range(L):
        print(i+1, x[i], ' --- ', ranking[i]+1, ordering[i]+1, x[ordering[i]])

# main

test()