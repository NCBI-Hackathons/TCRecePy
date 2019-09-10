import numpy as np

def nearest_neighbor(test, cancer_data, non_cancer_data, dist):
    """
    Compute the close non-cancer and cancer neighbors to the input to determine the status of the input
    """
    cancer_data = [dist(test, val) for val in cancer_data]
    non_cancer_data = [dist(test, val) for val in non_cancer_data]
    cancer_neighbor = np.mean(sorted(cancer_data)[:5])
    non_cancer_neighbor = np.mean(sorted(non_cancer_data)[:5])

    return cancer_neighbor / non_cancer_neighbor
