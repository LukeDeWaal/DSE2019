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

#Aerodynamics Parameters
R_cruise_wing=rho_cruise*V_cruise*c/miu_cruise
R_cruise_tail=rho_cruise*V_cruise*horizontal_tail_chord/miu_cruise
R_cruise=rho_cruise*V_cruise*c/miu_cruise
R_cruise_ht=rho_cruise*V_cruise*horizontal_tail_chord/miu_cruise
R_cruise_fus = rho_cruise*V_cruise*fus_l/miu_cruise
R_cruise_eng = rho_cruise*V_cruise*eng_l/miu_cruise

mach = 0.286
beta = np.sqrt(1-mach**2)

Cl_alpha = 6.25
airfoil_efficiency = Cl_alpha/(2*np.pi/beta) 
CL_alpha_w = 2*np.pi*AR/(2 + np.sqrt(4 + (AR*beta/airfoil_efficiency)**2 * (1 + np.tan(sweep)**2)))
CL_alpha_A_h = CL_alpha_w * (S_wing - c*hull_width)/S_wing * 1.07*(1+hull_width/b)**2
CL_alpha_h = 2*np.pi*horizontal_tail_aspect_ratio/(2 + np.sqrt(4 + (horizontal_tail_aspect_ratio*beta/airfoil_efficiency)**2 * (1 + (np.tan(sweep)/beta)**2)))
K_epsilon_delta0 = 0.1124/L_ht**2 + 0.1024/L_ht + 2
K_epsilon_delta = (0.1124 + 0.1265*sweep + 0.1766*sweep**2)/L_ht**2 + 0.1024/L_ht + 2
de_da = K_epsilon_delta/K_epsilon_delta0 * (L_ht/(L_ht**2  + vertical_tail_root_chord**2) * 0.4876/np.sqrt(L_ht**2 + 0.6319 + vertical_tail_height**2) + (1 + (L_ht**2/(L_ht**2 + 0.7915 + 5.0735*vertical_tail_height**2))**0.3113) * (1 - np.sqrt(vertical_tail_height**2/(1 + vertical_tail_height**2)))) * CL_alpha_w/(np.pi*AR)

x_ac_airfoil = 0.265 # x/c
x_ac_wing = wing_position -c/2 + x_ac_airfoil * c # m
x_ac = x_ac_wing - (1.8 * hull_width * hull_height * fus_l)/(CL_alpha_A_h * S_wing * c) + 0.273/(1 + taper_ratio) * (hull_width * S_wing/b * (b - hull_width))/(c**2 * (b + 2.15*hull_width)) * np.tan(sweep) # m