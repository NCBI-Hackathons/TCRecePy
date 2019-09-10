import numpy as np
import itertools as it
import operator as op
from tcrecepy.distances import *

def error_evaluation(weights, data, gaps=0):
    N1, N2 = map(len, data)
    Mean1, Mean2, Mean3 = 0, 0, 0
    data1, data2 = data.values()

    for i in range(N1):
        if verbose: print('1, {0:.1f}%'.format(100*(i/N1)))
        for j in range(i+1,N1):
            Mean1 += blosum62_distance(data1[i], data1[j], weights, gaps)
    Mean1 /= N1*N1

    for i in range(N1):
        if verbose: print('2, {0:.1f}%'.format(100*(i/N1)))
        for j in range(N2):
            Mean2 += blosum62_distance(data1[i], data2[j], weights, gaps)
    Mean2 /= N1*N2

    for i in range(N2):
        if verbose: print('3, {0:.1f}%'.format(100*(i/N2)))
        for j in range(i+1,N2):
            Mean3 += blosum62_distance(data2[i], data2[j], weights, gaps)
    Mean3 /= N2*N2

    return (Mean1 + Mean3) / Mean2

def concurrent_error_evaluation(weights, data, gaps=0):
    pass
