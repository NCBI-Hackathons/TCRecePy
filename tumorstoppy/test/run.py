from importlib import reload
import numpy as np
import itertools as it
from tumorstoppy import distances, measures, data, knn

data_points = 100
Data = data.Data
cdr3 = data.CDR3_13
cut_cdr3 = Data(
        [
            Data(['./data/processed_data/TumorCDR3s_test/TumorCDR3s_test_13.txt',
                  './data/processed_data/NonTumorCDR3s_test/NonTumorCDR3s_test_13.txt'],
                 ['tumorous', 'benign'], data_points),
            Data(['./data/processed_data/TumorCDR3s_training/TumorCDR3s_training_13.txt',
                  './data/processed_data/NonTumorCDR3s_training/NonTumorCDR3s_training_13.txt'],
                 ['tumorous', 'benign'], data_points),
            ],
        ['test', 'training'],
        )
error_evaluation = measures.error_evaluation
distance = distances.blosum62_distance

#print(error_evaluation(None, cdr3['training'], verbose=True))
weights = np.array([ 8.31503303,  6.3603994 ,  2.26271026, -1.51866793,  7.5740573 ,
       7.66745514,  4.72895374,  1.29182651,  6.50981513,  3.79679703,
       6.12735646,  1.11650591,  1.27719528])

def dist(s1, s2):
    return distance(s1, s2, weights)

results = []
for seq in cut_cdr3['test','tumorous']:
    print('Testing ' + seq)
    results.append(knn.nearest_neighbor(seq, *cut_cdr3['training'], dist))

results = np.array(results)

success = results[results>1]
failure = results[results<1]

print(len(success)/len(failure))
