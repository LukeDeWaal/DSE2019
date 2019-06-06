''' Gets the input from Google Sheets '''
import os
import sys
import numpy as np

### Google Sheet Import ###

# Mac to windows: select correct file to import from (so: GoogleSheetsImport) and change '/' to '\\'
print()
sys.path.insert(0, '/'.join(os.getcwd().split('/')[:-1]) + '/tools')
from GoogleSheetsImportMac import GoogleSheetsDataImport, SHEET_NAMES, SPREADSHEET_ID
data = GoogleSheetsDataImport(SPREADSHEET_ID, *SHEET_NAMES).get_data()

# Conversions
m_to_ft = 1/.3048
kg_to_lbs = 1/.454
N_m2_to_lb_ft2 = 0.2248
L_to_gal = 0.22 # imperial gallon
g = 9.80665
m_to_inch = 39.37

A = data['Aero']['AR [-]'] # -
A_h = 3.83 # -
A_v = 1.3 # -
B_w = m_to_ft*data['Aero']['Wing Span'] # ft
D = m_to_ft*2.5 # ft
F_w = m_to_ft*0.2 # ft
Ht_Hv = 1.
I_y = -1.
K_door = 1.0
K_Lg = 1.12
K_mp = 1.0
K_ng = 1.0
K_np = 1.0
K_p = 1.4
K_r = 1.0
K_tp = .793
K_tr = 1.0
K_uht = 1.0
L = m_to_ft*data['Structures']['Max_fuselage_length'] # ft
L_a = m_to_ft*5.0 # ft
L_ec = m_to_ft*4.0 # ft
L_f = L
L_m = m_to_inch*2.0 # ft
L_n = m_to_inch*1.0 # ft
L_t = m_to_ft*1.5 # ft
Lambda = 0.
Lambda_ht = 0.
Lambda_vt = 0,
lambda_ = 1.0
lambda_h = 1.0
lambda_vt = 0.3
M = 0.25
N_c = 0.
N_en = 1
N_f = 7.
N_gen = N_en
N_Lt = m_to_ft*data['FPP']['Engine Length [m]'] # ft
N_l = 1.5*4.4 # -
N_m = 2.
N_mss = 2.
N_mw = 2.
N_p = 0.
N_t = 2.
N_w = m_to_ft*data['FPP']['Engine Width [m]'] # ft
N_z = 1.5*data['FPP']['n_ult [-]'] # -
q = 0.5*0.9*100**2*0.2248 # lb/ft^2 at 3km altitude (rho = 0.9)
R_kva = 50.
S_cs = m_to_ft**2*6.08 # ft^2
S_csw = m_to_ft**2*3.26 # ft^2
S_e = m_to_ft**2*2.82 # ft^2
S_f = m_to_ft**2*data['Structures']['Wetted Area'] #ft^2
S_ht = m_to_ft**2*data['C&S']['Sh'] #ft^2
S_n = N_w*N_Lt # ft^2
S_vt = m_to_ft**2*data['C&S']['Sv'] #ft^2
S_w =  m_to_ft**2*data['FPP']['S [m^2]'] #ft^2
tc = .15
tc_root = .15
V_i = data['Weights']['WF [N]']/g/804.*L_to_gal # gal (804 is density of jet fuel)
V_p = V_i
V_pr = 0.
V_stall = 35*m_to_ft # ft/s
V_t = data['Weights']['WF [N]']/g/804.*L_to_gal # gal (804 is density of jet fuel)
W_av = -1.
W_c = kg_to_lbs*data['Weights']['WF [N]']/g # lbs
W_dg = kg_to_lbs*0.5*data['Weights']['WF [N]']/g # lbs
W_en = kg_to_lbs*data['FPP']['Engine Weight [N]']/g # lbs
W_fw = 0.
W_l = 2/3*kg_to_lbs*data['Weights']['WTO [N]']/g # lbs
W_press = 0.
W_uav = kg_to_lbs*100

K_ws = 0.75*(1+2*lambda_)/(1+lambda_)*B_w*np.tan(Lambda/L)
K_y = 0.3*L_t
K_z = L_t
W_ec = 2.331*W_en**0.901*K_p*K_tr # lbs

