### Imports ###
import os
import sys
import numpy as np

sys.path.insert(0, '/'.join(os.getcwd().split('/')[:-1]) + '/tools')
from GoogleSheetsImportMac import GoogleSheetsDataImport, SHEET_NAMES, SPREADSHEET_ID
data = GoogleSheetsDataImport(SPREADSHEET_ID, *SHEET_NAMES).get_data()

### Conversions ###
kg_to_lb = 2.205
ms_to_mph = 2.237
km_to_sm = .6214
g = 9.80665
ms_to_kts = 1.944
m_to_ft = 3.281
W_to_hp = 1.341

### Initial values ###
# Weights
W_pl = 3000 * kg_to_lb  # lb
W_pl_mto_ratio = .33333
W_to_initial = W_pl / W_pl_mto_ratio  # lb
W_F_res_used_ratio = 0.05
W_E_ratio_initial = 6751. / 16000.  # AT 802

### Class I ###
## Input Parameters ##
# Altitudes
h_cr = 3000  # m
h_refill = 250  # m, assumed altitude to travel

# Performance parameters
rc = 10  # m/s
V_cl = data['FPP']['V_climb [m/s]'] * ms_to_mph  # mph
# V_cl_empty = 45 * ms_to_mph  # mph (for MTOW = 6000 in Kars Excel)
V_cr = 0.9 * data['FPP']['V_max [m/s]']  # m/s
V_loiter = data['FPP']['V_loit [m/s]']  # m/s
eta_p = data['FPP']['eta_p [-]']  # propeller efficiency
c_p = 0.45  # specific fuel consumption
L_D_cl = 10.2  # lift over drag for climb
L_D_cr = 8.0  # lift over drag for cruise at 113 m/s
L_D_9_8 = 7.9  # lift over drag at 44 m/s (assumed dropping speed/loiter)
# L_D_9_8_empty = 10.2  # at 44 m/s (for MTOW = 6000 in Kars Excel)
x = 23  # 23  # number of refills 16

# Distances
d_fire_loiter = 1.0  # km
d_fire_source = 10  # km, distance fire to water
d_airport_fire = 50  # km


## Definitions ##
def range_endurance_time_values():
    """ Find the endurance and range values for differen performance and mission parameters, also finds the time estimate for different phases of the flight. """

    # Brequet Equations for range and endurance of several phases of flight (Roskam)
    E_cl = h_cr / rc / 3600  # fraction of an hour
    R_cr = (d_airport_fire - V_cl / ms_to_mph / 1000 * E_cl * 3600) \
           * km_to_sm  # sm, distance airport to fire, assume horizontal speed is indicated speed
    print('R_cr', R_cr/km_to_sm)
    R_9_8 = d_fire_loiter * km_to_sm  # sm, distance covered to get away from dropping location before climbing
    E_10_9 = h_refill / rc / 3600  # fraction of an hour
    R_refill = (d_fire_source - V_cl / ms_to_mph / 1000 * E_10_9 *
                3600) * km_to_sm  # distance cruise between fire and water
    print('R_refill', R_refill/km_to_sm)

    # Time estimations for different phases of flight
    t_initial_attack = 60 + 60 + 30 + E_cl * 3600 + R_cr / km_to_sm * 1000 / V_cr + 60 + 30 + R_9_8 / km_to_sm * 1000 / V_loiter  # 60 for 1, 2, 6 and 8, 30 for 3 and 8, calculated for 4, 5 and 9
    t_one_refill = E_10_9 * 3600 + R_refill / km_to_sm * 1000 / V_cr + 25 + 30 + E_10_9 * 3600 + R_refill / km_to_sm * 1000 / V_cr + 25 + 30 + R_9_8 / km_to_sm * 1000 / V_loiter  # 25 for 12 and 16, 30 for 13 and 18, calculated for 10, 11, 14, 15 and 19
    t_back_to_base = E_cl * 3600 + R_cr / km_to_sm * 1000 / V_cr + 60 + 60  # 60 for 22 and 23, calculated for 20 and 21

    # Total mission time
    t_total = t_initial_attack + t_one_refill * x + t_back_to_base

    return E_cl, R_cr, R_9_8, E_10_9, R_refill, t_initial_attack, t_one_refill, t_back_to_base, t_total


