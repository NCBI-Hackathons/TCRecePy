import numpy as np
from itertools import product
from Bio import pairwise2 as pairwise
from Bio.SubsMat import MatrixInfo as matlist

def trivial_cost(c1, c2):
    return 0 if (c1 == c2 and '-' not in (c1,c2)) else 1

def blosum62(c1, c2):
    return matlist.blosum62[(c1, c2)] if '-' not in (c1, c2) else -4

def levenshtein_distance(s1, s2, cost_func=trivial_cost):
    s1 = '-' + s1
    s2 = '-' + s2
    l1,l2 = len(s1), len(s2)
    dist = np.zeros((l1,l2))

    for i in range(1,l1):
        dist[i,0] = dist[i-1,0] + cost_func(s1[i],s2[0])
    for j in range(1,l2):
        dist[0,j] = dist[0,j-1] + cost_func(s1[0],s2[j])

    for i,j in product(range(1,l1), range(1,l2)):
        dist[i,j] = min(
                [
                    dist[i-1,j] + cost_func(s1[i], s2[0]), # deletion
                    dist[i,j-1] + cost_func(s1[0], s2[j]), # addition
                    dist[i-1,j-1] + cost_func(s1[i], s2[j]), # substitution
                    ])

    return dist[l1,l2]

def blosum62_distance(s1, s2, weights=None):
    if len(s1) is not len(s2):
        pairs = pairwise.align.globaldx(s1, s2, matlist.blosum62)
        s1, s2 = sorted(pairs, key=lambda p: p[2])[0][:1]

    if not weights:
        weights = len(s1)*[1]

    cost = 0
    for i in range(len(s1)):
        cost += weights[i] * blosum62(s1[i], s2[i])

    return cost
