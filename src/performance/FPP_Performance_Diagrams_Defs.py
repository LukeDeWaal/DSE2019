# Imports
import numpy as np
import matplotlib.pyplot as plt
from FPP_Parameters import V_end, V_step, W_mto, rho_std, S, C_D_0, AR, e, P_a, rho_fire, C_L_max, delta_e_to, \
    delta_e_landing, delta_C_D_0_to, delta_C_D_0_landing, C_L_cruise, C_L_max_to, V_stall_req, rc_req, eta_p, n_max, \
    c_V_req, rho_alt, V_cruise_req, s_landing_req_land, s_landing_req_water, f_land, f_water, ft_to_m, lbs_to_kg, \
    hp_to_W, g
from FPP_General_Definitions import V_row, aerodynamic_coefficients, P_r_calc, P_dif_calc, index_finder, V_stall_calc, \
    TOP_calc
from FPP_Flight_Envelope_Defs import arrays_maneuvre


def power_diagram():
    ''' Generate power diagram (available and required) for different densities. '''

    # Get velocity arrays (also for stall and plots)
    V_stall_std, V_stall_fire, V_std, V_fire, V_stall_std_line, V_stall_fire_line = V_performance()

    # Find power required for the two densities
    P_r_array_std = P_r_calc(V_std, W_mto, rho_std, S, C_D_0, AR, e)
    P_r_array_fire = P_r_calc(V_fire, W_mto, rho_fire, S, C_D_0, AR, e)

    # Arrays for line plotting
    V_Pa = np.linspace(0, V_end, 2)
    P_Pa = np.linspace(P_a, P_a, 2)

    P_stall_std = np.linspace(0, 1.5 * P_a, 2)
    P_stall_fire = np.linspace(0, 1.5 * P_a, 2)

    # Plotting of power diagram
    plt.plot(V_Pa, P_Pa, 'navy', label='Power available')
    plt.plot(V_std, P_r_array_std, 'orange', label='Power required, standard atmosphere (15C)')
    plt.plot(V_fire, P_r_array_fire, 'firebrick', label='Power required, fire atmosphere (200C)')

    plt.plot(V_stall_std_line, P_stall_std, '--', color='black', linewidth=0.8)
    plt.plot(V_stall_fire_line, P_stall_fire, '--', color='black', linewidth=0.8)

    plt.xlabel('V (m/s)')
    plt.ylabel('P (kW)')
    plt.axis([0, V_end, 0, 1.5 * P_a])
    plt.grid(True)
    plt.title('Power vs. Velocity')
    plt.legend(loc='upper left')

    plt.show()

    return V_stall_std, V_stall_fire


def rc_diagram():
    ''' Generates the rate of climb diagram for different densities. '''

    # Get velocity arrays (also for stall and plots)
    V_stall_std, V_stall_fire, V_std, V_fire, V_stall_std_line, V_stall_fire_line = V_performance()

    # Get excess power for the two densities
    P_dif_std = P_dif_calc(V_std, W_mto, rho_std, S, C_D_0, AR, e, P_a)
    P_dif_fire = P_dif_calc(V_fire, W_mto, rho_fire, S, C_D_0, AR, e, P_a)

    # Calculate (maximum) rate of climb (*1000 because of kW to W)
    RC_std = P_dif_std * 1000 / W_mto
    RC_fire = P_dif_fire * 1000 / W_mto

    RC_std_max = max(RC_std)
    RC_fire_max = max(RC_fire)

    # Arrays for line plotting
    RC_stall_std = np.linspace(0, 1.5 * P_a, 2)
    RC_stall_fire = np.linspace(0, 1.5 * P_a, 2)

    # Plotting of rate of climb diagram
    plt.plot(V_std, RC_std, 'orange', label='Rate of Climb, standard atmosphere (15C)')
    plt.plot(V_fire, RC_fire, 'firebrick', label='Rate of Climb, fire atmosphere (200C)')

    plt.plot(V_stall_std_line, RC_stall_std, '--', color='black', linewidth=0.8)
    plt.plot(V_stall_fire_line, RC_stall_fire, '--', color='black', linewidth=0.8)

    plt.xlabel('V (m/s)')
    plt.ylabel('RC (m/s)')
    plt.axis([0, V_end, 0, int(max(RC_std) + 1)])
    plt.grid(True)
    plt.title('Rate of Climb vs. Velocity')
    plt.legend(loc='best')

    plt.show()

    return RC_std_max, RC_fire_max


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
    plt.plot(C_L_clean, C_D_clean, 'gold', label='clean')
    plt.plot(C_L_landing, C_D_landing, 'orange', label='landing, gear up')
    plt.plot(C_L_to, C_D_to, 'firebrick', label='take-off, gear up')

    plt.xlabel('Lift Coefficient (-)')
    plt.ylabel('Drag Coefficient (-)')
    plt.axis([0, 3, 0, 0.6])
    plt.grid(True)
    plt.title('Drag Polar')
    plt.legend(loc='upper left')

    plt.show()

    return


