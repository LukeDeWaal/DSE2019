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

    def __dictionary_pos_unpack_search(self, source: dict, target: dict = {}, top_key: str = ''):

        cg = self.__data['geometry']['cg']

        for key, value in source.items():
            if key == "pos":

                delta_x = self.__get_delta_x(value, cg)
                delta_z = self.__get_delta_z(value, cg)

                target[top_key] = [delta_x, delta_z]

            else:
                if type(value) == dict:
                    self.__dictionary_pos_unpack_search(source[key], target, key)

    def cm(self):
        print(self.__data['C&S']['Sh'], type(self.__data['C&S']['Sh']))
        # tail_volume = self.__data['C&S']['Sh'] / self.__data['geometry']['S'] * (
        # self.__data['geometry']['Vh/V']) ** 2
        # thrust_coefficient = self.__data['P']['Tc'] * 2 * (self.__data['P']['D'] ** 2) / self.__data['geometry']['S']
        # ip = self.__data['P']['ip']
        #
        # deltas = {}
        # self.__dictionary_pos_unpack_search(self.__data, deltas)
        #
        # wing_contribution = self.__data['coefficients']['W']['cmac'] + self.__data['coefficients']['W']['N'] * \
        #                     deltas['W'][0] - self.__data['coefficients']['W']['T'] * deltas['W'][1]
        # tail_contribution = tail_volume * (
        #             self.__data['coefficients']['H']['N'] * deltas['H'][0] - self.__data['coefficients']['H']['T'] *
        #             deltas['H'][1])
        # thrust_contribution = thrust_coefficient * deltas['P'][1]
        #
        # return wing_contribution + tail_contribution + thrust_contribution

    @staticmethod
    def __get_delta_x(first: list, second: list):
        return second[0] - first[0]

    @staticmethod
    def __get_delta_z(first: list, second: list):
        return second[1] - first[1]

    def cm_alpha(self, coefficients: dict, distances: dict, misc: dict):

        deltas = {}
        self.__dictionary_pos_unpack_search(self.__data, deltas)

        wing_contribution = None
        # TODO: Incorporate JSON format in all methods

    def cm0(self, coefficients: dict, misc: dict):

        cm0 = coefficients['W']['Cmac'] - coefficients['H']['N']['alpha'] * \
              (misc['a0'] + misc['ih']) * (misc['Vh/V']) ** 2 * misc['Sh/S'] * misc['lh'] / misc['c']

        return cm0

    def cm_de(self, coefficients: dict, misc: dict):

        cmde = - coefficients['H']['N']['delta'] * (misc['a0'] + misc['ih']) * \
               (misc['Vh/V']) ** 2 * misc['Sh/S'] * misc['lh'] / misc['c']

        return cmde


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
    cm = M.cm()
