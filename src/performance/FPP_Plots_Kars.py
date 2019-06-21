# Load the Pandas libraries with alias 'pd'
import pandas as pd
import matplotlib.pyplot as plt
import numpy as np

# ## Engines Available
# # Read data from file 'filename.csv'
# data = pd.read_csv("engine_plot.csv")
#
# # Preview the first 5 lines of the loaded data
# print(data.head())
# print(data['Power (kW)'], data['Weight (kg)'])
#
# x = np.array(data['Weight (kg)'])
# print(x)
#
# colours = [  # Use these colours to cycle through if you want to plot multiple lines in the same plot
#        (255 / 255, 0, 0),
#        (107 / 255, 142 / 255, 35 / 255),
#        (30 / 255, 144 / 255, 255 / 255),
#        (0, 0, 139 / 255),
#        (255 / 255, 165 / 255, 0),
#        (34 / 255, 139 / 255, 34 / 255)
#     ]
# line_types = ['-', '--']  # Choose one of these linetypes
# marker_types = ['.', 'o', 'x']  # In case markers are desired, use one of these
# plot_label = 'label'  # Set the desired label
# axis_labels = ['Power (kW)', 'Weight (kg)']  # Set the axis labels
# axis_ranges = [(0, 3400), (0, 600)]  # Set the axis ranges
# plot_title = 'Engines Available'
#
# fig_engine = plt.figure(figsize=(20,5))
# plt.scatter(np.array(data['Power (kW)']), np.array(data['Weight (kg)']), c=colours[5], marker=f'{marker_types[0]}', label=plot_label)
# plt.plot(1693, 241, f'{marker_types[1]}', c=colours[0], label=plot_label)
# plt.xlim(axis_ranges[0][0], axis_ranges[0][1])
# plt.ylim(axis_ranges[1][0], axis_ranges[1][1])
# plt.xticks(fontsize=12)
# plt.yticks(fontsize=12)
# plt.grid(True)
# # plt.legend()
# plt.xlabel(axis_labels[0], fontsize=16)
# plt.ylabel(axis_labels[1], fontsize=16)
# plt.title(plot_title, fontsize=18)
#
# plt.show()


# ## CL 415 relative wing surface plot
# # Read data from file 'filename.csv'
#
# data1 = pd.read_csv("banking.csv")
#
# # Preview the first 5 lines of the loaded data
# print(data1.head())
# print(data1['Bank angle'], data1['Percentage'])
#
# x = np.array(data1['Percentage'])
# print(x)
#
# colours = [  # Use these colours to cycle through if you want to plot multiple lines in the same plot
#        (255 / 255, 0, 0),
#        (107 / 255, 142 / 255, 35 / 255),
#        (30 / 255, 144 / 255, 255 / 255),
#        (0, 0, 139 / 255),
#        (255 / 255, 165 / 255, 0),
#        (34 / 255, 139 / 255, 34 / 255)
#     ]
# line_types = ['-', '--']  # Choose one of these linetypes
# marker_types = ['.', 'o', 'x']  # In case markers are desired, use one of these
# plot_label = 'label'  # Set the desired label
# axis_labels = ['Bank Angle (degrees)', 'Relative Wing Surface Area (%)']  # Set the axis labels
# axis_ranges = [(0, 70), (0, 170)]  # Set the axis ranges
# plot_title = 'Preliminary Wing Sizing'
#
# fig_cl415 = plt.figure(figsize=(20,5))
# plt.plot(np.array(data1['Bank angle']), np.array(data1['Percentage']), f'{line_types[0]}', c=colours[4], label=plot_label)
# plt.plot([30,30], [0,180], f'{line_types[0]}', c=colours[5], label=plot_label)
# plt.xlim(axis_ranges[0][0], axis_ranges[0][1])
# plt.ylim(axis_ranges[1][0], axis_ranges[1][1])
# plt.xticks(fontsize=12)
# plt.yticks(fontsize=12)
# plt.grid(True)
# # plt.legend()
# plt.xlabel(axis_labels[0], fontsize=16)
# plt.ylabel(axis_labels[1], fontsize=16)
# plt.title(plot_title, fontsize=18)
#
# plt.show()