def print_class_I_values(t_initial_attack, t_one_refill, t_back_to_base, t_total, W_fuel_after_first_drop,
                         W_fuel_refill, W_fuel_back_to_base, W_to, W_fuel, W_E_tent):
    """ Prints the values for an overview of the values found for the Class I Weight Estimation (Roskam). """

    # Print title
    print('Class I weight estimation:')
    print()

    # Print time estimates
    print('Times:')
    print('initial attack =', int(t_initial_attack / 60), 'min (includes engine start, warm up and take-off)')
    print('one refill =', (t_one_refill / 60),
          'min (includes climb/cruise from fire, scooping and climb/cruise to fire)')
    print('back to base =', int(t_back_to_base / 60), 'min (includes cruise from fire to base and landing and taxiing)')
    print('total =', int(t_total / 60), f'min (includes {x + 1} drops)')
    print(f'{int((x + 1) * W_pl / kg_to_lb)}L of water dropped in {int(t_total / 60)} min, this leads to {int((x + 1) * W_pl / kg_to_lb / t_total * 3600)}L/hr')
    print()

    # Print fuel weights
    print('Fuel weights of different phases:')
    print('after first drop =', W_fuel_after_first_drop / kg_to_lb * (1 + W_F_res_used_ratio), 'kg')
    print('one refill =', W_fuel_refill / kg_to_lb * (1 + W_F_res_used_ratio), 'kg (average)')
    print('back to base =', W_fuel_back_to_base / kg_to_lb * (1 + W_F_res_used_ratio), 'kg')
    print()

    # Print final values Class I
    print('Iterated weights (in kg)')
    print('TO  ', 'Fuel', 'Empty')  # , 'Exp.')
    print(int(W_to / kg_to_lb), int(W_fuel / kg_to_lb), int(W_E_tent / kg_to_lb))  # , int(W_E_allowed / kg_to_lb))

    return


