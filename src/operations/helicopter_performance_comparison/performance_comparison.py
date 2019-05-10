import numpy as np
import matplotlib.pyplot as plt
from performance_data_import import ReferenceHelicopters, CL415CompData


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

    return cr_e + t_refill + t_turn_f + cr_f + t_drop + t_turn_e


def __n_ops_per_tank(endurance: float, operation_time: float, d_base: float, v_empty: float):
    """
    Time it takes to perform maximum operations and refuel
    :param endurance:
    :param operation_time:
    :param d_base:
    :param v_empty:
    :return:
    """

    cr_base = d_base/v_empty
    time = float(cr_base)

    n = 0

    while True:
        time += operation_time
        n += 1
        if (time + operation_time + cr_base) >= endurance:
            break

    time += cr_base

    return time, n


def __n_ops_per_day(time_per_tank: float, daytime: float):
    """
    Total refueling missions per day
    :param time_per_tank:
    :param daytime:
    :return:
    """
    total = 0
    n = 0
    while True:
        total += time_per_tank
        n += 1
        if total > daytime:
            break

    return total, n


def performance(vehicle: dict, distances: dict, actions: dict):
    # actions: dict, velocities: dict, capacities: dict, distances: dict, endurance: float):
    """
    Main Function
    :param actions:
    :param velocities:
    :param capacities:
    :param distances:
    :param endurance:
    :return:
    """

    operation_time = __operation_time(distances['source'], vehicle['v_empty'], vehicle['v_full'],
                                      actions['drop'], vehicle['water_capacity'], vehicle['refill_speed']/60,
                                      actions['turn_full'], actions['turn_empty'])

    tank_time, n_ops = __n_ops_per_tank(vehicle['endurance'], operation_time, distances['base'], vehicle['v_empty'])

    total_time, total_n_ops = __n_ops_per_day(tank_time, 16.00*3600)

    return total_time, total_n_ops


if __name__ == "__main__":

    H = ReferenceHelicopters().get_data()
    A = CL415CompData().get_data()

    a = performance(A['cl_415'],
                    distances={'base': 50000.0, 'source': 10000.0},
                    actions={'turn_empty': 19.0, 'turn_full': 35.0, 'drop': 1.0})
