# Imports
import numpy as np
import matplotlib.pyplot as plt
from FPP_Parameters import V_end, V_step, W_mto, rho_std, S, C_D_0, AR, e, P_a, rho_fire, C_L_max, delta_e_to, \
    delta_e_landing, delta_C_D_0_to, delta_C_D_0_landing, C_L_cruise, C_L_max_to, V_stall_req, rc_req, eta_p, n_max, \
    c_V_req, rho_alt, V_cruise_req, s_landing_req_land, s_landing_req_water, f_land, f_water, ft_to_m, lbs_to_kg, \
    hp_to_W, g
from FPP_General_Definitions import V_row, aerodynamic_coefficients, P_r_calc, P_dif_calc, index_finder, V_stall_calc, \
    TOP_calc, V_max_calc, rho_altitude
from FPP_Flight_Envelope_Defs import arrays_maneuvre

colours = [  # Use these colours to cycle through if you want to plot multiple lines in the same plot
    (255 / 255, 0, 0), # red
    (255 / 255, 165 / 255, 0), # orange
    (132 / 255, 198 / 255, 0 / 255), # light green
    (30 / 255, 144 / 255, 255 / 255), # light blue
    (0, 0, 139 / 255), # dark blue
    (193 / 255, 38 / 255, 144 / 255) # purple
]
line_types = ['-', '--', ':', '-.']  # Choose one of these linetypes
marker_types = ['.', 'o', 'x']  # In case markers are desired, use one of these

def optimal_altitude():
    d_airport_fire = 50  # km

    h = np.arange(0, 3100, 100)
    print(h[-1])
    V_cruise = np.linspace(112.5, 123, len(h))
    V_cl = np.linspace(54, 63, len(h))
    rc = np.linspace(13.1, 12.3, len(h))

    V = V_row(0, 150 , 0.1)

    for i in range(len(h)):
        P_dif = P_dif_calc(V, W_mto, rho_altitude, S, C_D_0, AR, e, P_a)




        # t_cl = h[i] / rc[i]
        # d_cruise = d_airport_fire * 1000 - V_cl[i] * t_cl
        # t_arrival = t_cl + d_cruise/V_cruise[i]
        # print(t_arrival, t_cl, d_cruise)

    return


def power_diagram_bank():
    ''' Generate power diagram (available and required) for different densities. '''

    # Get velocity arrays (also for stall and plots)
    V_stall_std, V_stall_fire, V_std, V_fire, V_stall_std_line, V_stall_fire_line = V_performance()

    # Find power required for the two densities and plot
    V_Pa = np.linspace(0, V_end, 2)
    P_Pa = np.linspace(P_a, P_a, 2)

    # Generate figure, plot power available
    fig_power_bank = plt.figure(figsize=(20, 5))
    plt.plot(V_Pa, P_Pa, f'{line_types[0]}', c=colours[0], label='Power available')

    # Find power required for banked condition for two densities and plot
    x = 1  # to loop colours
    for i in range(0, 66, 15):
        if i == 15:
            x = x
        else:
            n = 1 / np.cos(i / 180 * np.pi)
            P_r_array_std_banked = P_r_calc(V_std, W_mto * n, rho_std, S, C_D_0, AR, e)
            plt.plot(V_std, P_r_array_std_banked, f'{line_types[0]}', c=colours[x],
                     label=f'Pr, {i} degrees banking')
            x = x + 1

    # Stall line
    P_stall_std = np.linspace(0, P_r_array_std_banked[0], 2)
    plt.plot(V_stall_std_line, P_stall_std, '--', color='black', linewidth=0.8)

    # Plot rest of figure
    axis_labels = ['V (m/s)', 'P (kW)']  # Set the axis labels
    axis_ranges = [(0, V_end), (0, 2500)]  # Set the axis ranges
    plot_title = 'Power Required at different banking angles, T = 15C'

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

    return V_stall_std, fig_power_bank


