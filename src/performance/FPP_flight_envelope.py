### Imports ###
import numpy as np
import os
import sys
import matplotlib.pyplot as plt

### Google Sheet Import ###
sys.path.insert(0, '/'.join(os.getcwd().split('/')[:-1]) + '/tools')
from GoogleSheetsImportMac import GoogleSheetsDataImport, SHEET_NAMES, SPREADSHEET_ID
data = GoogleSheetsDataImport(SPREADSHEET_ID, *SHEET_NAMES).get_data()

# Parameters
W_fuel = data['Weights']['WF [N]']      # N
W_mto = data['Weights']['WTO [N]']      # N
rho_std = 1.225                         # kg/m^3
S = data['FPP']['S [m^2]']              # m^2
C_L_max = data['Aero']['CL_max']        # -
C_D_0 = data['Aero']['Cd0']             # -
AR = data['Aero']['AR [-]']             # -
e = data['Aero']['e']                   # -
P_a = data['FPP']['Pa [kW]']            # kW
n_max = 4.4                             # -
n_min = -1.8                            # -
V_D = 120                               # m/s
print(W_fuel/9.81, W_mto/9.81, S, C_L_max, C_D_0, AR, e, P_a)

### Main ###
# Velocity and loading arrays
V_array = np.arange(0.1,125,0.1)        # m/s
n_array = np.array([])                  # -
for i in range(len(V_array)):
    n_array = np.append(n_array, (0.5*rho_std*C_L_max*V_array[i]**2)/(W_mto/S))

# Aerodynamic parameters and power
C_L_list = []                           # -
C_D_list = []                           # -
P_r_list = []                           # kW
P_dif_list = []                         # kW

for i in range(len(V_array)):
    C_L_list.append(2*W_mto/(rho_std*V_array[i]**2*S))
    C_D_list.append(C_D_0+C_L_list[i]**2/(np.pi*AR*e))
    P_r_list.append(C_D_list[i]*0.5*rho_std*V_array[i]**3*S/1000.)
    P_dif_list.append(P_a-P_r_list[i])

C_L_array = np.array(C_L_list)
C_D_array = np.array(C_D_list)
P_r_array = np.array(P_r_list)
P_dif_array = np.array(P_dif_list)

# Stall speed
V_stall = np.sqrt((2*W_mto)/(rho_std*S*C_L_max))
V_stall_index = np.where(V_array > V_stall)[0][0]

# Min. speed at max. load
V_A_index = np.where(n_array > n_max)[0][0]
V_A = V_array[V_A_index]

# Max speed
V_max_indices = np.where(P_dif_array < 0)
V_max_index = V_max_indices[0][np.where(V_max_indices > V_stall_index)[1][0]]
V_max = V_array[V_max_index]

# Cruise speed
V_C = 0.9*V_max
V_C_index = np.where(V_array > V_C)[0][0]

# Lists for plotting
V_0A = V_array[0:V_A_index]
n_0A = n_array[0:V_A_index]
V_A_line = np.linspace(V_A,V_A,len(n_0A))
V_0h = V_array[0:V_stall_index]
n_0h = -1*n_array[0:V_stall_index]
n_stall_line_ver = np.linspace(-1.,1.,10)
V_stall_line_ver = np.linspace(V_stall,V_stall,10)
n_stall_line_hor = np.linspace(1.,1.,10)
V_stall_line_hor = np.linspace(0,V_max,10)
V_hf = V_array[V_stall_index:V_C_index]
n_hf = np.linspace(-1.0,n_min,len(V_hf))
n_cruise_line = np.concatenate((n_0h, n_hf), axis=None)
V_cruise_line = np.linspace(V_C,V_C,len(n_cruise_line))
V_fe = V_array[V_C_index:V_max_index]
n_fe = np.linspace(n_min,0,len(V_fe))
n_de = np.linspace(0,n_max,2)
V_de = np.linspace(V_max,V_max,2)
V_ae = np.linspace(V_A,V_max,2)
n_ae = np.linspace(n_max,n_max,2)

# Plot flight envelope
plt.plot(V_0A,n_0A,'blue')
plt.plot(V_0h,n_0h,'blue')
plt.plot(V_fe,n_fe,'blue')
plt.plot(V_de,n_de,'blue')
plt.plot(V_ae,n_ae,'blue')
plt.plot(V_hf,n_hf,'blue')
plt.plot(V_A_line,n_0A,'--',color='black')
plt.plot(V_stall_line_ver,n_stall_line_ver,'--',color='black')
plt.plot(V_stall_line_hor,n_stall_line_hor,'--',color='black')
plt.plot(V_cruise_line,n_cruise_line,'--',color='black')

plt.rcParams.update({'font.size': 16})
# plt.axhline(0, color='black')
plt.xlabel('V (m/s)')
plt.ylabel('n (-)')
plt.axis([0,V_D+5,n_min-0.2,n_max+0.6])
plt.grid(True)
plt.text(V_stall+1,-0.25, 'V_Stall')
plt.text(V_A-3,-0.25, 'V_A')
plt.text(V_C-7,0.1, 'V_Cruise')
plt.text(V_C-7,0.1, 'V_Cruise')
plt.text(V_max+1,0.1, 'V_Max.')
plt.show()

