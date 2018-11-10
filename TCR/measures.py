import numpy as np
import itertools as it
import operator as op
from distances import *

def error_evaluation(weights, data, gaps=0):
    N1, N2 = map(len, data)
    Mean1, Mean2, Mean3 = 0, 0, 0

    for i in range(N1):
        for j in range(i+1,N1):
            Mean1 += list(blosum62_distance(data['tumorous'][i],
                                         data['tumorous'][j],
                                         weights, gaps))[0]
    Mean1 /= N1*N1

    for i in range(N1):
        for j in range(N2):
            Mean2 += list(blosum62_distance(data['tumorous'][i],
                                         data['benign'][j],
                                         weights, gaps))[0]
    Mean2 /= N1*N2

    for i in range(N2):
        for j in range(i+1,N2):
            Mean3 += list(blosum62_distance(data['benign'][i],
                                         data['benign'][j],
                                         weights, gaps))[0]
    Mean3 /= N2*N2

    return (Mean1 + Mean3) / Mean2
