import numpy as np
import os
import json

import sys
sys.path.insert(0, '\\'.join(os.getcwd().split('\\')[:-1]) + '\\tools')

from GoogleSheetsImport import GoogleSheetsDataImport, SHEET_NAMES, SPREADSHEET_ID


class Force(object):

    def __init__(self, vector: np.array, location: np.array):
        self.__vector = vector
        self.__position = location

    def get_position(self):
        return self.__position

    def get_vector(self):
        return self.__vector

    def get_magnitude(self):
        return np.linalg.norm(self.__vector)

    def get_direction(self):
        return self.__vector / self.get_magnitude()


class Moment(object):

    def __init__(self, magnitude: float, location: np.array):
        self.__moment = magnitude
        self.__position = location

    def get_magnitude(self):
        return self.__moment

    def get_position(self):
        return self.__position


class ForceMomentBalance(object):

    def __init__(self, **kwargs):

        try:
            self.__forces = kwargs['forces']

        except KeyError:
            self.__forces = []

        try:
            self.__moments = kwargs['moments']

        except KeyError:
            self.__moments = []

    def add_force(self, force_object: Force):
        self.__forces.append(force_object)

    def add_moment(self, moment_object: Moment):
        self.__moments.append(moment_object)

    def calculate(self, moment_coordinate: np.array):

        s_X = 0
        s_Y = 0
        M = 0

        for force in self.__forces:
            s_X += force.get_direction()[0] * force.get_magnitude()
            s_Y += force.get_direction()[1] * force.get_magnitude()

            r = force.get_position() - moment_coordinate

            M += np.cross(r, force.get_vector())[-1]

        for moment in self.__moments:
            M += moment.get_magnitude()

        return s_X, s_Y, M


class MomentCoefficientCalculations(object):

    def __init__(self):

        try:
            self.__data = GoogleSheetsDataImport(SPREADSHEET_ID, *SHEET_NAMES).get_data()

        except (PermissionError, ConnectionError, ConnectionRefusedError, ConnectionAbortedError):
            print("No Data Found In Current Path")
            self.__data = None

    def aerial_cm(self):

        cg = self.__data['C&S']['CG_abs']

        tail_volume = self.__data['C&S']['Sh'] / self.__data['Aero']['Wing Area'] * (self.__data['Aero']['Vh/V']) ** 2
        thrust_coefficient = self.__data['FPP']['Tc'] * 2 * (self.__data['FPP']['Prop Diameter [m]'] ** 2) / self.__data['Aero']['Wing Area']

        wing_contribution = self.__data['Aero']['Cm_ac'] + self.__data['Aero']['CN_w'] * self.__get_delta(self.__data['C&S']['Wing'], cg)[0] - \
                            self.__data['Aero']['CT_w'] * self.__get_delta(self.__data['C&S']['Wing'], cg)[1]

        tail_contribution = tail_volume * (self.__data['Aero']['CN_h'] * self.__data['C&S']['lh'] -
                                           self.__data['Aero']['CT_h'] * self.__get_delta(self.__data['C&S']['H Wing'], cg)[1])

        thrust_contribution = thrust_coefficient * self.__get_delta(self.__data['C&S']['Engine'], cg)[1]

        return wing_contribution + tail_contribution + thrust_contribution

    def scooping_cm(self):

        cg = self.__data['C&S']['CG_abs']

        tail_volume = self.__data['C&S']['Sh'] / self.__data['Aero']['Wing Area'] * (self.__data['Aero']['Vh/V']) ** 2
        thrust_coefficient = self.__data['FPP']['Tc'] * 2 * (self.__data['FPP']['Prop Diameter [m]'] ** 2) / self.__data['Aero']['Wing Area']

        wing_contribution = self.__data['Aero']['Cm_ac'] + self.__data['Aero']['CN_w'] * self.__get_delta(self.__data['C&S']['Wing'], cg)[0] - \
                            self.__data['Aero']['CT_w'] * self.__get_delta(self.__data['C&S']['Wing'], cg)[1]

        tail_contribution = tail_volume * (self.__data['Aero']['CN_h'] * self.__data['C&S']['lh'] -
                                           self.__data['Aero']['CT_h'] * self.__get_delta(self.__data['C&S']['H Wing'], cg)[1])

        thrust_contribution = thrust_coefficient * self.__get_delta(self.__data['C&S']['Engine'], cg)[1]

        water_contribution = self.__data['Structures']['CN_s'] * self.__get_delta_x(self.__data['Structures']['Scooper_location'], cg)*self.__data['Structures']['Scooper Area']/self.__data['Aero']['Wing Area'] - \
                             self.__data['Structures']['CT_s'] * self.__get_delta_z(self.__data['Structures']['Scooper_location'], cg)*self.__data['Structures']['Scooper Area']/self.__data['Aero']['Wing Area']

        return wing_contribution + tail_contribution + thrust_contribution + water_contribution

    def cm_alpha(self):

        cg = self.__data['C&S']['CG_abs']
        tail_volume = self.__data['C&S']['Sh'] / self.__data['Aero']['Wing Area'] * (self.__data['Aero']['Vh/V']) ** 2

        wing_contribution = self.__data['Aero']['CN_w_a'] * self.__get_delta_x(self.__data['C&S']['Wing'], cg) - \
                            self.__data['Aero']['CT_w_a'] * self.__get_delta_z(self.__data['C&S']['Wing'], cg)

        tail_contributuon = tail_volume * self.__data['Aero']['CN_h_a'] * self.__get_delta_x(self.__data['C&S']['H Wing'], cg)

        return wing_contribution + tail_contributuon

    @staticmethod
    def __get_delta_x(first: list, second: list):
        return second[0] - first[0]

    @staticmethod
    def __get_delta_z(first: list, second: list):
        return second[1] - first[1]

    @classmethod
    def __get_delta(cls, first: list, second: list):
        return [cls.__get_delta_x(first, second), cls.__get_delta_z(first, second)]





if __name__ == '__main__':
    """
    Sum of Forces and Moments Example
    """

    M = [Moment(5, np.array([0, 0, 0])),
         Moment(5, np.array([1, 0, 0])),
         Moment(-5, np.array([1, 1, 0]))]

    F = [Force(np.array([1, 0, 0]), np.array([0, 0, 0])),
         Force(np.array([0, 1, 0]), np.array([1, 0, 0])),
         Force(np.array([-1, 1, 0]), np.array([0, 1, 0]))]

    # Sys = ForceMomentBalance(moments=M, forces=F)
    # a = Sys.calculate(np.array([0,2,0]))

    """
    Cma calculation Example
    """

    coefficients = {
        'W': {
            'N': 7.6,
            'T': 3.6
        },
        'H': {
            'N': 7.6,
            'T': 3.6
        }
    }

    distances = {
        'X': {
            'W': 0.3,
            'H': -2.0
        },
        'Z': {
            'W': -0.1,
            'H': -0.05
        }
    }

    misc = {
        'Sh/S': 0.33,
        'Vh/V': 0.99,
        'de/da': 0.9
    }

    M = MomentCoefficientCalculations()
    print(M.aerial_cm())
    print(M.scooping_cm())
    print(M.cm_alpha())
