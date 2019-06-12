from Class_II import kg_to_lbs, S_w, W_fw, A, Lambda, q, lambda_, tc, N_z, W_dg, S_ht, Lambda_ht, lambda_h, Ht_Hv, S_vt, Lambda_vt, lambda_vt, S_f, L_t, L, D, W_press, N_l, W_l, L_m, L_n, W_en, N_en, V_t, V_i, N_t, B_w, N_p, W_uav, M
import numpy as np

# W_fw
W_wing = 0.036*S_w**.758*W_fw**.0035*(A/(np.cos(Lambda)**2))**.6*q**.006*lambda_**.04*(100*tc/np.cos(Lambda))**-.3*(N_z*W_dg)**.49
print('W_wing',W_wing/kg_to_lbs)

W_ht = .016*(N_z*W_dg)**.414*q**.168*S_ht**.896*(100*tc/np.cos(Lambda))**-.12*(A/(np.cos(Lambda_ht)**2))**.043*lambda_h**-.02
print('W_ht', W_ht/kg_to_lbs)

W_vt = .073*(1+.2*Ht_Hv)*(N_z*W_dg)**.376*q**.122*S_vt**.873*(100*tc/np.cos(Lambda_vt))**-.49*(A/(np.cos(Lambda_vt)**2))**.357*lambda_vt**.039
print('W_vt',W_vt/kg_to_lbs)

W_fus = 1.25*.052*S_f**1.086*(N_z*W_dg)**.177*L_t**-.051*(L/D)**-.072*q**.241+W_press
print('W_fus',W_fus/kg_to_lbs)

W_main = .095*(N_l*W_l)**.768*(L_m/12.)**.409
print('W_main',W_main/kg_to_lbs)

W_nose = .125*(N_l*W_l)**.566*(L_n/12.)**.845
print('W_nose',W_nose/kg_to_lbs)

W_engine = 2.575*W_en**.922*N_en
print('W_eng', W_engine/kg_to_lbs)

W_fuel_sys = 2.49*V_t**.726*(1/(1+V_i/V_t))**.363*N_t**.242*N_en**.157
print('W_fuel_system', W_fuel_sys/kg_to_lbs)

W_flight_controls = .053*L**1.536*B_w**.371*(N_z*W_dg*10**-4)**.8
print('W_flight_controls', W_flight_controls/kg_to_lbs)

W_hydraulics = .001*W_dg
print('W_hydraulics', W_hydraulics/kg_to_lbs)

W_avionics = 2.117*W_uav**.933
print('W_avionics', W_avionics/kg_to_lbs)

W_electrical = 12.57*(W_fuel_sys+W_avionics)**.51
print('W_electrical', W_electrical/kg_to_lbs)

W_ac_ice = .265*W_dg**.52*N_p**.68*W_avionics**.17*M**.08
print('W_ac_ice', W_ac_ice/kg_to_lbs)

W_OEW = W_wing+W_ht+W_vt+W_fus+W_main+W_nose+W_engine+W_fuel_sys+W_flight_controls+W_hydraulics+W_avionics+W_electrical+W_ac_ice
print('W_OEW', W_OEW/kg_to_lbs)