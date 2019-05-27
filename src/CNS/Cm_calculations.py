import numpy as np


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
        return self.__vector/self.get_magnitude()


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

    @staticmethod
    def cm_alpha(coefficients: dict, distances: dict, misc: dict):

        cma = coefficients['W']['N']['alpha'] * distances['X']['W'] + \
              coefficients['H']['N']['alpha'] * misc['Sh/S'] * (1 - misc['de/da']) * (misc['Vh/V'])**2 * distances['X']['H']  -\
              coefficients['W']['T']['alpha'] * distances['Z']['W'] -\
              coefficients['H']['T']['alpha'] * misc['Sh/S'] * (1 - misc['de/da']) * (misc['Vh/V'])**2 * distances['Z']['H']

        return cma

    @staticmethod
    def cm0(coefficients: dict, misc: dict):

        cm0 = coefficients['W']['Cmac'] - coefficients['H']['N']['alpha'] * \
              (misc['a0'] + misc['ih']) * (misc['Vh/V'])**2 * misc['Sh/S'] * misc['lh']/misc['c']

        return cm0

    @staticmethod
    def cm_de(coefficients: dict, misc: dict):

        cmde = - coefficients['H']['N']['delta'] * (misc['a0'] + misc['ih']) * \
               (misc['Vh/V']) ** 2 * misc['Sh/S'] * misc['lh'] / misc['c']

        return cmde


if __name__ == '__main__':

    """
    Sum of Forces and Moments Example
    """

    M = [Moment(5, np.array([0,0,0])),
         Moment(5, np.array([1,0,0])),
         Moment(-5, np.array([1,1,0]))]

    F = [Force(np.array([1,0,0]), np.array([0,0,0])),
         Force(np.array([0,1,0]), np.array([1,0,0])),
         Force(np.array([-1,1,0]), np.array([0,1,0]))]

    Sys = ForceMomentBalance(moments=M, forces=F)
    a = Sys.calculate(np.array([0,2,0]))


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

    cma = cm_alpha(coefficients, distances, misc)