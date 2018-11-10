import numpy as np
import itertools as it
import operator as op
from distances import *

def error_evaluation(weights, data, gaps=0):
    N1, N2 = map(len, data)
    M1, M2, M3 = 0, 0, 0
    N1 = len(tumor)
    N2 = len(nontumor)
    
    M1 = 0
    # Calculating M1
    for i in range(N1):
        for j in range(i+1,N1):
            M1 += list(blosum62_distance(data['tumorous'][i],
                                         data['tumorous'][j],
                                         weights, gaps))[0]
    M1 /= N1*N1

    for i in range(N1):
        for j in range(N2):
            M2 += list(blosum62_distance(data['tumorous'][i],
                                         data['benign'][j],
                                         weights, gaps))[0]
    M2 /= N1*N2

    for i in range(N2):
        for j in range(i+1,N2):
            M3 += list(blosum62_distance(data['benign'][i],
                                         data['benign'][j],
                                         weights, gaps))[0]
    M3 /= N2*N2

    M2 = 0
    # Calculating M2
    for i in range(N1):
        for j in range(N2):
            M2 += distance(tumor[i],nontumor[j],weights)
    M2 /= N1*N2

    return (M1 + M3) / M2
