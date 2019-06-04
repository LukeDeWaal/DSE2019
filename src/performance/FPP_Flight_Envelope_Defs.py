### Imports ###
import numpy as np
import matplotlib.pyplot as plt
from FPP_Parameters import *
from FPP_General_Definitions import *

def print_inputs(W_fuel, g, W_mto, S, C_L_max, C_D_0, AR, e, P_a, rho_std, n_max, n_min):
    ''' Print the input variables '''

    # Should make this a bit nicer with a function.
    print('Input variables:')
    print('W_fuel = ', int(W_fuel/g))
    print('W_mto = ', int(W_mto/g))
    print('S = ', S)
    print('C_L_max = ', C_L_max)
    print('C_D_0 = ', C_D_0)
    print('AR = ', AR)
    print('e = ', e)
    print('P_a = ', P_a)
    print('rho_std = ', rho_std)
    print('n_max = ', n_max)
    print('n_min = ', n_min)

    return

def arrays_maneuvre():
    ''' Generate the arrays required for the maneuvre diagram. '''

    V_array = np.arange(0.1,125,0.1)        # m/s
    n_array = load_factor(V_array, rho_std, C_L_max, W_mto, S)
    C_L_array, C_D_array = aerodynamic_coefficients(V_array, W_mto, rho_std, S, C_D_0, AR, e)
    P_r_array, P_dif_array = Pa_minus_Pr(C_D_array, rho_std, V_array, S, P_a)
    V_stall, V_stall_index = V_stall_calc(W_mto, rho_std, S, C_L_max, V_array)
    V_A, V_A_index = V_A_calc(n_array, n_max, V_array)
    V_max, V_max_index = V_max_calc(P_dif_array, V_stall_index, V_array)
    V_C, V_C_index = V_cruise_calc(V_max, V_array)

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

    plt.plot(V_A_line,n_0A,'--',color=color2)
    plt.plot(V_stall_line_ver,n_stall_line_ver,'--',color=color2)
    plt.plot(V_stall_line_hor,n_stall_line_hor,'--',color=color2)
    plt.plot(V_cruise_line,n_cruise_line,'--',color=color2)

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
    plt.show()

    return  V_stall, int(V_stall_index), V_A, int(V_A_index), V_max, int(V_max_index), V_C, int(V_C_index)
