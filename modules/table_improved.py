import matplotlib.pyplot as plt
import matplotlib
import pandas
import numpy


def mergecells(table, cells):
    '''
    Merge N matplotlib.Table cells

    Parameters
    -----------
    table: matplotlib.Table
        the table
    cells: list[set]
        list of sets od the table coordinates
        - example: [(0,1), (0,0), (0,2)]

    Notes
    ------
    https://stackoverflow.com/a/53819765/12684122
    '''
    cells_array = [numpy.asarray(c) for c in cells]
    h = numpy.array([
        cells_array[i + 1][0] - cells_array[i][0]
        for i in range(len(cells_array) - 1)
    ])
    v = numpy.array([
        cells_array[i + 1][1] - cells_array[i][1]
        for i in range(len(cells_array) - 1)
    ])

    # if it's a horizontal merge, all values for `h` are 0
    if not numpy.any(h):
        # sort by horizontal coord
        cells = numpy.array(sorted(list(cells), key=lambda v: v[1]))
        edges = ['BTL'] + ['BT' for i in range(len(cells) - 2)] + ['BTR']
    elif not numpy.any(v):
        cells = numpy.array(sorted(list(cells), key=lambda h: h[0]))
        edges = ['TRL'] + ['RL' for i in range(len(cells) - 2)] + ['BRL']
    else:
        raise ValueError("Only horizontal and vertical merges allowed")

    for cell, e in zip(cells, edges):
        table[cell[0], cell[1]].visible_edges = e

    txts = [table[cell[0], cell[1]].get_text() for cell in cells]
    tpos = [numpy.array(t.get_position()) for t in txts]

    # transpose the text of the left cell
    trans = (tpos[-1] - tpos[0]) / 2
    # didn't had to check for ha because I only want ha='center'
    txts[0].set_transform(matplotlib.transforms.Affine2D().translate(*trans))
    for txt in txts[1:]:
        txt.set_visible(False)


def draw_table(df):
    # df = pandas.DataFrame()
    # df['Animal'] = ['Cow', 'Bear']
    # df['Weight'] = [250, 450]
    # df['Favorite'] = ['Grass', 'Honey']
    # df['Least Favorite'] = ['Meat', 'Leaves']

    print(df)

    fig = plt.figure(figsize=(9, 2))
    ax = fig.gca()
    ax.axis('off')
    r, c = df.shape
    r += 1

    # ensure consistent background color
    ax.table(cellColours=[['lightgray']] + [['none']], bbox=[0, 0, 1, 1])

    # plot the real table
    table = ax.table(cellText=numpy.vstack(
        [['', '', '', '', '', '', '', '', '', '', ''],
        ['', '', '', '', '', '', '', 'material2', '', 'material1', ''],
         df.columns, df.values]),
                     cellColours=[['none'] * c] * (2 + r),
                     bbox=[0, 0, 1, 1])

    # # do the 3 cell merges needed
    # mergecells(table, [(1,0), (0,0)])
    # mergecells(table, [(1,1), (0,1)])
    # mergecells(table, [(0, 7), (0, 8), (0, 9), (0, 10)])
    # mergecells(table, [(1, 9), (1, 10)])
    # mergecells(table, [(1, 7), (1, 8)])

    # need to draw here so the text positions are calculated
    fig.canvas.draw()
    fig.savefig('img.png')
    fig.show()