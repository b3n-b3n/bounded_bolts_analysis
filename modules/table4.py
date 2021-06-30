import pandas as pd
import numpy as np
import matplotlib.pyplot as plt

d = {
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
df = pd.DataFrame(data=d)


def render_mpl_table(data,
                     col_width=3.0,
                     row_height=0.625,
                     font_size=14,
                     header_color='#40466e',
                     row_colors=['#f1f1f2', 'w'],
                     edge_color='w',
                     bbox=[0, 0, 1, 1],
                     header_columns=0,
                     ax=None,
                     **kwargs):
    if ax is None:
        size = (np.array(data.shape[::-1]) + np.array([0, 1])) * np.array(
            [col_width, row_height])
        fig, ax = plt.subplots(figsize=size)
        ax.axis('off')
    mpl_table = ax.table(cellText=data.values,
                         bbox=bbox,
                         colLabels=data.columns,
                         **kwargs)
    mpl_table.auto_set_font_size(False)
    mpl_table.set_fontsize(font_size)

    for k, cell in mpl_table._cells.items():
        cell.set_edgecolor(edge_color)
        if k[0] == 0 or k[1] < header_columns:
            cell.set_text_props(weight='bold', color='w')
            cell.set_facecolor(header_color)
        else:
            cell.set_facecolor(row_colors[k[0] % len(row_colors)])
    return ax.get_figure(), ax


fig, ax = render_mpl_table(df, header_columns=0, col_width=2.0)
fig.savefig("table_mpl.png")