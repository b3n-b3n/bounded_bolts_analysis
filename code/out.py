import plotly
import pandas
import numpy
import math

import calc

from PIL import Image
from io import BytesIO


def calculate_tau(vect, d, bolts_num, round_to):
    out = []
    if not vect:
        return ['-' for i in range(bolts_num)]
    else:
        for i in range(len(vect)):
            area = math.pi*d[i] / 4
            out.append(round(vect[i]*area, round_to))
        return out

def calculate_sigma(vect, t, c, inpt, bolts_num, round_to):
    if not vect:
        return ['-' for i in range(bolts_num)]
    else:
        out = []
        x = inpt.bolt_info['x-pos[mm]']
        y = inpt.bolt_info['y-pos[mm]']
        for idx, v in enumerate(vect):
            d = calc.Auxilliary.distance_from_centroid(None, c[0], c[1], x[idx], y[idx])
            out.append(round(vect[idx] / d*t[idx], round_to))
        return out

def vect_to_size(vect, bolts_num, round_to):
    # takes vector and calculates its size
    if not vect:
        return ['-' for i in range(bolts_num)]
    else:
        return [round(math.sqrt(vect[i][0]**2 + vect[i][1]**2), round_to) for i in range(len(vect))] 

def create_dataframe(calc, inpt, round_to, c):
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
    tab_data['Sigma_1[MPa]'] = calculate_sigma(tab_data['F[N]'], inpt.bolt_info['t1[mm]'], c, inpt, bolts_num, round_to)
    tab_data['Sigma_2[MPa]'] = calculate_sigma(tab_data['F[N]'], inpt.bolt_info['t2[mm]'], c, inpt, bolts_num, round_to)
    tab_data['RF-1'] = ['-' for i in range(bolts_num)]
    tab_data['RF-2'] = ['-' for i in range(bolts_num)]



    print(tab_data)

    df = pandas.DataFrame(data=tab_data)
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
        df = create_dataframe(self.calc, self.inpt, self.round_to, centroid)

        layout = plotly.graph_objs.Layout(autosize=True, margin={'l': 0, 'r': 0, 't': 0, 'b': 0})

        fig = plotly.graph_objs.Figure(layout=layout,
        data=[plotly.graph_objs.Table(header=dict(values=list(df.columns), fill_color='paleturquoise', align='left'),
        cells=dict(values=list(df[col] for col in list(df.columns)), fill_color='lavender',align='left'))])
        fig.show()

    def crop_image(self):
        pass


# img = fig.to_image(format="png")
# i = Image.open(BytesIO(img))
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
