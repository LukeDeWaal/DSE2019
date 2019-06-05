import numpy as np
import matplotlib.pyplot as plt
from mpl_toolkits import mplot3d

import os
import sys
sys.path.insert(0, '\\'.join(os.getcwd().split('\\')[:-1]) + '\\tools')

from GoogleSheetsImport import GoogleSheetsDataImport, SHEET_NAMES, SPREADSHEET_ID


def data_import():
    return GoogleSheetsDataImport(SPREADSHEET_ID, *SHEET_NAMES).get_data()


def control_surface_ratio(data, PL = 1):

    chord = data['Aero']['Wing chord']
    coefficient = lambda xw, xpl: (data['Aero']['CL_h']/data['Aero']['CL_A-h']*(data['Aero']['Vh/V']**2)*((data['C&S']['H Wing'][0] - 1)/chord - xw - data['Aero']['x_ac']))**(-1)
    cg = lambda xw, xpl: ((data['Structures']['Wing_weight [N]'] + data['Weights']['WF [N]'])*xw + data['Weights']['WPL [N]']*xpl*PL + data['Structures']['Fuselage_weight [N]']*(data['C&S']['Fuselage'][0]-1)/chord + data['FPP']['Engine Weight [N]']*(data['C&S']['Engine'][0] - 1)/chord)/\
                         (data['Structures']['Wing_weight [N]'] + data['Weights']['WF [N]'] + data['Weights']['WPL [N]']*PL + data['Structures']['Fuselage_weight [N]'] + data['FPP']['Engine Weight [N]'])
    thrust = data['FPP']['Tc']/data['Aero']['CL_A-h']*2*(data['FPP']['Prop Diameter [m]']**2/data['FPP']['S [m^2]'])*(data['C&S']['Engine'][1] - data['C&S']['Wing'][1])

    return lambda xw, xpl: coefficient(xw, xpl)*(cg(xw, xpl) - xw - data['Aero']['x_ac'] + data['Aero']['Cm_ac']/data['Aero']['CL_A-h'] - thrust), cg


def stability_surface_ratio(data, PL = 1):

    chord = data['Aero']['Wing chord']
    coefficient = -((1 - data['Aero']['de/da'])*data['Aero']['Vh/V']**2)**(-1)*data['Aero']['CL_alpha_A-h']/data['Aero']['CL_alpha_h']

    cg = lambda xw, xpl: ((data['Structures']['Wing_weight [N]'] + data['Weights']['WF [N]']) * xw + data['Weights']['WPL [N]'] * xpl * PL + data['Structures']['Fuselage_weight [N]'] * (data['C&S']['Fuselage'][0] - 1) / chord +data['FPP']['Engine Weight [N]'] * (data['C&S']['Engine'][0] - 1) / chord) / \
                         (data['Structures']['Wing_weight [N]'] + data['Weights']['WF [N]'] + data['Weights']['WPL [N]'] * PL + data['Structures']['Fuselage_weight [N]'] + data['FPP']['Engine Weight [N]'])

    return lambda xw, xpl: coefficient*((cg(xw, xpl) - (data['C&S']['Wing'][0] - 1)/chord - data['Aero']['x_ac'] + data['C&S']['SM'])/(cg(xw, xpl) - (data['C&S']['H Wing'][0] - 1)/chord + data['C&S']['SM']))


if __name__ == '__main__':

    xwing = np.linspace(0, 3., 50)
    xpayload = np.linspace(0, 3., 50)

    data = GoogleSheetsDataImport(SPREADSHEET_ID, *SHEET_NAMES).get_data()

    fulldatalst = []
    emptdatalst = []

    cgfulllst = []
    cgemptylst = []

    fc_Sh_full, cgfull = control_surface_ratio(data, PL=1)
    fc_Sh_empty, cgempty = control_surface_ratio(data, PL=0)

    for xw in xwing:
        for xpl in xpayload:
            fulldatalst.append([xw, xpl, fc_Sh_full(xw, xpl)])
            emptdatalst.append([xw, xpl, fc_Sh_empty(xw, xpl)])

            cgfulllst.append([xw, xpl, cgfull(xw, xpl)])
            cgemptylst.append([xw, xpl, cgempty(xw, xpl)])

    fc = lambda x: (fc_Sh_full(x, x), fc_Sh_empty(x, x))
    fcg = lambda x: (cgfull(x, x), cgempty(x, x))

    fulldataarr = np.array(fulldatalst)
    emptydataarr = np.array(emptdatalst)

    fullcgarr = np.array(cgfulllst)
    emptycgarr = np.array(cgemptylst)

    fig = plt.figure()
    ax = plt.axes(projection='3d')

    ax.scatter3D(fulldataarr[:, 0], fulldataarr[:, 1], fulldataarr[:, 2], c='b')
    ax.scatter3D(emptydataarr[:, 0], emptydataarr[:, 1], emptydataarr[:, 2], c='r')
    ax.set_xlabel('Wing Position')
    ax.set_ylabel('Payload Position')
    ax.set_zlabel('Sh/S')
    ax.title.set_text('Controllability')
    # ax.set_ylim(0, 1)

    fig = plt.figure()
    ax = plt.axes(projection='3d')

    ax.scatter3D(fullcgarr[:, 0], fullcgarr[:, 1], fullcgarr[:, 2], c='b')
    ax.scatter3D(emptycgarr[:, 0], emptycgarr[:, 1], emptycgarr[:, 2], c='r')
    ax.set_xlabel('Wing Position')
    ax.set_ylabel('Payload Position')
    ax.set_zlabel('X CG')

    fulldatalst = []
    emptdatalst = []

    cgfulllst = []
    cgemptylst = []

    fs_Sh_full = stability_surface_ratio(data, PL=1)
    fs_Sh_empty = stability_surface_ratio(data, PL=0)

    for xw in xwing:
        for xpl in xpayload:
            fulldatalst.append([xw, xpl, fs_Sh_full(xw, xpl)])
            emptdatalst.append([xw, xpl, fs_Sh_empty(xw, xpl)])

            cgfulllst.append([xw, xpl, cgfull(xw, xpl)])
            cgemptylst.append([xw, xpl, cgempty(xw, xpl)])

    fs = lambda x: (fs_Sh_full(x, x), fs_Sh_empty(x, x))

    fulldataarr = np.array(fulldatalst)
    emptydataarr = np.array(emptdatalst)

    fullcgarr = np.array(cgfulllst)
    emptycgarr = np.array(cgemptylst)

    fig = plt.figure()
    ax = plt.axes(projection='3d')

    ax.scatter3D(fulldataarr[:, 0], fulldataarr[:, 1], fulldataarr[:, 2], c='b')
    ax.scatter3D(emptydataarr[:, 0], emptydataarr[:, 1], emptydataarr[:, 2], c='r')
    ax.set_xlabel('Wing Position')
    ax.set_ylabel('Payload Position')
    ax.set_zlabel('Sh/S')
    ax.title.set_text('Stability')
    # ax.set_ylim(0, 1)

    print("CG: ", fcg(1))
    print("Control: ",fc(1))
    print("Stability: ",fs(1))