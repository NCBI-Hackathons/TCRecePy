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
                self._data[key] = list(it.zip_longest(self._pull_data(key),
                                                      [], fillvalue=key))
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

    def __getitem__(self, keys=None):
        if isinstance(keys, tuple):
            return self._data[keys[0]].__getitem__(*keys[1:])
        else:
            return self._data[keys]

# Amino Acid dictionary
AA = np.genfromtxt(
        Path('./data/AAindex_544nr.csv'),
        delimiter=',', names=True)

CDR3 = Data(
        [
            Data(['./data/TumorCDR3s_test.txt','./data/NonTumorCDR3s_test.txt'],
                 ['tumorous', 'benign']),
            Data(['./data/TumorCDR3s_training.txt','./data/NonTumorCDR3s_training.txt'],
                 ['tumorous', 'benign'])
            ],
        ['test', 'training'],
        )