def get_ff(W_to, x, E_cl, R_cr, R_9_8, E_10_9, R_refill):
    """ Generate (weight drop/gain corrected) fuel fractions, find final fuel fraction, intermediate fuel usages and produces a list with the fuel fractions. """

    # List for fuel fractions
    fuel_fractions = [
        ['1: Engine start and warm-up', '2: Taxi', '3: Take-off', '4: Climb to cruise alt. from ground',
         '5: Cruise-out',
         '6: Descent to drop alt. from cruise alt.', '7: Flight to drop location', '8: Drop',
         '9: Flight to climb location', '10: Climb to refill alt. from drop alt.', '11: Cruise to source',
         '12: Descent to source', '13: Scoop up water', '14: Climb to refill alt. from ground', '15: Cruise to fire',
         '16: Descent to drop alt. from refill alt.', '17: Flight to drop location', '18: Drop',
         '19: Flight to climb location', '20: Climb to cruise alt. from drop alt.', '21: Cruise-in',
         '22: Descent from cruise alt. to ground', '23: Landing, taxi and shut down'], 23 * [0]]

    # Fuel fractions: take-off to 8
    ff_1_to = .996  # table 2.1: 4
    ff_2_1 = .995  # table 2.1: 4
    ff_3_2 = .996  # table 2.1: 4
    ff_4_3 = 1 / (np.e ** (E_cl / 375 * V_cl / eta_p * c_p / L_D_cl))  # eq. 2.7
    ff_5_4 = 1 / (np.e ** (R_cr / 375 / eta_p * c_p / L_D_cr))  # eq. 2.9
    ff_6_5 = .999  # table 2.1: 4
    ff_7_6 = 1.0  # neglected, assumed that will immediately descent to drop location
    ff_8_7 = 1.0

    # Total fuel fraction: take-off to 8
    M_ff_1_8 = ff_1_to * ff_2_1 * ff_3_2 * ff_4_3 * ff_5_4 * ff_6_5 * ff_7_6 * ff_8_7

    # Weights after phase 8 (uncorrected and corrected)
    W_now_uncorrected = W_to * M_ff_1_8
    W_now = W_now_uncorrected - W_pl  # drop water

    # Fuel fractions: 8 to 9 (corrected for weight loss)
    ff_9_8_uncorrected = 1 / (np.e ** (R_9_8 / 375 / eta_p * c_p / L_D_9_8))  # eq. 2.9
    ff_9_8 = (1 - (1 - ff_9_8_uncorrected) * W_now / W_now_uncorrected)

    # Weight after phase 9
    W_now = W_now * ff_9_8

    # (Fuel) Weight calculation for intermediate fuel weights
    W_8_b = W_to * M_ff_1_8
    W_8_a = W_8_b - W_pl
    W_9 = (W_8_b - (1 - ff_9_8_uncorrected) * W_8_a)
    W_fuel_after_first_drop = W_to - W_9

    # For loop for the number of refills (x)
    W_fuel_refill_total = 0
    for i in range(x):
        # Fuel fractions: 9 to 13
        ff_10_9 = 1 / (np.e ** (E_10_9 / 375 * V_cl / eta_p * c_p / L_D_cl))  # eq. 2.7
        ff_11_10 = 1 / (np.e ** (R_refill / 375 / eta_p * c_p / L_D_cr))  # eq. 2.9
        ff_12_11 = .999  # table 2.1: 4
        ff_13_12 = .998 * .996  # table 2.1: 4 (landing and take-off)

        # Total fuel fraction: 9 to 13
        M_ff_10_13 = ff_10_9 * ff_11_10 * ff_12_11 * ff_13_12

        # Weights after phase 13 (uncorrected and corrected)
        W_now_uncorrected = W_now * M_ff_10_13  # weight after scooping (payload not added)
        W_now = W_now_uncorrected + W_pl  # scoop up water

        # Fuel fractions: 13 to 14 (corrected for weight gain)
        ff_14_13_uncorrected = ff_10_9  # same because difference of dropping altitude and ground altitude for climb is neglected
        ff_14_13 = (1 - (1 - ff_14_13_uncorrected) * W_now / W_now_uncorrected)  # corrected weight fraction

        # (Fuel) Weight calculation for intermediate fuel weights
        W_13_b = W_9 * M_ff_10_13
        W_13_a = W_13_b + W_pl
        W_14 = (W_13_b - (1 - ff_14_13_uncorrected) * W_13_a)

        # Fuel fractions: 14 to 18
        ff_15_14 = ff_11_10  # same because same distance to be travelled (but now water to fire)
        ff_16_15 = ff_12_11  # same because descending similarly
        ff_17_16 = ff_7_6  # same because same phase
        ff_18_17 = ff_8_7  # same because same phase

        # Total fuel fraction: 13 to 18
        M_ff_14_18 = ff_14_13 * ff_15_14 * ff_16_15 * ff_17_16 * ff_18_17

        # Weights after phase 18 (uncorrected and corrected)
        W_now_uncorrected = W_now * M_ff_14_18
        W_now = W_now_uncorrected - W_pl  # drop water

        # Fuel fractions: 18 to 19 (corrected for weight loss)
        ff_19_18_uncorrected = 1 / (np.e ** (R_9_8 / 375 / eta_p * c_p / L_D_9_8))  # eq. 2.9
        ff_19_18 = (1 - (1 - ff_19_18_uncorrected) * W_now / W_now_uncorrected)

        # Weight after phase 19
        W_now = W_now * ff_19_18

        # (Fuel) Weight calculation for intermediate fuel weights
        W_18_b = W_14 * M_ff_14_18
        W_18_a = W_18_b - W_pl
        W_19 = (W_18_b - (1 - ff_19_18_uncorrected) * W_18_a)

        W_fuel_after_refill = W_to - W_19 - W_fuel_after_first_drop - W_fuel_refill_total
        W_fuel_refill_total = W_fuel_refill_total + W_fuel_after_refill

        # Redefine W_9 for the loop
        W_9 = W_19

    # Fuel fractions: 19 to 23
    ff_20_19 = ff_4_3  # same climb
    ff_21_20 = ff_5_4  # same cruise
    ff_22_21 = .999  # table 2.1: 4
    ff_23_22 = .998  # table 2.1: 4

    # Total fuel fraction: 19 to 23
    M_ff_20_23 = ff_20_19 * ff_21_20 * ff_22_21 * ff_23_22

    # Total fuel fraction: take-off to 23 (to the power of x for the number of refills)
    M_ff_final1 = M_ff_20_23 * (ff_19_18 * M_ff_14_18 * M_ff_10_13) ** x * ff_9_8 * M_ff_1_8

    # (Fuel) Weight calculation for intermediate fuel weights
    W_23 = W_19 * M_ff_20_23

    W_fuel_back_to_base = W_to - W_23 - W_fuel_refill_total - W_fuel_after_first_drop
    W_fuel_refill = W_fuel_refill_total / x

    # Fill the fuel fraction list
    for i in range(len(fuel_fractions[0])):
        if i == 0:
            fuel_fractions[1][i] = ff_1_to
        else:
            fuel_fractions[1][i] = eval(f"ff_{i + 1}_{i}")

    return fuel_fractions, M_ff_final1, W_fuel_refill, W_fuel_after_first_drop, W_fuel_back_to_base


