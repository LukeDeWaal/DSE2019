import numpy as np
from FPP_General_Definitions import V_row, aerodynamic_coefficients, P_r_calc, P_dif_calc, index_finder, V_stall_calc, \
    TOP_calc, V_max_calc, rho_altitude, V_cruise_calc, V_climb_calc, rc_calc
from FPP_Parameters import V_end, V_step, W_mto, rho_std, S, C_D_0, AR, e, P_a, rho_fire, C_L_max, delta_e_to, \
    delta_e_landing, delta_C_D_0_to, delta_C_D_0_landing, C_L_cruise, C_L_max_to, V_stall_req, rc_req, eta_p, n_max, \
    c_V_req, rho_alt, V_cruise_req, s_landing_req_land, s_landing_req_water, f_land, f_water, ft_to_m, lbs_to_kg, \
    hp_to_W, g
import matplotlib.pyplot as plt

def arrays_maneuvre(rho):
    ''' Generate the arrays required for the maneuvre diagram. '''

    V_array = V_row(30, 150, V_step)
    V_stall = V_stall_calc(W_mto, rho, S, C_L_max)
    V_stall_index = index_finder(V_array, V_stall)
    V_max, V_max_index = V_max_calc(V_stall_index, V_array, W_mto, rho, S, C_D_0, AR, e, P_a)
    V_C = V_cruise_calc(V_max)

    return V_array, V_stall, V_stall_index, V_max, V_max_index, V_C


d_airport_fire = 50  # km
h = np.arange(0, 3100, 100)

rho = rho_altitude(h)

V_max = []
V_stall = []
V_cruise = []
V_climb = []

for i in range(len(h)):
    V_array, Vstall, V_stall_index, Vmax, V_max_index, V_C = arrays_maneuvre(rho[i])
    Vclimb = V_climb_calc(V_array, W_mto, rho[i], S, C_D_0, AR, e, P_a)
    V_max.append(Vmax)
    V_stall.append(Vstall)
    V_cruise.append(V_C)
    V_climb.append(Vclimb)

V_max = np.array(V_max)
V_stall = np.array(V_stall)
V_cruise = np.array(V_cruise)
V_climb = np.array(V_climb)

RC = rc_calc(V_array, W_mto, rho, S, C_D_0, AR, e, P_a)

t_climb_list = []
t_cruise_list = []
t_total_list = []

for i in range(len(h)):
    t_climb = 0
    t_cruise = 0
    t_total = 0

    d_climb = 0

    x = 100
    for j in range(0, h[i] + x, x):
        j = int(j / x)
        V_climb_index = index_finder(V_array, V_climb[j])
        t_this_climb = x / RC[int(j)][int(j)]
        t_climb = t_climb + t_this_climb
        d_climb = d_climb + V_climb[j] * t_this_climb

    d_cruise = d_airport_fire * 1000 - d_climb
    t_cruise = d_cruise / V_cruise[i]

    t_total = t_climb + t_cruise

    t_climb_list.append(t_climb)
    t_cruise_list.append(t_cruise)
    t_total_list.append(t_total)


# Plot
colours = [  # Use these colours to cycle through if you want to plot multiple lines in the same plot
    (255 / 255, 0, 0),
    (107 / 255, 142 / 255, 35 / 255),
    (30 / 255, 144 / 255, 255 / 255),
    (0, 0, 139 / 255),
    (255 / 255, 165 / 255, 0),
    (34 / 255, 139 / 255, 34 / 255)
]
line_types = ['-', '--']  # Choose one of these linetypes
marker_types = ['.', 'o', 'x']  # In case markers are desired, use one of these
plot_label = 'label'  # Set the desired label
axis_labels = ['Altitude, h (m)', 'Time, t (s)']  # Set the axis labels
axis_ranges = [(0, 3000), (0, 600)]  # Set the axis ranges
plot_title = f'Attack time at different cruise altitudes for {d_airport_fire} km between airport and fire'

fig = plt.figure(figsize=(20,5))
plt.plot(h, t_climb_list, f'{line_types[0]}', c=colours[0], label='Climbing time')
plt.plot(h, t_cruise_list, f'{line_types[0]}', c=colours[1], label='Cruising time')
plt.plot(h, t_total_list, f'{line_types[0]}', c=colours[2], label='Total time')
plt.xlim(axis_ranges[0][0], axis_ranges[0][1])
plt.ylim(axis_ranges[1][0], axis_ranges[1][1])
plt.xticks(fontsize=12)
plt.yticks(fontsize=12)
plt.grid(True)
plt.legend()
plt.xlabel(axis_labels[0], fontsize=16)
plt.ylabel(axis_labels[1], fontsize=16)
plt.title(plot_title, fontsize=18)

plt.show()
