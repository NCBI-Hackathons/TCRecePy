import numpy as np
import itertools as it
from pathlib import Path

class Data (object):
    def __init__(self, data, classifiers):
        self._files = {}
        self._data = {}

        for i, (obj, key) in enumerate(zip(data, classifiers)):
            if isinstance(obj, str):
                self._files[key] = obj
                self._data[key] = list(self._pull_data(key))
            else:
                self._files[key] = list(obj.files)
                self._data[key] = obj

    def _pull_data(self, key):
        with open(Path(self._files[key]), 'r') as FILE:
            for seq in FILE.readlines():
                yield seq.strip('\n')

    @property
    def files(self):
        return list(self._files.values())

    @property
    def data(self):
        return list(it.chain(*self._data.values()))

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
