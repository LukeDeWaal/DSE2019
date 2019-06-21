import matplotlib.pyplot as plt

def plot(data, label, axes, ranges, title, colour, marker):
    colours = [  # Use these colours to cycle through if you want to plot multiple lines in the same plot
       (255 / 255, 0, 0),
       (107 / 255, 142 / 255, 35 / 255),
       (30 / 255, 144 / 255, 255 / 255),
       (0, 0, 139 / 255),
       (255 / 255, 165 / 255, 0),
       (34 / 255, 139 / 255, 34 / 255)
    ]
    line_types = ['-', '--']  # Choose one of these linetypes
    marker_types = ['.', 'o', 'x']  # In case markers are desired, use one of these
    data = [[1, 2, 3], [1, 2, 3]]  # Replace with our data sets
    plot_label = 'label'  # Set the desired label
    axis_labels = ['#x_axis_label', '#y_axis_label']  # Set the axis labels
    axis_ranges = [(0, 3), (0, 5)]  # Set the axis ranges
    plot_title = 'title'

    fig = plt.figure()
    plt.plot(data[0], data[1], f'{line_types[0]}{marker_types[0]}', c=colours[5], label=plot_label)
    plt.xlim(axis_ranges[0][0], axis_ranges[0][1])
    plt.ylim(axis_ranges[1][0], axis_ranges[1][1])
    plt.xticks(fontsize=12)
    plt.yticks(fontsize=12)
    plt.grid(True)
    plt.legend()
    plt.xlabel(axis_labels[0], fontsize=16)
    plt.ylabel(axis_labels[1], fontsize=16)
    plt.title(plot_title, fontsize=18)

    plt.show()

    return

plot()