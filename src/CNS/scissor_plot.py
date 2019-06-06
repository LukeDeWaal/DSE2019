import numpy as np
import matplotlib.pyplot as plt

import os
import sys
sys.path.insert(0, '\\'.join(os.getcwd().split('\\')[:-1]) + '\\tools')

from GoogleSheetsImport import GoogleSheetsDataImport, SHEET_NAMES, SPREADSHEET_ID


class ControllabilityCurve(object):

    def __init__(self, canard=False):

        self.canard = canard
        self.__data = GoogleSheetsDataImport(SPREADSHEET_ID, *SHEET_NAMES).get_data()

        self.__curve = self.__get_control_curve()

    def __get_control_curve(self):

        # Common items in formulas
        chord = self.__data['Aero']['Wing chord']
        xlemac = (self.__data['C&S']['Wing'][0]-1)/chord
        xac = xlemac + self.__data['Aero']['x_ac']

        lh = self.__data['C&S']['H Wing'][0] - self.__data['C&S']['Wing'][0]

        # Shorten some code by defining this coefficient
        coefficient = 1.0/(self.__data['Aero']['CL_h']/self.__data['Aero']['CL_A-h'] * self.__data['Aero']['Vh/V']**2 * lh/chord)

        first_term = lambda xcg: coefficient*xcg
        second_term = (self.__data['Aero']['Cm_ac']/self.__data['Aero']['CL_A-h'] - xac)*coefficient
        thrust_term = self.__data['FPP']['Tc']/self.__data['Aero']['CL_A-h']*(2*(self.__data['FPP']['Prop Diameter [m]']**2)/self.__data['FPP']['S [m^2]'])*(self.__data['C&S']['Engine'][1] - self.__data['C&S']['Wing'][1])/chord*coefficient

        if self.canard:
            canard_term = (self.__data['Aero']['CL_c']/self.__data['Aero']['CL_A-h']*self.__data['C&S']['Sc']/self.__data['FPP']['S [m^2]']*((self.__data['C&S']['Canard'][0]-1)/chord - xac))*coefficient
        else:
            canard_term = 0

        # Return a function to plot against xcg
        return lambda xcg: first_term(xcg) + second_term - thrust_term - canard_term

    def plot(self, fig: plt.figure = None):

        if fig is None:
            fig = plt.figure()

        xrange = np.linspace(0, 3, 100)
        chord = self.__data['Aero']['Wing chord']

        # Function to calculate CG
        cg = lambda xw, PL, F: ((self.__data['Structures']['Wing_weight [N]'] + self.__data['Weights']['WF [N]']) * F * xw +
                              self.__data['Weights']['WPL [N]'] * PL * (self.__data['C&S']['Payload'][0]-1)/chord +
                              self.__data['Structures']['Fuselage_weight [N]'] * (self.__data['C&S']['Fuselage'][0] - 1) / chord +
                              self.__data['FPP']['Engine Weight [N]'] * (self.__data['C&S']['Engine'][0] - 1) / chord) / \
                             (self.__data['Structures']['Wing_weight [N]'] +
                              self.__data['Weights']['WF [N]']* F +
                              self.__data['Weights']['WPL [N]'] * PL +
                              self.__data['Structures']['Fuselage_weight [N]'] +
                              self.__data['FPP']['Engine Weight [N]'])

        # Calculate CG for plotting
        cgx_full = [cg((self.__data['C&S']['Wing'][0] - 1)/chord, 1, 1) for i in range(10)]
        cgx_empty = [cg((self.__data['C&S']['Wing'][0] - 1)/chord, 0, 0) for i in range(10)]
        cgx_fuel = [cg((self.__data['C&S']['Wing'][0] - 1)/chord, 0, 1) for i in range(10)]
        cgx_payload = [cg((self.__data['C&S']['Wing'][0] - 1)/chord, 1, 0) for i in range(10)]
        cgy = [i for i in np.linspace(0, 1, 10)]

        # Plot
        plt.plot(xrange, self.__curve(xrange), 'b-', label='Control Curve')
        plt.plot(cgx_full, cgy, 'k--', label='CG - MTOW')
        plt.plot(cgx_empty, cgy, 'k.-', label='CG - OEW')
        plt.plot(cgx_fuel, cgy, '.', label='CG - Only fuel')
        plt.plot(cgx_payload, cgy, 'v', label='CG - Only Payload')
        plt.xlabel(r'$x_{cg} / MAC [-]$')
        plt.ylabel(r'$S_{h}/S [-]$')
        plt.grid(True, which='both')
        plt.legend()

        return fig


class StabilityCurve(object):

    def __init__(self, canard=False):

        self.canard = canard
        self.__data = GoogleSheetsDataImport(SPREADSHEET_ID, *SHEET_NAMES).get_data()

        self.__curve = self.__get_stability_curve()
        self.__xlemac = self.__data['C&S']['Wing'][0]

    def __get_stability_curve(self):

        # Common items in formulas
        chord = self.__data['Aero']['Wing chord']
        xlemac = (self.__data['C&S']['Wing'][0]-1)/chord
        xac = xlemac + self.__data['Aero']['x_ac']
        SM = self.__data['C&S']['SM']

        lh = self.__data['C&S']['H Wing'][0] - self.__data['C&S']['Wing'][0]

        # Canard Version
        if self.canard:
            denominator = lambda xcg: self.__data['Aero']['CL_alpha_h']/self.__data['Aero']['CL_alpha_A-h']*(self.__data['Aero']['Vh/V']**2)*(1-self.__data['Aero']['de/da'])*(xcg + SM - (self.__data['C&S']['H Wing'][0]-1)/chord)
            first_term = lambda xcg: (xcg + SM)*(1 + self.__data['Aero']['CL_alpha_c']/self.__data['Aero']['CL_alpha_A-h']*self.__data['C&S']['Sc']/self.__data['FPP']['S [m^2]'])
            second_term = xac + (self.__data['C&S']['Canard'][0]-1)/chord*self.__data['Aero']['CL_alpha_c']/self.__data['Aero']['CL_alpha_A-h']*self.__data['C&S']['Sc']/self.__data['FPP']['S [m^2]']
            return lambda xcg: -(first_term(xcg) - second_term)/denominator(xcg)

        # Conventional Version
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
        plt.title(f'Wing @ {round((self.__xlemac - 1)/self.__data["Structures"]["Max_fuselage_length"], 2)*100} % fuselage\n'
                  f'Engine @ {round((self.__data["C&S"]["Engine"][0]- 1)/self.__data["Structures"]["Max_fuselage_length"], 2)*100} % fuselage\n'
                  f'Payload @ {round((self.__data["C&S"]["Payload"][0]- 1)/self.__data["Structures"]["Max_fuselage_length"], 2)*100} % fuselage ')
        plt.legend()

        return fig


if __name__ == '__main__':

    Ctr = ControllabilityCurve(False)
    Stab = StabilityCurve(False)

    fig = plt.figure()
    Stab.plot(fig)
    Ctr.plot(fig)