def power_diagram_temp():
    ''' Generate power diagram (available and required) for different densities. '''
    # Generate plot
    fig_power_temp = plt.figure(figsize=(20, 5))

    # Find power required for banked condition for two densities and plot
    density = [[15, 100, 200, 300, 400], [1.225, .947, .745, .617, .523]]
    P_stall_fire = np.linspace(0, P_a, 2)

    x = 0
    z = 0
    for i in density[1][:4]:
        if i < 1.225:
            z = 0

        # Get velocity arrays (also for stall and plots)
        V_stall_fire = V_stall_calc(W_mto, i, S, C_L_max)
        V_fire = V_row(V_stall_fire, V_end + 50, V_step)
        V_stall_fire_line = np.linspace(V_stall_fire, V_stall_fire, 2)

        # Find power required at different temperatures and plot (also the stall line)
        P_r_array_fire = P_r_calc(V_fire, W_mto, i, S, C_D_0, AR, e)

        T = density[0][x]
        plt.plot(V_fire, P_r_array_fire, f'{line_types[z]}', c=colours[x + 1],
                 label=f'Pr at T = {T}C')
        plt.plot(V_stall_fire_line, P_stall_fire, '--', color='black', linewidth=0.8)

        # Loop colours
        x = x + 1

    # Determine maximum velocity for plotting range
    V_stall_index = index_finder(V_fire, V_stall_fire)
    V_max, V_max_index = V_max_calc(V_stall_index, V_fire, W_mto, i, S, C_D_0, AR, e, P_a)

    # Power available
    V_Pa = np.linspace(0, V_max + 10, 2)
    P_Pa = np.linspace(P_a, P_a, 2)
    plt.plot(V_Pa, P_Pa, f'{line_types[0]}', c=colours[0], label='Power available')

    # Plot rest
    axis_labels = ['V (m/s)', 'P (kW)']  # Set the axis labels
    plot_title = 'Power Required at different temperatures'
    axis_ranges = [(0, int(V_max + 5)), (0, 2500)]  # Set the axis ranges
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

    return V_stall_fire, fig_power_temp


def rc_diagram_temp():
    ''' Generates the rate of climb diagram for different densities. '''

    # Generate figure
    fig_rc_temp = plt.figure(figsize=(20, 5))

    # Temperature-Density table
    density = [[15, 100, 200, 300, 400], [1.225, .947, .745, .617, .523]]

    # Stall line

    # Find rate of climb for different temperatures and plot
    x = 0
    for i in density[1][:5]:
        # Get specific velocity arrays and stalls
        V_stall_fire = V_stall_calc(W_mto, i, S, C_L_max)
        V = V_row(V_stall_fire, V_end + 50, V_step)
        V_stall_fire_line = np.linspace(V_stall_fire, V_stall_fire, 2)


        # Get excess power for the two densities
        P_dif_fire = P_dif_calc(V, W_mto, i, S, C_D_0, AR, e, P_a)

        # Calculate rate of climb (*1000 because of kW to W)
        RC_fire = P_dif_fire * 1000 / W_mto

        # Calculate maximum rc
        if i == 1.225:
            RC_fire_max = max(RC_fire)

        RC_stall_fire = np.linspace(0, RC_fire[0], 2)

        # Plot lines (including stall line)
        plt.plot(V, RC_fire, f'{line_types[0]}', c=colours[x + 1], label=f'RC at {density[0][x]}C')
        plt.plot(V_stall_fire_line, RC_stall_fire, '--', color='black', linewidth=0.8)

        x = x + 1

    # Plotting of rate of climb diagram
    axis_labels = ['Velocity, V (m/s)', 'Rate of Climb, RC (m/s)']  # Set the axis labels
    axis_ranges = [(0, V_end + 20), (0, 14)]  # Set the axis ranges
    plot_title = 'Rate of Climb at different temperatures'

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

    return RC_fire_max, fig_rc_temp


