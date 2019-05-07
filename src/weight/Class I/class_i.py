import numpy as np
from json_import import ReferenceAircraft, NameList
from breguet_calculations import PropellerCalculations, JetCalculations

import unittest as ut


def get_statistical_we(wto: float, coefficients: dict) -> float:
    """
    Get the empty weight from reference aircraft at wto
    :param wto: take off weight
    :param coefficients: dictionary with regression coefficients
    :return: statistical empty weight
    """
    return 10**((np.log10(wto) - coefficients['A'])/coefficients['B'])


def mff_calculation(weight_fraction_dict: dict) -> float:
    """
    :param weight_fraction_dict: Statistical values for mass fuel fraction
    :return: mass fuel fraction
    """
    mff = 1.0
    for key, weight in weight_fraction_dict.items():
        mff *= weight
        if int(key) > 8:
            raise IndexError("Too many Fuel Fractions in Dictionary")

    return mff


def wf_used_calculation(mff: float, wto: float) -> float:
    """
    :param mff: mass fuel fraction
    :param wto: take off weight
    :return: used fuel weight
    """
    return (1 - mff)*wto


def wf_calculation(mff: float, wto: float, wf_res: float) -> float:
    """
    :param mff: mass fuel fraction
    :param wto: take off weight
    :param wf_res: percentage of wto which should be assigned to reserve fuel (so values between 0 and 1)
    :return: total fuel weight
    """
    return wf_used_calculation(mff, wto) + wf_res*wto


def split(tup: tuple, N: int) -> np.array:
    """
    Split a range of values up in N items
    :param tup: tuple containing min and max value of the range
    :param N: number of items
    :return: array of items
    """
    return np.arange(tup[0], tup[1], (tup[1] - tup[0])/N)


def class_i_main(weight_dict: dict, performance_dict: dict, velocity_dict: dict, ac_data_dict: dict, **kwargs) -> dict or None:

    """
    Main function for performing Class I weight estimation using Roskam Statistical Data
    :param weight_dict: weights = {
        'wto': lbs,
        'wpl': lbs,
        'wfres': fraction of wto
    }
    :param performance_dict: performance = {
        'endurance': hrs,
        'range': nautical miles
    }
    :param velocity_dict: velocities = {
        'loiter': mph,
        'cruise': mph
    }
    :param ac_data_dict: ac_data = {
        'type': 'regional_tbp',
        'propulsion': 'propeller'
    }
    :param kwargs:  N - number of iterations
                    method - random, 1 value or 2 values
                    margin - how close the values need to converge and step size per iteration
    :return:
    """

    # Initialize Iteration and Calculation Settings
    if kwargs:
        try:
            max_iter = kwargs['N']

        except KeyError:
            max_iter = 50

        try:
            method = kwargs['method']

        except KeyError:
            method = 'random'

        try:
            margin = kwargs['margin']

        except KeyError:
            margin = 0.025

    else:
        max_iter = 50
        method = 'random'
        margin = 0.025

    # Initialize Data
    wto = weight_dict['wto']
    wpl = weight_dict['wpl']
    we = None
    wfres = weight_dict['wfres']

    ac_type = ac_data_dict['type']
    prop_type = ac_data_dict['propulsion']

    v_ltr = velocity_dict['loiter']
    v_cr  = velocity_dict['cruise']

    endurance = performance_dict['endurance']
    cruise_range = performance_dict['range']

    # Setup Reference Data
    RefAC = ReferenceAircraft(ac_type)
    breguet_data = RefAC.get_breguet_data()
    fuel_frac = RefAC.get_fuel_frac()

    # Setup Calculations
    if prop_type == 'propeller':

        if breguet_data['cruise']['cp']['min'] is None:
            return None

        try:
            propcalc = PropellerCalculations(breguet_data)

        except TypeError:
            return None

        if method == 'random':
            pass

        else:
            if len(method) == 1:
                propcalc.set_decision_options(method)

            elif len(method) == 2:
                propcalc.set_decision_options(method[0], method[1])

    elif prop_type == 'jet':

        if breguet_data['cruise']['cj']['min'] is None:
            return None

        try:
            jetcalc = JetCalculations(breguet_data)

        except TypeError:
            return None

        if method == 'random':
            pass

        else:
            if len(method) == 1:
                jetcalc.set_decision_options(method)

            elif len(method) == 2:
                jetcalc.set_decision_options(method[0], method[1])

    else:
        raise TypeError("Unknown Propulsion System Input")

    # Start Iteration Process
    for ii in range(max_iter):
        # print(f"Iteration {ii+1}")
        # Determine Fuel Weight
        if prop_type == 'propeller':
            fuel_frac['5'] = propcalc.cruise_fraction_calculation(cruise_range=cruise_range)
            fuel_frac['6'] = propcalc.loiter_fraction_calculation(endurance=endurance,
                                                                  v=v_ltr)

        elif prop_type == 'jet':
            fuel_frac['5'] = jetcalc.cruise_fraction_calculation(cruise_range=cruise_range,
                                                                 v=v_cr)
            fuel_frac['6'] = jetcalc.loiter_fraction_calculation(endurance=endurance)

        mff = mff_calculation(fuel_frac)
        wf = wf_calculation(mff=mff, wto=wto, wf_res=wfres)

        # Calculate Tentative Value for WE
        we_t = wto - wpl - wf

        # Get WE from statistics
        we_s = get_statistical_we(wto, RefAC.get_stat_coefficients())

        # Compare both empty weights, adjust WTO and repeat
        diff = (we_s - we_t)/wto

        if abs(diff) < margin:
            we = (we_t + we_s)/2.0
            # print(f"Difference = {round(diff*100, 3)}% of WTO")
            break

        elif diff > 0.0:
            # Do Something
            wto = wto*(1.0 + margin)

        elif diff < 0.0:
            # Do Something else
            wto = wto*(1.0 - margin)

    return {
        'weights':{
            'wto':wto,
            'wpl':wpl,
            'wf': wf,
            'we': we
        },
        'fractions':{
            'wpl': wpl/wto,
            'wf': wf/wto,
            'we': we/wto if we is not None else -1
        },
        'metadata':{
            'iterations': ii,
            'diff': diff
        }
    }


