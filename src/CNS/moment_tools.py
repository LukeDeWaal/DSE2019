import numpy as np


def shift_moment_at_point(Cm0: float, Cn: float, Ct: float, p0: tuple, p1: tuple, c: float = 1.0):
    return Cm0 + Cn*(p1[0] - p0[0])/c - Ct*(p1[1] - p0[1])/c

