import matplotlib.pyplot as plt
import matplotlib.patches as mpatches

data2 = {
    'ID number': ['1', '2', '3', '4'],
    'd [mm]': [9.525, 9.525, 9.525, 9.525],
    'Fx [N]': [-8.022, -6.171, -3.086, -6.171],
    'Fy [N]': [33.03, 25.408, 12.704, 25.408],
    'F [N]': [33.99, 26.15, 13.07, 26.15],
    'τ [MPa]': [254.28, 195.63, 97.78, 195.63],
    'RF [-]': [0.39, 1.03, 0.01, 1.03],
    'σ1 [MPa]': [3.57, 2.75, 0.53, 2.75],
    'RF1 [-]': [0.28, 0.36, 1.89, 0.36],
    'σ2 [MPa]': [3.57, 2.75, 0.01, 2.75],
    'RF2 [-]': [0.28, 0.36, 100.0, 0.36]
}

d = list(data2.values())
values = [[d[j][i] for j in range(len(d))] for i in range(len(d[0]))]

table = plt.table(
    cellText=values,
    colLabels=list(data2.keys()),
    #   Rowloc='center',
    cellLoc='center',
    loc={
        'bottom': 0,
        'top': 0
    })
#   bbox=(0, 0.2, 1, 0.8))
h = table.get_celld()[(0, 0)].get_height()
w = table.get_celld()[(0, 0)].get_width()

# Create an additional Header
header = [
    table.add_cell(-1, pos, w, h, loc="center", facecolor="none")
    for pos in [5, 6]
]
header[0].visible_edges = "TBL"
header[1].visible_edges = "TBR"
header[1].get_text().set_text("Header")

header2 = [
    table.add_cell(-2, pos, w, h, loc="center", facecolor="none")
    for pos in [7, 8, 9, 10]
]
header2[0].visible_edges = "TBL"
header2[1].visible_edges = "TB"
header2[2].visible_edges = "TB"
header2[3].visible_edges = "TBR"
header2[0].get_text().set_text("Bearing")
header2[1].get_text().set_text("Stress")
header2[2].get_text().set_text("Analysis")

header3 = [
    table.add_cell(-1, pos, w, h, loc="center", facecolor="none")
    for pos in [7, 8, 9, 10]
]
header3[0].visible_edges = "TBL"
header3[1].visible_edges = "TBR"
header3[2].visible_edges = "TBL"
header3[3].visible_edges = "TBR"

red_patch = mpatches.Patch(color='red', label='The red data')
plt.legend(handles=[red_patch])

plt.axis('off')
plt.show()