def rc_diagram_bank():
    ''' Generates the rate of climb diagram for different densities. '''

    # Generate figure
    fig_rc_bank = plt.figure(figsize=(20, 5))


    # Velocity arrays and stall
    V_stall_std = V_stall_calc(W_mto, rho_std, S, C_L_max)
    V_std = V_row(V_stall_std, V_end, V_step)
    V_stall_fire_line = np.linspace(V_stall_std, V_stall_std, 2)

    # Calculate rate of climb for different banking angles and plot
    x = 1
    for i in range(0, 66, 15):
        # Skip 15 degrees
        if i == 15:
            x = x
        else:
            # Find load factor
            n = 1 / np.cos(i / 180 * np.pi)

            # Calculate excess in power and find rc
            P_dif_std = P_dif_calc(V_std, W_mto * n, rho_std, S, C_D_0, AR, e, P_a)
            RC_std = P_dif_std * 1000 / W_mto

            # Find maximum rc
            if i == 0:
                RC_std_max = RC_std[0]

            # Plot
            plt.plot(V_std, RC_std, f'{line_types[0]}', c=colours[x], label=f'RC, {i} degrees banking')
            x = x + 1

    # Plotting of rate of climb diagram
    axis_labels = ['Velocity, V (m/s)', 'Rate of Climb, RC (m/s)']  # Set the axis labels
    axis_ranges = [(0, V_end), (0, 14)]  # Set the axis ranges
    plot_title = 'Rate of Climb at different banking angles, T = 15C'


    # Lines for stall
    RC_stall_std = np.linspace(0, RC_std_max, 2)
    plt.plot(V_stall_fire_line, RC_stall_std, '--', color='black', linewidth=0.8)

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

    return max(RC_std), fig_rc_bank


def V_performance():
    ''' Generate velocity arrays and stuff for the performance diagrams. '''

    # Get stall velocities for different densities
    V_stall_std = V_stall_calc(W_mto, rho_std, S, C_L_max)
    V_stall_fire = V_stall_calc(W_mto, rho_fire, S, C_L_max)

    # Generate velocity arrays
    V_std = V_row(V_stall_std, V_end, V_step)
    V_fire = V_row(V_stall_fire, V_end, V_step)

    # Velocity lines for plotting
    V_stall_std_line = np.linspace(V_stall_std, V_stall_std, 2)
    V_stall_fire_line = np.linspace(V_stall_fire, V_stall_fire, 2)

    return V_stall_std, V_stall_fire, V_std, V_fire, V_stall_std_line, V_stall_fire_line


def drag_polar():
    ''' Generate drag polar for different configurations. '''

    # Get aerodynamic parameters for different configurations
    C_D_0_landing = C_D_0 + delta_C_D_0_landing
    C_D_0_to = C_D_0 + delta_C_D_0_to
    e_landing = e + delta_e_landing
    e_to = e + delta_e_to

    # Get velocity array
    V_stall_std, V_stall_fire, V_std, V_fire, V_stall_std_line, V_stall_fire_line = V_performance()
    V_std = np.append(V_std, np.arange(V_std[-1] + 0.1, V_end + 300, V_step))

    # Get CL and CD arrays
    C_L_clean, C_D_clean = aerodynamic_coefficients(V_std, W_mto, rho_std, S, C_D_0, AR, e)
    C_L_landing, C_D_landing = aerodynamic_coefficients(V_std, W_mto, rho_std, S, C_D_0_landing, AR, e_landing)
    C_L_to, C_D_to = aerodynamic_coefficients(V_std, W_mto, rho_std, S, C_D_0_to, AR, e_to)

    clean_index = np.where(C_L_clean < C_L_cruise)[0][0]
    to_index = np.where(C_L_to < C_L_max_to)[0][0]
    C_L_clean, C_D_clean = C_L_clean[clean_index:], C_D_clean[clean_index:]
    C_L_to, C_D_to = C_L_to[to_index:], C_D_to[to_index:]

    # Plot drag polar
    fig_drag = plt.figure(figsize=(20, 5))

    axis_labels = ['Drag Coefficient, CD (-)', 'Lift Coefficient, CL (-)']  # Set the axis labels
    axis_ranges = [(0, 0.7), (0, 3.5)]  # Set the axis ranges
    plot_title = 'Drag Polar at different configurations'

    plt.plot(C_D_landing, C_L_landing, f'{line_types[0]}', c=colours[2], label='Landing')
    plt.plot(C_D_to, C_L_to, f'{line_types[0]}', c=colours[3], label='Take-off')
    plt.plot(C_D_clean, C_L_clean,f'{line_types[0]}', c=colours[1], label='Cruise')

    plt.plot([0, C_D_clean[0]], [C_L_clean[0], C_L_clean[0]], '--', color='black', linewidth=0.8)
    plt.plot([0, C_D_to[0]], [C_L_to[0], C_L_to[0]], '--', color='black', linewidth=0.8)
    plt.plot([0, C_D_landing[0]], [C_L_landing[0], C_L_landing[0]], '--', color='black', linewidth=0.8)

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

    return fig_drag


