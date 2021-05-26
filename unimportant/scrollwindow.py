import tkinter

nroot = tkinter.Tk()

scrollbar = tkinter.Scrollbar(nroot)
scrollbar.pack(side='right', fill='y')

inputs = tkinter.LabelFrame(nroot, text='inputs', relief='solid')
inputs.pack()
        
#listbox = tkinter.Listbox(nroot, yscrollcommand=scrollbar.set)
for i in range(10):
    tkinter.Entry(inputs).pack()
    
#listbox.pack(side='left', fill='both')

#scrollbar.config(command=inputs.yview)

nroot.mainloop()