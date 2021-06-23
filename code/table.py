import matplotlib.pyplot as plt

data2 = {
    'ID-number': ['1', '2', '3', '4'],
    'd [mm]': [9.525, 9.525, 9.525, 9.525],
    'Fs [N]': [33.99, 26.15, 13.07, 26.15],
    'Fm [N]': [6.52, 5.01, 2.51, 5.01],
    'F [N]': [33.99, 26.15, 13.07, 26.15],
    'τ [MPa]': [254.28, 195.63, 97.78, 195.63],
    'RF-0 [MPa]': [0.2, 0.51, 0.01, 0.51],
    'σ1 [MPa]': [3.57, 2.75, 0.53, 2.75],
    'σ2 [MPa]': [3.57, 2.75, 0.01, 2.75],
    'RF-1 [MPa]': [0.28, 0.36, 1.89, 0.36],
    'RF-2 [MPa]': [0.28, 0.36, 100.0, 0.36]
}

d = list(data2.values())
values = [ [d[j][i] for j in range(len(d))] for i in range(len(d[0]))]

table = plt.table(cellText=values,
                  colLabels=list(data2.keys()),
                #   Rowloc='center',
                  cellLoc='center',
                  loc= {'bottom': 0, 'top': 0})
                #   bbox=(0, 0.2, 1, 0.8))
h = table.get_celld()[(0, 0)].get_height()
w = table.get_celld()[(0, 0)].get_width()

# Create an additional Header
header = [table.add_cell(-1, pos, w, h, loc="center", facecolor="none")
        for pos in [1, 2, 3]]
header[0].visible_edges = "TBL"
header[1].visible_edges = "TB"
header[2].visible_edges = "TBR"
header[1].get_text().set_text("Header")

header2 = [table.add_cell(-1, pos, w, h, loc="center", facecolor="none")
        for pos in [6, 7]]
header2[0].visible_edges = "TBL"
header2[1].visible_edges = "TBR"
header2[0].get_text().set_text("Header2")


plt.axis('off')
plt.show()