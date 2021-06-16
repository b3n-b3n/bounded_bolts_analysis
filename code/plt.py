import plotly
import pandas
import numpy

from PIL import Image
from io import BytesIO

# import plotly.io as pio
# from PIL import Image
# import io

df = pandas.DataFrame([['1', '2', '3', '4'],
                        [9.525, 9.525, 9.525, 9.525],
                        [50.08, 0.0, 0.0, 50.08],
                        [50.08, 50.08, 0.0, 0.0],
                        [2.6, 2.0, 1.0, 2.0],
                        [1.0, 2.6, 1.0, 2.6],
                        [1.0, 1.0, 2.6, 1.0],
                        [1.0, 1.0, 2.6, 1.0],
                        [1.0, 1.0, 2.6, 1.0],
                        [1.0, 1.0, 1.0, 1.0]],
                        columns=['name', 'diameter', 'xpos', 'ypos'])
print(df)

layout = plotly.graph_objs.Layout(autosize=True, margin={'l': 0, 'r': 0, 't': 0, 'b': 0})

fig = plotly.graph_objs.Figure(layout=layout,
        data=[plotly.graph_objs.Table(header=dict(values=list(df.columns), fill_color='paleturquoise', align='left'),
        cells=dict(values=[df.name, df.diameter, df.xpos, df.ypos], fill_color='lavender',align='left'))])


img = fig.to_image(format="png")
i = Image.open(BytesIO(img))
pix = numpy.asarray(i)

count = 1
while (False in (pix[count][1] == 255)) or (False in (pix[count+1][1] == 255)):
    count += 1

pix = pix[:count]
out = im = Image.fromarray(numpy.uint8(pix))
out.show()


# fig.show()



"""
======================================================================= 
Open I as an array:

>>> I = numpy.asarray(PIL.Image.open('test.jpg'))

Do some stuff to I, then, convert it back to an image:

>>> im = PIL.Image.fromarray(numpy.uint8(I))
=======================================================================
"""