def class_i_comparison(wto: tuple, cr_range: tuple, endurance: tuple, prop: str = 'propeller',
                       v_ltr: float = 100.0, v_cr: float = 200.0) -> dict:

    steps = 10
    counter = 0

    result = {}

    wpl = 0.3

    for aircraft in NameList:
        # print(f"Calculating {aircraft}")
        result[aircraft] = []
        for wto_i in split(wto, steps):
            for range_i in split(cr_range, steps):
                for end_i in split(endurance, steps):
                    # print(f"Iteration {counter}")
                    weights = {
                        'wto': wto_i,
                        'wpl': wto_i*wpl,
                        'wfres': 0.05
                    }
                    performance = {
                        'endurance': end_i,
                        'range': range_i
                    }
                    velocities = {
                        'loiter': v_ltr,
                        'cruise': v_cr
                    }
                    ac_data = {
                        'type': aircraft,
                        'propulsion': prop
                    }

                    values = class_i_main(weights, performance, velocities, ac_data, N=100)

                    if values is not None:
                        result[aircraft].append(values)
                        counter += 1
    return result


"""
TESTS COME AFTER THIS
"""


class ClassITestCases(ut.TestCase):
    # TODO: Write tests
    def setUp(self):

        self.weight = {
            'wto': 10000.0,
            'wpl': 2000.0,
            'wfres': 0.05
        }
        self.performance = {
            'endurance': 5.0,
            'range': 1500.0
        }
        self.velocity = {
            'loiter': 80.0,
            'cruise': 240.0
        }
        self.ac_data_1 = {
            'type': 'regional_tbp',
            'propulsion': 'propeller'
        }
        self.ac_data_2 = {
            'type': 'business_jet',
            'propulsion': 'jet'
        }
        self.ac_data_3 = {
            'type': 'single_engine',
            'propulsion': 'jet'
        }

        self.RefAC = [ReferenceAircraft(name) for name in NameList]

    def tearDown(self):
        pass

    def test_split(self):
        minval = np.random.uniform(0, 1)
        maxval = np.random.uniform(minval, 2)

        N = np.random.randint(2, 10)

        result = split((minval, maxval), N)

        self.assertLessEqual(max(result), maxval)
        self.assertGreaterEqual(min(result), minval)
        self.assertEqual(len(result), N)

    def test_class_i(self):

        class_i_1 = class_i_main(self.weight, self.performance, self.velocity, self.ac_data_1, margin=0.033)
        class_i_2 = class_i_main(self.weight, self.performance, self.velocity, self.ac_data_2, N=100, method=(0.5,))
        class_i_3 = class_i_main(self.weight, self.performance, self.velocity, self.ac_data_3, method=(0.33, 0.66))

        self.assertLessEqual(class_i_1['metadata']['iterations'], 50)
        self.assertLessEqual(class_i_2['metadata']['iterations'], 100)
        self.assertIsNone(class_i_3)

        self.assertLessEqual(class_i_1['metadata']['diff'], 0.033)
        self.assertLessEqual(class_i_2['metadata']['diff'], 0.025)

    def test_fuel_functions(self):

        for AC in self.RefAC:
            ff = AC.get_fuel_frac()
            mff = mff_calculation(ff)

            self.assertLessEqual(len(ff), 8)
            self.assertLessEqual(mff, 1.0)

    def test_statistical_weight(self):

        for AC in self.RefAC:
            coeffs = AC.get_stat_coefficients()
            we = get_statistical_we(10000.0, coeffs)

            self.assertGreaterEqual(we, 0.0)
            self.assertLessEqual(we, 10000.0)


if __name__ == "__main__":

    ut.main()
