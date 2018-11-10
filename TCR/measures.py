import numpy as np
import itertools as it
import operator as op
from distances import *

def error_evaluation(weights, data, gaps=0):
    N1, N2 = map(len, data)
    data = data.values()
    M1 = sum(blosum62_distance(data[0], data[0], weights, gaps))
    M2 = sum(blosum62_distance(data[0], data[1], weights, gaps))
    M3 = sum(blosum62_distance(data[1], data[1], weights, gaps))
    return N1*N2*(M1/N1**2+M3/N2**2)/M2