def class_I(W_to, W_E_to_ratio):
    """ Perform Class I Weight Estimation with initial take-off weight and ratio from reference aircraft. """

    # Get endurance, range and time values
    E_cl, R_cr, R_9_8, E_10_9, R_refill, t_initial_attack, t_one_refill, t_back_to_base, t_total = range_endurance_time_values()

    # Get (total) fuel fractions and intermediate fuel weights
    fuel_fractions, M_ff_final, W_fuel_refill, W_fuel_after_first_drop, W_fuel_back_to_base = get_ff(
        W_to, x, E_cl, R_cr, R_9_8, E_10_9, R_refill)

    # Calculate fuel used (with 5% reserved fuel for emergencies), tentative empty weight and allowed empty weight
    W_fuel = ((1 - M_ff_final) * W_to) / (1 - W_F_res_used_ratio)
    W_E_tent = W_to - W_fuel - W_pl
    W_E_allowed = W_E_to_ratio * W_to

    # Iterate until tentative and allowed empty weights are within one percent of each other
    while abs((W_E_allowed - W_E_tent) / W_E_allowed) > 0.01:

        # print('W E allowed', W_E_allowed / kg_to_lb)
        # Add take-off weight to initial take-off weight, if too small
        if W_E_allowed > W_E_tent:
            W_to = W_to + 10

        # Subtract take-off weight to initial take-off weight, if too big
        if W_E_allowed < W_E_tent:
            W_to = W_to - 10

        # Get new (total) fuel fractions and intermediate fuel weights
        fuel_fractions, M_ff_final, W_fuel_refill, W_fuel_after_first_drop, W_fuel_back_to_base = get_ff(
            W_to, x, E_cl, R_cr, R_9_8, E_10_9, R_refill)

        # Calculate new fuel used (with 5% reserved fuel for emergencies), tentative empty weight and allowed empty weight
        W_fuel = ((1 - M_ff_final) * W_to) / (1 - W_F_res_used_ratio)
        W_E_tent = W_to - W_fuel - W_pl
        W_E_allowed = W_E_to_ratio * W_to

    # Print final values
    # print_class_I_values(t_initial_attack, t_one_refill, t_back_to_base, t_total, W_fuel_after_first_drop,
    #                      W_fuel_refill, W_fuel_back_to_base, W_to, W_fuel, W_E_tent, W_E_allowed)

    return W_fuel, W_to, W_E_tent, t_initial_attack, t_one_refill, t_back_to_base, t_total, W_fuel_after_first_drop, W_fuel_refill, W_fuel_back_to_base


