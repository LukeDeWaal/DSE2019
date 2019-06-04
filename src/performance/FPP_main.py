# Imports
from FPP_Flight_Envelope_Defs import *

# Flight Envelope
print_inputs(W_fuel, g, W_mto, S, C_L_max, C_D_0, AR, e, P_a, rho_std, n_max, n_min)
V_stall, V_stall_index, V_A, V_A_index, V_max, V_max_index, V_C, V_C_index = maneuvre_plot(n_min, n_max, 'blue', 'black')
