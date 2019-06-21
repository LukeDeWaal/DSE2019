''' Gets the input from Google Sheets '''
import os
import sys

### Google Sheet Import ###
sys.path.insert(0, '/'.join(os.getcwd().split('/')[:-1]) + '/tools')
from GoogleSheetsImportMac import GoogleSheetsDataImport, SHEET_NAMES, SPREADSHEET_ID
data = GoogleSheetsDataImport(SPREADSHEET_ID, *SHEET_NAMES).get_data()

g = 9.80665                             # m/s^2

# Parameters from Google #
W_fuel =  data['Weights']['WF [N]']      # N 2200*g
W_mto = data['Weights']['WTO [N]']      # N 9000*g #
S = data['FPP']['S [m^2]']              # m^2 40.8 #
C_L_max = data['Aero']['CL_max']        # - 3.0 #
C_L_cruise = data['Aero']['CL_clean']    # - 1.448 #
C_D_0 = data['Aero']['Cd0']             # - 0.03 #
AR = data['Aero']['AR [-]']             # - 7.5 #
e = data['Aero']['e']                   # -  0.7 #
P_a = data['FPP']['Pa [kW] Ultim']            # kW 1626 #
eta_p = data['FPP']['eta_p [-]']        # - .85 #

# Other defined parameters #
rho_std = 1.225                         # kg/m^3
n_max = 4.4                             # -
n_min = -1.8                            # -

V_end = 130                             # m/s
V_step = 0.1                            # m/s
rho_fire = 0.75                         # kg/m^3 (.75 at ±200C) (.5 at ±400C)
C_L_max_to = 0.8*C_L_max                       # -
delta_e_to = 0.05
delta_e_landing = 0.10
delta_C_D_0_to = data['Aero']['delta_CD0_plain_TO'] #.036 #
delta_C_D_0_landing = data['Aero']['delta_CD0_plain_LAND']  # .144 #
V_stall_req = 120 / 3.6
rc_req = 10
c_V_req = 0.25
rho_alt = 0.909 # at 3 km
V_cruise_req = 300 / 3.6
s_landing_req_land = 500 # m
s_landing_req_water = 500 # m
f_land = 0.71
f_water = 0.71

# Conversions
ft_to_m = .3048
lbs_to_kg = .454
hp_to_W = 745.7