def power_loading():
    fig_powerloading = plt.figure(figsize=(20, 5))
    plt.plot(W_mto / S, W_mto / P_a / 1000, f'{marker_types[1]}', markersize = 4 ,c=colours[0], label='Design')

    linestyles = [':', '-.', '-']
    wing_loading = np.arange(1, 3000, 1)

    # # Stall
    # x = 0
    # for i in np.arange(C_L_max - 0.6, C_L_max, 0.3):
    #     wing_stall = 0.5 * rho_std * V_stall_req ** 2 * i
    #     wing_stall = np.linspace(wing_stall, wing_stall, 2)
    #     power_stall = np.linspace(0, 1, 2)
    #
    #     plt.plot(wing_stall, power_stall, f'{linestyles[x]}', c=colours[3], label=f'Stall at {round(V_stall_req, 1)} m/s for C_L_max of {round(i, 3)}')
    #     x = x + 1

    # Rate of climb
    # x = 0
    # for i in np.arange(rc_req-2, rc_req+4, 2):
    #
    #     C_L_rc, C_D_rc = np.sqrt(3*C_D_0*np.pi*AR*e),  4*C_D_0
    #     power_rc = eta_p/(i+(np.sqrt(wing_loading*2/rho_std)/(C_L_rc**1.5/C_D_rc)))
    #
    #     plt.plot(wing_loading, power_rc, f'{linestyles[x]}', c=colours[1], label=f'Rate of climb of {i} m/s')
    #     x = x + 1
    #
    # # Climb gradient
    # x = 0
    # for i in np.arange(AR - 2, AR + 4, 2):
    #     C_L_max_to = 0.8*C_L_max
    #     power_cv = eta_p / (np.sqrt(wing_loading * 2 / rho_std / C_L_max_to) * (c_V_req + (C_D_0 + C_L_max_to ** 2 / (np.pi * i * e)) / C_L_max_to))
    #
    #     plt.plot(wing_loading, power_cv, f'{linestyles[x]}', c=colours[3], label=f'Climb gradient (25%) with AR of {i}')
    #     x = x + 1

    # # Cruise
    # x = 0
    # for i in np.arange(AR - 2, AR + 4, 2):
    #     power_cruise = 0.8 * eta_p * (rho_alt / rho_std) ** 0.75 * (C_D_0 * 0.5 * rho_alt * V_cruise_req ** 3 / wing_loading + wing_loading / (np.pi * i * e * 0.5 * rho_alt * V_cruise_req)) ** (-1)
    #     plt.plot(wing_loading, power_cruise, f'{linestyles[x]}', c=colours[4], label=f'Cruise at {round(V_cruise_req, 1)} m/s with A of {i}')
    #     x = x + 1

    # # Landing
    # x = 0
    # for i in np.arange(C_L_max - 0.6, C_L_max, 0.3):
    #     wing_landing_land = 0.5 * rho_std * i * s_landing_req_land / 0.5915 / f_land
    #     wing_landing_land = np.linspace(wing_landing_land, wing_landing_land, 2)
    #
    #     # wing_landing_water = 0.5 * rho_std * i * s_landing_req_water/0.5915/f_water
    #     # wing_landing_water = np.linspace(wing_landing_water, wing_landing_water, 2)
    #
    #     power_landing = np.linspace(0, 1, 2)
    #
    #     # plt.plot(wing_landing_water, power_landing, linestyles[x], color='darkorchid', label=f'Landing (land and water) for C_L_max of {round(i, 3)}')
    #
    #     plt.plot(wing_landing_land, power_landing, f'{linestyles[x]}', c=colours[4],
    #          label=f'Landing (land and water) for C_L_max of {round(i, 3)}')
    #
    #     x = x + 1
    #
    # # Take-off
    # TOP = TOP_calc(s_landing_req_land, ft_to_m, lbs_to_kg, hp_to_W, g)
    #
    # x = 0
    # for i in np.arange(C_L_max, C_L_max + 0.7, 0.3):
    #     C_L_max_to = 0.8 * i
    #     power_to = TOP * C_L_max_to / wing_loading
    #
    #     plt.plot(wing_loading, power_to, f'{linestyles[x]}', c=colours[3],
    #          label=f'Take-off (land) for C_L_max of {round(i, 3)}')
    #
    #     x = x + 1
    #
    # # # Load factor maneuvring
    # # # V_array, n_array, V_stall, V_stall_index, V_A, V_A_index, V_max, V_max_index, V_C, V_C_index = arrays_maneuvre()
    # # V_A = 100
    # # n_max = 4.4
    # # power_n = eta_p / (C_D_0 * 0.5 * rho_std * V_A ** 3 / wing_loading + wing_loading * n_max ** 2 / (
    # #             np.pi * AR * e * 0.5 * rho_std * V_A))
    # # plt.plot(wing_loading, power_n, linestyles[2], color='mediumorchid',
    # #          label=f'Maximum maneuvre load factor of {n_max}')
    # # turn_rate = (g / V_A) * np.sqrt(n_max ** 2 - 1)
    # # print(turn_rate)

    axis_labels = ['Wing Loading, W/S (N/m^2)', 'Power Loading, W/P (N/W)']  # Set the axis labels
    axis_ranges = [(0, 3000), (0, .6)]  # Set the axis ranges
    plot_title = 'Power- and Wingloading diagram'



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

    return fig_powerloading


