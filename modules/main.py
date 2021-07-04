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
dname = r'{}'.format(os.path.realpath(__file__).replace('modules/main.py', ''))
# change the working directory if it is somewhere else
os.chdir(dname)

root = tkinter.Tk()
root.title('Eccentric Joint Analysis')

# general appearance options
bg = 'grey100'
root['bg'] = bg
ch = 400  # canvas height
cw = 400  # canvas width
relief = 'groove'
font = [('ms sans', '13'), ('ms sans', '11'), ('ms sans', '9'),
        ('ms sans', '7')]

err_lab = tkinter.Label(root, text='', font=font[1], fg='red', bg=bg)
err_lab.grid(row=0, column=1, pady=(10, 0))

g = tkinter.Canvas(root, width=cw, height=ch, bg=bg, highlightthickness=0)
g.grid(row=1, column=1, rowspan=2, sticky='s')

name_ent = tkinter.Entry(root,
                         font=font[3],
                         justify='center',
                         width=40,
                         borderwidth=0,
                         highlightthickness=1)
name_ent.grid(row=1, column=1, pady=(0, 150))


def calculate_centroid(bolts):
    out, xy = [], ['x-pos[mm]', 'y-pos[mm]']
    # calculate coordinate for x and y separately
    for i in range(2):
        numerator, denominator = 0, 0
        for j in range(len(bolts['x-pos[mm]'])):
            # expression taken form images/notes/vypocez_taziska
            Gj = bolts['E[MPa]'][j] / 2.6
            Aj = (bolts['diameter[mm]'][j]**2 * math.pi) / 4
            numerator += bolts[xy[i]][j] * Gj * Aj
            denominator += Gj * Aj
        out.append(numerator / denominator)
    return out


def redraw_scheme():
    # a tkinter button cannot have more than one fuctions bounded to it
    # try:
    centroid = calculate_centroid(table.bolt_info)
    sktch.redraw(table.bolt_info, table.force_info, centroid)
    # except:
    #     # if the user inputs wrong data manually
    #     err_lab.config(text='there are none or invalid geometry and/or force data')


def run_calculations():
    # a tkinter button cannot have more than one fuctions bounded to it
    # try:
    centroid = calculate_centroid(table.bolt_info)
    calc.calc_driver(centroid, table.force_moment)
    sktch.redraw(table.bolt_info, table.force_info, centroid, calc.sum_load)
    # except:
    #     # if the user inputs wrong data manually
    #     err_lab.config(text='there are none or invalid geometry and/or force data')


def create_buttons(sktch, inpt):
    button_id = [
        'draw', 'calculate', 'generate report', 'csv report',
        'fill in geometry', 'fill in load'
    ]
    functions = [
        redraw_scheme, run_calculations, rprt.gen_image_report,
        rprt.gen_cvs_table, lambda: table.load_data('bolt'),
        lambda: table.load_data('force')
    ]

    for index, id in enumerate(button_id):
        tkinter.Button(inpt.buttons,
                       text=id,
                       command=functions[index],
                       height=2,
                       font=font[1],
                       bg=bg,
                       relief=relief,
                       width=18).grid(row=index // 2,
                                      column=index % 2,
                                      sticky='e' + 'w',
                                      padx=2,
                                      pady=2)


# INPUT FORMAT ------------------------------------------
# sample bolt
sp_bolt = {
    'name': [''],
    'diameter[mm]': [''],
    'x-pos[mm]': [''],
    'y-pos[mm]': [''],
    'E[MPa]': [''],
    'Rms[MPa]': [''],
    't1[mm]': [''],
    't2[mm]': ['']
}

# sample force
sp_force = {
    'name': [''],
    'force[N]': [''],
    'x-pos[mm]': [''],
    'y-pos[mm]': [''],
    'angle[deg]': ['']
}

# CLASS INITIALIZAION --------------------------------------
table = input_interface.InputTable(sp_bolt, sp_force, dname)
inpt = input_interface.Interface(root, bg, font, err_lab, table)

sktch = scheme.Scheme(g, inpt, cw, ch, err_lab, font, dname, table)
calc = calc.Calculate(err_lab, table)
rprt = out.Report(calc, inpt, table, root, [cw, ch], name_ent, dname)

create_buttons(sktch, inpt)

g.update()
g.mainloop()
