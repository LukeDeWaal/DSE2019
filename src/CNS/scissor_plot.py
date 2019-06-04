import numpy as np
import matplotlib.pyplot as plt

import os
import sys
sys.path.insert(0, '\\'.join(os.getcwd().split('\\')[:-1]) + '\\tools')

from GoogleSheetsImport import GoogleSheetsDataImport, SHEET_NAMES, SPREADSHEET_ID


class ControllabilityCurve(object):

    def __init__(self, **kwargs):

        self.__data = GoogleSheetsDataImport(SPREADSHEET_ID, *SHEET_NAMES).get_data()

        self.__curve = self.__get_control_curve()

    def __get_control_curve(self):

        first_term = (self.__data['Aero']['CL_h'] / self.__data['Aero']['CL_A-h'] * self.__data['C&S']['lh'] / self.__data['Aero']['Wing chord'] * (self.__data['Aero']['Vh/V']) ** 2) ** (-1)
        second_term = float(first_term) * (self.__data['Aero']['Cm_ac'] / self.__data['Aero']['CL_A-h'] - self.__data['Aero']['x_ac'])

        return lambda xcg: first_term * xcg - second_term

    def plot(self, fig: plt.figure = None):

        if fig is None:
            fig = plt.figure()

        xrange = np.linspace(-1, 2, 100)

        plt.plot(xrange, self.__curve(xrange), 'b-', label='Control Curve')
        plt.xlabel(r'$x_{cg} / c [-]$')
        plt.ylabel(r'$S_{h}/S [-]$')
        plt.grid(True, which='both')
        plt.legend()

        return fig


class StabilityCurve(object):

    def __init__(self, **kwargs):

        self.__data = GoogleSheetsDataImport(SPREADSHEET_ID, *SHEET_NAMES).get_data()

        self.__curve = self.__get_stability_curve()

    def __get_stability_curve(self):

        first_term = (self.__data['Aero']['CL_alpha_h'] / self.__data['Aero']['CL_alpha_A-h'] * (1 - self.__data['Aero']['de/da']) * self.__data['C&S']['lh'] / self.__data['Aero']['Wing chord'] * self.__data['Aero']['Vh/V'] ** 2) ** (-1)
        second_term = float(first_term) * (self.__data['Aero']['x_ac'] - self.__data['C&S']['SM'])

        return lambda xcg: first_term * xcg - second_term

    def plot(self, fig: plt.figure = None):

        if fig is None:
            fig = plt.figure()

        xrange = np.linspace(-1, 2, 100)

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
