import json
import os, pathlib
import numpy as np

g0 = 9.80665


class ClassII(object):

    def __init__(self, name: str, filepath: str = r"C:\Users\LRdeWaal\Desktop\DSE2019\data\Class II Data\\", datadict: dict = {}):

        self.__name = name
        self.__fp = filepath
        self.__datadict = datadict

        self.__full_data = dict()
        self.__data = dict()

        self.__read_from_json()

        self.wing_area()
        self.climb_rate_max()
        self.clean_CL_calculation()
        self.climb_rate_clean()

        self.__write_to_json()

    def __write_to_json(self):

        self.__full_data[self.__name] = self.__data

        with open(self.__fp, 'w') as file:
            json.dump(self.__full_data, file)

    def __read_from_json(self):

        try:
            with open(self.__fp, 'r') as file:
                self.__full_data = json.load(file)

            try:
                self.__data = dict(self.__full_data[self.__name])

            except KeyError:
                self.__data = self.__datadict

        except (json.decoder.JSONDecodeError, FileNotFoundError):
            pathlib.Path(self.__fp).touch()
            self.__data = self.__datadict

    def get_data(self):
        return self.__data

    def wing_area(self):

        # Load Factor
        n = 1.0 / np.cos(self.__data['performance']['bankangle'])

        # Lift Required
        L = self.__data['weights']['wto'] * g0 * n

        # Wing Area
        rho = 1.225
        S = 2 * L / (self.__data['aerodynamics']['CL_max'] * rho * self.__data['velocities']['loiter'] ** 2)

        self.__data['wing']['area'] = S
        span = self.__data['wing']['span']
        self.__data['wing']['chord'] = S/span
        self.__data['wing']['AR'] = (span**2)/S
        self.__data['performance']['loadfactor'] = n

    def climb_rate_max(self):

        # Calculate Cd
        Cd = self.__data['aerodynamics']['Cd0'] + (self.__data['aerodynamics']['CL_max'] ** 2) / (
                    np.pi * self.__data['wing']['span'] / self.__data['wing']['chord'] * self.__data['aerodynamics']['oswald'])

        # Calculate Power Required
        rho = 1.225
        self.__data['performance']['Pr'] = Cd * 0.5 * rho * self.__data['wing']['area'] * (self.__data['velocities']['loiter'] ** 3)

        # Diff
        diff = self.__data['performance']['Pa'] - self.__data['performance']['Pr']

        # Climb Rate
        self.__data['performance']['RC_max'] = diff / (self.__data['weights']['wto'] * g0)

    def climb_rate_clean(self):

        # Calculate Cd
        Cd = self.__data['aerodynamics']['Cd0'] + (self.__data['aerodynamics']['CL_clean'] ** 2) / (
                    np.pi * self.__data['wing']['span'] / self.__data['wing']['chord'] * self.__data['aerodynamics']['oswald'])

        # Calculate Power Required
        rho = 1.225
        self.__data['performance']['Pr'] = Cd * 0.5 * rho * self.__data['wing']['area'] * (self.__data['velocities']['loiter'] ** 3)

        # Diff
        diff = self.__data['performance']['Pa'] - self.__data['performance']['Pr']

        # Climb Rate
        self.__data['performance']['RC_clean'] = diff / (self.__data['weights']['wto'] * g0)

    def clean_CL_calculation(self):

        rho = 1.225
        self.__data['aerodynamics']['CL_clean'] = 2*(self.__data['weights']['wto'] * g0)/(rho*self.__data['wing']['area']*(self.__data['velocities']['loiter']**2))



if __name__ == "__main__":
    # TODO: Write Tests
    pass
