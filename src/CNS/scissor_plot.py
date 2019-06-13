import numpy as np
import matplotlib.pyplot as plt

import os
import sys
sys.path.insert(0, '\\'.join(os.getcwd().split('\\')[:-1]) + '\\tools')

from GoogleSheetsImport import GoogleSheetsDataImport, SHEET_NAMES, SPREADSHEET_ID
from COG_calculation import CgCalculation


class ControllabilityCurve(object):

    def __init__(self, canard=False, amphib=False):

        self.canard = canard
        self.amphib = amphib
        self.__data = dict(GoogleSheetsDataImport(SPREADSHEET_ID, *SHEET_NAMES).get_data())

        self.__curve = self.__get_control_curve()

    def __get_control_curve(self):

        # Common items in formulas
        chord = self.__data['Aero']['Wing chord']
        xlemac = (self.__data['C&S']['Wing'][0] - 1) / chord
        zlemac = (self.__data['C&S']['Wing'][1] - 10) / chord
        xac = xlemac + self.__data['Aero']['x_ac']

        lh = self.__data['C&S']['H Wing'][0] - self.__data['C&S']['Wing'][0]

        # Shorten some code by defining this coefficient
        coefficient = 1.0/(self.__data['Aero']['CL_h']/self.__data['Aero']['CL_A-h'] * self.__data['Aero']['Vh/V']**2 * lh/chord)

        first_term = lambda xcg: coefficient*xcg
        second_term = (self.__data['Aero']['Cm_ac']/self.__data['Aero']['CL_A-h'] - xac)*coefficient
        thrust_term = self.__data['FPP']['Tc']/self.__data['Aero']['CL_A-h']*(2*(self.__data['FPP']['Prop Diameter [m]']**2)/self.__data['FPP']['S [m^2]'])*(self.__data['C&S']['Engine'][1] - self.__data['C&S']['Wing'][1])/chord*coefficient

        if self.canard:
            canard_term = (self.__data['Aero']['CL_c']/self.__data['Aero']['CL_A-h']*self.__data['C&S']['Sc']/self.__data['FPP']['S [m^2]']*((self.__data['C&S']['Canard'][0]-1)/chord - xac))*coefficient
            return lambda xcg: first_term(xcg) + second_term - thrust_term - canard_term

        elif self.amphib:
            amphib_term = self.__data['Structures']['CR']/self.__data['Aero']['CL_A-h']*1000/1.225*(0.05)/self.__data['FPP']['S [m^2]']*(self.__data['Structures']['Vw/V']**2)*(zlemac - (self.__data['Structures']['CoB'][1]-10)/chord)*coefficient
            print(amphib_term, (zlemac - (self.__data['Structures']['CoB'][1]-10)/chord))
            return lambda xcg: first_term(xcg) + second_term - thrust_term - amphib_term

        else:
            return lambda xcg: first_term(xcg) + second_term - thrust_term

        # Return a function to plot against xcg


    def cgcalc(self, PL, F):

        xw = [self.__data['C&S']['Wing'][0] + 0.25*self.__data['Aero']['Wing chord'], self.__data['C&S']['Wing'][1]]
        
        if PL == 1 and F == 1:
            components = {
                'Fuselage': (self.__data['Structures']['Fuselage_weight [N]'], self.__data['C&S']['Fuselage']),
                'Wing': (self.__data['Structures']['Wing_weight [N]'], xw),
                'Engine': (self.__data['FPP']['Engine Weight [N]'], self.__data['C&S']['Engine']),
                'Horizontal Tail': (self.__data['Structures']['HTail_weight [N]'], self.__data['C&S']['H Wing']),
                'Vertical Tail': (self.__data['Structures']['VTail_weight [N]'], self.__data['C&S']['V Wing']),
                'Payload': (self.__data['Weights']['WPL [N]'], self.__data['C&S']['Payload']),
                'Fuel': (self.__data['Weights']['WF [N]'], xw),
                'Nose landing gear': (self.__data['Structures']['NLG_weight'], self.__data['C&S']['NLG']),
                'Main landing gear': (self.__data['Structures']['MLG_weight'], self.__data['C&S']['MLG']),
                'Floats': (self.__data['Structures']['Float_weight'], self.__data['C&S']['Floats'])
            }


        elif PL == 1 and F == 0:

            components = {
                'Fuselage': (self.__data['Structures']['Fuselage_weight [N]'], self.__data['C&S']['Fuselage']),
                'Wing': (self.__data['Structures']['Wing_weight [N]'], xw),
                'Engine': (self.__data['FPP']['Engine Weight [N]'], self.__data['C&S']['Engine']),
                'Horizontal Tail': (self.__data['Structures']['HTail_weight [N]'], self.__data['C&S']['H Wing']),
                'Vertical Tail': (self.__data['Structures']['VTail_weight [N]'], self.__data['C&S']['V Wing']),
                'Payload': (self.__data['Weights']['WPL [N]'], self.__data['C&S']['Payload']),
                'Nose landing gear': (self.__data['Structures']['NLG_weight'], self.__data['C&S']['NLG']),
                'Main landing gear': (self.__data['Structures']['MLG_weight'], self.__data['C&S']['MLG']),
                'Floats': (self.__data['Structures']['Float_weight'], self.__data['C&S']['Floats'])
            }
        
        elif PL == 0 and F == 1:

            components = {
                'Fuselage': (self.__data['Structures']['Fuselage_weight [N]'], self.__data['C&S']['Fuselage']),
                'Wing': (self.__data['Structures']['Wing_weight [N]'], xw),
                'Engine': (self.__data['FPP']['Engine Weight [N]'], self.__data['C&S']['Engine']),
                'Horizontal Tail': (self.__data['Structures']['HTail_weight [N]'], self.__data['C&S']['H Wing']),
                'Vertical Tail': (self.__data['Structures']['VTail_weight [N]'], self.__data['C&S']['V Wing']),
                'Fuel': (self.__data['Weights']['WF [N]'], xw),
                'Nose landing gear': (self.__data['Structures']['NLG_weight'], self.__data['C&S']['NLG']),
                'Main landing gear': (self.__data['Structures']['MLG_weight'], self.__data['C&S']['MLG']),
                'Floats': (self.__data['Structures']['Float_weight'], self.__data['C&S']['Floats'])
            }
        
        elif PL == 0 and F == 0:

            components = {
                'Fuselage': (self.__data['Structures']['Fuselage_weight [N]'], self.__data['C&S']['Fuselage']),
                'Wing': (self.__data['Structures']['Wing_weight [N]'], xw),
                'Engine': (self.__data['FPP']['Engine Weight [N]'], self.__data['C&S']['Engine']),
                'Horizontal Tail': (self.__data['Structures']['HTail_weight [N]'], self.__data['C&S']['H Wing']),
                'Vertical Tail': (self.__data['Structures']['VTail_weight [N]'], self.__data['C&S']['V Wing']),
                'Nose landing gear': (self.__data['Structures']['NLG_weight'], self.__data['C&S']['NLG']),
                'Main landing gear': (self.__data['Structures']['MLG_weight'], self.__data['C&S']['MLG']),
                'Floats': (self.__data['Structures']['Float_weight'], self.__data['C&S']['Floats'])
            }
        
        else:
            raise ValueError

        cg = CgCalculation(components).calculate_cg()

        return [(cg[0] - 1)/self.__data['Aero']['Wing chord'], (cg[1] - 10)/self.__data['Aero']['Wing chord']]

    def plot(self, fig: plt.figure = None):

        if fig is None:
            fig = plt.figure()

        xrange = np.linspace(0, 3, 100)
        chord = self.__data['Aero']['Wing chord']

        # Function to calculate CG
        cg = lambda xw, PL, F: ((self.__data['Structures']['Wing_weight [N]'] + self.__data['Weights']['WF [N]']*F) * (xw + 0.4) +
                              self.__data['Weights']['WPL [N]'] * PL * (self.__data['C&S']['Payload'][0]-1)/chord +
                              self.__data['Structures']['Fuselage_weight [N]'] * (self.__data['C&S']['Fuselage'][0] - 1) / chord +
                              self.__data['FPP']['Engine Weight [N]'] * (self.__data['C&S']['Engine'][0] - 1) / chord +
                              self.__data['Structures']['HTail_weight [N]'] * (self.__data['C&S']['H Wing'][0] - 1)/chord +
                              self.__data['Structures']['VTail_weight [N]'] * (self.__data['C&S']['V Wing'][0] - 1)/chord) / \
                             (self.__data['Structures']['Wing_weight [N]'] +
                              self.__data['Weights']['WF [N]']* F +
                              self.__data['Weights']['WPL [N]'] * PL +
                              self.__data['Structures']['HTail_weight [N]'] +
                              self.__data['Structures']['VTail_weight [N]'] +
                              self.__data['Structures']['Fuselage_weight [N]'] +
                              self.__data['FPP']['Engine Weight [N]'])

        # Calculate CG for plotting
        # cgx_full = [cg((self.__data['C&S']['Wing'][0] - 1)/chord, 1, 1) for i in range(10)]
        # cgx_empty = [cg((self.__data['C&S']['Wing'][0] - 1)/chord, 0, 0) for i in range(10)]
        # cgx_fuel = [cg((self.__data['C&S']['Wing'][0] - 1)/chord, 0, 1) for i in range(10)]
        # cgx_payload = [cg((self.__data['C&S']['Wing'][0] - 1)/chord, 1, 0) for i in range(10)]


        # cgx_min = [min(cg((self.__data['C&S']['Wing'][0] - 1)/chord, 1, 1), cg((self.__data['C&S']['Wing'][0] - 1)/chord, 1, 0), cg((self.__data['C&S']['Wing'][0] - 1)/chord, 0, 1), cg((self.__data['C&S']['Wing'][0] - 1)/chord, 0, 0)) for i in range(10)]
        # cgx_max = [max(cg((self.__data['C&S']['Wing'][0] - 1)/chord, 1, 1), cg((self.__data['C&S']['Wing'][0] - 1)/chord, 1, 0), cg((self.__data['C&S']['Wing'][0] - 1)/chord, 0, 1), cg((self.__data['C&S']['Wing'][0] - 1)/chord, 0, 0)) for i in range(10)]

        # Plot
        if not self.amphib:
            plt.plot(xrange, self.__curve(xrange), '-x', c=(91/255, 188/255, 47/255),label='Aerial Control Curve')
        elif self.amphib:
            plt.plot(xrange, self.__curve(xrange), '-.', c=(47/255, 71/255, 183/255), label='Amphibious Control Curve')
        # plt.plot(cgx_min, cgy, 'k--', label='CG - Most Forward')
        # plt.plot(cgx_max, cgy, 'k.-', label='CG - Most Aft')
        plt.xlabel(r'$\bar{x}_{cg}$', fontsize=16)
        plt.ylabel(r'$S_{h}/S [-]$', fontsize=16)
        plt.grid(b=True, which='major')
        plt.legend(fontsize='large')

        return fig

    def cgplot(self, fig = None):

        if fig is None:
            fig = plt.figure()

        cgx_full = [self.cgcalc(1, 1)[0] for i in range(50)]
        cgx_empty = [self.cgcalc(0, 0)[0] for i in range(50)]
        cgx_fuel = [self.cgcalc(0, 1)[0] for i in range(50)]
        cgx_payload = [self.cgcalc(1, 0)[0] for i in range(50)]
        cgy = [i for i in np.linspace(0, 1, 50)]
        fwd_cg = min(cgx_full,cgx_empty,cgx_fuel,cgx_payload)
        aft_cg = max(cgx_full,cgx_empty,cgx_fuel,cgx_payload)
        plt.plot(fwd_cg, cgy, '--', label='Forward CG')
        # plt.plot(cgx_payload, cgy, 'x', label='CG - Only Payload')
        # plt.plot(cgx_full, cgy, '--', label='CG - MTOW')
        plt.plot(aft_cg, cgy, '--', label='Aft CG')
        plt.xlabel(r'$\bar{x}_{cg} [-]$', fontsize=16)
        plt.ylabel(r'$S_{h}/S [-]$', fontsize=16)
        plt.grid(b=True, which='major')
        plt.legend(fontsize='large')