def power_loading():
    plt.plot(W_mto / S, W_mto / P_a / 1000, marker='o', markersize=3, color='black')

    linestyles = [':', '-.', '-']
    wing_loading = np.arange(1, 3000, 1)

    # Stall
    x = 0
    for i in np.arange(C_L_max-0.6, C_L_max, 0.3):

        wing_stall = 0.5 * rho_std * V_stall_req ** 2 * i
        wing_stall = np.linspace(wing_stall, wing_stall, 2)
        power_stall = np.linspace(0, 1, 2)

        plt.plot(wing_stall, power_stall, linestyles[x], color = 'gold', label= f'Stall for C_L_max of {round(i,3)}')
        x = x + 1

    # # Rate of climb
    # x = 0
    # for i in np.arange(rc_req-2, rc_req+4, 2):
    #
    #     C_L_rc, C_D_rc = np.sqrt(3*C_D_0*np.pi*AR*e),  4*C_D_0
    #     power_rc = eta_p/(i+(np.sqrt(wing_loading*2/rho_std)/(C_L_rc**1.5/C_D_rc)))
    #
    #     plt.plot(wing_loading, power_rc, linestyles[x], color='firebrick', label= f'Rate of climb of {i} m/s')
    #     x = x + 1
    #
    # # Climb gradient
    # x = 0
    # for i in np.arange(AR - 2, AR + 4, 2):
    #     C_L_max_to = 0.8*C_L_max
    #     power_cv = eta_p / (np.sqrt(wing_loading * 2 / rho_std / C_L_max_to) * (c_V_req + (C_D_0 + C_L_max_to ** 2 / (np.pi * i * e)) / C_L_max_to))
    #
    #     plt.plot(wing_loading, power_cv, linestyles[x], color='forestgreen', label=f'Climb gradient (25%) with AR of {i}')
    #     x = x + 1
    #
    # Cruise
    x = 0
    for i in np.arange(AR - 2, AR + 4, 2):
        power_cruise = 0.8*eta_p * (rho_alt/rho_std)**0.75 * (C_D_0*0.5*rho_alt*V_cruise_req**3/wing_loading+wing_loading/(np.pi*i*e*0.5*rho_alt*V_cruise_req))**(-1)

        plt.plot(wing_loading, power_cruise, linestyles[x], color='steelblue', label=f'Cruise at {V_cruise_req} m/s with A of {i}')
        x = x + 1

    # Landing
    x = 0
    for i in np.arange(C_L_max - 0.6, C_L_max, 0.3):
        wing_landing_land = 0.5 * rho_std * i * s_landing_req_land/0.5915/f_land
        wing_landing_land = np.linspace(wing_landing_land, wing_landing_land, 2)

        # wing_landing_water = 0.5 * rho_std * i * s_landing_req_water/0.5915/f_water
        # wing_landing_water = np.linspace(wing_landing_water, wing_landing_water, 2)

        power_landing = np.linspace(0, 1, 2)

        plt.plot(wing_landing_land, power_landing, linestyles[x], color='darkorchid', label=f'Landing (land and water) for C_L_max of {round(i, 3)}')
        # plt.plot(wing_landing_water, power_landing, linestyles[x], color='darkorchid', label=f'Landing (land and water) for C_L_max of {round(i, 3)}')

        x = x + 1

    # Take-off
    TOP = TOP_calc(s_landing_req_land, ft_to_m, lbs_to_kg, hp_to_W, g)

    x = 0
    for i in np.arange(C_L_max, C_L_max+0.7, 0.3):
        C_L_max_to = 0.8*i
        power_to = TOP * C_L_max_to / wing_loading

        plt.plot(wing_loading, power_to, linestyles[x], color='pink', label=f'Take-off (land) for C_L_max of {round(i, 3)}')
        x = x + 1

    # # Load factor maneuvring
    # # V_array, n_array, V_stall, V_stall_index, V_A, V_A_index, V_max, V_max_index, V_C, V_C_index = arrays_maneuvre()
    # V_A = 100
    # n_max = 4.4
    # power_n = eta_p / (C_D_0 * 0.5 * rho_std * V_A ** 3 / wing_loading + wing_loading * n_max ** 2 / (
    #             np.pi * AR * e * 0.5 * rho_std * V_A))
    # plt.plot(wing_loading, power_n, linestyles[2], color='mediumorchid',
    #          label=f'Maximum maneuvre load factor of {n_max}')
    # turn_rate = (g / V_A) * np.sqrt(n_max ** 2 - 1)
    # print(turn_rate)

    plt.xlabel('Wing Loading, W/S (N/m^2)')
    plt.ylabel('Power Loading, W/P (N/W)')
    plt.axis([0, 3000, 0, 0.6])
    plt.grid(True)
    plt.title('W/P vs. W/S diagram')
    plt.legend(loc='best')

    plt.show()
    return
