## Imports ##
from FPP_Flight_Envelope_Defs import flight_envelope
from FPP_Performance_Diagrams_Defs import power_diagram, rc_diagram, drag_polar, power_loading

## Flight Envelope ##
V, n, V_stall_index, V_A, V_A_index, V_max, V_max_index, V_C, V_C_index = flight_envelope()

# ## Performance Diagrams ##
# V_stall_std, V_stall_fire = power_diagram()
# RC_std_max, RC_fire_max = rc_diagram()
# drag_polar()
power_loading()
