import numpy as np
import itertools as it
import operator as op
from distances import *

def error_evaluation(weights, data, gaps=0):
    N1, N2 = map(len, data)
    data = data.values()
    M1 = it.accumulate(
            blosum62_distance(data[0], data[0], weights, gaps),
            op.add)[-1] / (N1*N1)
    M2 = it.accumulate(
            blosum62_distance(data[0], data[1], weights, gaps),
            op.add)[-1] / (N1*N2)
    M3 = it.accumulate(
            blosum62_distance(data[1], data[1], weights, gaps),
            op.add)[-1] / (N2*N2)
    return (M1+M3)/M2

def undefined_cost_function (tumor, nontumor, weights):
    # tumor and nontumor are lists of strings
    # weights is a list of floating point numbers
    N1 = len(tumor)
    N2 = len(nontumor)
    
    M1 = 0
    # Calculating M1
    for i in range(N1):
        for j in range(i+1,N1):
            M1 += distance(tumor[i],tumor[j],weights)
    M1 /= N1*N1

    M3 = 0
    # Calculating M3
    for i in range(N2):
        for j in range(i+1,N2):
            M3 += distance(nontumor[i],nontumor[j],weights)
    M3 /= N2*N2

    M2 = 0
    # Calculating M2
    for i in range(N1):
        for j in range(N2):
            M2 += distance(tumor[i],nontumor[j],weights)
    M2 /= N1*N2

    return (M1 + M3) / M2
