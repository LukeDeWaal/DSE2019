import numpy as np

# General parameters
MTOW = 9000 # kg
aircraft_length = 9 # m
cg_position = aircraft_length * 0.4
rho = 1.225 # kg/m^3

# Wing parameters
AR = 7.5
S = 50 # m^2
b = np.sqrt(AR*S) # m
c = S/b # m
V_cruise = 80 # m/s
V_loit = 44 # m/s
Cl_cruise = 0.45046
Cl_loit = 2.1
L_cruise = Cl_cruise * 0.5 * rho * V_cruise**2 * S
wing_position = cg_position * 1.2
wing_moment = L_cruise * (wing_position - cg_position) # Nm

# Horizontal tail parameters
max_tail_span = 4 # m
tail_position = 8.75 # m
tail_force = wing_moment/(tail_position - cg_position) # N
Cl_h = -0.5
#S_h = -tail_force/(Cl_h*0.5*rho*V_cruise**2)
#tail_chord = S_h/max_tail_span
L_ht = tail_position - wing_position
horizontal_tail_volume_coefficient = 0.5
horizontal_tail_area = horizontal_tail_volume_coefficient * (c*S)/L_ht
horizontal_tail_chord = horizontal_tail_area/max_tail_span

# Vertical tail parameters
vertital_tail_volume_coefficient = 0.04



# Hull parameters
hull_width = 1.5 # m