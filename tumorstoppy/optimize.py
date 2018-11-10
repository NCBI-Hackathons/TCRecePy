# Optimization functions
import numpy as np
from scipy.optimize import minimize
from measures import *
from data import *

# TODO
# Load the appropriate data
# Create a partially passed-argument-function
# Optimize based on some randomly chosen weights
# Celebrate

def f(w):
    return sum([x*x for x in w])

data_points = 100

CDR3_13 = Data(
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

w0 = [4] * 13
f = lambda w : error_evaluation(w,CDR3_13['training'],verbose=True)

result = minimize(f, w0, method="nelder-mead", options={'xtol': 1e-8, 'disp': True})
print (result)

# print(error_evaluation(None,CDR3_13['training'],verbose=True))
