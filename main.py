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


g = tkinter.Canvas(root, width=cw, height=ch, bg='grey80', highlightthickness=0)  # 1000x600
g.grid(row=0, column=1, rowspan=2, sticky='s')

# sample bolt
sp_bolt = {'name': [None],
        'diameter[mm]': [None],
        'x-position': [None],
        'y-position': [None],
        'E[MPa]': [None],
        'Rm[MPa]': [None],
        't[mm]': [None],
        't2[mm]': [None]}

# sample force
sp_force = {'name': [None],
        'size': [None],  
        'x-position': [None],
        'y-position': [None],
        'angle': [None]}


def calculate_centroid(bolts):
        x = sum(bolts['x-position']) / len(bolts['x-position'])
        y = sum(bolts['y-position']) / len(bolts['y-position'])
        return [x,y]

def centroid_and_scheme(bolt, force):
        centroid = calculate_centroid(inpt.bolt_info)
        sktch.redraw(inpt.bolt_info, inpt.force_info, centroid)

def create_buttons(sktch, inpt):
        button_id = ['draw', 'calculate', 'genrate report', 'multiple reports']
        functions = [lambda: centroid_and_scheme(inpt.bolt_info, inpt.force_info), 
                    lambda: print(inpt.bolt_info),
                    sktch.idk, 
                    sktch.idk]

        for index, id in enumerate(button_id):
            tkinter.Button(inpt.buttons, text=id, command=functions[index], width=15,
                        font=font[1], bg=bg, relief=relief).grid(row=index//2, 
                        column=index % 2, sticky='e'+'w', padx=2, pady=2)
                        
inpt = input_interface.UI(root, bg, font, sp_bolt, sp_force, dname)
sktch = scheme.Scheme(g, inpt, cw, ch)
create_buttons(sktch, inpt)


g.update()
g.mainloop()