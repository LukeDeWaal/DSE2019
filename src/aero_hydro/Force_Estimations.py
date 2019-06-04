# -*- coding: utf-8 -*-
"""
Created on Mon Jun  3 09:43:00 2019

@author: patri
"""

import matplotlib.pyplot as plt
import numpy as np

from wing_surface_locations import *
from parameters import *
#from Code_Verification_Parameters import *

k_paint=0.634*10**-5 #m This is a smoothness parameter depending on the surface finish
k_comp = 0.052*10**-5


######PARASITE DRAG#####
def skinfriction_drag(S_ref,S_component,R,M, lt_ratio,t_c,x_c_max,sweep_angle_max,k,l,component):
    
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
        S_wet = 2*1.07*S_component
    elif component == 'horizontal tail':
        S_wet= 2*1.05*S_component
    elif component == 'vertical tail':
        S_wet = 2*1.05*S_component
    elif component == 'fuselage':
        S_wet = (np.pi*(fus_B*2)/4)*(1/(3*fus_len_1**2)*((4*fus_len_1**2+(fus_B*2)**2/4)**1.5-(fus_B*2)**3/8)-(fus_B*2)+4*fus_len_2+2*np.sqrt(fus_len_3**2+(fus_B*2)**2/4))
    elif component == 'nacelle':
        S_wet = (np.pi*(eng_cowling**2)/4)*eng_l
        
    
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
    
    if component == 'nacelle':
        f = l/(np.sqrt((4/np.pi)*(np.pi*(eng_cowling**2)/4)))
        
        FF= 1 + (0.35/f)
        
    
    Cd0_sf = FF*S_wet*Cf_final/S_ref
        
    return Cd0_sf #, R_cutoff, R_final, FF, Cf_final, S_ref,S_wet

def miscellaneous_drag(FA_tire_1,FA_tire_2, SA_strut, n_tires_1, n_tires_2, n_struts):
    ###This function outputs other parasitic drag sources
    
    ###Inputs###
        #d_tire: Diameter of tires
        #width_tire: Width of the tires
        #SA_strut: Surface area of the strut
    
    
    #fuselage upsweep:
    D_q_upsweep=3.83*fus_upsweep*np.pi/180**2.5*fus_front_area
    
    S_ref=S_wing
    
    Cd0_fus_upsweep = D_q_upsweep/S_ref
    
    
    #Landing Gear:
    #For the moment for landing gear statistical data is used as it hasn't yet been sized
    D_q_gear1 = FA_tire_1*0.25*n_tires_1
    D_q_gear2 = FA_tire_2*0.25*n_tires_2
    D_q_strut = SA_strut*0.05*n_struts
    
    Cd0_gear = ((D_q_gear1+D_q_gear2+D_q_strut)/S_ref)*1.2
    
    #Floats
    
    Cd0_misc_tot = Cd0_gear + Cd0_fus_upsweep
    
    return Cd0_misc_tot


def parasite_addition_flaps(flap_deflection):
    #This function calculates the additonal Cd0 due to the flaps
    
    ###INPUTS###
        #Flap deflection angle as integer in degrees
 
        
    delta_Cd0_slotted = 0.0074*0.35*(flap_deflection-10)*1.2
        
    delta_Cd0_plain = 0.0144*0.25*(flap_deflection-10)
        
    return delta_Cd0_slotted, delta_Cd0_plain
        
    


####MAIN####
    
Sf_wing = (skinfriction_drag(S_wing, S_wing, R_cruise_wing,M_cruise,0.2,0.15,0.5,0,k_paint,c,'wing'))

Sf_ht = (skinfriction_drag(S_wing, horizontal_tail_area, R_cruise_ht, M_cruise,0.2,0.12,0.3,0,k_paint,horizontal_tail_chord,'horizontal tail'))*1.05

Sf_vt = (skinfriction_drag(S_wing,vertical_tail_area, R_cruise_ht,M_cruise,0.2,0.12,0.3,0,k_paint,vertical_tail_chord,'vertical tail'))*1.05

Sf_fus = (skinfriction_drag(S_wing,0,R_cruise_fus,M_cruise,0.25,0.7,0.2,0,k_paint,fus_l,'fuselage'))

Sf_nacelle = (skinfriction_drag(S_wing,0,R_cruise_eng,M_cruise,0.2,0.7,0.2,0,k_paint,eng_l,'nacelle'))*1.5

Sf_total = Sf_wing +Sf_ht + Sf_vt+ Sf_fus + Sf_nacelle

misc_total=miscellaneous_drag(0.09, 0.09, 0.05,2,1,2)

flap_total = parasite_addition_flaps(30)

total_parasitic_noflaps = Sf_total+misc_total

total_parasitic_slotted = Sf_total+misc_total+flap_total[0]

total_parasitic_simple = Sf_total+misc_total+flap_total[1]

#print("The Total Skin Friction Drag is", Sf_total)

print(("The Total Parasitic Drag with no flaps is", total_parasitic_noflaps*1.1))

print ("The Total Parasitic Drag with simple flaps is", total_parasitic_simple*1.1)

print ("The Total Parasitic Drag with slotted flaps is", total_parasitic_slotted*1.1)

print(Sf_nacelle)









###CODE VERIFICATION USING TEST PARAMETERS FROM RAYMER###

#Sf_wing = (skinfriction_drag(S_ref_ray, S_ref_ray, Reynolds_wing,Mcruise,0,0.135,0.35,0,k_paint,c_wing,'wing'))
#
#Sf_horiz = (skinfriction_drag(S_ref_ray, area_horizontal, Reynolds_tail,Mcruise,0,0.12,0.4,0,k_paint,1.54,'horizontal tail'))
#
#Sf_vertical=(skinfriction_drag(S_ref_ray, area_vertical, Reynolds_tail ,Mcruise,0,0.12,0.4,0,k_paint,0.625,'vertical tail'))

#Sf_fus = (skinfriction_drag(S_ref_ray, area_horizontal, Reynolds_fus,Mcruise,0,0.12,0.4,0,k_paint,fus_length,'fuselage'))

#print ("The Total skin friction of tails is",(Sf_vertical[0]+Sf_horiz[0])*1.1)

#print ("The Total skin friction of wing is",(Sf_wing[0]))

#print (Sf_fus)



    
    




