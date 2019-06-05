import numpy as np

# General parameters
MTOW = 9000 # kg
aircraft_length = 9 # m
cg_position = aircraft_length * 0.3
rho_SL = 1.225 # kg/m^3
rho_cruise=1.225 # kg/m^3
miu_cruise=1.650*10**-5 #Ns/m^2
miu_SL = 1.789*10**-5 #Ns/m^2

# Wing parameters
AR = 7.5
S_wing = 42 # m^2
b = np.sqrt(AR*S_wing) # m
c = S_wing/b # m
V_cruise = 103 # m/s
V_loit = 44 # m/s
M_cruise=V_cruise/np.sqrt(1.4*287*273)
Cl_cruise = 0.45046
Cl_loit = 2.1
L_cruise = Cl_cruise * 0.5 * rho_cruise * V_cruise**2 * S_wing
wing_position = cg_position + 1.5
wing_moment = L_cruise * (wing_position - cg_position) # Nm
sweep = 0 # deg
taper_ratio = 1
e=0.7
V_stall=32
M_stall=V_stall/np.sqrt(1.4*287*273)

# Horizontal tail parameters
max_tail_span = 4 # m
tail_position = 8.75 # m
tail_force = wing_moment/(tail_position - cg_position) # N
Cl_h = -0.5
L_ht = tail_position - wing_position # m
horizontal_tail_volume_coefficient = 0.5
horizontal_tail_area = horizontal_tail_volume_coefficient * (c*S_wing)/L_ht # m^2
horizontal_tail_chord = horizontal_tail_area/max_tail_span * 0.9 # m
horizontal_tail_aspect_ratio = max_tail_span/horizontal_tail_chord

# Vertical tail parameters
vertital_tail_volume_coefficient = 0.05
vertical_tail_aspect_ratio = 1
vertical_tail_taper_ratio = 0.6

vertical_tail_area = vertital_tail_volume_coefficient*b*S_wing/L_ht * 0.9 # m^2
vertical_tail_height = np.sqrt(vertical_tail_area*vertical_tail_aspect_ratio)
vertical_tail_root_chord = 2/(1+vertical_tail_taper_ratio) * vertical_tail_area/vertical_tail_height
vertical_tail_tip_chord = vertical_tail_root_chord * vertical_tail_taper_ratio
vertical_tail_average_chord=(vertical_tail_tip_chord+vertical_tail_root_chord)/2

#Fuselage parameters
fus_l=9.0 #m
fus_front_area=0.75*1.25*np.pi
fus_A=0.75
fus_B=1.25
fus_front_area=fus_A*fus_B*np.pi
fus_len_1=2.25
fus_len_2=1.53
fus_len_3=5.22
hull_width = 1.5 #m
hull_height = 2.5 #m
fus_upsweep = 10 #deg

# Control surface parameters
aileron_length = 0.4 * b / 2 # m
aileron_chord = 0.2 * c # m
elevon_length = 0.8 * max_tail_span # m
elevon_chord = 0.375 * horizontal_tail_chord # m

#Engine parameters
eng_l = 6.0
eng_width = 0.6
eng_cowling = 0.6*1.2

#Reynolds numbers
R_cruise_wing=rho_cruise*V_cruise*c/miu_cruise
R_cruise_tail=rho_cruise*V_cruise*horizontal_tail_chord/miu_cruise
R_cruise=rho_cruise*V_cruise*c/miu_cruise
R_cruise_ht=rho_cruise*V_cruise*horizontal_tail_chord/miu_cruise
R_cruise_fus = rho_cruise*V_cruise*fus_l/miu_cruise
R_cruise_eng = rho_cruise*V_cruise*eng_l/miu_cruise

#Aerodynamics Parameters
R_stall_wing=rho_SL*V_stall*c/miu_SL

Cl_alpha = 6.25
