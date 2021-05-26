import tkinter 
from tkscrolledframe import ScrolledFrame

nroot = tkinter.Tk()
entrys_id = []
bolt_info = {'radius':[1], 'x-position':[1], 'y-position':[1], 'E':[1], 'Rm':[1]} # toto bude global

# Create a ScrolledFrame widget and buttons
scrll_frm = ScrolledFrame(nroot, width=480, height=250)
scrll_frm.grid(row=0, column=0, rowspan=3)

# Bind the arrow keys and scroll wheel
scrll_frm.bind_arrow_keys(nroot)
scrll_frm.bind_scroll_wheel(nroot)

# Create a frame within the ScrolledFrame
inner_frame = scrll_frm.display_widget(tkinter.Frame)
entrys = ['radius', 'x-position', 'y-position', 'E', 'Rm']

# all list will have the same length this is just representation of all lists
samplekey = list(bolt_info.keys())[0]
#if not entrys_id[samplekey]:
entrys_id = [['' for _ in range(len(entrys))] for _ in range(len(bolt_info[samplekey])+1)]

err = ''
num_rows = 1 if not bolt_info else len(bolt_info[samplekey])
for row in range(num_rows):
    for column in range(len(entrys)):
        if row == 0:
            tkinter.Label(inner_frame, text=entrys[column], relief="flat", justify="center").grid(row=row, column=column, padx=0, pady=0)
       
        if bolt_info[samplekey]:
            entrys_id[row][column] = tkinter.Entry(inner_frame, width=15, borderwidth=2, relief="groove", justify="center")
            entrys_id[row][column].grid(row=row+1, column=column, padx=0, pady=0)
            entrys_id[row][column].insert(0, bolt_info[entrys[column]][row])

        if row == num_rows-1:
            entrys_id[row+1][column] = tkinter.Entry(inner_frame, width=15, borderwidth=2, relief="groove", justify="center")
            entrys_id[row+1][column].grid(row=row+2, column=column, padx=0, pady=0)

def add_row():
    global num_rows, err
    if err != '': err.grid_forget() 
    entrys_id.append(['' for _ in range(len(entrys))])
    num_rows += 1 
    
    for column in range(len(entrys)):
        entrys_id[num_rows][column] = tkinter.Entry(inner_frame, width=15, borderwidth=2, relief="groove", justify="center")
        entrys_id[num_rows][column].grid(row=num_rows+1, column=column, padx=0, pady=0)


def remove_row():
    global num_rows, err
    if err != '': err.grid_forget()
    if num_rows > 0:
        for column in range(len(entrys)):
            entrys_id[num_rows][column].grid_remove()
        entrys_id.pop()
        num_rows -= 1 


def submit_data():
    global num_rows, err
    stop = 0
    if err != '': err.grid_forget()

    for column in range(len(entrys)):
        if stop == 1:
            break
        bolt_info[entrys[column]] = []
        for row in range(num_rows+1):
            value = entrys_id[row][column].get()
            if not value:
                err = tkinter.Label(nroot, text='all entrys must be filled', fg='red')
                err.grid(row=3, column=0, sticky='n'+'s'+'e'+'w')
                stop = 1
                break
            else:
                bolt_info[entrys[column]].append(value)
    print(bolt_info)
            
tkinter.Button(nroot, text='add row', command=lambda: add_row()).grid(row=0, column=1, sticky='n'+'s'+'e'+'w')
tkinter.Button(nroot, text='delete row', command=lambda: remove_row()).grid(row=1, column=1, sticky='n'+'s'+'e'+'w')
tkinter.Button(nroot, text='submit data', command=lambda: submit_data()).grid(row=2, column=1, sticky='n'+'s'+'e'+'w')


# Start Tk's event loop
nroot.mainloop()

# chces error message ak nie je vsetko vyplnene