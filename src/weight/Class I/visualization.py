import numpy as np
import matplotlib.pyplot as plt
from mpl_toolkits import mplot3d

from class_i import class_i_comparison
from json_import import NameList

import unittest as ut


def make_into_weight_arrays(result: dict):

    data = np.zeros((len(result), 3))

    for idx in range(len(result)):
        data[idx][0] = result[idx]['weights']['wto']
        data[idx][1] = result[idx]['weights']['wf']
        data[idx][2] = result[idx]['weights']['wpl']

    return data


def make_into_fractional_arrays(result: dict):

    data = np.zeros((len(result), 3))

    for idx in range(len(result)):
        data[idx][0] = result[idx]['fractions']['we']
        data[idx][1] = result[idx]['fractions']['wf']
        data[idx][2] = result[idx]['fractions']['wpl']

    return data


def plot_fractions(*names):

    fig = plt.figure()
    ax = plt.axes(projection='3d')

    result = class_i_comparison((10000, 40000), (500, 1500), (2.0, 4.0), prop='jet')

    if len(names) == 0:
        names = NameList

    data = [make_into_fractional_arrays(result[name]) for name in names]

    for idx, name in enumerate(names):
        ax.scatter3D(data[idx][:,0], data[idx][:,1], data[idx][:,2], label=" ".join([n.capitalize() for n in name.split('_')]))

    ax.set_xlabel('WE')
    ax.set_ylabel('WF')
    ax.set_zlabel('WPL')
    ax.legend()
    ax.set_xlim3d(0, 1.0)
    ax.set_ylim3d(0, 1.0)
    ax.set_zlim(0, 0.5)


if __name__ == "__main__":

    plot_fractions('military_trainer', 'fighters', 'mil_patrol', 'transport_jet', 'business_jet', 'amphibious')

    # TODO: Write tests

    class PlottingTestCases(ut.TestCase):

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
        suite = ut.TestLoader().loadTestsFromTestCase(PlottingTestCases)
        ut.TextTestRunner(verbosity=2).run(suite)


    run_TestCases()
