''' Some general definitions for FPP that can be called from other files '''
# Imports
import numpy as np

def V_row(V_start, V_end, step):
    ''' Generate an array for velocity. '''

    V_array = np.arange(V_start,V_end,step)

    return V_array

def load_factor(V, rho, C_L_max, W, S):
    ''' Generates load factors for a velocity array. '''

    n = []

    for i in range(len(V)):
        n.append((0.5*rho*C_L_max*V[i]**2)/(W/S))

    n_array = np.array(n)

    return n_array

def aerodynamic_coefficients(V, W, rho, S, C_D_0, AR, e):
    ''' Generates aerodynamic coefficients in arrays for a velocity array. '''

    C_L_list = []
    C_D_list = []

    for i in range(len(V)):
        C_L_list.append(2*W/(rho*V[i]**2*S))
        C_D_list.append(C_D_0+C_L_list[i]**2/(np.pi*AR*e))

    C_L_array = np.array(C_L_list)
    C_D_array = np.array(C_D_list)

    return C_L_array, C_D_array

def P_r_calc(V, W, rho, S, C_D_0, AR, e):
    ''' Generate the power required for a velocity array. '''

    C_L_array, C_D = aerodynamic_coefficients(V, W, rho, S, C_D_0, AR, e)

    P_r_list = []

    for i in range(len(V)):
        P_r_list.append(C_D[i]*0.5*rho*V[i]**3*S/1000.)

    P_r_array = np.array(P_r_list)

    return P_r_array

def P_dif_calc(V, W, rho, S, C_D_0, AR, e, Pa):
    ''' Generate excess power for a certain velocity array. '''

    P_r_array = P_r_calc(V, W, rho, S, C_D_0, AR, e)
    P_dif_list = []

    for i in range(len(P_r_array)):
        P_dif_list.append(Pa - P_r_array[i])

    P_dif_array = np.array(P_dif_list)

    return P_dif_array

def index_finder(X, x_req):
    ''' Find index in an array (X) for a required x. '''

    x_index = np.where(X > x_req)[0][0]

    return x_index

def V_stall_calc(W, rho, S, C_L_max):
    ''' Find stall speed. '''

    V_stall = np.sqrt((2*W)/(rho*S*C_L_max))

    return V_stall

def V_A_calc(n, n_max, V):
    ''' Find V_A and its index in the velocity array. '''

    V_A_index = np.where(n > n_max)[0][0]
    V_A = V[V_A_index]

    return V_A, V_A_index

def V_max_calc(V_stall_index, V, W, rho, S, C_D_0, AR, e, Pa):
    ''' Find maximum velocity and its index in the velocity array. '''

    P_dif = P_dif_calc(V, W, rho, S, C_D_0, AR, e, Pa)

    V_max_indices = np.where(P_dif < 0)
    V_max_index = V_max_indices[0][np.where(V_max_indices > V_stall_index)[1][0]]
    V_max = V[V_max_index]

    return V_max, V_max_index

def V_cruise_calc(V_max):
    ''' Find cruise velocity. '''

    V_C = 0.9*V_max

    return V_C
