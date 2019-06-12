import numpy as np
import matplotlib.pyplot as plt

import os
import sys
sys.path.insert(0, '\\'.join(os.getcwd().split('\\')[:-1]) + '\\tools')

from GoogleSheetsImport import GoogleSheetsDataImport, SHEET_NAMES, SPREADSHEET_ID


class CgCalculation(object):

    def __init__(self, components: dict):
        """
        Object to calculate the centre of gravity in 3 Dimensions for any system
        :param components: {
                    component: (weight, (x, z)),
                    ...
                    }
        """
        # self.__data = GoogleSheetsDataImport(SPREADSHEET_ID, *SHEET_NAMES).get_data()
        self.__components = components
        self.__cg = [None, None]
        self.__cg_lemac = [None, None]
        self.calculate_cg()
        # self.cg_xlemac()

    def add_component(self, name: str, weight: float, position: tuple):
        """
        Add Component to the calculation
        :param name: Component Name
        :param weight: Component Weight
        :param position: Component position in (x, z)
        :return:
        """

        self.__components[name] = (weight, position)
        self.calculate_cg()

    @staticmethod
    def __calculate_cg_along_x(components: dict):
        """
        Calculate X coordinate of CG
        :return:
        """
        return sum([weight * position[0] for name, (weight, position) in components.items()])\
               / sum([weight for name, (weight, position) in components.items()])

    @staticmethod
    def __calculate_cg_along_z(components: dict):
        """
        Calculate Z coordinate of CG
        :return:
        """
        return sum([weight * position[1] for name, (weight, position) in components.items()])\
               / sum([weight for name, (weight, position) in components.items()])

    def calculate_cg(self):
        """
        Calculate x, z position of CG
        :return:
        """
        self.__cg = [self.__calculate_cg_along_x(self.__components), self.__calculate_cg_along_z(self.__components)]
        return self.__cg

    def cg_xlemac(self, d_xlemac: float):
        """
        Calculate CG in XLEMAC coordinates
        :param d_xlemac: Distance from nose tip to XLEMAC
        :return:
        """
        self.__cg_lemac = [self.__cg[0] - d_xlemac, self.__cg[1]]
        return self.__cg_lemac

    @staticmethod
    def __plot_cilinder(length: float, height: float, offset: tuple = (0, 0)):

        height = height/2
        xdata = []
        ydata = []

        # First Circular Part
        for theta in np.linspace(0, np.pi/2, 10):
            xdata.append(height - np.cos(theta)*height)
            ydata.append(np.sin(theta)*height)

        # Straight Part
        for xi in np.linspace(height, length-height, 100):
            xdata.append(xi)
            ydata.append(height)

        # Second Circular Part
        for theta in np.linspace(np.pi/2, 0, 10):
            xdata.append(length - height + np.cos(theta)*height)
            ydata.append(np.sin(theta)*height)

        bottom_x = []
        bottom_y = []

        for xi, yi in zip(xdata[::-1], ydata[::-1]):
            bottom_x.append(xi)
            bottom_y.append(-yi)

        xdata.extend(bottom_x)
        ydata.extend(bottom_y)

        return np.array(xdata) + offset[0], np.array(ydata) + offset[1]

    def wing_positioning_plot(self, fig=None):
        """
        Wing Positioning
        :return:
        """

        xrange = np.linspace(0, 0.75)

        data = GoogleSheetsDataImport(SPREADSHEET_ID, *SHEET_NAMES)
        # data.coordinate_transform()
        data = data.get_data()
        fuselage = data['Structures']['Max_fuselage_length']
        chord = data['Aero']['Wing chord']

        if fig is None:
            fig = plt.figure()

        wing_weight = self.__components['Wing'][0]
        wing_pos = self.__components['Wing'][1]
        components = dict(self.__components)

        empty_cgs = []

        for xwing in xrange:
            components['Wing'] = (wing_weight, (xwing*fuselage, wing_pos[1]))
            components['Payload'] = (0,(0,0))
            cg = (self.__calculate_cg_along_x(components) - xwing*fuselage)/chord
            empty_cgs.append(cg)

        empty_cgs = np.array(empty_cgs)

        full_cgs = []
        components = dict(self.__components)

        for xwing in xrange:
            components['Wing'] = (wing_weight, (xwing*fuselage, wing_pos[1]))
            cg = (self.__calculate_cg_along_x(components) - xwing*fuselage)/chord
            full_cgs.append(cg)

        full_cgs = np.array(full_cgs)

        plt.plot(empty_cgs, xrange, 'r-', label='Empty Payload')
        plt.plot(full_cgs, xrange, 'b-', label='Full Payload')
        plt.grid()
        plt.legend()
        plt.xlabel('$x_{cg}/MAC$')
        plt.ylabel('$x_{LEMAC}/l_{fus}$')
        plt.title(f'Payload @ {round((components["Payload"][1][0] - 1)/fuselage, 2)*100} % of fuselage')

    def plot_locations(self, fig: plt.figure = None):
        """
        Make a component plot of all components and weights
        :param fig: fig to plot in
        :return:
        """

        CoB = data['Structures']['CoB']
        fwd,aft = self.fwd_aft_cg()
        fwd_weird_frame = fwd + 1
        aft_weird_frame = aft + 1
        if fig is None:
            fig, ax = plt.subplots()
            ax.set_aspect(1.0)
            plt.xlim(0, 15)
            plt.ylim(0, 15)

        coordinate_history = []
        for name, (weight, (x, z)) in self.__components.items():
            i = 1
            if (x, z) in coordinate_history:
                i = 3
            plt.scatter(x, z, s=np.sqrt(weight), c='k')
            plt.annotate(name, xy=(x+i*0.1, z+i*0.1))
            coordinate_history.append((x,z))
        plt.scatter(self.__cg[0], self.__cg[1], c='r')
        plt.annotate('CG', xy=self.__cg)
        plt.scatter(CoB[0], CoB[1], c='b')
        plt.annotate('CoB', xy=CoB)
        plt.scatter(fwd_weird_frame, 10)
        plt.annotate('Forward CG',xy=[fwd_weird_frame,10])
        plt.scatter(fwd_weird_frame, 10)
        plt.annotate('Aft CG', xy=[aft_weird_frame, 10])

        # fuselage = self.__plot_cilinder(9, 2.5)
        # wing = self.__plot_cilinder(2.25, 0.5, offset=(3, 1.5))
        #
        # plt.plot(fuselage[0], fuselage[1], 'k-')
        # plt.plot(wing[0], wing[1], 'k-')

        plt.grid()
        plt.xlabel('X Position [m]')
        plt.ylabel('Y Position [m]')
        plt.title('CG Location')
        plt.show()

    # def fwd_aft_cg(self):
    #
    #     chord = self.__data['Aero']['Wing chord']
    #
    #     cg = lambda PL, F: ((self.__data['Structures']['Wing_weight [N]'] + self.__data['Weights']['WF [N]']) * F * ((self.__data['C&S']['Wing'][0]-1)/chord + self.__data['Aero']['x_ac']) +
    #                           self.__data['Weights']['WPL [N]'] * PL * (self.__data['C&S']['Payload'][0]-1)/chord +
    #                           self.__data['Structures']['Fuselage_weight [N]'] * (self.__data['C&S']['Fuselage'][0] - 1) / chord +
    #                           self.__data['FPP']['Engine Weight [N]'] * (self.__data['C&S']['Engine'][0] - 1) / chord +
    #                           self.__data['Structures']['HTail_weight [N]'] * (self.__data['C&S']['H Wing'][0] - 1)/chord +
    #                           self.__data['Structures']['VTail_weight [N]'] * (self.__data['C&S']['V Wing'][0] - 1)/chord) / \
    #                          (self.__data['Structures']['Wing_weight [N]'] +
    #                           self.__data['Weights']['WF [N]']* F +
    #                           self.__data['Weights']['WPL [N]'] * PL +
    #                           self.__data['Structures']['HTail_weight [N]'] +
    #                           self.__data['Structures']['VTail_weight [N]'] +
    #                           self.__data['Structures']['Fuselage_weight [N]'] +
    #                           self.__data['FPP']['Engine Weight [N]'])
    #     cgx_full = cg(1,1)
    #
    #     cgx_empty = cg(0,0)
    #     cgx_fuel = cg(0,1)
    #     cgx_payload = cg(0,1)
    #     fwd_cg = min(cgx_payload,cgx_fuel,cgx_empty,cgx_full)
    #     aft_cg = max(cgx_payload,cgx_fuel,cgx_empty,cgx_full)
    #     return fwd_cg,aft_cg


