import numpy as np

import unittest as ut


class Calculations(object):

    def __init__(self, data_dict: dict):

        self.__data_dict = data_dict

        self.__cruise_data = self.__data_dict['cruise']
        self.__loiter_data = self.__data_dict['loiter']

        self.decision_options = dict()
        self.decision_options['method'] = 'random'
        self.decision_options['value'] = None
        self.decision_options['lower'] = 0
        self.decision_options['upper'] = 1

    def get_cruise_data(self):
        return self.__cruise_data

    def get_loiter_data(self):
        return self.__loiter_data

    @staticmethod
    def extract_value(lower: float, upper: float, settings: dict):
        """
        Method to extract a value for a coefficient given the decision options
        :param lower: Min of range
        :param upper: Max of range
        :param settings: decison_options dictionary
        :return: value for coefficient
        """
        if lower is None or upper is None:
            return

        if settings['method'] == 'single':
            return lower + settings['value'] * (upper - lower)

        elif settings['method'] == 'random':
            new_lower = lower + settings['lower'] * (upper - lower)
            new_upper = lower + settings['upper'] * (upper - lower)
            return np.random.uniform(new_lower, new_upper)

    def set_seed(self, seed: int):
        """
        Set the seed for the numpy randomization functions
        :param seed: seed
        """
        np.random.seed(seed)

    def set_decision_options(self, *args):
        """
        Change the decision options using this method.
        :param args: One input: This is a value from 0 to 1.
                     Eg. if the coefficient ranges from 3-5, then with input = 0.3, a value of 3+0.3*(5-3) will be chosen
                     Two inputs: Both values from 0 to 1.
                     Eg. if the coefficient ranges from 3-5, then with input = 0.3, 0.5,
                     a random value between 3+0.3*(5-3) and 3+0.5*(5-3) will be chosen.
                     Think of it as a weight assignment
        """
        if len(args) == 1:
            self.decision_options['method'] = 'single'
            self.decision_options['value'] = args[0]
            self.decision_options['lower'] = None
            self.decision_options['upper'] = None

        elif len(args) == 2:
            self.decision_options['method'] = 'random'
            self.decision_options['value'] = None
            self.decision_options['lower'] = args[0]
            self.decision_options['upper'] = args[1]


class PropellerCalculations(Calculations):

    def __init__(self, data_dict: dict):

        super().__init__(data_dict=data_dict)

        self.lift_drag_ratio = None
        self.cp = None
        self.calculate_parameters()

    def calculate_parameters(self):

        self.lift_drag_ratio = self.extract_value(self.get_loiter_data()['L/D']['min'],
                                                  self.get_loiter_data()['L/D']['max'],
                                                  self.decision_options)

        self.cp = self.extract_value(self.get_loiter_data()['cp']['min'],
                                     self.get_loiter_data()['cp']['max'],
                                     self.decision_options)

    def loiter_fraction_calculation(self, endurance: float, v: float):

        return np.exp(-(endurance/375.0)*(v/self.lift_drag_ratio)*(self.cp/self.get_loiter_data()['np']))

    def cruise_fraction_calculation(self, cruise_range: float):

        return np.exp(-(cruise_range / (375.0 * self.lift_drag_ratio)) * (self.cp / self.get_cruise_data()['np']))


class JetCalculations(Calculations):

    def __init__(self, data_dict: dict):

        super().__init__(data_dict=data_dict)

        self.lift_drag_ratio = None
        self.cj = None
        self.calculate_parameters()

    def calculate_parameters(self):

        self.lift_drag_ratio = self.extract_value(self.get_loiter_data()['L/D']['min'],
                                                  self.get_loiter_data()['L/D']['max'],
                                                  self.decision_options)

        self.cj = self.extract_value(self.get_loiter_data()['cj']['min'],
                                     self.get_loiter_data()['cj']['max'],
                                     self.decision_options)

    def loiter_fraction_calculation(self, endurance: float):

        return np.exp(-(endurance*(self.cj/self.lift_drag_ratio)))

    def cruise_fraction_calculation(self, cruise_range: float, v: float):

        return np.exp(-(cruise_range / self.lift_drag_ratio) * (self.cj / v))


if __name__ == "__main__":

    class CalculationTestCases(ut.TestCase):
        # TODO: Finish Testcases for breguet calculations
        def setUp(self):
            pass

        def tearDown(self):
            pass

        def test_extract_value(self):
            pass

        def test_set_seed(self):
            pass

        def test_decision_options(self):
            pass

        def test_loiter(self):
            pass

        def test_cruise(self):
            pass


    def run_TestCases():
        suite = ut.TestLoader().loadTestsFromTestCase(CalculationTestCases)
        ut.TextTestRunner(verbosity=2).run(suite)


    run_TestCases()