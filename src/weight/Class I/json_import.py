import json
import os

import unittest as ut

NameList = ['homebuilt', 'single_engine', 'twin_engine', 'agricultural', 'business_jet', 'regional_tbp',
            'transport_jet', 'military_trainer', 'fighters', 'mil_patrol', 'amphibious']


class ReferenceAircraft(object):

    def __init__(self, name: str):

        self.name = name

        self.__fuel_fractions = self.__import_fuel_fractions(self.name)
        self.__breguet_data = self.__import_breguet_data(self.name)

    def get_fuel_frac(self):
        return self.__fuel_fractions

    def get_breguet_data(self):
        return self.__breguet_data

    @staticmethod
    def __import_data(data_type: str, name: str):
        cwd = os.getcwd()
        cwd = cwd.split('\\')

        roskam_folder = ''
        for folder in cwd:
            roskam_folder += folder + "\\"
            if folder == 'DSE2019':
                roskam_folder += "data\\roskam_statistics"
                break

        with open(roskam_folder + '\\' + f'{data_type}.json') as file:
            data = json.load(file)

        return data[name]

    def __import_fuel_fractions(self, name: str) -> list:
        return self.__import_data('fuel_frac', name)

    def __import_breguet_data(self, name: str) -> list:
        return self.__import_data('breguet_values', name)


if __name__ == "__main__":

    class DataImportTestCases(ut.TestCase):

        def setUp(self):

            self.RefAC = {}

            for name in NameList:
                self.RefAC[name] = ReferenceAircraft(name)

        def test_fuel_frac_count(self):
            """
            Test if all entries have the correct amount of fuel fractions in their data (6)
            """

            for AC in self.RefAC.values():
                self.assertEqual(6, len(AC.get_fuel_frac()))

        def test_fuel_frac_indices(self):
            """
            Test if all inndices have been implemented correctly
            """
            for AC in self.RefAC.values():
                for index in AC.get_fuel_frac().keys():
                    self.assertTrue(index in ['1', '2', '3', '4', '7', '8'])


    def run_TestCases():
        suite = ut.TestLoader().loadTestsFromTestCase(DataImportTestCases)
        ut.TextTestRunner(verbosity=2).run(suite)

    run_TestCases()