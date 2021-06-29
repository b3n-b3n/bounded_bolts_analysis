import matplotlib
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
    cellLoc='center',
    loc={'bottom': 0,'top': 0})

h = table.get_celld()[(0, 0)].get_height()
w = table.get_celld()[(0, 0)].get_width()
c = ['k', 'k', 'k', 'k', 'k', 'b', 'b', 'r', 'r', 'r', 'r']
c2 = ['w', 'w', 'w', 'w', 'w', 'w', 'w', '0.8', '0.8', '0.6', '0.6']

table.auto_set_font_size(False)
table.set_fontsize(5.5)
for y in range(len(d[0])+1):
    for x in range((len(d))):
        table[(y, x)].set_edgecolor(c[x])
        table[(y, x)].set_facecolor(c2[x])
        if y==0:
            table[(y, x)].set_text_props(fontweight='bold')
    # table[(0, idx)].get_text().set_fontsize('xx-large')


#   bbox=(0, 0.2, 1, 0.8))

# # Create an additional Header
# header = [
#     table.add_cell(-1, pos, w, h, loc="center", facecolor="none")
#     for pos in [5, 6]
# ]
# # header[0].visible_edges = "TBL"
# # header[1].visible_edges = "TBR"
# header[1].get_text().set_text("Header")

# header2 = [
#     table.add_cell(-2, pos, w, h, loc="center", facecolor="none")
#     for pos in [7, 8, 9, 10]
# ]
# # header2[0].visible_edges = "TBL"
# # header2[1].visible_edges = "TB"
# # header2[2].visible_edges = "TB"
# # header2[3].visible_edges = "TBR"
# header2[0].get_text().set_text("Bearing")
# header2[1].get_text().set_text("Stress")
# header2[2].get_text().set_text("Analysis")

# # header3[0].visible_edges = "TBL"
# # header3[1].visible_edges = "TBR"
# # header3[2].visible_edges = "TBL"
# # header3[3].visible_edges = "TBR"

red_patch = mpatches.Patch(color='red', label='Bearing Stress analysis')
blue_patch = mpatches.Patch(color='blue', label='Bolt Strength Analysis')
p = mpatches.Patch(color='0.8', label='Material1')
p2 = mpatches.Patch(color='0.6', label='Material2')

plt.legend(handles=[red_patch, blue_patch, p, p2], ncol=2, bbox_to_anchor=(0.8, 0.8))

plt.tight_layout(h_pad=1, w_pad=1)
plt.axis('off')
plt.savefig("table_mpl.png", pad_inches=0, dpi=1000)
plt.show()