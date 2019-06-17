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
C_L_cruise = data['Aero']['CL_clean']    # -
C_D_0 = data['Aero']['Cd0']             # -
AR = data['Aero']['AR [-]']             # -
e = data['Aero']['e']                   # -
P_a = data['FPP']['Pa [kW] Ultim']            # kW
eta_p = data['FPP']['eta_p [-]']

# Other defined parameters #
rho_std = 1.225                         # kg/m^3
n_max = 4.4                             # -
n_min = -1.8                            # -
g = 9.80665                             # m/s^2
V_end = 130                             # m/s
V_step = 0.1                            # m/s
rho_fire = 0.75                         # kg/m^3 (.75 at ±200C) (.5 at ±400C)
C_L_max_to = 0.8*C_L_max                       # -
delta_e_to = 0.05
delta_e_landing = 0.10
delta_C_D_0_to = data['Aero']['delta_CD0_plain_TO']
delta_C_D_0_landing = data['Aero']['delta_CD0_plain_LAND']
V_stall_req = 35
rc_req = 10
c_V_req = 0.25
rho_alt = 0.9 # at 3 km
V_cruise_req = 100
s_landing_req_land = 500 # m
s_landing_req_water = 500 # m
f_land = 0.71
f_water = 0.71

# Conversions
ft_to_m = .3048
lbs_to_kg = .454
hp_to_W = 745.7



