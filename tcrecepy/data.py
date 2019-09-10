import numpy as np
import itertools as it
from pathlib import Path

class Data (object):
    """
    Represents collections of data retreived from files.

    Data is an immutable, dictionary-like structure, so subsets of data
    within it are represented by keys.

    Parameters
    ==========
    data : iterable of data objects. If this object is a string, it assumed
           that the string represents the path of a file to retrieve data from.
           Objects that are not strings should be iterables,
           such as other objects of type Data.
    keys : iterable of strings representing the keys used to classify
           objects in the above data array.

    Examples
    ========
    >>> from tcrecepy.data import Data
    >>> paths = ['./file1', './file2']
    >>> seqs = Data(paths, ['seq1', 'seq2'])
    >>> seqs['seq1']
    array([
        # data elements aquired from './file1'
        ...
        ], dtype='<U30')
    >>> seqs.data
    array([
        # data elements aquired from both './file1' and './file2'
        ...
        ], dtype='<U30')
    >>> seqs.files
    [ './file1', './file2' ]
    >>> new_paths = ['./file3', './file4']
    >>> new_seqs = Data(new_paths, ['seq3', 'seq4'])
    # You can use Data objects to build a superset of data
    >>> all_data = Data([seqs, new_seqs], ['old', 'new'])
    >>> all_data['new', 'seq4']
    array([
        # data elements aquired from './file4'
        ...
        ], dtype='<U30')
    """
    def __init__(self, data, keys, lines=None):
        self._files = {}
        self._data = {}

        for i, (obj, key) in enumerate(zip(data, keys)):
            if isinstance(obj, str):
                self._files[key] = obj
                self._data[key] = np.fromiter(self._pull_data(key,lines), '<U30')
            else:
                self._files[key] = list(obj.files)
                self._data[key] = obj

    def _pull_data(self, key, lines=None):
        with open(Path(self._files[key]), 'r') as FILE:
            if lines == None:
                for seq in FILE.readlines():
                    yield seq.strip('\n')
            else:
                for i in range(lines):
                    yield FILE.readline().rstrip('\n')

    @property
    def files(self):
        return list(self._files.values())

    @property
    def data(self):
        try:
            return np.fromiter(it.chain(*self._data.values()), '<U30')
        except ValueError:
            return self.values()

    def values(self):
        return list(self._data.values())

    def keys(self):
        return list(self._data.keys())

    def __getitem__(self, keys=None):
        if isinstance(keys, tuple):
            return self._data[keys[0]].__getitem__(*keys[1:])
        else:
            return self._data[keys]

    def __len__(self):
        return len(self._data)

    def __iter__(self):
        return (val for val in self.values())

# Amino Acid dictionary
AA = np.genfromtxt(
        Path('./data/AAindex_544nr.csv'),
        delimiter=',', names=True)

CDR3 = Data(
        [
            Data(['./data/TumorCDR3s_test.txt',
                  './data/NonTumorCDR3s_test.txt'],
                 ['tumorous', 'benign']),
            Data(['./data/TumorCDR3s_training.txt',
                  './data/NonTumorCDR3s_training.txt'],
                 ['tumorous', 'benign'])
            ],
        ['test', 'training'],
        )

CDR3_13 = Data(
        [
            Data(['./data/processed_data/TumorCDR3s_test/TumorCDR3s_test_13.txt',
                  './data/processed_data/NonTumorCDR3s_test/NonTumorCDR3s_test_13.txt'],
                 ['tumorous', 'benign']),
            Data(['./data/processed_data/TumorCDR3s_training/TumorCDR3s_training_13.txt',
                  './data/processed_data/NonTumorCDR3s_training/NonTumorCDR3s_training_13.txt'],
                 ['tumorous', 'benign']),
            ],
        ['test', 'training'],
        )
