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

tables = {'fontsize': [7, 7, 7, 6], 'cols': [1, 1 , 2, len(dataframe.columns)]}
# get the data from dataframe
n_rows = len(dataframe)
cell_text = [[dataframe[col][row] for col in dataframe.columns] for row in range(n_rows)]

# define dimensions of the plot
# these should not be changed because cropping of image depends
# on concrete number of pixels in the image
f, ax = plt.subplots(figsize=(6.5, 10))

# create table just to get size of a singe cell for calculation
# of position of the headers
the_table = plt.table(cellText=cell_text, colLabels=dataframe.columns, loc='center')

# height of the cell
h = the_table.get_celld()[(0, 0)].get_height()
# ending height of the table where headers would start
end_h = 0.5+h*(n_rows+1)/2


# creating the main table alongside with the headers
tables['header_0'] = plt.table(cellText=[['']],
                    colLabels=['Bearing Strength\nAnalysis'],
                    fontsize=5,
                    loc='bottom',
                    bbox=[1 / 11 * 5, end_h-2*h, 1 / 11 * 2, h*4])

tables['header_1'] = plt.table(cellText=[['']],
                    colLabels=['Bolt Stress Analysis'],
                    loc='bottom',
                    bbox=[1 / 11 * 7, end_h, 1 / 11 * 4, h*2])

tables['materials'] = plt.table(cellText=[[''] * 2],
                     colLabels=['Material 1', 'Material 2'],
                     loc='bottom',
                     bbox=[1 / 11 * 7, end_h-h, 1 / 11 * 4, h*2])

tables['the_table'] = plt.table(cellText=cell_text,
                     colLabels=dataframe.columns,
                     cellLoc='center',
                     colLoc='center',
                     loc='center')

# set font properies for the headers and column names
for idx, key in enumerate(list(tables.keys())[2:]):
    tables[key].auto_set_font_size(False)
    tables[key].set_fontsize(tables['fontsize'][idx])
    for cell in range(tables['cols'][idx]):
        tables[key][(0, cell)].set_text_props(fontweight='bold')


# Adjust layout of the figure
plt.axis('off')
plt.tight_layout(h_pad=1, w_pad=1)

# transform the figure into list of pixels
f.canvas.draw()
buf = f.canvas.tostring_rgb()
ncols, nrows = f.canvas.get_width_height()
img = numpy.frombuffer(buf, dtype=numpy.uint8).reshape(nrows, ncols, 3)

# cut the image to the desired size
start, table_found = 0, False
for y in range(len(img)):
    if (False in (img[y][635] == 255)) and not table_found:
        table_found = True
        start = y
    if (True in (img[y][635] == 255)) and table_found:
        img = img[start-15:y+15]
        break
    
pil_img = PIL.Image.fromarray(img)
pil_img.show()