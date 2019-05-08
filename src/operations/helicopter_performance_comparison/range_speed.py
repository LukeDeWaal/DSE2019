import numpy as np
import matplotlib.pyplot as plt
from performance_data_import import ReferenceHelicopters, CL415StatData, CL415EstData


def knots_to_mps(knots: float):
    return knots * 0.514444


def miles_to_km(distance: float):
    return distance*1.60934


def helicopter_performance_calculation(data: dict):

    def performance(helicopter: dict, initial_distance: float, source_distance: float, n_drops: int, drop_time: float = 5.0, swarm_size: int = 1):

        base_cruise = initial_distance / knots_to_mps(helicopter['v_without'])

        empty_turntime = 5.0
        full_turntime = 10.0

        empty_cruise = source_distance / knots_to_mps(helicopter['v_without'])
        refill_time  = helicopter['system_capacity']/helicopter['refill_speed']
        full_cruise = source_distance / knots_to_mps(helicopter['v_with'])

        operation_time = empty_cruise + refill_time + full_turntime + full_cruise + drop_time + empty_turntime

        total_time = float(base_cruise)

        for drop in range(n_drops):
            total_time += operation_time

        total_time += base_cruise

        return swarm_size*n_drops*helicopter['system_capacity']/(total_time/3600), total_time/3600

    performance_result = {}
    time_result = {}

    for helicopter in data.keys():
        performance_result[helicopter] = []
        time_result[helicopter] = []
        for dist in range(0, 41):
            p = performance(helicopter=data[helicopter],
                            initial_distance=20.0e3,
                            source_distance=dist*(10**3),
                            n_drops=5)

            performance_result[helicopter].append(p[0])
            time_result[helicopter].append(p[1])

    return performance_result, time_result


def fixedwing_performance_calculation(data: dict):

    def performance(aircraft: dict,initial_distance: float, source_distance: float, n_drops: int, swarm_size: int = 1):

        base_cruise = initial_distance / aircraft['empty']['velocities']['cruise']

        empty_turnaroundtime = aircraft['empty']['turntime']
        full_turnaroundtime = aircraft['full']['turntime']

        empty_cruise = source_distance / aircraft['empty']['velocities']['cruise']
        refill_time = aircraft['filling']['landing'] + aircraft['filling']['scoop'] + aircraft['filling']['takeoff']
        full_cruise = source_distance / aircraft['full']['velocities']['cruise']

        operation_time = empty_cruise + refill_time + full_turnaroundtime + full_cruise + aircraft['dropping'] + empty_turnaroundtime

        total_time = float(base_cruise)

        for drop in range(n_drops):
            total_time += operation_time

        total_time += base_cruise

        return swarm_size*n_drops*aircraft['filling']['capacity']/(total_time/3600), total_time/3600

    performance_result = []
    time_result = []

    for dist in range(0, 41):
        p = performance(aircraft=data,
                        initial_distance=20.0e3,
                        source_distance=dist * (10 ** 3),
                        n_drops=5)

        performance_result.append(p[0])
        time_result.append(p[1])

    return performance_result, time_result


def cl415_statdata_to_array(data_obj: CL415StatData):

    data = np.zeros((len(data_obj.get_data()), 3))

    for idx, (key, value) in enumerate(data_obj.get_data().items()):
        data[idx, 0] = miles_to_km(int(key))
        data[idx, 1] = value['DPH']
        data[idx, 2] = value['LPH']

    return data


def plot_results():

    refheli = ReferenceHelicopters()
    refcl415 = CL415StatData()
    refcl415_2 = CL415EstData()

    heli_performance, heli_time = helicopter_performance_calculation(refheli.get_data())
    cl415_performance = cl415_statdata_to_array(refcl415)
    cl415_performance_2, cl415_time_2 = fixedwing_performance_calculation(refcl415_2.get_data()['CL415'])

    fig, ax = plt.subplots(nrows=2, ncols=1, sharex=True)

    top = ax[0]
    bot = ax[1]

    distance = [i for i in range(41)]
    for heli in heli_performance.keys():
        top.plot(distance, heli_performance[heli], label=" ".join(heli.capitalize().split('_')))
        bot.plot(distance, heli_time[heli], label=heli)

    top.plot(distance, cl415_performance_2, 'm--', label='CL415')
    # top.plot(cl415_performance[:,0], cl415_performance[:,2], label='CL-415')


    top.grid()
    top.legend()
    bot.grid()





if __name__ == "__main__":

    plot_results()
