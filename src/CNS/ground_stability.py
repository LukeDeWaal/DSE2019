import numpy as np
import os
import sys
import math
sys.path.insert(0, '\\'.join(os.getcwd().split('\\')[:-1]) + '\\tools')

from GoogleSheetsImport import GoogleSheetsDataImport, SHEET_NAMES, SPREADSHEET_ID


class GearPositioning(object):

    def __init__(self):

        try:
            self.__data = GoogleSheetsDataImport(SPREADSHEET_ID, *SHEET_NAMES).get_data()

        except (PermissionError, ConnectionError, ConnectionRefusedError, ConnectionAbortedError):
            print("No Data Found In Current Path")
            self.__data = None

        self.cg = self.__data['C&S']['CG_aft']
        self.XMLG, self.ZMLG = self.MLG_loc()

    def MLG_loc(self):
        x_cg = self.cg[0]
        z_cg = self.cg[1]
        tipback_angle_deg = self.__data['C&S']['Tipback angle']
        tipback_angle_rad = (tipback_angle_deg*math.pi)/180
        low_side_fuselage = 10 - self.__data['Structures']['Max_fuselage_height']/2
        z_tail = low_side_fuselage + 0.84
        x_tail = self.__data['Structures']['Max_fuselage_length'] + 1

        X_MLG = (math.cos(tipback_angle_rad))**2 * x_cg + (math.sin(tipback_angle_rad))**2 * x_tail -0.5*(z_tail-z_cg)*math.sin(2*tipback_angle_rad)
        Z_MLG = (1/math.tan(tipback_angle_rad))*(x_cg - X_MLG) + z_cg
        return X_MLG, Z_MLG

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

if __name__ == '__main__':
    gear = GearPositioning()
    print(gear.XMLG,gear.ZMLG)