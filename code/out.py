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

    def generate_figure(self, dataframe):
        layout = plotly.graph_objs.Layout(margin={'l': 0, 'r': 0, 't': 0, 'b': 0})
        fig = plotly.graph_objs.Figure(layout=layout, data=[plotly.graph_objs.Table(
            header=dict(
                values=list(dataframe.columns), 
                fill_color='paleturquoise', 
                align='left', 
                line_color='darkslategray'),
            cells=dict(
                values=list(dataframe[col] for col in list(dataframe.columns)), 
                fill_color='lavender',
                align='left', 
                line_color='darkslategray'))])

    def gen_image_report(self):
        df = calc.OutCalc(self.calc, self.inpt).create_dataframe()

        fig = self.generate_figure(df)
        img = fig.to_image(format="png", width = 1000, height = 800)
        img = numpy.asarray(Image.open(BytesIO(img)))

        count = 1
        while (False in (img[count][1] == 255)): count += 1
        img = img[:count]
        shape = len(img[0])
        
        # img = Image.open(img)
        snd = Image.open('images/screen.png')
        width, height = snd.size
        amount = 1000-height
        snd = snd.resize((1000, width+amount))
        snd = numpy.asarray(snd)

        print(img.shape, snd.shape)

        # pick the image which is the smallest, and resize the others to match it (can be arbitrary image shape here)
        # min_shape = sorted([(numpy.sum(i.size), i.size ) for i in imgs])[0][1]
        imgs_comb = numpy.concatenate([snd, img])
        # imgs_comb = numpy.vstack((numpy.asarray( i.resize(shape))) for i in imgs)
        imgs_comb = Image.fromarray(imgs_comb)
        imgs_comb.show()

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