if __name__ == '__main__':

    data = GoogleSheetsDataImport(SPREADSHEET_ID, *SHEET_NAMES).get_data()

    data['C&S']['Wing'] = [data['C&S']['Wing'][0] + data['Aero']['x_ac'] * data['Aero']['Wing chord'],  data['C&S']['Wing'][1]]

    full_components = {
        'Fuselage': (data['Structures']['Fuselage_weight [N]'], data['C&S']['Fuselage']),
        'Wing': (data['Structures']['Wing_weight [N]'], data['C&S']['Wing']),
        'Engine': (data['FPP']['Engine Weight [N]'], data['C&S']['Engine']),
        'Horizontal Tail': (data['Structures']['HTail_weight [N]'], data['C&S']['H Wing']),
        'Vertical Tail': (data['Structures']['VTail_weight [N]'], data['C&S']['V Wing']),
        'Payload': (data['Weights']['WPL [N]'], data['C&S']['Payload']),
        'Fuel': (data['Weights']['WF [N]'], data['C&S']['Wing']),
        'Nose landing gear': (data['Structures']['NLG_weight'], data['C&S']['NLG']),
        'Main landing gear': (data['Structures']['MLG_weight'], data['C&S']['MLG'])
    }

    empty_components = {
        'Fuselage': (data['Structures']['Fuselage_weight [N]'], data['C&S']['Fuselage']),
        'Wing': (data['Structures']['Wing_weight [N]'], data['C&S']['Wing']),
        'Engine': (data['FPP']['Engine Weight [N]'], data['C&S']['Engine']),
        'Horizontal Tail': (data['Structures']['HTail_weight [N]'], data['C&S']['H Wing']),
        'Vertical Tail': (data['Structures']['VTail_weight [N]'], data['C&S']['V Wing']),
        'Nose landing gear': (data['Structures']['NLG_weight'], data['C&S']['NLG']),
        'Main landing gear': (data['Structures']['MLG_weight'], data['C&S']['MLG'])
    }

    full_PL_components = {
        'Fuselage': (data['Structures']['Fuselage_weight [N]'], data['C&S']['Fuselage']),
        'Wing': (data['Structures']['Wing_weight [N]'], data['C&S']['Wing']),
        'Engine': (data['FPP']['Engine Weight [N]'], data['C&S']['Engine']),
        'Horizontal Tail': (data['Structures']['HTail_weight [N]'], data['C&S']['H Wing']),
        'Vertical Tail': (data['Structures']['VTail_weight [N]'], data['C&S']['V Wing']),
        'Payload': (data['Weights']['WPL [N]'], data['C&S']['Payload']),
        'Nose landing gear': (data['Structures']['NLG_weight'], data['C&S']['NLG']),
        'Main landing gear': (data['Structures']['MLG_weight'], data['C&S']['MLG'])
    }

    full_F_components = {
        'Fuselage': (data['Structures']['Fuselage_weight [N]'], data['C&S']['Fuselage']),
        'Wing': (data['Structures']['Wing_weight [N]'], data['C&S']['Wing']),
        'Engine': (data['FPP']['Engine Weight [N]'], data['C&S']['Engine']),
        'Horizontal Tail': (data['Structures']['HTail_weight [N]'], data['C&S']['H Wing']),
        'Vertical Tail': (data['Structures']['VTail_weight [N]'], data['C&S']['V Wing']),
        'Fuel': (data['Weights']['WF [N]'], data['C&S']['Wing']),
        'Nose landing gear': (data['Structures']['NLG_weight'], data['C&S']['NLG']),
        'Main landing gear': (data['Structures']['MLG_weight'], data['C&S']['MLG'])
    }

    B1 = CgCalculation(full_components).calculate_cg()
    B2 = CgCalculation(empty_components).calculate_cg()
    B3 = CgCalculation(full_F_components).calculate_cg()
    B4 = CgCalculation(full_PL_components).calculate_cg()
    # B.plot_locations()
    # print("CG: ", B.calculate_cg())
    # B.wing_positioning_plot()
