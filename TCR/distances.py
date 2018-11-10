import numpy as np
import itertools as it
from warnings import warn
from Bio import pairwise2
from Bio.SubsMat import MatrixInfo as matlist

def sigmoid (z):
    """
    The sigmoid, or logistic, function defined for all real numbers z.
    Returns values on the interval [0., 1.] and is bijective.
    """
    return 1 / (1+np.exp(z))

def blosum62_score(s1, s2):
    """
    Compute the score between two sequences defined by the blosum62 matrix.
    The score measures the similarity between sequences
    and ranges from -4 to 11.

    Returns a generator of the list of scores with each element corresponding
    to the score of each character of the sequences.
    """
    for pair in zip(s1,s2):
        try:
            if pair in matlist.blosum62.keys():
                yield matlist.blosum62[pair]
            else:
                yield matlist.blosum62[list(pair).reverse()]
        except KeyError as err:
            warn('unknown amino acid substitution encountered: {}'\
                    .format(*err.args),
                 RuntimeWarning, stacklevel=2)
            yield -4

def blosum62_distance(seqs1, seqs2, weights=None, allowed_gaps=0):
    """
    Returns the distances between each pair of sequences as measured
    by a logistic function on the domain [0.,1.].
    A distance of 0. implies the sequences are the same, while
    a distance of 1. implies that the sequences are infinitely different.
    """
    for s1, s2 in zip(seqs1, seqs2):
        if 0 in (len(s1), len(s2)):
            warn('empty sequence passed', RuntimeWarning, stacklevel=2)
            yield 1.
        elif len(s1) is not len(s2):
            # sort the pairs that we recieve by their unweighted scores.
            pairs = pairwise2.align.globaldx(s1, s2, matlist.blosum62)\
                        .sort(key=lambda p: p[2], reverse=True)
            try:
                # eliminate matches that don't match our criteria.
                s1, s2 = it.filterfalse(
                        lambda p: p[0].count('-') is not allowed_gaps,
                        pairs,
                        )[0][:2]
            except (IndexError, TypeError):
                # thrown in the case it.filterfalse returns an empty list.
                warn('insufficient or invalid number of allowed gaps',
                     RuntimeWarning, stacklevel=2)
                yield 1.
        if weights is None:
            weights = np.array(len(s1)*[1])
        elif len(weights) is not len(s1):
            raise ValueError('not enough weights for test data')
        elif not isinstance(weights, (list,tuple)):
            weights = np.array(weights)
        yield sigmoid(weights @ np.fromiter(blosum62_score(s1,s2),int))
