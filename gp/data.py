import numpy as np


# The angluar features. From 0.0, 10.0, 20.0, ..., 350.0 ?
angles = np.array([
        [0.01, 0.00, 0.00],
        [0.00, 0.01, 0.02],
        [0.00, 0.00, 0.01]])

# The training data for the regression values to learn
x = np.array([1.0, 2.0, 3.0])
y = np.array([1.0, 2.0, 3.0])

# M is the number of examples
M = angles.shape[0]

# N is the number of features
N = angles.shape[1]

# Angles for testing / plotting / demo purposes.
test_angles = np.array([
        [0.0, 0.01, 0.02],
        [0.0, 0.01, 0.02]])

# Data consistency test
assert test_angles.shape[1] == angles.shape[1]
assert x.shape[0] == angles.shape[0]
assert y.shape[0] == angles.shape[0]
