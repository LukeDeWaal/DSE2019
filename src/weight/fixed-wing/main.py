import numpy as np
import tqdm
from Class1.class_i import class_i_main
from Class2.class_ii import ClassII

import sys
sys.path.insert(0, r'C:\Users\LRdeWaal\Desktop\DSE2019\src\tools')

from WebScraping import extract_filtered_data

# np.random.seed(1)


def estimate_parameters(name: str, **kwargs):

    def mps_to_mph(mps: float):
        return mps/0.44704

    def mph_to_mps(mph: float):
        return mph*0.44704

    def km_to_nm(km: float):
        return km*0.539957

    def nm_to_km(nm: float):
        return nm/0.539957

    def kg_to_lbs(kg: float):
        return kg*2.20462

    def lbs_to_kg(lbs: float):
        return lbs/2.20462

    if kwargs:
        try:
            ac_type = kwargs['ac_type']
        except KeyError:
            ac_type = input("Aircraft Type: ")

        try:
            propulsion = kwargs['propulsion']
        except KeyError:
            propulsion = input("Propulsion Type: ")

        try:
            AR = kwargs['AR']
        except KeyError:
            AR = float(input('Aspect Ratio: '))

        try:
            wto = kg_to_lbs(kwargs['wto'])
        except KeyError:
            wto = kg_to_lbs(float(input("MTOW: ")))

        try:
            wpl = kg_to_lbs(kwargs['wpl'])
        except KeyError:
            wpl = kg_to_lbs(float(input("WPL: ")))

        try:
            loiter = mps_to_mph(kwargs['loiter'])
        except KeyError:
            loiter = mps_to_mph(float(input("Loiter Velocity: ")))

        try:
            cruise = mps_to_mph(kwargs['cruise'])
        except KeyError:
            cruise = mps_to_mph(float(input("Cruise Velocity: ")))

        try:
            cruise_range = km_to_nm(kwargs['range'])
        except KeyError:
            cruise_range = km_to_nm(float(input("Range: ")))

        try:
            endurance = kwargs['endurance']
        except KeyError:
            endurance = float(input("Endurance: "))

        try:
            oswald = kwargs['oswald']
        except KeyError:
            oswald = 0.7

        try:
            CLmax = kwargs['CL_max']
        except KeyError:
            CLmax = float(input("CL: "))

        try:
            RC = kwargs['RC']
        except KeyError:
            RC = float(input("RC: "))

        try:
            cd0 = kwargs['Cd0']
        except KeyError:
            cd0 = 0.04

        try:
            n_engines = kwargs['n_engines']
        except KeyError:
            n_engines = int(input("# of engines: "))

    else:
        return

    class_i = class_i_main(weight_dict={
                                'wto': wto,
                                'wpl': wpl,
                                'wfres': 0.025
                            },
                           performance_dict={
                                'range': cruise_range,
                                'endurance': endurance
                            },
                           velocity_dict={
                                'loiter': loiter,
                                'cruise': cruise
                            },
                           ac_data_dict={
                                'type': ac_type,
                                'propulsion': propulsion
                            },
                           N=200)

    data = {
        "weights": {key: lbs_to_kg(value) for key, value in class_i['weights'].items()},
        "velocities": {
            "loiter": mph_to_mps(loiter),
            "cruise": mph_to_mps(cruise)
        },
        "performance": {
            "range": nm_to_km(cruise_range),
            "endurance": endurance,
            "bankangle": 45*np.pi/180,
            "n_engines": n_engines,
            "steady": {
                "RC": RC
            },
            "turning":{
            }
        },
        "aerodynamics": {
            "CL_max": CLmax,
            "Cd0": cd0,
            "oswald": oswald
        },
        "wing": {
            "AR": AR
        }
    }

    class_ii = ClassII(name=name,
                       filepath=f"C:\\Users\\LRdeWaal\\Desktop\DSE2019\\data\\Class II Data\\{ac_type}_estimate.json",
                       datadict=data,
                       )

    return class_ii.get_data()


if __name__ == "__main__":

    # TODO: Write Tests

    a = extract_filtered_data({
        'Power': (1000, 2500),  # kW
        'Weight': (150, 550),   # kg
        'SFC': (0.15, 0.35)    # kg/kW-hr
    })

    for ac in ['twin_engine', 'single_engine', 'regional_tbp', 'military_trainer']:
        for payload in tqdm.tqdm(range(2000, 8500, 500)):

            if ac in ['single_engine', 'military_trainer']:
                n_engines = 1

            else:
                n_engines = 2

            if payload >= 6000:
                power = 1591e3

            else:
                power = 1061e3

            estimate_parameters(
                name=f'{payload}L',
                ac_type=ac,
                propulsion='propeller',
                wto=6000.0,
                wpl=payload,
                range=1200.0,
                endurance=6.0,
                RC=6.0,
                loiter=44.0,
                cruise=80.0,
                oswald=0.7,
                CL_max=2.1,
                AR=8.0,
                n_engines=n_engines
            )
