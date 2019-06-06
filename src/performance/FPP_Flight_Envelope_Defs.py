### Imports ###
import numpy as np
import matplotlib.pyplot as plt
from FPP_Parameters import W_fuel, g, W_mto, S, C_L_max, C_L_cruise, C_D_0, AR, e, P_a, rho_std, n_max, n_min, V_end, V_step, rho_fire
from FPP_General_Definitions import V_row, load_factor, index_finder, V_stall_calc, V_A_calc, V_max_calc, V_cruise_calc

def print_inputs(W_fuel, g, W_mto, S, C_L_max, C_D_0, AR, e, P_a, rho_std, n_max, n_min, rho_fire, C_L_cruise):
    ''' Print the input variables '''

    # Should make this a bit nicer with a function.
    print('Input variables:')
    print('W_fuel = ', int(W_fuel/g))
    print('W_mto = ', int(W_mto/g))
    print('P_a = ', P_a)
    print()
    print('C_L_max = ', C_L_max)
    print('C_L_clean = ', C_L_cruise)
    print('C_D_0 = ', C_D_0)
    print('n_max = ', n_max)
    print('n_min = ', n_min)
    print()
    print('S = ', S)
    print('AR = ', AR)
    print('e = ', e)
    print()
    print('rho_std = ', rho_std)
    print('rho_fire = ', rho_fire)


    return

def arrays_maneuvre():
    ''' Generate the arrays required for the maneuvre diagram. '''

    V_array = V_row(0.1, V_end, V_step)
    n_array = load_factor(V_array, rho_std, C_L_max, W_mto, S)
    V_stall = V_stall_calc(W_mto, rho_std, S, C_L_max)
    V_stall_index = index_finder(V_array, V_stall)
    V_A, V_A_index = V_A_calc(n_array, n_max, V_array)
    V_max, V_max_index = V_max_calc(V_stall_index, V_array, W_mto, rho_std, S, C_D_0, AR, e, P_a)
    V_C = V_cruise_calc(V_max)
    V_C_index = index_finder(V_array, V_C)

    return V_array, n_array, V_stall, V_stall_index, V_A, V_A_index, V_max, V_max_index, V_C, V_C_index

def maneuvre_plot(n_min, n_max, color1, color2):
    ''' Generate maneuvre plot, this includes the outerlines and the show of specific velocities. '''

    # Get arrays
    V, n, V_stall, V_stall_index, V_A, V_A_index, V_max, V_max_index, V_C, V_C_index = arrays_maneuvre()

    # Maneuvre lines
    V_0A = V[0:V_A_index]
    n_0A = n[0:V_A_index]

    V_0h = V[0:V_stall_index]
    n_0h = -1*n[0:V_stall_index]

    V_hf = V[V_stall_index:V_C_index]
    n_hf = np.linspace(-1.0,n_min,len(V_hf))

    V_fe = V[V_C_index:V_max_index]
    n_fe = np.linspace(n_min,0,len(V_fe))

    V_de = np.linspace(V_max, V_max, 2)
    n_de = np.linspace(0,n_max,2)

    V_ae = np.linspace(V_A,V_max,2)
    n_ae = np.linspace(n_max,n_max,2)

    # Horizontal and vertical lines
    V_A_line = np.linspace(V_A, V_A, len(n_0A))
    n_stall_line_ver = np.linspace(-1., 1., 10)
    V_stall_line_ver = np.linspace(V_stall, V_stall, 10)
    n_stall_line_hor = np.linspace(1., 1., 10)
    V_stall_line_hor = np.linspace(0, V_max, 10)
    n_cruise_line = np.concatenate((n_0h, n_hf), axis=None)
    V_cruise_line = np.linspace(V_C, V_C, len(n_cruise_line))

    # Actual plotting #
    plt.plot(V_0A,n_0A,color1)
    plt.plot(V_0h,n_0h,color1)
    plt.plot(V_fe,n_fe,color1)
    plt.plot(V_de,n_de,color1)
    plt.plot(V_ae,n_ae,color1)
    plt.plot(V_hf,n_hf,color1)

    plt.plot(V_A_line,n_0A,'--',color=color2, linewidth = 0.8)
    plt.plot(V_stall_line_ver,n_stall_line_ver,'--',color=color2, linewidth = 0.8)
    plt.plot(V_stall_line_hor,n_stall_line_hor,'--',color=color2, linewidth = 0.8)
    plt.plot(V_cruise_line,n_cruise_line,'--',color=color2, linewidth = 0.8)
    plt.axhline(0,0,V_max+15, color = 'black', linewidth = 0.7)

    # Labelling and such #
    plt.rcParams.update({'font.size': 10})
    plt.xlabel('V (m/s)')
    plt.ylabel('n (-)')
    plt.axis([0,V_max+15,n_min-0.2,n_max+0.6])
    plt.grid(True)
    plt.text(V_stall+1,-0.25, 'V_Stall')
    plt.text(V_A-3,-0.25, 'V_A')
    plt.text(V_C-7,0.1, 'V_Cruise')
    plt.text(V_C-7,0.1, 'V_Cruise')
    plt.text(V_max+1,0.1, 'V_Max.')
    plt.title('Flight Envelope')
    plt.show()

    return  V, n, V_stall, int(V_stall_index), V_A, int(V_A_index), V_max, int(V_max_index), V_C, int(V_C_index)

def flight_envelope():
    ''' Generate flight envelope diagram and return special velocities. '''

    # Print inputs
    print_inputs(W_fuel, g, W_mto, S, C_L_max, C_D_0, AR, e, P_a, rho_std, n_max, n_min, rho_fire, C_L_cruise)

    # Plot maneuvre diagram
    V, n, V_stall, V_stall_index, V_A, V_A_index, V_max, V_max_index, V_C, V_C_index = maneuvre_plot(n_min, n_max, 'blue',
                                                                                               'black')
    return V, n, V_stall_index, V_A, V_A_index, V_max, V_max_index, V_C, V_C_index
