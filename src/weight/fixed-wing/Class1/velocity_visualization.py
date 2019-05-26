import numpy as np
import matplotlib.pyplot as plt
from mpl_toolkits import mplot3d

from class_i import class_i_range_n_endurance, class_i_payload_n_speed
from json_import import NameList

import unittest as ut


def make_into_velocity_arrays(result: dict):
    """
    Function to put the data from the Class I resultant velocities and fractions file into a numpy array
    :param result: Dictionary obtained from the class_i_payload_n_speed function
    :return: numpy array with loiter and cruise speed, and payload fraction
    """

    data = np.zeros((len(result), 3))

    for idx in range(len(result)):
        data[idx][0] = result[idx]['velocities']['vltr']
        data[idx][1] = result[idx]['velocities']['vcr']
        data[idx][2] = result[idx]['fractions']['wpl']

    return data


def plot_fractions(propulsion_type: str = 'propeller', *names):
    """
    Plot the Payload fraction against Loiter and Cruise speed for certain aircraft types and propulsion types
    :param propulsion_type: propeller or jet
    :param names: roskam category names
    :return: None
    """

    fig = plt.figure()
    ax = plt.axes(projection='3d')

    result = class_i_payload_n_speed(wto=20000.0, wpl=(0.1, 0.6), v_cr=(100, 250), v_ltr=(50, 150),
                                     cr_range=1000.0, endurance=4.0)

    if len(names) == 0:
        names = NameList

    data = [make_into_velocity_arrays(result[name]) for name in names]

    for idx, name in enumerate(names):
        ax.scatter3D(data[idx][:,0], data[idx][:,1], data[idx][:,2], label=" ".join([n.capitalize() for n in name.split('_')]))

    ax.set_xlabel('$V_{Loiter} [mph]$')
    ax.set_ylabel('$V_{Cruise} [mph]$')
    ax.set_zlabel('WPL [-]')
    ax.legend()
    ax.title.set_text(propulsion_type.capitalize())
    # ax.set_xlim3d(0, 1.0)
    # ax.set_ylim3d(0, 1.0)
    # ax.set_zlim(0, 0.5)


"""
TESTS COME AFTER THIS
"""


if __name__ == "__main__":

    class PlottingTestCases(ut.TestCase):

        def setUp(self):

            low_weight = np.random.randint(5000, 15000)
            high_weight = np.random.randint(low_weight, 40000)

            low_range = np.random.randint(250, 750)
            high_range = np.random.randint(low_range, 2000)

            low_endurance = np.random.uniform(1.0, 2.0)
            high_endurance = np.random.uniform(low_endurance, 5.0)

            self.propeller_results_dict = class_i_range_n_endurance((low_weight, high_weight), (low_range, high_range),
                                                                    (low_endurance, high_endurance), prop='propeller')
            self.jet_results_dict = class_i_range_n_endurance((low_weight, high_weight), (low_range, high_range),
                                                              (low_endurance, high_endurance), prop='jet')

        def tearDown(self):
            pass

        def test_make_weight_array(self):

            for name in NameList:
                prop = make_into_velocity_arrays(self.propeller_results_dict[name])
                jet = make_into_velocity_arrays(self.jet_results_dict[name])

                self.assertEqual(len(self.propeller_results_dict[name]), prop.shape[0])
                self.assertEqual(len(self.jet_results_dict[name]), jet.shape[0])

        def test_make_fraction_array(self):

            for name in NameList:
                prop = make_into_velocity_arrays(self.propeller_results_dict[name])
                jet = make_into_velocity_arrays(self.jet_results_dict[name])

                self.assertEqual(len(self.propeller_results_dict[name]), prop.shape[0])
                self.assertEqual(len(self.jet_results_dict[name]), jet.shape[0])

        def test_plots(self):

            plot_fractions('propeller')
            plot_fractions('jet')


    def run_TestCases():
        suite = ut.TestLoader().loadTestsFromTestCase(PlottingTestCases)
        ut.TextTestRunner(verbosity=2).run(suite)

    run_TestCases()
