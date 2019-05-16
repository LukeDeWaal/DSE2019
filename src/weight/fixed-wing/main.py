import numpy as np
from Class1.class_i import class_i_main
from Class2.class_ii import ClassII

np.random.seed(1)


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
            span = kwargs['span']
        except KeyError:
            span = float(input('Wing Span: '))

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
            Pa = kwargs['Pa']
        except KeyError:
            Pa = float(input("Pa: "))

        try:
            cd0 = kwargs['Cd0']
        except KeyError:
            cd0 = 0.04

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
            "Pa": Pa
        },
        "aerodynamics": {
            "CL_max": CLmax,
            "Cd0": cd0,
            "oswald": oswald
        },
        "wing": {
            "span": span
        }
    }

    class_ii = ClassII(name=name,
                       datadict=data)

    return class_ii.get_data()


if __name__ == "__main__":

    # TODO: Write Tests

    a = estimate_parameters(
        name='TE_5000L',
        ac_type='twin_engine',
        propulsion='propeller',
        wto=6000.0,
        wpl=5500.0,
        range=1200.0,
        endurance=6.0,
        Pa=2*1061e3,
        loiter=44.0,
        cruise=80.0,
        oswald=0.7,
        CL_max=2.1,
        span=17
    )