def W_structure(W_to):
    # Struc parameters
    n_ult = 1.5 * data['FPP']['n_ult [-]']  # x1.5? 6.8 from FPP
    A = data['Aero']['AR [-]']  # Aero
    Lambda = 0  # Aero
    S = m_to_ft ** 2 * data['FPP']['S [m^2]']  # FPP
    lambda_ = 1.0  # Aero
    t_c_m = .15  # Aero
    V_H = data['FPP']['V_max [m/s]'] * ms_to_kts  # V_max from FPP_main

    S_h = m_to_ft ** 2 * data['C&S']['Sh']  # CS
    l_h = (data['C&S']['H Wing'][0] - (
                0.25 * data['Aero']['Wing chord'] + data['C&S']['Wing'][0])) * m_to_ft  # CS 2.33 is wing chord
    print('l h', l_h/m_to_ft)
    b_h = data['Aero']['horizontail_tail_span [m]'] * m_to_ft  # Aero
    t_r_h = 0.12 * data['Aero']['horizontal_tail_chord [m]'] * m_to_ft  # Aero

    S_v = data['C&S']['Sv_t'] * m_to_ft ** 2  # Aero
    b_v = data['Aero']['vertical_tail_height [m]'] * m_to_ft  # Aero
    t_r_v = 0.12 * data['Aero']['vertical_tail_root [m]'] * m_to_ft  # Aero
    # S_v_m = data['C&S']['Sv_m'] * m_to_ft ** 2  # Aero
    # b_v_m = 1249 / 1000 * m_to_ft  # Aero
    # t_r_v_m = 0.12 * 1478 / 1000 * m_to_ft  # Aero

    l_f = m_to_ft * data['Structures']['Max_fuselage_length']  # Struc
    w_f = data['Structures']['Max_fuselage_width'] * m_to_ft  # Struc
    h_f = data['Structures']['Max_fuselage_height'] * m_to_ft  # Struc
    V_C = 0.9 * data['FPP']['V_max [m/s]'] * np.sqrt(
        0.9 / 1.225) * ms_to_kts  # KEAS (equivalent air speed (3km altitude))

    l_s_m = 2.5 * m_to_ft  # Ask Geert
    W_L = W_to - W_pl  # same assumption as in wing loading diagram (get rid of water before landing)
    n_ult_l = 5.7  # Roskam p81

    # W_struc
    W_w = 10848 / g * kg_to_lb  # Max
    W_w_USAF = 96.948 * ((W_to * n_ult / 10 ** 5) ** 0.65 * (A / np.cos(Lambda)) ** 0.57 * (S / 100) ** 0.61 * (
            (1 + lambda_) / (2 * t_c_m)) ** 0.36 * (1 + V_H / 500) ** 0.5) ** 0.993
    W_h = 127 * ((W_to * n_ult / 10 ** 5) ** 0.87 * (S_h / 100) ** 1.2 * 0.289 * (l_h / 10) ** 0.483 * (
            b_h / t_r_h) ** 0.5) ** 0.458
    W_v = 98.5 * ((W_to * n_ult / 10 ** 5) ** 0.87 * (S_v / 100) ** 1.2 * 0.289 * (
            b_v / t_r_v) ** 0.5) ** 0.458
    # W_v_m = 98.5 * ((W_to * n_ult / 10 ** 5) ** 0.87 * (S_v_m / 100) ** 1.2 * 0.289 * (
    #         b_v_m / t_r_v_m) ** 0.5) ** 0.458
    # W_v_USAF = 2 * W_v_s + W_v_m
    # W_v_torenbeek = (0.04 * (n_ult * (S_h + 2 * S_v_s + S_v_m) ** 2) ** 0.75)  # but not conventional
    W_f = 1.65 * (200 * ((W_to * n_ult / 10 ** 5) ** 0.286 * (l_f / 10) ** 0.857 * ((w_f + h_f) / 10) * (
            V_C / 100) ** 0.338) ** 1.1)  # 1.65*W_f because of flying boat (p75 Roskam)
    W_g = 0.054 * (l_s_m) ** 0.501 * (W_L * n_ult_l) ** 0.684
    # print(W_g / kg_to_lb)
    W_float = data['Structures']['Float_weight']/g* kg_to_lb  # Liesbeth
    print(W_float/kg_to_lb)

    print('W w, h, v, f, g', W_w / kg_to_lb, W_h / kg_to_lb, W_v / kg_to_lb, W_f / kg_to_lb, W_g / kg_to_lb)

    W_struc = W_w + W_h + W_v + W_f + W_g + W_float  # + W_detachment

    return W_struc, W_f


