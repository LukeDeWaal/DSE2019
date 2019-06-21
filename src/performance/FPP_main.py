## Imports ##
from FPP_Flight_Envelope_Defs import flight_envelope
from FPP_Performance_Diagrams_Defs import optimal_altitude, power_diagram_bank, power_diagram_temp, rc_diagram_temp, rc_diagram_bank, drag_polar, power_loading, lift_over_drag, lift_over_drag_alt

## Flight Envelope ##
# V, n, V_stall_index, V_A, V_A_index, V_max, V_max_index, V_C, V_C_index = flight_envelope()

## Performance Diagrams ##
# V_stall_std, fig_power_bank = power_diagram_bank()
# V_stall_fire, fig_power_temp = power_diagram_temp()
# RC_fire_max, fig_rc_temp = rc_diagram_temp()
# RC_std_max, fig_rc_bank = rc_diagram_bank()
# fig_drag = drag_polar()
# fig_powerloading = power_loading()

# L_D, fig_LD = lift_over_drag()
# L_D_alt, fig_LD_alt = lift_over_drag_alt()

optimal_altitude()
