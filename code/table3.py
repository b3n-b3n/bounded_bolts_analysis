import numpy as np
import matplotlib.pyplot as plt

data = {
    'ID number': ['1', '2', '3', '4', 9.525, 9.525, 9.525, '2', '3', '4', 9.525, 9.525, 9.525],
    'd [mm]': [9.525, 9.525, 9.525, 9.525, 9.525, 9.525, 9.525, '2', '3', '4', 9.525, 9.525, 9.525],
    'Fx [N]': [-8.022, -6.171, -3.086, -6.171, 9.525, 9.525, 9.525, '2', '3', '4', 9.525, 9.525, 9.525],
    'Fy [N]': [33.03, 25.408, 12.704, 25.408, 9.525, 9.525, 9.525, '2', '3', '4', 9.525, 9.525, 9.525],
    'F [N]': [33.99, 26.15, 13.07, 26.15, 9.525, 9.525, 9.525, '2', '3', '4', 9.525, 9.525, 9.525],
    'τ [MPa]': [254.28, 195.63, 97.78, 195.63, 9.525, 9.525, 9.525, '2', '3', '4', 9.525, 9.525, 9.525],
    'RF [-]': [0.39, 1.03, 0.01, 1.03, 9.525, 9.525, 9.525, '2', '3', '4', 9.525, 9.525, 9.525],
    'σ1 [MPa]': [3.57, 2.75, 0.53, 2.75, 9.525, 9.525, 9.525, '2', '3', '4', 9.525, 9.525, 9.525],
    'RF1 [-]': [0.28, 0.36, 1.89, 0.36, 9.525, 9.525, 9.525, '2', '3', '4', 9.525, 9.525, 9.525],
    'σ2 [MPa]': [3.57, 2.75, 0.01, 2.75, 9.525, 9.525, 9.525, '2', '3', '4', 9.525, 9.525, 9.525],
    'RF2 [-]': [0.28, 0.36, 100.0, 0.36, 9.525, 9.525, 9.525, '2', '3', '4', 9.525, 9.525, 9.525]
}

columns = list(data.keys())
n_rows = len(data[columns[0]])


# Plot bars and create text labels for the table
cell_text = []
for row in range(n_rows):
    cell_text.append([data[col][row] for col in columns])

f, ax = plt.subplots()
print(f, ax)

# Add headers and a table at the bottom of the axes
header_0 = ax.table(cellText=[[''] * 2],
                     colLabels=['Extra header 1', 'Extra header 2'],
                     loc='bottom',
                     # (posx, posy, width, height)
                     bbox=[0, 0.85, 0.8, 0.1])

header_1 = ax.table(cellText=[['']],
                     colLabels=['Just Hail'],
                     loc='bottom',
                     bbox=[0.8, 0.85, 0.2, 0.1])

the_table = ax.table(cellText=cell_text,
                      colLabels=columns,
                      bbox=[0, 0.6, 1.0, 0.3])

the_table.scale(1, 7)
# Adjust layout to make room for the table:
# plt.subplots_adjust(left=0.2, bottom=-0.2)
plt.axis('off')
# plt.margins(x=None, y=None)
plt.tight_layout(h_pad=1, w_pad=1)
plt.savefig("table_mpl.png", pad_inches=0, dpi=1000)
plt.show()
