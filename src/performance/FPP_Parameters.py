''' Gets the input from Google Sheets '''
import os
import sys

### Google Sheet Import ###
sys.path.insert(0, '/'.join(os.getcwd().split('/')[:-1]) + '/tools')
from GoogleSheetsImportMac import GoogleSheetsDataImport, SHEET_NAMES, SPREADSHEET_ID
data = GoogleSheetsDataImport(SPREADSHEET_ID, *SHEET_NAMES).get_data()

# Parameters from Google #
W_fuel = data['Weights']['WF [N]']      # N
W_mto = data['Weights']['WTO [N]']      # N
S = data['FPP']['S [m^2]']              # m^2
C_L_max = data['Aero']['CL_max']        # -
C_D_0 = data['Aero']['Cd0']             # -
AR = data['Aero']['AR [-]']             # -
e = data['Aero']['e']                   # -
P_a = data['FPP']['Pa [kW]']            # kW

# Other defined parameters #
rho_std = 1.225                         # kg/m^3
n_max = 4.4                             # -
n_min = -1.8                            # -
g = 9.80665                             # m/s^2



