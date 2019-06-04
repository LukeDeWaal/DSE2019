import numpy as np
import os
import sys
sys.path.insert(0, '\\'.join(os.getcwd().split('\\')[:-1]) + '\\tools')

from GoogleSheetsImport import GoogleSheetsDataImport, SHEET_NAMES, SPREADSHEET_ID


class GearPositioning(object):

    def __init__(self):

        try:
            self.__data = GoogleSheetsDataImport(SPREADSHEET_ID, *SHEET_NAMES).get_data()

        except (PermissionError, ConnectionError, ConnectionRefusedError, ConnectionAbortedError):
            print("No Data Found In Current Path")
            self.__data = None

        self.cg = self.__data['C&S']['CG_abs']

    def y_mlg(self, psi):

        ymlg = (self.__get_delta_x(self.__data['NLG'], self.cg) + self.__get_delta_x(self.__data['MLG'], self.cg))/np.sqrt((self.__get_delta_x(self.__data['NLG'], self.cg) * np.tan(psi)/self.cg[1])**2 - 1)
        return ymlg

    def tip_clearance(self):

        ymlg = span/2 - zt/np.tan(phi)

    @staticmethod
    def __get_delta_x(first: list, second: list):
        return second[0] - first[0]

    @staticmethod
    def __get_delta_z(first: list, second: list):
        return second[1] - first[1]

    @classmethod
    def __get_delta(cls, first: list, second: list):
        return [cls.__get_delta_x(first, second), cls.__get_delta_z(first, second)]