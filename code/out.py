import plotly
import pandas
import numpy
import math

import calc

from PIL import Image
from io import BytesIO

class Report:
    """ 
    class responsible for creating image and cvs reports of the calculations
    """
    def __init__(self, calc, inpt) -> None:
        self.calc = calc
        self.inpt = inpt

    def gen_cvs_table(self):
        pass

    def gen_image_report(self):
        instance = calc.OutCalc(self.calc, self.inpt)
        df = instance.create_dataframe()

        layout = plotly.graph_objs.Layout(margin={'l': 0, 'r': 0, 't': 0, 'b': 0})

        fig = plotly.graph_objs.Figure(data=[plotly.graph_objs.Table(
            columnwidth=[100, 140, 140, 140, 140, 140, 140, 140, 140, 140, 140], 
            header=dict(
                values=list(df.columns), 
                fill_color='paleturquoise', 
                align='left', 
                line_color='darkslategray'),
            cells=dict(
                values=list(df[col] for col in list(df.columns)), 
                fill_color='lavender',
                align='left', 
                line_color='darkslategray'))])
        # fig.show()
        # img = fig.to_image(format="png")
        # i = Image.open(BytesIO(img))
        # i.show()

    def crop_image(self):
        pass


# pix = numpy.asarray(i)

# count = 1
# while (False in (pix[count][1] == 255)) or (False in (pix[count+1][1] == 255)):
#     count += 1

# pix = pix[:count]
# out = im = Image.fromarray(numpy.uint8(pix))
# out.show()


# fig.show()



"""
======================================================================= 
Open I as an array:

>>> I = numpy.asarray(PIL.Image.open('test.jpg'))

Do some stuff to I, then, convert it back to an image:

>>> im = PIL.Image.fromarray(numpy.uint8(I))
=======================================================================
"""
