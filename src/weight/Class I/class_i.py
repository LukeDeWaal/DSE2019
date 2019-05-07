import numpy as np
from json_import import ReferenceAircraft, NameList
from breguet_calculations import PropellerCalculations, JetCalculations

import unittest as ut


def get_statistical_we(wto: float, coefficients: dict):
    """
    Get the empty weight from reference aircraft at wto
    :param wto: take off weight
    :param coefficients: dictionary with regression coefficients
    :return: statistical empty weight
    """
    return 10**((np.log10(wto) - coefficients['A'])/coefficients['B'])



def mff_calculation(weight_fraction_dict: dict):
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

def wf_used_calculation(mff: float, wto: float):
    """
    :param mff: mass fuel fraction
    :param wto: take off weight
    :return: used fuel weight
    """
    return (1 - mff)*wto


def wf_calculation(mff: float, wto: float, wf_res: float):
    """
    :param mff: mass fuel fraction
    :param wto: take off weight
    :param wf_res: percentage of wto which should be assigned to reserve fuel (so values between 0 and 1)
    :return: total fuel weight
    """
    return wf_used_calculation(mff, wto) + wf_res*wto


def class_i_main(weight_dict: dict, performance_dict: dict, velocity_dict: dict, ac_data_dict: dict, **kwargs):

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
    :param kwargs:  N - number of itrations
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
                jetcalc.set_decision_method(method)

            elif len(method) == 2:
                jetcalc.set_decision_method(method[0], method[1])

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
        we_s = get_statistical_we(wto, RefAC.get_coefficients())

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


def split(tup: tuple, N: int):
    return np.arange(tup[0], tup[1], (tup[1] - tup[0])/N)


def class_i_comparison(wto: tuple, cr_range: tuple, endurance: tuple, prop: str = 'propeller',
                       v_ltr: float = 100.0, v_cr: float = 200.0):

    steps = 10
    counter = 0

    result = {}

    wpl = 0.3

    for aircraft in NameList:
        print(f"Calculating {aircraft}")
        result[aircraft] = []
        for wto_i in split(wto, steps):
            for range_i in split(cr_range, steps):
                for end_i in split(endurance, steps):
                    print(f"Iteration {counter}")
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
                        result[aircraft].append(values )
                        counter += 1
    return result


if __name__ == "__main__":

    # TODO: Write tests

    class ClassITestCases(ut.TestCase):

        def setUp(self):
            pass

        def tearDown(self):
            pass

        def test_split(self):
            pass

        def test_class_i(self):
            pass

        def test_fuel_functions(self):
            pass

    def run_TestCases():
        suite = ut.TestLoader().loadTestsFromTestCase(ClassITestCases)
        ut.TextTestRunner(verbosity=2).run(suite)

    run_TestCases()
