import pyautogui
import plotly
import numpy
import math
import time
from bokeh.io import export_png, export_svgs
from bokeh.models import ColumnDataSource, DataTable, TableColumn

import calc

from PIL import Image
from io import BytesIO


class Report:
    """ 
    class responsible for creating image and cvs reports of the calculations
    """
    def __init__(self, calc, inpt, root, scheme_dimension) -> None:
        self.calc = calc
        self.inpt = inpt
        # root window to take screenshot of
        self.root = root
        self.scheme_dimension = scheme_dimension

    def gen_cvs_table(self):
        pass

    def generate_figure(self, dataframe):
        # make the column names appear in bold font type
        column_names = ['<b>'+name+'</b>' for name in list(dataframe.columns)]
        layout = plotly.graph_objs.Layout(margin={'l': 0, 'r': 0, 't': 0, 'b': 0})
        
        fig = plotly.graph_objs.Figure(layout=layout, data=[plotly.graph_objs.Table(
            header=dict(
                values=column_names, 
                font_family="Courier New Bold",
                fill_color='white', 
                align='center', 
                line_color='darkslategray'),
            cells=dict(
                values=list(dataframe[col] for col in list(dataframe.columns)), 
                fill_color='white',
                align='center', 
                line_color='darkslategray'))])
        return fig


    def take_screenshot(self):
        # take screenshot of the schceme from root window
        width = self.scheme_dimension[0]
        height = self.scheme_dimension[1]
        xpos = self.root.winfo_x()+self.root.winfo_width()-width
        ypos = self.root.winfo_y()+self.root.winfo_height()-height

        return pyautogui.screenshot(region=(xpos, ypos, width, height))


    def gen_image_report(self):
        # set focus away from the entry box so that it is not highlighted
        self.root.focus_set()
        self.root.update()

        df = calc.OutCalc(self.calc, self.inpt).create_dataframe()
        
        # table_improved.draw_table(df)
        fig = self.generate_figure(df)
        img = fig.to_image(format="jpg", width = 1000, height = 800)
        img = numpy.asarray(Image.open(BytesIO(img)))

        count = 1
        while (False in (img[count][1] == 255)): count += 1
        img = img[:count]
        shape = len(img[0]);
        
        snd = self.take_screenshot()
        width, height = snd.size
        amount = 1000-height
        snd = snd.resize((1000, width+amount))        
        snd = numpy.asarray(snd)

        print(img.shape, snd.shape)
        imgs_comb = numpy.concatenate([snd, img])
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
