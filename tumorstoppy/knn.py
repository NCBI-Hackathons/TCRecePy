import numpy as np
import tensorflow as tf
from sklearn.model_selection import train_test_split
def nearest_neighbor(non_cancer_data, cancer_data):
    """
    Compute the close non-cancer and cancer neighbors to the input to determine the status of the input
    """
    #status is based on the mean of smallest elements of cancer and non_cancer groups
    #sort
    non_cancer_data = sorted(non_cancer_data)
    cancer_data = sorted(cancer_data)

    #choose nearest neighbors
    non_cancer_neighbor = np.mean(non_cancer_data[:2])
    cancer_neighbor = np.mean(cancer_data[:2])

    #etermine cell status
    if non_cancer_neighbor > cancer_neighbor:
        print("Negative")
    else:
        print("Positive")
