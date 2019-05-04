import numpy as np
from .json_import import ReferenceAircraft, NameList
from .breguet_calculations import PropellerCalculations, JetCalculations

import unittest as ut


def mff_calculation(weight_fraction_list: list)

    mff = 1.0
    for weight in weight_fraction_list:
        mff *= weight

    return mff

def wf_used_calculation(mff: float, wto: float):

    return (1 - mff)*wto


def wf_calculation(wf_used: float, wf_res: float):
    pass