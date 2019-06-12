import numpy as np

import os
import sys
sys.path.insert(0, '\\'.join(os.getcwd().split('\\')[:-1]) + '\\tools')

from GoogleSheetsImport import GoogleSheetsDataImport, SHEET_NAMES, SPREADSHEET_ID


def vtail_size(k, flight, vratio):

    data = dict(GoogleSheetsDataImport(SPREADSHEET_ID, *SHEET_NAMES).get_data())

    lh = data['C&S']['H Wing'][0] - data['C&S']['Wing'][0]
    chord = data['Aero']['Wing chord']

    if flight == 'cruise':
        tc = 0.383
    elif flight == 'loiter':
        tc = 0.5446

    return 2*(tc/2/data['Aero']['CL_A-h']*(data['FPP']['Prop Diameter [m]']/2+data['Structures']['Max_fuselage_width']/2)*1.1/(lh/chord)*(data['FPP']['Prop Diameter [m]'])**2)/(vratio**2+k+1)


if __name__ == '__main__':

    Sv = vtail_size(1.1, 'loiter', 1.0)
