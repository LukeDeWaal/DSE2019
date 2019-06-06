import numpy as np
import matplotlib.pyplot as plt

import os
import sys
sys.path.insert(0, '\\'.join(os.getcwd().split('\\')[:-1]) + '\\tools')

from GoogleSheetsImport import GoogleSheetsDataImport, SHEET_NAMES, SPREADSHEET_ID


class ControllabilityCurve(object):

    def __init__(self):

        self.__data = GoogleSheetsDataImport(SPREADSHEET_ID, *SHEET_NAMES).get_data()

        self.__curve = self.__get_control_curve()

    def __get_control_curve(self, canard=False):

        chord = self.__data['Aero']['Wing chord']
        xlemac = (self.__data['C&S']['Wing'][0]-1)/chord
        xac = xlemac + self.__data['Aero']['x_ac']

        lh = self.__data['C&S']['H Wing'][0] - self.__data['C&S']['Wing'][0]

        coefficient = 1.0/(self.__data['Aero']['CL_h']/self.__data['Aero']['CL_A-h'] * self.__data['Aero']['Vh/V']**2 * lh/chord)

        first_term = lambda xcg: coefficient*xcg
        second_term = (self.__data['Aero']['Cm_ac']/self.__data['Aero']['CL_A-h'] - xac)*coefficient
        thrust_term = self.__data['FPP']['Tc']/self.__data['Aero']['CL_A-h']*(2*(self.__data['FPP']['Prop Diameter [m]']**2)/self.__data['FPP']['S [m^2]'])*(self.__data['C&S']['Engine'][1] - self.__data['C&S']['Wing'][1])/chord*coefficient

        if canard:
            canard_term = self.__data['Aero']['CL_c']/self.__data['Aero']['CL_A-h']*self.__data['C&S']['Sc']/self.__data['FPP']['S [m^2]']*((self.__data['C&S']['Canard'][0]-1)/chord - xac)
        else:
            canard_term = 0

        return lambda xcg: first_term(xcg) + second_term - thrust_term - canard_term

    def plot(self, fig: plt.figure = None):

        if fig is None:
            fig = plt.figure()

        xrange = np.linspace(0, 3, 100)

        plt.plot(xrange, self.__curve(xrange), 'b-', label='Control Curve')
        plt.xlabel(r'$x_{cg} / MAC [-]$')
        plt.ylabel(r'$S_{h}/S [-]$')
        plt.grid(True, which='both')
        plt.legend()

        return fig


class StabilityCurve(object):

    def __init__(self):

        self.__data = GoogleSheetsDataImport(SPREADSHEET_ID, *SHEET_NAMES).get_data()

        self.__curve = self.__get_stability_curve()
        self.__xlemac = self.__data['C&S']['Wing'][0]

    def __get_stability_curve(self, canard=False):

        chord = self.__data['Aero']['Wing chord']
        xlemac = (self.__data['C&S']['Wing'][0]-1)/chord
        xac = xlemac + self.__data['Aero']['x_ac']
        SM = self.__data['C&S']['SM']

        lh = self.__data['C&S']['H Wing'][0] - self.__data['C&S']['Wing'][0]

        if canard:
            denominator = lambda xcg: self.__data['Aero']['CL_alpha_h']/self.__data['Aero']['CL_alpha_A-h']*(self.__data['Aero']['Vh/V']**2)*(1-self.__data['Aero']['de/da'])*(xcg + SM - (self.__data['C&S']['H Wing'][0]-1)/chord)
            first_term = lambda xcg: (xcg + SM)*(1 + self.__data['Aero']['CL_alpha_c']/self.__data['Aero']['CL_alpha_A-h']*self.__data['C&S']['Sc']/self.__data['FPP']['S [m^2]'])
            second_term = xac + (self.__data['C&S']['Canard'][0]-1)/chord*self.__data['Aero']['CL_alpha_c']/self.__data['Aero']['CL_alpha_A-h']*self.__data['C&S']['Sc']/self.__data['FPP']['S [m^2]']
            return lambda xcg: -(first_term(xcg) - second_term)/denominator(xcg)

        else:
            CL_ratio = -(self.__data['Aero']['CL_alpha_A-h']/self.__data['Aero']['CL_alpha_h'])
            coefficient = 1/((1-self.__data['Aero']['de/da'])*(self.__data['Aero']['Vh/V']**2))

            return lambda xcg: coefficient*CL_ratio*(xcg+SM-xac)/(xcg+SM-(self.__data['C&S']['H Wing'][0]-1)/chord)

    def plot(self, fig: plt.figure = None):

        if fig is None:
            fig = plt.figure()

        xrange = np.linspace(0, 3, 100)

        plt.plot(xrange, self.__curve(xrange), 'r-', label='Stability Curve')
        plt.xlabel(r'$x_{cg} / MAC [-]$')
        plt.ylabel(r'$S_{h}/S [-]$')
        plt.grid(True, which='both')
        plt.ylim(0, 1.0)
        plt.title(f'Wing @ {round((self.__xlemac - 1)/self.__data["Structures"]["Max_fuselage_length"], 2)*100} % fuselage')
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

    Ctr = ControllabilityCurve()
    Stab = StabilityCurve()

    fig = plt.figure()
    Stab.plot(fig)
    Ctr.plot(fig)
