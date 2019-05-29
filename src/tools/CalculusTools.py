import numpy as np


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


def nth_derivative(f, n, h=10e-5):

    fp = derive(f, h=h)

    if n == 1:
        return fp

    elif n == 0:
        return f

    elif n < 0:
        raise ValueError("Can only take positive nonzero integers for n")

    else:
        return nth_derivative(fp, n-1, h=h)


if __name__ == '__main__':

    pass