import numpy
import matplotlib.pyplot as plt
import PIL
import pandas

data = {
    'ID number': [
        '1', '2', '3', '4', 9.525, 9.525, 9.525, '2', '3', '4', 9.525, 9.525,
        9.525
    ],
    'd [mm]': [
        9.525, 9.525, 9.525, 9.525, 9.525, 9.525, 9.525, '2', '3', '4', 9.525,
        9.525, 9.525
    ],
    'Fx [N]': [
        -8.022, -6.171, -3.086, -6.171, 9.525, 9.525, 9.525, '2', '3', '4',
        9.525, 9.525, 9.525
    ],
    'Fy [N]': [
        33.03, 25.408, 12.704, 25.408, 9.525, 9.525, 9.525, '2', '3', '4',
        9.525, 9.525, 9.525
    ],
    'F [N]': [
        33.99, 26.15, 13.07, 26.15, 9.525, 9.525, 9.525, '2', '3', '4', 9.525,
        9.525, 9.525
    ],
    'τ [MPa]': [
        254.28, 195.63, 97.78, 195.63, 9.525, 9.525, 9.525, '2', '3', '4',
        9.525, 9.525, 9.525
    ],
    'RF [-]': [
        0.39, 1.03, 0.01, 1.03, 9.525, 9.525, 9.525, '2', '3', '4', 9.525,
        9.525, 9.525
    ],
    'σ1 [MPa]': [
        3.57, 2.75, 0.53, 2.75, 9.525, 9.525, 9.525, '2', '3', '4', 9.525,
        9.525, 9.525
    ],
    'RF1 [-]': [
        0.28, 0.36, 1.89, 0.36, 9.525, 9.525, 9.525, '2', '3', '4', 9.525,
        9.525, 9.525
    ],
    'σ2 [MPa]': [
        3.57, 2.75, 0.01, 2.75, 9.525, 9.525, 9.525, '2', '3', '4', 9.525,
        9.525, 9.525
    ],
    'RF2 [-]': [
        0.28, 0.36, 100.0, 0.36, 9.525, 9.525, 9.525, '2', '3', '4', 9.525,
        9.525, 9.525
    ]
}

dataframe = pandas.DataFrame({
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
)

columns = dataframe.columns
n_rows = len(dataframe)

# Plot bars and create text labels for the table
cell_text = []
for row in range(n_rows):
    cell_text.append([dataframe[col][row] for col in columns])

f, ax = plt.subplots(figsize=(6.5, 10))

# Add headers and a table at the bottom of the axes

the_table = plt.table(cellText=cell_text,
                     colLabels=columns,
                     cellLoc='center',
                     colLoc='center',
                     loc='center')

h = the_table.get_celld()[(0, 0)].get_height()

end_h = 0.5+h*(n_rows+1)/2

header_0 = plt.table(cellText=[['']],
                    colLabels=['Bearing Strength\nAnalysis'],
                    fontsize=5,
                    loc='bottom',
                    bbox=[1 / 11 * 5, end_h-2*h, 1 / 11 * 2, h*4])

header_1 = plt.table(cellText=[['']],
                    colLabels=['Bolt Stress Analysis'],
                    loc='bottom',
                    bbox=[1 / 11 * 7, end_h, 1 / 11 * 4, h*2])


materials = plt.table(cellText=[[''] * 2],
                     colLabels=['Material 1', 'Material 2'],
                     loc='bottom',
                     bbox=[1 / 11 * 7, end_h-h, 1 / 11 * 4, h*2])

the_table = plt.table(cellText=cell_text,
                     colLabels=columns,
                     cellLoc='center',
                     colLoc='center',
                     loc='center')

header_0.auto_set_font_size(False)
header_0.set_fontsize(8)
header_1.auto_set_font_size(False)
header_1.set_fontsize(8)
materials.auto_set_font_size(False)
materials.set_fontsize(8)
the_table.auto_set_font_size(False)
the_table.set_fontsize(6)

for cell in range(len(columns)):
    the_table[(0, cell)].set_text_props(fontweight='bold')


# Adjust layout to make room for the table:
plt.axis('off')
plt.tight_layout(h_pad=1, w_pad=1)
f.canvas.draw()
buf = f.canvas.tostring_rgb()
ncols, nrows = f.canvas.get_width_height()
img = numpy.frombuffer(buf, dtype=numpy.uint8).reshape(nrows, ncols, 3)


start, end = 0, nrows
table_found = False
for y in range(len(img)):
    if (False in (img[y][635] == 255)) and not table_found:
        table_found = True
        start = y
    if (True in (img[y][635] == 255)) and table_found:
        end = y
        break
img = img[start-15:end+15]
pil_img = PIL.Image.fromarray(img)
pil_img.show()