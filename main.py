# general libraries
import tkinter.filedialog
import pyautogui
import tkinter
import math
import os

# including local files
import input_interface
import sketch

# get a path to this file
dname = r'{}'.format(os.path.realpath(__file__).strip('main.py'))
os.chdir(dname)  # working directory

root = tkinter.Tk()
root.title('bounded_bolts')

# general appearance options
bg = 'grey99'
root['bg'] = bg
ch = 420  # canvas height
cw = 450  # canvas width
relief = 'groove'
font = [('ms sans', '13'), ('ms sans', '11'), ('ms sans', '9')]


g = tkinter.Canvas(root, width=cw, height=ch, bg='grey80', highlightthickness=0)  # 1000x600
g.grid(row=0, column=1, rowspan=2, sticky='s')


sp_bolt = {'diameter': [2, 2, 2, 2],  # sample bolt data
        'x-position': [0, 2, 0, 2],
        'y-position': [0, 0, 2, 2],
        'E': [10, 10, 10, 10],
        'Rm': [10, 10, 10, 10],
        't': [1, 1, 1, 1],
        't2': [2, 2, 2, 2]}

sp_force = {'size': [40, 40, 40],  # sample force data
            'x-position': [1, 1.5, 2],
            'y-position': [1.5, 1.5, 2],
            'angle': [90, 180, 270]}


def calculate_centroid(bolts):
        x = sum(bolts['x-position']) / len(bolts['x-position'])
        y = sum(bolts['y-position']) / len(bolts['y-position'])
        return [x,y]


def create_buttons(sktch, inpt):
        button_id = ['draw', 'calculate', 'genrate report', 'multiple reports']
        functions = [lambda: sktch.redraw(inpt.bolt_info, inpt.force_info, calculate_centroid(inpt.bolt_info)), 
                    lambda: print(inpt.bolt_info),
                    sktch.idk, 
                    sktch.idk]

        for index, id in enumerate(button_id):
            tkinter.Button(inpt.buttons, text=id, command=functions[index], width=15,
                        font=font[1], bg=bg, relief=relief).grid(row=index//2, 
                        column=index % 2, sticky='e'+'w', padx=2, pady=2)
                        
inpt = input_interface.UI(root, bg, font, sp_bolt, sp_force)
sktch = sketch.Sketch(g, inpt, cw, ch)
create_buttons(sktch, inpt)
calculate_centroid(inpt.bolt_info)



g.update()
g.mainloop()