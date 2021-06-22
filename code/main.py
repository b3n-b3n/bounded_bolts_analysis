# libraries
import tkinter.filedialog
import tkinter
import math
import os

# including local files
import input_interface
import scheme
import out
import calc

# get a path to this file
dname = r'{}'.format(os.path.realpath(__file__).replace('code/main.py', ''))
# change the working directory if it is somewhere else
os.chdir(dname)

root = tkinter.Tk()
root.title('eccentric joints')

# general appearance options
bg = 'grey99'
root['bg'] = bg
ch = 400  # canvas height
cw = 400  # canvas width
relief = 'groove'
font = [('ms sans', '13'), ('ms sans', '11'), ('ms sans', '9'), ('ms sans', '7')]

err_lab = tkinter.Label(root, text='', font=font[1], fg='red', bg=bg)
err_lab.grid(row=0, column=1, pady=(10, 0))


g = tkinter.Canvas(root, width=cw, height=ch, bg='grey90', highlightthickness=0)
g.grid(row=1, column=1, rowspan=2, sticky='s')

tkinter.Entry(root, font=font[3], justify='center', width=40).grid(row=1, column=1, pady=(0, 150))


def calculate_centroid(bolts):
    out, xy = [], ['x-pos[mm]', 'y-pos[mm]']
    # calculate coordinate for x and y separately 
    for i in range(2):
        numerator, denominator = 0, 0
        for j in range(len(bolts['x-pos[mm]'])):
            # expression taken form images/notes/vypocez_taziska
            Gj = bolts['E[MPa]'][j]/2.6
            Aj = (bolts['diameter[mm]'][j]**2 * math.pi) / 4
            numerator += bolts[xy[i]][j] * Gj * Aj
            denominator += Gj * Aj
        out.append(numerator/denominator)
    return out


def redraw_scheme():
    # a tkinter button cannot have more than one fuctions bounded to it 
    # try:
    centroid = calculate_centroid(inpt.bolt_info)
    sktch.redraw(inpt.bolt_info, inpt.force_info, centroid)
    # except:
    #     # if the user inputs wrong data manually
    #     err_lab.config(text='there are none or invalid geometry and/or force data')


def run_calculations():
    # a tkinter button cannot have more than one fuctions bounded to it 
    # try:
    centroid = calculate_centroid(inpt.bolt_info)
    calc.calc_driver(centroid, inpt.force_moment)
    sktch.redraw(inpt.bolt_info, inpt.force_info, centroid, calc.sum_load)
    # except:
    #     # if the user inputs wrong data manually
    #     err_lab.config(text='there are none or invalid geometry and/or force data')


def create_buttons(sktch, inpt):
    button_id = ['draw', 'calculate', 
                'generate report', 'multiple reports',
                'fill in geometry', 'fill in load']
    functions = [redraw_scheme, run_calculations,
                rprt.gen_image_report, sktch.idk,
                lambda: inpt.update_data('bolt'), lambda: inpt.update_data('force')]

    for index, id in enumerate(button_id):
        tkinter.Button(inpt.buttons, text=id, command=functions[index], width=15,
                       font=font[1], bg=bg, relief=relief).grid(row=index//2,
                                                                column=index % 2, sticky='e'+'w', padx=2, pady=2)

# INPUT FORMAT ------------------------------------------
# sample bolt
sp_bolt = {'name': [''],
           'diameter[mm]': [''],
           'x-pos[mm]': [''],
           'y-pos[mm]': [''],
           'E[MPa]': [''],
           'Rm[MPa]': [''],
           't1[mm]': [''],
           't2[mm]': ['']}

# sample force
sp_force = {'name': [''],
            'force[N]': [''],
            'x-pos[mm]': [''],
            'y-pos[mm]': [''],
            'angle[deg]': ['']}

# CLASS INITIALIZAION --------------------------------------
inpt = input_interface.UI(root, bg, font, sp_bolt, sp_force, dname, err_lab)
sktch = scheme.Scheme(g, inpt, cw, ch, err_lab, font, dname, inpt)
calc = calc.Calculate(err_lab, inpt)
rprt = out.Report(calc, inpt, root, [cw, ch])

create_buttons(sktch, inpt)


g.update()
g.mainloop()
