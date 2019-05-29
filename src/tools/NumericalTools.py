import numpy as np
import scipy.linalg
from mpl_toolkits.mplot3d import Axes3D
import matplotlib.pyplot as plt


def linear_least_squares(x, y):
    """
    Linear Least Squares regression
    :param x: X data
    :param y: Y data
    :return: a and b coefficients (ax + b)
    """

    if len(x) != len(y):
        raise IndexError

    x, y = np.array(x), np.array(y)

    x, y = x.reshape((len(x), 1)), y.reshape((len(y), 1))

    A = np.concatenate([x, np.ones((len(x), 1))], axis=1)

    return np.linalg.lstsq(A, y, rcond=None)[0]


def quadratic_least_squares(x, y):
    """
    Quadratic Least Squares regression
    :param x: X data
    :param y: Y data
    :return: a, b and c coefficients (ax^2 + bx + c)
    """

    if len(x) != len(y):
        raise IndexError

    x, y = np.array(x), np.array(y)

    x, y = x.reshape((len(x), 1)), y.reshape((len(y), 1))

    A = np.concatenate([x**2, x, np.ones((len(x), 1))], axis=1)

    return np.linalg.lstsq(A, y, rcond=None)[0]


def line(x, p1, p2):
    """
    Linear Interpolation function between 2 points
    :param x: Point at which to evaluate
    :param p1: Data Point 1
    :param p2: Data Point 2
    :return: Value of the linear interpolation between p1 and p2 evaluated at x
    """

    return (p2[1] - p1[1])/(p2[0] - p1[0])*(x - p1[0]) + p1[1]


def deg_2_rad(angle):
    """
    Convert degrees to radians
    :param angle: Angle in degrees
    :return: Angle in radians
    """
    return angle*np.pi/180.0


def multivariate_plane_fitting(data: np.array, order: int, colour: str = 'b', fig = None):

    # some 3-dim points
    # data = np.random.multivariate_normal(mean, cov, 50)

    # regular grid covering the domain of the data
    X, Y = np.meshgrid(np.linspace(np.min(data[:, 0]), np.max(data[:, 0]), 20),
                       np.linspace(np.min(data[:, 1]), np.max(data[:, 1]), 20))

    XX = X.flatten()
    YY = Y.flatten()

    # 1: linear, 2: quadratic
    if order == 1:
        # best-fit linear plane
        A = np.c_[data[:, 0], data[:, 1], np.ones(data.shape[0])]
        C, _, _, _ = scipy.linalg.lstsq(A, data[:, 2])  # coefficients

        # evaluate it on grid
        Z = C[0] * X + C[1] * Y + C[2]

        # or expressed using matrix/vector product
        # Z = np.dot(np.c_[XX, YY, np.ones(XX.shape)], C).reshape(X.shape)

    elif order == 2:
        # best-fit quadratic curve
        A = np.c_[np.ones(data.shape[0]), data[:, :2], np.prod(data[:, :2], axis=1), data[:, :2] ** 2]
        C, _, _, _ = scipy.linalg.lstsq(A, data[:, 2])

        # evaluate it on a grid
        Z = np.dot(np.c_[np.ones(XX.shape), XX, YY, XX * YY, XX ** 2, YY ** 2], C).reshape(X.shape)


    # plot points and fitted surface
    if fig is None:
        fig = plt.figure()
    ax = fig.gca(projection='3d')
    ax.plot_surface(X, Y, Z, rstride=1, cstride=1, alpha=0.2) if order is not None else None
    ax.scatter(data[:, 0], data[:, 1], data[:, 2], s=50, c=colour)
    plt.xlabel('Power [kW]')
    plt.ylabel('Weight [kg]')
    ax.set_zlabel('SFC [kg/kW-hr]')
    ax.axis('equal')
    ax.axis('tight')
    plt.show()





if __name__ == '__main__':
    pass
    # multivariate_plane_fitting()