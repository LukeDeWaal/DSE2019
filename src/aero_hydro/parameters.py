import numpy as np

# General parameters
MTOW = 9000 # kg
aircraft_length = 9 # m
cg_position = aircraft_length * 0.3
rho_SL = 1.225 # kg/m^3
rho_cruise=0.85 # kg/m^3
miu_cruise=1.650*10**-5 #Ns/m^2
miu_SL = 1.789*10**-5 #Ns/m^2

# Wing parameters
AR = 7.5
S_wing = 50 # m^2
b = np.sqrt(AR*S_wing) # m
c = S_wing/b # m
V_cruise = 80 # m/s
V_loit = 44 # m/s
Cl_cruise = 0.45046
Cl_loit = 2.1
L_cruise = Cl_cruise * 0.5 * rho_cruise * V_cruise**2 * S_wing
wing_position = cg_position * 1.2
wing_moment = L_cruise * (wing_position - cg_position) # Nm
sweep = 0 # deg

# Horizontal tail parameters
max_tail_span = 4 # m
tail_position = 8.75 # m
tail_force = wing_moment/(tail_position - cg_position) # N
Cl_h = -0.5
L_ht = tail_position - wing_position
horizontal_tail_volume_coefficient = 0.5
horizontal_tail_area = horizontal_tail_volume_coefficient * (c*S_wing)/L_ht
horizontal_tail_chord = horizontal_tail_area/max_tail_span * 0.9

# Vertical tail parameters
vertital_tail_volume_coefficient = 0.05
vertical_tail_area = vertital_tail_volume_coefficient*b*S_wing/L_ht * 0.9

# Control surface parameters
aileron_length = 0.4 * b / 2
aileron_chord = 0.2 * c
elevon_length = 0.8 * max_tail_span
elevon_chord = 0.375 * horizontal_tail_chord

# Hull parameters
hull_width = 1.5 # m

#Aerodynamics Parameters
R_cruise=rho_cruise*V_cruise*c/miu_cruise
mach = 0.286
beta = np.sqrt(1-mach**2)
Cl_alpha = 6.25
airfoil_efficiency = Cl_alpha/(2*np.pi/beta) 
CL_alpha = 2*np.pi*AR/(2 + np.sqrt(4 + (AR*beta/airfoil_efficiency)**2 * (1 + np.tan(sweep)**2))) * (S_wing - c*hull_width)/S_wing * 1.07*(1+hull_width/b)**2
