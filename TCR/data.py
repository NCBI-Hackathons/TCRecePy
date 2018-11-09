import numpy as np
from pathlib import Path

def pull_sequences(fname):
    with open(Path('./data/' + fname), 'r') as FILE:
        for line in FILE.readlines():
            yield line.strip('\n')

# Amino Acid dictionary
AA = np.genfromtxt(
        Path('./data/AAindex_544nr.csv'),
        delimiter=',', names=True)

TR_DATA = {}
TE_DATA = {}

TR_DATA['tumor'] = list(pull_sequences('TumorCDR3s_training.txt'))
TE_DATA['tumor'] = list(pull_sequences('TumorCDR3s_test.txt'))

TR_DATA['normal'] = list(pull_sequences('NonTumorCDR3s_training.txt'))
TE_DATA['normal'] = list(pull_sequences('NonTumorCDR3s_test.txt'))
