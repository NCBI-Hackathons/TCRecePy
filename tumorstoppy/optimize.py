# Optimization functions
import numpy as np
from scipy.optimize import minimize
import cost_functions # Will be renamed to 'measures'

# TODO
# Load the appropriate data
# Create a partially passed-argument-function
# Optimize based on some randomly chosen weights
# Celebrate

def f(w):
    return sum([x*x for x in w])

w0 = [4] * 13
#f = lambda w : error_evaluation(w,data,verbose=True)

result = minimize(f, w0, method="nelder-mead", options={'xtol': 1e-8, 'disp': True})
print (result)
