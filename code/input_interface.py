from tkscrolledframe import ScrolledFrame
import tkinter
import os


class UI:
    """ this class creates interface where the user can input data"""

    def __init__(self, root, bg, font, bolt, force, dname):
        self.bg = bg
        self.font = font
        self.path = dname
        self.relief = 'groove'
        self.bolt_info = bolt
        self.force_info = force

        # --LABELFRAMES------------------------------------------------------------------
        self.inputs = tkinter.LabelFrame(
            root, text='inputs', relief='solid', bg=self.bg)
        self.inputs.grid(row=0, column=0, rowspan=2, sticky='n'+'e'+'w', ipady=5, ipadx=5, padx=5)

        self.table = tkinter.LabelFrame(
            self.inputs, text='input_tables', relief='groove', bg=self.bg)
        self.table.grid(row=0, column=0, sticky='e'+'w')

        self.object1 = tkinter.LabelFrame(
            self.inputs, text='connection material 0', relief='groove', bg=self.bg)
        self.object1.grid(row=1, column=0, sticky='n'+'e'+'w'+'s')

        self.object2 = tkinter.LabelFrame(
            self.inputs, text='connection material 1', relief='groove', bg=self.bg)
        self.object2.grid(row=2, column=0, sticky='n'+'e'+'w'+'s')

        self.buttons = tkinter.LabelFrame(
            text='buttons', relief='solid', bg=self.bg)
        self.buttons.grid(row=2, column=0, sticky='n'+'e'+'w', padx=5)

        tkinter.Button(self.table, text='edit geometry data', command=lambda: self.input_table('bolt'),
                       font=self.font[1], bg=self.bg, relief=self.relief).pack(fill='x')

        tkinter.Button(self.table, text='edit stress data', command=lambda: self.input_table('force'),
                       font=self.font[1], bg=self.bg, relief=self.relief).pack(fill='x')

        self.object1_ui()
        self.object2_ui()

    def choose_width(self, idx, width):
        """returns desired width for an entry box
        the ones containing name should be wider"""

        if idx == 0: return width[1]
        else: return width[0]


    # --INPUT TABLES------------------------------------------------
    def input_table(self, table_type):
        """function responsible for generating the input table
        for both force and bolt data
        
        it includes all the secondary functions for table like add
        submit or remove"""

        nroot = tkinter.Tk()
        nroot.title('input table')
        entrys_id = []
        entry_width = [12, 15]

        if table_type == 'bolt':
            width, height = 860, 250
            info = self.bolt_info
        else:
            width, height = 600, 250
            info = self.force_info

        entrys = list(info.keys())
        samplekey = list(info.keys())[0]
        entrys_id = [['' for _ in range(len(entrys))]
                     for _ in range(len(info[samplekey]))]

        err_lab = tkinter.Label(nroot, text='', fg='red')
        err_lab.grid(row=5, column=0, columnspan=3, sticky='n'+'s'+'e'+'w')
        err_lab.grid_remove()
        num_rows = 1 if not info[samplekey] else len(info[samplekey])

        # Create a ScrolledFrame widget and buttons
        scrll_frm = ScrolledFrame(nroot, width=width, height=height)
        scrll_frm.grid(row=0, column=0, columnspan=3)

        # Bind the arrow keys and scroll wheel
        scrll_frm.bind_arrow_keys(nroot)
        scrll_frm.bind_scroll_wheel(nroot)

        # Create a frame within the ScrolledFrame
        inner_frame = scrll_frm.display_widget(tkinter.Frame)

        def add_row():
            nonlocal num_rows

            err_lab.grid_forget()
            entrys_id.append(['' for _ in range(len(entrys))])

            for column in range(len(entrys)):
                entrys_id[num_rows][column] = tkinter.Entry(
                    inner_frame, width=self.choose_width(column, entry_width), borderwidth=2, relief="groove", justify="center")
                entrys_id[num_rows][column].grid(
                    row=num_rows+1, column=column, padx=0, pady=0)
            num_rows += 1


        def remove_row():
            nonlocal num_rows

            err_lab.grid_forget()
            if num_rows > 1:
                for column in range(len(entrys)):
                    entrys_id[num_rows-1][column].grid_remove()
                entrys_id.pop()
                num_rows -= 1

        def submit_data():
            nonlocal num_rows

            err_lab.grid_remove()
            ypos = entrys.index('y-position')
            xpos = entrys.index('x-position')

            for column in range(len(entrys)):
                info[entrys[column]] = []
                for row in range(num_rows):
                    value = entrys_id[row][column].get()

                    # save name as string others as float
                    if column != 0: info[entrys[column]].append(float(value))
                    else: info[entrys[column]].append(value)
                    
                    # check if all entries are filled
                    if not value:
                        err_lab.grid(row=3, column=0, sticky='n'+'s'+'e'+'w')
                        err_lab.config(text='all entrys must be filled')
                        return
                    # checking if two positions of bolt are the same
                    # if column == ypos:
                    #     value2 = entrys_id[row][xpos].get()
                    #     lx = [i for i, v in enumerate(
                    #         info[entrys[xpos]]) if v == value2]
                    #     ly = [i for i, v in enumerate(
                    #         info[entrys[ypos]]) if v == value]
                    #     rng = min(len(lx), len(ly))
                    #     for i in range(rng):
                    #         if lx[i] == ly[i]:
                    #             err_lab.grid(row=3, column=0,
                    #                          sticky='n'+'s'+'e'+'w')
                    #             err_lab.config(
                    #                 text='two positions of bolt are the same')
                    #             return
            if table_type == 'bolt':
                self.bolt_info = info.copy()
            else:
                self.force_info = info.copy()
            return 'ok'

        def select_entry(event):
            id = nroot.focus_get()
            for i in range(len(entrys_id)):
                if id in entrys_id[i]:
                    idx = entrys_id[i].index(id)
                    if idx+1 == len(entrys):  # if forcus is on last entry in column
                        if i != len(entrys_id)-1:  # if focus is NOT in last row
                            entrys_id[i+1][0].focus()
                            if entrys_id[i+1][0].get() == '':
                                entrys_id[i+1][0].insert(0,
                                                         info[entrys[0]][i])
                        else:
                            if submit_data() == 'ok':  # if all entrys are filled
                                add_row()
                                entrys_id[i+1][0].focus()
                                entrys_id[i+1][0].delete(0, 'end')
                                entrys_id[i+1][0].insert(0,
                                                         info[entrys[0]][i])
                    else:
                        entrys_id[i][idx+1].focus()
                        if i != 0 and 2 < idx+1:
                            if entrys_id[i][idx+1].get() == '':
                                entrys_id[i][idx+1].delete(0, 'end')
                                entrys_id[i][idx +
                                             1].insert(0, info[entrys[idx+1]][i-1])
                    break

        # generate initial table
        for row in range(num_rows):
            for column in range(len(entrys)):
                if row == 0:
                    tkinter.Label(inner_frame, text=entrys[column], relief="flat", justify="center").grid(
                        row=row, column=column, padx=0, pady=0)

                if not info[samplekey]:
                    add_row()

                if info[samplekey] and row < num_rows:
                    entrys_id[row][column] = tkinter.Entry(
                        inner_frame, width=self.choose_width(column, entry_width), borderwidth=2, 
                        relief="groove", justify="center")
                    entrys_id[row][column].grid(
                        row=row+1, column=column, padx=0, pady=0)
                    # inserting default values
                    entrys_id[row][column].insert(
                        0, info[entrys[column]][row])
        
        # display image of axis orientation
        if table_type == 'force':
            img = tkinter.PhotoImage(master=nroot, file=os.path.join(self.path, r'images/angle_orientation.png'))
            img = img.subsample(4, 4)
            img_lab = tkinter.Label(nroot, image=img)
            img_lab.grid(row=0, column=3, rowspan=3)

            tkinter.Label(nroot, text='momet sily[N/mm]').grid(row=1, column=0, columnspan=2)
            tkinter.Entry(nroot, width=20, justify='center').grid(row=1, column=2, sticky='E'+'W')

        tkinter.Button(nroot, text='add row', command=lambda: add_row()).grid(
            row=2, column=0, sticky='n'+'s'+'e'+'w')
        tkinter.Button(nroot, text='delete row', command=lambda: remove_row()).grid(
            row=2, column=1, sticky='n'+'s'+'e'+'w')
        tkinter.Button(nroot, text='submit data', command=submit_data).grid(
            row=2, column=2, sticky='n'+'s'+'e'+'w')
        nroot.bind('<Tab>', select_entry)
        nroot.mainloop()

    # MATERIAL INFORMATION -------------------------------------------
    def object1_ui(self):
        entry_id = ['t', 'name']
        object1_entry = {}

        for index, id in enumerate(entry_id):
            tkinter.Label(self.object1, text=id, font=self.font[1],
                          bg=self.bg).grid(row=index, column=0, padx=55)
            object1_entry[id] = tkinter.Entry(
                self.object1, justify='center', font=self.font[1], relief=self.relief, width=20)
            object1_entry[id].grid(row=index, column=1, sticky='e')

    def object2_ui(self):
        entry_id = ['t', 'name']
        object2_entry = {}

        for index, id in enumerate(entry_id):
            tkinter.Label(self.object2, text=id, font=self.font[1],
                          bg=self.bg).grid(row=index, column=0, padx=55)
            object2_entry[id] = tkinter.Entry(
                self.object2, justify='center', font=self.font[1], relief=self.relief, width=20)
            object2_entry[id].grid(row=index, column=1, sticky='e')


    # UPDATING DATA ---------------------------------------------------
    def update_data(self, inpt_type):
        test_data = tkinter.filedialog.askopenfile(mode='r+')
        if inpt_type == 'bolt': data = self.bolt_info
        else: data = self.force_info

        # remove old data from the dictionary
        for x in list(data.keys()): data[x].clear()

        while True:
            line = test_data.readline()
            if line == '': break

            line = line.strip().split('\t')
            line = [float(d.replace(',', '.')) if i!= 0 else d for i, d in enumerate(line)]

            # append the files to the dictionary
            for idx, column in enumerate(list(data.keys())): data[column].append(line[idx])