def lift_over_drag():

    fig_LD = plt.figure(figsize=(20, 5))

    x = 0
    for i in [9000, 6500, 5500, 4500, 3800]:
        if i == 9000:
            V_stall_alt = V_stall_calc(i * g, rho_alt, S, C_L_max)
            V_std_alt = V_row(V_stall_alt, V_end, V_step)
            C_L, C_D = aerodynamic_coefficients(V_std_alt, i * g, rho_alt, S, C_D_0, AR, e)
            L_D_alt = C_L / C_D

            plt.plot(V_std_alt, L_D_alt, f'{line_types[1]}', c=colours[x], label=f'W = {i} kg at 3 km')

        V_stall = V_stall_calc(i * g, rho_std, S, C_L_max)
        V_std = V_row(V_stall, V_end, V_step)
        C_L, C_D = aerodynamic_coefficients(V_std, i * g, rho_std, S, C_D_0, AR, e)
        L_D = C_L / C_D

        plt.plot(V_std, L_D, f'{line_types[0]}', c=colours[x], label= f'W = {i} kg at 0 km')

        x = x + 1

    axis_labels = ['Velocity, V (m/s)', 'Lift over Drag, L/D (-)']  # Set the axis labels
    axis_ranges = [(0, 125), (0, 14)]  # Set the axis ranges
    plot_title = 'L/D vs Velocity at different weights'


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



    return L_D, fig_LD


def lift_over_drag_alt():

    fig_LD_alt = plt.figure(figsize=(20, 5))

    x = 0
    for i in [9000, 6500, 5500, 4500, 3800]:
        if i == 9000:
            V_stall = V_stall_calc(i * g, rho_std, S, C_L_max)
            V_std = V_row(V_stall, V_end, V_step)
            C_L, C_D = aerodynamic_coefficients(V_std, i * g, rho_std, S, C_D_0, AR, e)
            L_D = C_L / C_D

            plt.plot(V_std, L_D, f'{line_types[0]}', c=colours[x], label= f'W = {i} kg at 0 km')

        V_stall_alt = V_stall_calc(i * g, rho_alt, S, C_L_max)
        V_std_alt = V_row(V_stall_alt, V_end, V_step)
        C_L, C_D = aerodynamic_coefficients(V_std_alt, i * g, rho_alt, S, C_D_0, AR, e)
        L_D_alt = C_L / C_D

        plt.plot(V_std_alt, L_D_alt, f'{line_types[1]}', c=colours[x], label=f'W = {i} kg at 3 km')

        x = x + 1

    axis_labels = ['Velocity, V (m/s)', 'Lift over Drag, L/D (-)']  # Set the axis labels
    axis_ranges = [(0, 125), (0, 12)]  # Set the axis ranges
    plot_title = 'L/D vs Velocity at cruise altitude for different weights'


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



    return L_D_alt, fig_LD_alt