def W_power(W_f):
    # Pwr parameters
    N_p = 2.0
    N_bl = data['FPP']['No. Blades [-]']
    D_p = data['FPP']['Prop Diameter [m]'] * m_to_ft
    P_to = data['FPP']['Pa [kW] Ultim'] * W_to_hp
    N_e = 1.0

    K_fsp = 5.87  # p91 Roskam
    N_t = 2

    # W_pwr
    W_eng = 220 * kg_to_lb  # Kars (dry weight engines)
    W_prop = 24.0 * N_p * N_bl ** 0.391 * (D_p * P_to / N_e / 1000) ** .782
    W_ai_p = 1.03 * N_e ** 0.3 * (P_to / N_e) ** 0.7
    W_fs = 2.49 * ((W_f / K_fsp) ** 0.6 * (1 / (1 + 1)) ** 0.3 * N_t ** 0.2 * N_e ** 0.13) ** 1.21

    # print(W_eng/kg_to_lb)
    # print(W_prop / kg_to_lb)
    # print(W_ai_p / kg_to_lb)
    print(W_fs/kg_to_lb)

    W_pwr = W_eng + W_ai_p + W_prop + W_fs
    # print(W_pwr/kg_to_lb)

    W_pwr = 654 * kg_to_lb + W_fs # Kars!

    return W_pwr, W_fs


def W_fixed_equipment(W_fs, W_to):
    # W_feq
    W_bat = 8 * 36 * kg_to_lb  # Wissam/Berend
    W_systems = (450 * kg_to_lb / 1.2 - W_bat)  # Wissam/Berend (1.2 because els account

    W_fc = (1.08 * W_to ** 0.7) / 2
    W_iae = W_systems
    W_els = 426 * ((W_fs + W_iae) / 1000) ** 0.51

    print('W bat, fc, iae, els', W_bat / kg_to_lb, W_fc / kg_to_lb, W_iae / kg_to_lb, W_els / kg_to_lb)

    W_feq = W_fc + W_els + W_iae + W_bat

    return W_feq


def class_II(W_to, W_fuel):
    # Addition of all weight components
    W_struc, W_f = W_structure(W_to)
    W_pwr, W_fs = W_power(W_f)
    W_feq = W_fixed_equipment(W_fs, W_to)

    print('Str.', 'Pwr', 'FEq')
    print(int(W_struc / kg_to_lb), int(W_pwr / kg_to_lb), int(W_feq / kg_to_lb))

    # New empty weight and take-off weight, also ratio
    W_E = W_struc + W_pwr + W_feq
    W_to_class_II = W_E + W_pl + W_fuel
    W_E_ratio_class_II = W_E / W_to_class_II

    # print()
    # print(W_to_class_II / kg_to_lb)
    print('W empty class II', W_E / kg_to_lb)

    return W_E_ratio_class_II, W_to_class_II

def final_weights():

    W_fuel, W_to, W_E_tent, t_initial_attack, t_one_refill, t_back_to_base, t_total, W_fuel_after_first_drop, W_fuel_refill, W_fuel_back_to_base = class_I(
        W_to_initial, W_E_ratio_initial)
    W_E_ratio_class_II, W_to_class_II = class_II(W_to, W_fuel)

    while abs((W_to_class_II - W_to) / W_to) > 0.005:
        W_fuel, W_to, W_E_tent, t_initial_attack, t_one_refill, t_back_to_base, t_total, W_fuel_after_first_drop, W_fuel_refill, W_fuel_back_to_base = class_I(
            W_to_class_II, W_E_ratio_class_II)
        W_E_ratio_class_II, W_to_class_II = class_II(W_to, W_fuel)

    print()
    W_fuel, W_to, W_E_tent, t_initial_attack, t_one_refill, t_back_to_base, t_total, W_fuel_after_first_drop, W_fuel_refill, W_fuel_back_to_base = class_I(
        W_to_class_II, W_E_ratio_class_II)
    print_class_I_values(t_initial_attack, t_one_refill, t_back_to_base, t_total, W_fuel_after_first_drop,
                         W_fuel_refill, W_fuel_back_to_base, W_to, W_fuel, W_E_tent)

    return W_fuel, W_to, W_E_tent, t_initial_attack, t_one_refill, t_back_to_base, t_total, W_fuel_after_first_drop, W_fuel_refill, W_fuel_back_to_base

W_fuel, W_to, W_E_tent, t_initial_attack, t_one_refill, t_back_to_base, t_total, W_fuel_after_first_drop, W_fuel_refill, W_fuel_back_to_base = final_weights()
