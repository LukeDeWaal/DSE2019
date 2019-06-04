# Imports
import numpy as np
import matplotlib.pyplot as plt
from FPP_Parameters import V_end, V_step, W_mto, rho_std, S, C_D_0, AR, e, P_a, rho_fire, C_L_max
from FPP_General_Definitions import V_row, P_r_calc, P_dif_calc, V_stall_calc

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

    P_stall_std = np.linspace(0, 1.5*P_a, 2)
    P_stall_fire = np.linspace(0, 1.5*P_a, 2)

    # Plotting of power diagram
    plt.plot(V_Pa, P_Pa, 'navy', label = 'Power available')
    plt.plot(V_std, P_r_array_std, 'orange', label = 'Power required, standard atmosphere (15C)')
    plt.plot(V_fire, P_r_array_fire, 'firebrick', label = 'Power required, fire atmosphere (200C)')

    plt.plot(V_stall_std_line, P_stall_std, '--', color='black', linewidth=0.8)
    plt.plot(V_stall_fire_line, P_stall_fire, '--', color='black', linewidth=0.8)

    plt.xlabel('V (m/s)')
    plt.ylabel('P (kW)')
    plt.axis([0, V_end, 0, 1.5*P_a])
    plt.grid(True)
    plt.title('Power vs. Velocity')
    plt.legend(loc= 'upper left')

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
    RC_std = P_dif_std*1000/W_mto
    RC_fire = P_dif_fire*1000/W_mto

    RC_std_max = max(RC_std)
    RC_fire_max = max(RC_fire)

    # Arrays for line plotting
    RC_stall_std = np.linspace(0, 1.5*P_a, 2)
    RC_stall_fire = np.linspace(0, 1.5*P_a, 2)

    # Plotting of rate of climb diagram
    plt.plot(V_std, RC_std, 'orange', label='Rate of Climb, standard atmosphere (15C)')
    plt.plot(V_fire, RC_fire, 'firebrick', label='Rate of Climb, fire atmosphere (200C)')

    plt.plot(V_stall_std_line, RC_stall_std, '--', color='black', linewidth=0.8)
    plt.plot(V_stall_fire_line, RC_stall_fire, '--', color='black', linewidth=0.8)

    plt.xlabel('V (m/s)')
    plt.ylabel('RC (m/s)')
    plt.axis([0, V_end, 0, int(max(RC_std)+1)])
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

