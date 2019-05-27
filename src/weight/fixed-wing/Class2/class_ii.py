import json
import os, pathlib
import numpy as np
import pandas as pd

g0 = 9.80665

import sys
sys.path.insert(0, r'C:\Users\LRdeWaal\Desktop\DSE2019\src\tools')

from WebScraping import extract_filtered_data, import_engine_Data


class ClassII(object):

    def __init__(self, name: str, filepath: str = r"C:\Users\LRdeWaal\Desktop\DSE2019\data\Class II Data\\", datadict: dict = {}):

        self.__name = name
        self.__fp = filepath
        self.__datadict = datadict

        self.__full_data = dict()
        self.__data = dict()
        self.__engine_data = pd.concat([import_engine_Data('civ'), import_engine_Data('mil')])
        self.__engine_data = self.__engine_data.reset_index(drop=True)

        self.__read_from_json()

        self.wing_area()
        self.steady_power_available()
        self.turning_power_available()
        self.clean_CL_calculation()

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
        AR = self.__data['wing']['AR']
        self.__data['wing']['chord'] = np.sqrt(S/AR)
        self.__data['wing']['span'] = np.sqrt(S*AR)
        self.__data['performance']['loadfactor'] = n

    def calculate_cd(self):

        return self.__data['aerodynamics']['Cd0'] + (self.__data['aerodynamics']['CL_max'] ** 2) / (
                    np.pi * self.__data['wing']['span'] / self.__data['wing']['chord'] * self.__data['aerodynamics'][
                'oswald'])

    @staticmethod
    def __normalize_array(array: np.array):

        for i in range(array.shape[1]):
            col_min = np.min(array[:,i])
            col_max = np.max(array[:,i])

            array[:,i] = (array[:,i] - col_min)/(col_max - col_min)

        return array

    def pick_engine(self, Pa: float):

        engines = extract_filtered_data({'Power': (Pa, 1.5*Pa)}, dataframe=self.__engine_data)
        engines = engines.sort_values('Power')

        delta_p = engines[['Power']] - Pa

        try:
            engines['DeltaP'] = delta_p

        except ValueError:
            return None

        #  Uncomment for weight optimization algorithm
        normalized = self.__normalize_array(np.array(engines[['DeltaP', 'Weight', 'SFC']]))

        weights = np.array([0.65, 0.1, 0.25])

        costs = np.zeros((normalized.shape[0],1))

        for i in range(len(normalized[:,0])):
            costs[i,:] = np.dot(normalized[i, :], weights)

        min_idx = costs.argmin()

        try:
            # print(engines.loc[0], engines['DeltaP'].idxmin())
            return engines.loc[min_idx]  # engines.loc[engines['DeltaP'].idxmin()]

        except (ValueError, KeyError):
            return None

    def steady_power_available(self):

        Cd = self.calculate_cd()

        Pr = 0.5 * Cd * 1.225 * self.__data['wing']['area'] * (self.__data['velocities']['loiter']**3)
        self.__data['performance']['steady']['Pr'] = Pr

        Pa = Pr + self.__data['performance']['steady']['RC'] * (self.__data['weights']['wto'] * g0)
        self.__data['performance']['steady']['Pa'] = Pa

        power_per_engine = Pa / (1000.0 * self.__data['performance']['n_engines'])

        engine = self.pick_engine(power_per_engine)

        if engine is None:
            self.__data['performance']['engine'] = {
                'Model': None,
                'Pa': None,
                'Weight': None,
                'SFC': None,
                'Size': (None, None)
            }

        else:
            self.__data['performance']['engine'] = {
                'Model': engine.loc['Model'],
                'Pa': engine.loc['Power']*1000.0,
                'Weight': engine.loc['Weight'],
                'SFC': engine.loc['SFC'],
                'Size': (engine.loc['Length'], engine.loc['Diameter'])
            }

            New_Pa = self.__data['performance']['engine']['Pa'] * self.__data['performance']['n_engines']
            self.__data['performance']['steady']['Pa'] = New_Pa

            self.__data['performance']['steady']['RC'] = (New_Pa - Pr) / (self.__data['weights']['wto'] * g0)

    def turning_power_available(self):

        Cd = self.calculate_cd()

        Pr = 0.5 * Cd * 1.225 * self.__data['wing']['area'] * (self.__data['velocities']['loiter'] ** 3)
        self.__data['performance']['turning']['Pr'] = Pr

        RC = (self.__data['performance']['steady']['Pa'] - Pr)/(self.__data['weights']['wto'] * g0 * self.__data['performance']['loadfactor'])

        self.__data['performance']['turning']['Pa'] = self.__data['performance']['steady']['Pa']
        self.__data['performance']['turning']['RC'] = RC

    # def climb_rate_max(self):
    #
    #     # Calculate Cd
    #     Cd = self.calculate_cd()
    #
    #     # Diff
    #     excess_power = self.__data['performance']['Pa'] - self.__data['performance']['Pr']
    #
    #     # Climb Rate
    #     self.__data['performance']['RC_max'] = excess_power / (self.__data['weights']['wto'] * g0)
    #
    # def climb_rate_clean(self):
    #
    #     # Calculate Cd
    #     Cd = self.__data['aerodynamics']['Cd0'] + (self.__data['aerodynamics']['CL_clean'] ** 2) / (
    #                 np.pi * self.__data['wing']['span'] / self.__data['wing']['chord'] * self.__data['aerodynamics']['oswald'])
    #
    #     # Calculate Power Required
    #     rho = 1.225
    #     self.__data['performance']['Pr'] = Cd * 0.5 * rho * self.__data['wing']['area'] * (self.__data['velocities']['loiter'] ** 3)
    #
    #     # Diff
    #     diff = self.__data['performance']['Pa'] - self.__data['performance']['Pr']
    #
    #     # Climb Rate
    #     self.__data['performance']['RC_clean'] = diff / (self.__data['weights']['wto'] * g0)

    def clean_CL_calculation(self):

        rho = 1.225
        self.__data['aerodynamics']['CL_clean'] = 2*(self.__data['weights']['wto'] * g0)/(rho*self.__data['wing']['area']*(self.__data['velocities']['loiter']**2))



if __name__ == "__main__":
    # TODO: Write Tests
    pass
