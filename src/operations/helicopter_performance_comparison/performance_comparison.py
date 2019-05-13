import numpy as np
import matplotlib.pyplot as plt
from performance_data_import import ReferenceHelicopters, CL415CompData


def knots_to_mps(knots: float):
    return knots*0.514444


def __operation_time(d_source: float, empty_velocity: float, full_velocity: float, drop_time: float,
                     volume: float, refill_speed: float, full_turn: float, empty_turn: float):
    """
    Time it takes to refill, drop and repeat
    :param d_source: meters
    :param empty_velocity: m/s
    :param full_velocity: m/s
    :param drop_time: Seconds
    :param volume: Liters
    :param refill_speed: Liters Per Minute
    :param full_turn: Seconds
    :param empty_turn: Seconds
    :return: Seconds
    """

    cr_e = d_source/empty_velocity
    cr_f = d_source/full_velocity
    t_refill = volume/refill_speed
    t_drop = drop_time
    t_turn_e = empty_turn
    t_turn_f = full_turn

    total = cr_e + t_refill + t_turn_f + cr_f + t_drop + t_turn_e

    return total


def __time_per_tank(endurance: float, operation_time: float, d_base: float, v_empty: float, refuel_time: float):
    """
    Time it takes to perform maximum operations and refuel
    :param endurance: Seconds
    :param operation_time: Seconds
    :param d_base: Meters
    :param v_empty: m/s
    :return: seconds, #
    """

    cr_base = d_base/v_empty
    time = float(cr_base)

    n = 0

    while True:
        time += operation_time
        n += 1

        future_time = time + operation_time + cr_base

        if future_time >= endurance:

            break

    time += cr_base

    time += refuel_time

    return time, n


def __n_ops_per_day(time_per_tank: float, daytime: float, n_per_tank: int, endurance: float):
    """
    Total refueling missions per day
    :param time_per_tank: seconds
    :param daytime: seconds
    :return: seconds, #
    """
    total = 0
    n = 0
    while True:
        total += time_per_tank
        n += 1

        future = float(total + time_per_tank)

        if future >= daytime:
            break

    # print(n, n_per_tank, round((time_per_tank-1200)/endurance, 4))

    return total, n*n_per_tank


def performance(vehicle: dict, distances: dict, actions: dict):
    # actions: dict, velocities: dict, capacities: dict, distances: dict, endurance: float):
    """
    Main Function
    :param actions: dict
    :param velocities: dict
    :param capacities: dict
    :param distances: dict
    :return:
    """

    operation_time = __operation_time(distances['source'], knots_to_mps(vehicle['v_empty']), knots_to_mps(vehicle['v_full']),
                                      actions['drop'], vehicle['water_capacity'], vehicle['refill_speed']/60,
                                      actions['turn_full'], actions['turn_empty'])



    tank_time, n_ops = __time_per_tank(vehicle['endurance']*3600.0, operation_time,
                                       distances['base'], knots_to_mps(vehicle['v_empty']), actions['refuel'])

    total_time, total_n_ops = __n_ops_per_day(tank_time, 16.00*3600, n_ops, vehicle['endurance']*3600.0)

    return total_time, total_n_ops


if __name__ == "__main__":

    H = ReferenceHelicopters().get_data()
    A = CL415CompData().get_data()

    distances = [i for i in range(0, 750000, 100)]
    ac_perf = [performance(A['cl_415'],
                           distances={
                               'base': distance,
                               'source': 10000.0},
                           actions={
                               'turn_empty': 20.0,
                               'turn_full': 35.0,
                               'drop': 1.0,
                               'refuel': 1600.0})[1]*A['cl_415']['water_capacity']/1000000 for distance in distances]

    plt.plot(distances, ac_perf, 'r-', label='CL415')

    for heli in H.keys():

        heli_perf = [performance(H[heli],
                                 distances={
                                     'base': distance,
                                     'source': 3500.0},
                                 actions={
                                     'turn_empty': 15.0,
                                     'turn_full': 25.0,
                                     'drop': 3.0,
                                     'refuel': 1300.0})[1]*H[heli]['water_capacity']/1000000 for distance in distances]

        plt.plot(distances, heli_perf, label=" ".join(heli.capitalize().split('_')))



    plt.legend()
    plt.grid()
    plt.xlabel('Distance From Base [m]')
    plt.ylabel('Total Amount Dropped Per Day [$10^6$ L] ')


