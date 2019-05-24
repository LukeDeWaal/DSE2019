import numpy as np
import matplotlib.pyplot as plt


class ControllabilityCurve(object):

    def __init__(self, **kwargs):

        keys = ['CL_h', 'CL_Ah', 'Cm_ac', 'lh', 'c', 'Vh_V', 'x_ac']

        self.CL_h, self.CL_Ah, self.Cm_ac, self.lh, self.c, self.Vh_V, self.x_ac = [None] * len(keys)

        for key, value in kwargs.items():
            if key in keys:
                setattr(self, key, value)
            else:
                raise AttributeError(f'"{key}" is not a valid input!')

        self.__curve = self.__get_control_curve()

    def __get_control_curve(self):

        first_term = (self.CL_h / self.CL_Ah * self.lh / self.c * (self.Vh_V) ** 2) ** (-1)
        second_term = float(first_term) * (self.Cm_ac / self.CL_Ah - self.x_ac)

        return lambda xcg: first_term * xcg - second_term

    def plot(self, fig: plt.figure = None):

        if fig is None:
            fig = plt.figure()

        xrange = np.linspace(0, 1, 100)

        plt.plot(xrange, self.__curve(xrange), 'b-', label='Control Curve')
        plt.xlabel(r'$x_{cg} / c [-]$')
        plt.ylabel(r'$S_{h}/S [-]$')
        plt.grid(True, which='both')
        plt.legend()

        return fig


class StabilityCurve(object):

    def __init__(self, **kwargs):

        keys = ['CL_ah', 'CL_aAh', 'de_da', 'lh', 'c', 'Vh_V', 'x_ac', 'SM']

        self.CL_ah, self.CL_aAh, self.de_da, self.lh, self.c, self.Vh_V, self.x_ac, self.SM = [None] * len(keys)

        for key, value in kwargs.items():
            if key in keys:
                setattr(self, key, value)
            else:
                raise AttributeError(f'"{key}" is not a valid input!')

        self.__curve = self.__get_stability_curve()

    def __get_stability_curve(self):

        first_term = (self.CL_ah / self.CL_aAh * (1 - self.de_da) * self.lh / self.c * self.Vh_V ** 2) ** (-1)
        second_term = float(first_term) * (self.x_ac - self.SM)

        return lambda xcg: first_term * xcg - second_term

    def plot(self, fig: plt.figure = None):

        if fig is None:
            fig = plt.figure()

        xrange = np.linspace(0, 1, 100)

        plt.plot(xrange, self.__curve(xrange), 'r-', label='Stability Curve')
        plt.xlabel(r'$x_{cg} / c [-]$')
        plt.ylabel(r'$S_{h}/S [-]$')
        plt.grid(True, which='both')
        plt.legend()

        return fig


if __name__ == '__main__':

    control_parameters = {
        'CL_h': -1,
        'CL_Ah': 1,
        'lh': 10,
        'c': 1,
        'Vh_V': 1,
        'x_ac': 1,
        'Cm_ac': 0.2
    }

    stability_parameters = {
        'CL_ah': 4.72,
        'CL_aAh': 7.97,
        'de_da': 0.1,
        'lh': 10,
        'c': 1,
        'Vh_V': 1,
        'x_ac': 0.3,
        'SM': 0.05
    }

    Ctr = ControllabilityCurve(**control_parameters)
    Stab = StabilityCurve(**stability_parameters)

    fig = plt.figure()
    Stab.plot(fig)
    Ctr.plot(fig)
