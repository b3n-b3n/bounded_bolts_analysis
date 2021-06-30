import matplotlib.pyplot as plt
import pyautogui
import tkinter
import numpy
import PIL
import math
import time

import calc

from PIL import Image
from io import BytesIO


class Report:
    """ 
    class responsible for creating image and cvs reports of the calculations
    """
    def __init__(self, calc, inpt, root, scheme_dimension, name_ent, dname) -> None:
        self.calc = calc
        self.inpt = inpt
        # root window to take screenshot of
        self.root = root
        self.scheme_dimension = scheme_dimension
        self.name_ent = name_ent
        self.dname = dname

    def gen_cvs_table(self) -> None:
        df = calc.OutCalc(self.calc, self.inpt).create_dataframe()
        path = tkinter.filedialog.asksaveasfilename(defaultextension='.csv', initialdir=self.dname+'/reports')
        df.to_csv(path_or_buf=path)

    def generate_figure(self, dataframe) -> numpy.ndarray:
        # get names of the material from main UI window
        mat1_name = self.inpt.object1['name'].get()
        mat2_name = self.inpt.object2['name'].get()

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
                            colLabels=[mat1_name, mat2_name],
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
        return img

    def take_screenshot(self) -> PIL.Image.Image:
        # take screenshot of the schceme from root window
        width = self.scheme_dimension[0]
        height = self.scheme_dimension[1]
        xpos = self.root.winfo_x()+self.root.winfo_width()-width
        ypos = self.root.winfo_y()+self.root.winfo_height()-height

        return pyautogui.screenshot(region=(xpos, ypos, width, height))

    def cut_figure(self, img) -> numpy.ndarray:
        start, table_found = 0, False
        for y in range(len(img)):
            if (False in (img[y][635] == 255)) and not table_found:
                table_found = True
                start = y
            if (True in (img[y][635] == 255)) and table_found:
                break
        return img[start-15:y+15]

    def create_background(self, shape) -> PIL.Image.Image:
        return numpy.ones((shape[0], shape[1], 3), dtype=numpy.uint8)*255

    def gen_image_report(self):
        # set focus away from the entry box so that it is not highlighted
        self.root.focus_set()
        self.name_ent.config(highlightthickness=0)
        self.root.update()

        df = calc.OutCalc(self.calc, self.inpt).create_dataframe()
        
        # get the table represented as a list of pixels
        fig = self.generate_figure(df)

        # cut off the white strips from the figure
        fig = self.cut_figure(fig)
        
        scr = self.take_screenshot()
        print(type(scr))
        width, height = scr.size
        amount = 100
        scr = scr.resize((height+amount, width+amount))        

        # get white backround to paste the screenshot on
        bg_size = [scr.size[1], len(fig[0])]
        bg = PIL.Image.fromarray(self.create_background(bg_size))

        x = int(bg_size[1]/2-scr.size[0]/2)
        bg.paste(scr, (x, 0))
        # bg.show()
        
        bg = numpy.asarray(bg)
        img_comb = numpy.concatenate([bg, fig])
        img_comb = Image.fromarray(img_comb)
        # img_comb.show()
        path = tkinter.filedialog.asksaveasfilename(defaultextension='.jpg', initialdir=self.dname+'/reports')
        img_comb.save(path)
        
        # set border of name entry (in scheme) to a non zero thickness
        self.name_ent.config(highlightthickness=1)