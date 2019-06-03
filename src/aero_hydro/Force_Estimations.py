# -*- coding: utf-8 -*-
"""
Created on Mon Jun  3 09:43:00 2019

@author: patri
"""

import matplotlib.pyplot as plt
import numpy as np

from wing_surface_locations import *
from parameters import *

k_paint=0.634*10**-5 #m This is a smoothness parameter depending on the surface finish
k_comp = 0.052*10**-5


######PARASITE DRAG#####
def skinfriction_drag(S_ref,R,M, lt_ratio,t_c,x_c_max,sweep_angle_max,k,l,component):
    
    ###Inputs###
        #R: Cruise Reynolds
        #M: Cruise Mach
        #lt_ratio: Point of turbulent transition
        #t/c: Thickness to chord ratio of the airfoil
        #x_c_max: Chordwise location of airfoil maximum thickness point
        #sweep_angle_max: Sweep of maximum thickness line (rad)
        #l: length or chord length
        #For the component type in the string for which you want the skin friciton drag
        
    
    #Wetted areas
    if component == 'wing':
        S_wet = 2*1.07*S_wing
    elif component == 'horizontal tail':
        S_wet= 2*1.05*horizontal_tail_area
    elif component == 'vertical tail':
        S_wet = 2*1.05*vertical_tail_area
    elif component == 'fuselage':
        S_wet = (np.pi*(fus_B*2)/4)*(1/(3*fus_len_1**2)*((4*fus_len_1**2+(fus_B*2)**2/4)**1.5-(fus_B*2)**3/8)-(fus_B*2)+4*fus_len_2+2*np.sqrt(fus_len_3**2+(fus_B*2)**2/4))
    elif component == 'nacelle':
        S_wet = (np.pi*(cowling_diameter**2)/4)*engine_length
        
    
    #The next parameter is dependent on the type of material used in the design
    R_cutoff = 38.21*((l/k)**1.053)

    
    #The lower of either the actual Reynolds or cutoff must be chosen, the cutoff gives an idea of where
    #transition occurs
    R_final = 0 
    
    if R<R_cutoff:
        R_final = R
    else:
        R_final = R_cutoff
    
    #Flat plate Skin Friction Coefficient
    #Laminar case:
    Cf_laminar = 1.328/np.sqrt(R)
    
    #Turbulence case
    Cf_turbulent = 0.455/((np.log10(R_final)**2.58)*(1+0.144*M**2)**0.65)
    
    #Based on the estimation of wing postion subjected to laminar (x_c_max)
    Cf_final = Cf_laminar*lt_ratio + Cf_turbulent*(1-lt_ratio)
        
    FF=(1+(0.6/x_c_max)*(t_c)+100*(t_c)**4)*(1.34*M**0.18*np.cos(sweep_angle_max)**0.28)
    
    #Correction for Fuselage Skin Friction
    if component == 'fuselage':
        
        f=l/(np.sqrt((4/np.pi)*fus_front_area))
        
        FF=1+(60/f**3)+f/400
        
        #Scaling due to flying boat hull
        FF=FF*1.5
    
        S_wet = 114
    if component == 'nacelle':
        f = l/(np.sqrt((4/np.pi)*(np.pi*(cowling_diameter**2)/4)))
        
        FF= 1 + (0.35/f)
        
        
        
    Cd0_sf = FF*S_wet*Cf_final/S_ref
        
    return Cd0_sf

def miscellaneous_drag():
    ###This function outputs other parasitic drag sources
    
    #fuselage upsweep:
    D_q=3.83*fus_upsweep*np.pi/180**2.5*fus_front_area
    
    S_ref=S_wing
    
    Cd0_fus_upsweep = D_q/S_ref
    
    
    #Landing Gear:
    #For the moment for landing gear statistical data is used as it hasn't yet been sized
    
    Cd0_land=(2*0.25/S_ref)*1.2
    
    Cd0_misc_tot=Cd0_land+Cd0_fus_upsweep
    
    return Cd0_misc_tot



####MAIN####
    
Sf_wing = (skinfriction_drag(S_wing, R_cruise_wing,M_cruise,0.2,0.15,0.5,0,k_comp,c,'wing'))

Sf_ht = (skinfriction_drag(S_wing, R_cruise_ht, M_cruise,0.2,0.12,0.3,0,k_comp,horizontal_tail_chord,'horizontal tail'))*1.05

Sf_vt = (skinfriction_drag(S_wing,R_cruise_ht,M_cruise,0.2,0.15,0.4,0,k_comp,horizontal_tail_chord,'vertical tail'))*1.05

Sf_fus = (skinfriction_drag(S_wing,R_cruise_fus,M_cruise,0.25,0.7,0.2,0,k_comp,fus_l,'fuselage'))

Sf_nacelle = (skinfriction_drag(S_wing,R_cruise_eng,M_cruise,0.2,0.7,0.2,0,k_comp,engine_length,'nacelle'))*1.5

Sf_total = Sf_wing +Sf_ht + Sf_vt+ Sf_fus + Sf_nacelle

Total_Parasitic = Sf_total+miscellaneous_drag()

print("The Total Skin Friction Drag is", Sf_total)

print ("The Total Parasitic Drag is", Total_Parasitic)






    
    




