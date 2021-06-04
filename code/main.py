# general libraries
from tkinter.constants import NONE
import tkinter.filedialog
import pyautogui
import tkinter
import math
import os

# including local files
import input_interface
import scheme

# get a path to this file
dname = r'{}'.format(os.path.realpath(__file__).strip('main.py'))
# change the working directory if it is somewhere else
os.chdir(dname)


root = tkinter.Tk()
root.title('eccentric joints')

# general appearance options
bg = 'grey99'
root['bg'] = bg
ch = 420  # canvas height
cw = 450  # canvas width
relief = 'groove'
font = [('ms sans', '13'), ('ms sans', '11'), ('ms sans', '9')]


g = tkinter.Canvas(root, width=cw, height=ch, bg='grey80',
                   highlightthickness=0)  # 1000x600
g.grid(row=1, column=1, rowspan=2, sticky='s')

err_lab = tkinter.Label(root, text='tuto je balel',
                        font=font[1], fg='red', bg=bg)
err_lab.grid(row=0, column=1, pady=(10, 0))

# sample bolt
sp_bolt = {'name': [''],
           'diameter[mm]': [''],
           'x-position': [''],
           'y-position': [''],
           'E[MPa]': [''],
           'Rm[MPa]': [''],
           't[mm]': [''],
           't2[mm]': ['']}

# sample force
sp_force = {'name': [''],
            'size[N]': [''],
            'x-position': [''],
            'y-position': [''],
            'angle[deg]': ['']}


def calculate_centroid(bolts):
    l = len(bolts['x-position'])
    x = sum(bolts['x-position'][1:l]) / len(bolts['x-position'])
    y = sum(bolts['y-position'][1:l]) / len(bolts['y-position'])
    return [x, y]


def centroid_and_scheme(bolt, force):
    # try:
    centroid = calculate_centroid(inpt.bolt_info)
    sktch.redraw(inpt.bolt_info, inpt.force_info, centroid)
    # except:
    #     err_lab.config(text='there are no geometry and/or force data')


def create_buttons(sktch, inpt):
    button_id = ['draw', 'calculate', 
                'genrate report', 'multiple reports',
                'load geometry', 'load stress']
    functions = [lambda: centroid_and_scheme(inpt.bolt_info, inpt.force_info),
                 lambda: print(inpt.bolt_info),
                 sktch.idk, sktch.idk,
                 sktch.idk, sktch.idk,]

    for index, id in enumerate(button_id):
        tkinter.Button(inpt.buttons, text=id, command=functions[index], width=15,
                       font=font[1], bg=bg, relief=relief).grid(row=index//2,
                                                                column=index % 2, sticky='e'+'w', padx=2, pady=2)


inpt = input_interface.UI(root, bg, font, sp_bolt, sp_force, dname)
sktch = scheme.Scheme(g, inpt, cw, ch, err_lab, font)
create_buttons(sktch, inpt)


g.update()
g.mainloop()
