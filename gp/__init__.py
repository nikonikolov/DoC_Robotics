import collections
import math

from gp import data
from matplotlib import pyplot as plt
import numpy as np
from numpy import random
from numpy import linalg
from sklearn import decomposition


GPResult = collections.namedtuple("GPResult", ["mean", "covariance"])


def cov(fa, fb):
    """Computes the squared exponential covariance matrix."""
    assert fa.ndim == fb.ndim
    if fa.ndim == 1:
        return np.exp(- 1 / 2 * np.sum((fa - fb) ** 2))
    elif fa.ndim == 2:
        return np.array(
                [[np.exp(- 1 / 2 * linalg.norm(a - b) ** 2) for b in fb]
                 for a in fa])


def random_sample(mean, covariance_matrix):
    """Obtain a random sample from a multivariate gaussian."""
    L = linalg.cholesky(covariance_matrix)
    u = np.array([random.normal(0, 1) for _ in range(len(mean))])
    return mean + L.dot(u)


def main():
    """For testing purposes only, plot the "learned" Gaussian distribution."""
    gp_x, gp_y = predict(data.test_angles)
    pca = decomposition.PCA()
    pca.fit(data.test_angles)
    xs = [random_sample(gp_x.mean, gp_x.covariance)
          for _ in range(5)]
    print xs
    return
    ys = [random_sample(gp_y.mean, gp_y.covariance)
          for _ in range(5)]
    return 0



    plt.figure()
    plt.title("Prior")
    intervals = np.array([np.sqrt(prior_variance[i, i])
                          for i in range(len(xs))])
    plt.fill_between([x[0] for x in xs],
                     prior_mean + intervals,
                     prior_mean - intervals, facecolor="yellow", alpha=0.3)
    plt.grid()
    plt.plot(xs, prior_ys)

    plt.figure()
    plt.grid()
    for ys in posterior_ys:
        plt.plot(xs, ys)
    intervals = np.array([np.sqrt(posterior_cov_matrix[i, i])
                          for i in range(len(xs))])
    print(intervals.shape)
    print(posterior_mean.shape)
    plt.fill_between([x[0] for x in xs],
                     posterior_mean + intervals,
                     posterior_mean - intervals,
                    facecolor="yellow", alpha=0.3)
    plt.plot([a[0] for a in X], Y, "x")
    plt.show()


def predict(test_angles):
    # Makes sure that test_angles is the M by N matrix before we run through the procedure.
    test_angles = np.array(list(test_angles))
    original_dimension = test_angles.ndim
    if test_angles.ndim == 1:
        test_angles = np.array([list(test_angles)])

    x_prior_mean = np.zeros(test_angles.shape)
    x_prior_cov_matrix = cov(test_angles, test_angles) + 0.0001 * np.eye(test_angles.shape[0])
    y_prior_mean = np.zeros(test_angles.shape)
    y_prior_cov_matrix = cov(test_angles, test_angles) + 0.0001 * np.eye(test_angles.shape[0])
    x_posterior_mean = cov(test_angles, data.angles).dot(
            linalg.inv(cov(data.angles, data.angles))).dot(data.x)
    y_posterior_mean = cov(test_angles, data.angles).dot(
            linalg.inv(cov(data.angles, data.angles))).dot(data.y)
    x_posterior_cov_matrix = cov(test_angles, test_angles) - cov(test_angles, data.angles).dot(
            linalg.inv(cov(data.angles, data.angles))).dot(cov(data.angles, test_angles))
    # recall that posterior covariance matrix is independent of the target values
    y_posterior_cov_matrix = x_posterior_cov_matrix

    return (GPResult(mean=x_posterior_mean, covariance=x_posterior_cov_matrix),
            GPResult(mean=y_posterior_mean, covariance=y_posterior_cov_matrix))


if __name__ == "__main__":
    main()