class StabilityCurve(object):

    def __init__(self, canard=False, amphib=False):

        self.canard = canard
        self.amphib = amphib
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

        mtv = (self.__data['C&S']['H Wing'][1] - self.__data['C&S']['Wing'][1])/(self.__data['Aero']['Wing Span']/2)
        r = lh/(self.__data['Aero']['Wing Span']/2)

        phi = np.arcsin(mtv/r)
        delta_deda = 6.5*((1.225*self.__data['FPP']['Pa [kW] Sustain']**2*self.__data['FPP']['S [m^2]']**3*self.__data['Aero']['CL_A-h']**3)/(lh**4*self.__data['Weights']['WTO [N]']**3))**(1/4)*(np.sin(6*phi))**4.5


        # Canard Version
        if self.canard:
            print("Canard")
            denominator = lambda xcg: self.__data['Aero']['CL_alpha_h']/self.__data['Aero']['CL_alpha_A-h']*(self.__data['Aero']['Vh/V']**2)*(1-self.__data['Aero']['de/da'])*(xcg + SM - (self.__data['C&S']['H Wing'][0]-1)/chord)
            first_term = lambda xcg: (xcg + SM)*(1 + self.__data['Aero']['CL_alpha_c']/self.__data['Aero']['CL_alpha_A-h']*self.__data['C&S']['Sc']/self.__data['FPP']['S [m^2]'])
            second_term = xac + (self.__data['C&S']['Canard'][0]-1)/chord*self.__data['Aero']['CL_alpha_c']/self.__data['Aero']['CL_alpha_A-h']*self.__data['C&S']['Sc']/self.__data['FPP']['S [m^2]']
            return lambda xcg: -(first_term(xcg) - second_term)/denominator(xcg)

        elif self.amphib:
            numerator = lambda xcg: xcg + SM - xac + 1000/1.225*self.__data['Structures']['Wetted Area']/self.__data['FPP']['S [m^2]']*1*(0.010775/self.__data['Aero']['CL_alpha_A-h']*(0.64)/chord)
            denominator = lambda xcg: (1-(self.__data['Aero']['de/da'] + delta_deda))*(self.__data['Aero']['Vh/V']**2)*self.__data['Aero']['CL_alpha_h']/self.__data['Aero']['CL_alpha_A-h']*(-xcg-SM+(self.__data['C&S']['H Wing'][0]-1)/chord)
            return lambda xcg: numerator(xcg)/denominator(xcg)

        # Conventional Version
        else:
            CL_ratio = -(self.__data['Aero']['CL_alpha_A-h']/self.__data['Aero']['CL_alpha_h'])
            coefficient = 1/((1-(self.__data['Aero']['de/da'] + delta_deda))*(self.__data['Aero']['Vh/V']**2))

            return lambda xcg: coefficient*CL_ratio*(xcg+SM-xac)/(xcg+SM-(self.__data['C&S']['H Wing'][0]-1)/chord)

    def plot(self, fig: plt.figure = None):

        if fig is None:
            fig = plt.figure()

        xrange = np.linspace(0, 3, 100)

        if self.amphib:
            plt.plot(xrange, self.__curve(xrange), '-^', c=(49/255, 165/255, 183/255), label='Amphibious Stability Curve')

        else:
            plt.plot(xrange, self.__curve(xrange), '-o', c=(216/255, 39/255, 39/255), label='Aerial Stability Curve')

        plt.xlabel(r'$\bar{x}_{cg} [-]$', fontsize=16)
        
        plt.ylabel(r'$S_{h}/S [-]$', fontsize=16)
        plt.grid(b=True, which='major', linestyle='-')
        # plt.grid(b=True, which='minor', color='k', linestyle='-')
        plt.ylim(0, 1.0)

        t = f'LEMAC @ {round((self.__xlemac - 1)/self.__data["Structures"]["Max_fuselage_length"], 2)*100} % fuselage\n' \
              f'Engine @ {round((self.__data["C&S"]["Engine"][0]- 1)/self.__data["Structures"]["Max_fuselage_length"], 2)*100} % fuselage\n' \
              f'Payload @ {round((self.__data["C&S"]["Payload"][0]- 1)/self.__data["Structures"]["Max_fuselage_length"], 2)*100} % fuselage '

        plt.title("Scissor Plot", fontsize=18)
        plt.legend()

        return fig


if __name__ == '__main__':

    Ctr_amphib = ControllabilityCurve(False, amphib=True)
    Ctr = ControllabilityCurve(False, amphib=False)
    Stab_amphib = StabilityCurve(False, amphib=True)
    Stab = StabilityCurve(False, amphib=False)

    fig = plt.figure()
    Stab_amphib.plot(fig)
    Stab.plot(fig)
    Ctr_amphib.plot(fig)
    Ctr.plot(fig)
    Ctr.cgplot(fig)
