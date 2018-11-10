from importlib import reload
import numpy as np
import itertools as it
<<<<<<< HEAD
import distances
import measures
import data
=======
from tumorstoppy import distances, measures, data
>>>>>>> 0ac875c... fixed setup.py

cdr3 = data.CDR3_13
error_evaluation = measures.error_evaluation
#print(error_evaluation(None, cdr3['training'], verbose=True))
