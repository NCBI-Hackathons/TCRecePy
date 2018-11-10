import numpy as np
from scipy.optimize import minimize

def x_squared (x):
    return x[0]*x[0] + x[1]*x[1]

res = minimize(x_squared, [5,5], method='nelder-mead', options={'xtol': 1e-8, 'disp': True})

print(res.x)
