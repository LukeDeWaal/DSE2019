import numpy as np
from .json_import import ReferenceAircraft, NameList
from .breguet_calculations import PropellerCalculations, JetCalculations

import unittest as ut


def mff_calculation(weight_fraction_list: list):
    """
    :param weight_fraction_list: Statistical values for mass fuel fraction
    :return: mass fuel fraction
    """
    mff = 1.0
    for weight in weight_fraction_list:
        mff *= weight

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


def main(w_pl: float, wto_guess: float, ref_ac: str, max_iter: int, endurance: float, cruise_range: float, v_ltr: float, v_cr: float, ac_type: str, reserve_frac: float):
    # TODO: Refactor this code
    """
    :param w_pl:
    :param wto_guess:
    :param ref_ac:
    :param max_iter:
    :param endurance:
    :param cruise_range:
    :param v_ltr:
    :param v_cr:
    :param ac_type:
    :return:
    """
    wto = float(wto_guess)
    RefAC = ReferenceAircraft(ref_ac)

    breguet_data = RefAC.get_breguet_data()
    fuel_frac = list(RefAC.get_fuel_frac().values())

    for _ in range(max_iter):

        #Determine Fuel Weight

        if ac_type == 'propeller':
            fuel_frac.append(PropellerCalculations(breguet_data).cruise_fraction_calculation(range=cruise_range))
            fuel_frac.append(PropellerCalculations(breguet_data).loiter_fraction_calculation(endurance=endurance,
                                                                                             v=v_ltr))

        elif ac_type == 'jet':
            fuel_frac.append(JetCalculations(breguet_data).cruise_fraction_calculation(range=cruise_range,
                                                                                       v=v_cr))
            fuel_frac.append(JetCalculations(breguet_data).loiter_fraction_calculation(endurance=endurance))

        mff = mff_calculation(fuel_frac)
        wf = wf_calculation(mff=mff, wto=wto, wf_res=reserve_frac)

        # Calculate Tentative Value for WE
        we_t = wto - w_pl - wf

        # Get WE from statistics
        # TODO: Add coefficient data and create code to extract we

        # Compare both empty weights, adjust WTO and repeat

        pass