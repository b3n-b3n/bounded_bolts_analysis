import plotly
import pandas
import numpy
import math

import calc

from PIL import Image
from io import BytesIO


def calculate_tau(vect, d, bolts_num, round_to):
    out = []
    if vect[0] == '-':
        return ['-' for i in range(bolts_num)]
    else:
        for i in range(len(vect)):
            area = math.pi*d[i] / 4
            out.append(round(float(vect[i])*area, round_to))
        return out

def calculate_sigma(vect, t, inpt, bolts_num, round_to):
    if vect[0] == '-':
        return ['-' for i in range(bolts_num)]
    else:
        out = []
        d = inpt.bolt_info['diameter[mm]']
        for i in range(len(vect)):
            out.append(round(vect[i] / (d[i]*t[i]), round_to))
        return out

def vect_to_size(vect, bolts_num, round_to):
    # takes vector and calculates its size
    if not vect:
        return ['-' for i in range(bolts_num)]
    else:
        return [round(math.sqrt(vect[i][0]**2 + vect[i][1]**2), round_to) for i in range(len(vect))] 

def create_dataframe(calc, inpt, round_to):
    round_to = round_to
    bolts_num = len(inpt.bolt_info['name'])
    tab_data = {}  # table data
    tab_data['name'] = inpt.bolt_info['name']
    tab_data['d[mm]'] = inpt.bolt_info['diameter[mm]']
    tab_data['Fs[N]'] = vect_to_size(calc.shear_load, bolts_num, round_to)
    tab_data['Fm[N]'] = vect_to_size(calc.moment_load, bolts_num, round_to)
    tab_data['F[N]'] = vect_to_size(calc.sum_load, bolts_num, round_to)
    tab_data['Tau[MPa]'] = calculate_tau(tab_data['F[N]'], inpt.bolt_info['diameter[mm]'], bolts_num, round_to)
    tab_data['RF-0'] = ['-' for i in range(bolts_num)]
    tab_data['Sigma_1[MPa]'] = calculate_sigma(tab_data['F[N]'], inpt.bolt_info['t1[mm]'], inpt, bolts_num, round_to)
    tab_data['Sigma_2[MPa]'] = calculate_sigma(tab_data['F[N]'], inpt.bolt_info['t2[mm]'], inpt, bolts_num, round_to)
    tab_data['RF-1'] = ['-' for i in range(bolts_num)]
    tab_data['RF-2'] = ['-' for i in range(bolts_num)]




    df = pandas.DataFrame(data=tab_data)
    print(df)
    return df
    # print(df.columns.values, 'cols')

class Report:
    """ 
    class responsible for creating image and cvs reports of the calculations
    """
    def __init__(self, calc, inpt):
        self.calc = calc
        self.inpt = inpt
        self.round_to = 3
        
    def gen_cvs_table(self):
        pass

    def gen_image_report(self, centroid):
        df = create_dataframe(self.calc, self.inpt, self.round_to)

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
