import numpy as np


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


def derive(f, h=10**(-5)):
    """
    Derive a single variable function
    :param f: function to derive
    :param h: stepsize
    :return: derivative function
    """
    def fp(x):
        return (f(x+h)-f(x))/h

    return fp


def newtons_method(f, x0, maxiter=1000):
    """
    Newtons method for finding roots
    :param f: Function to analyse
    :param x0: starting point
    :param maxiter: maximum iterations
    :return: Root coordinate
    """
    fp = derive(f)
    x = x0
    i = 0
    while True:
        old_x = x
        x = x - f(x)/fp(x)

        if i >= maxiter:
            print("max Iterations Reached")
            break

        if np.abs(old_x - x) <= 10**(-7):
            break

        i += 1

    return x


def deg_2_rad(angle):
    """
    Convert degrees to radians
    :param angle: Angle in degrees
    :return: Angle in radians
    """
    return angle*np.pi/180.0
