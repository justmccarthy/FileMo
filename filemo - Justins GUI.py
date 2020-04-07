import os, getpass, re, Interpreter
import tkinter as tk
from tkinter import filedialog
from tkfilebrowser import askopendirnames

class SampleApp(tk.Tk):

    def __init__(self):
        tk.Tk.__init__(self)

        self.files = []

        container = tk.Frame(self)
        container.pack(side="top", fill="both", expand=True)
        container.grid_rowconfigure(0, weight=1)
        container.grid_columnconfigure(0, weight=1)
        container.tk_setPalette(background='#e6e6e6')
        container.winfo_toplevel().title("FileMo")

        self.frames = {}
        for F in (StartPage, CodePage):
            page_name = F.__name__
            frame = F(parent=container, controller=self)
            self.frames[page_name] = frame

            frame.grid(row=0, column=0, sticky="nsew")

        self.show_frame("StartPage")

    def show_frame(self, page_name):
        '''Show a frame for the given page name'''
        for frame in self.frames.values():
            frame.grid_remove()
        frame = self.frames[page_name]
        frame.grid()
        frame.tkraise()
        frame.update_idletasks()
        x = (frame.winfo_screenwidth() - frame.winfo_reqwidth()) / 2
        y = (frame.winfo_screenheight() - frame.winfo_reqheight()) / 3
        self.geometry("+{}+{}".format(int(x), int(y)))


class StartPage(tk.Frame):

    def __init__(self, parent, controller):
        tk.Frame.__init__(self, parent)
        self.controller = controller

        label = tk.Label(self, text="This is the start page")
        label.pack(side="top", fill="x", pady=10)

        self.selected_list = tk.Listbox(self, selectmode="multiple", height=20, width=50, bg='#ffffff')
        self.selected_list.pack(padx=15, fill='both')

        file_button = tk.Button(self, text="Select folders",
                                command=self.openFolders)
        file_button.pack()

        #file_button = tk.Button(self, text="Select files",
        #                        command=self.openFiles)
        #ile_button.pack()

        file_button = tk.Button(self, text="Remove selected",
                                command=self.removeFile)
        file_button.pack()

        next_button = tk.Button(self, text="Next",
                                command=lambda: controller.show_frame("CodePage"))
        next_button.pack()

    def openFolders(self):
        #temp = askopendirnames()
        #self.controller.files = list(temp)
        user = getpass.getuser()  # gets username for default file path
        temp = filedialog.askdirectory(initialdir='C:/Users/%s' % user)
        self.controller.files.append(temp)
        for x in self.controller.files:
            self.selected_list.insert('end', x)

    def removeFile(self):
        selected = self.selected_list.curselection()
        try:
            value = self.selected_list.get(selected[0])
        except:
            print("No file is selected")
            return
        try:
            self.selected_list.delete(selected[0])
            self.controller.files.remove(value)
        except:
            print("Error removing file from files list")


class CodePage(tk.Frame):

    def __init__(self, parent, controller):
        tk.Frame.__init__(self, parent, width=450, height=50, pady=3)
        self.controller = controller

        # containers
        left_frame = tk.Frame(self, width=100, height=50, pady=10, padx=10)
        right_frame = tk.Frame(self, width=350, height=50, pady=10, padx=10)

        self.grid_rowconfigure(0, weight=1)
        self.grid_columnconfigure(0, weight=1)
        self.grid_columnconfigure(1, weight=3)

        left_frame.grid(row=0, column=0, sticky="nsew")
        right_frame.grid(row=0, column=1, sticky="nsew")


        # Left Frame
        cheat_label = tk.Label(left_frame, text="Cheat Sheet:")
        cheat_label.grid(sticky='w')

        cheat_sheet = tk.Text(left_frame, width=35, height=15, bg='#ffffff')
        cheat_sheet.grid(row=1, sticky='nsew', pady=(0,10))

        load_button = tk.Button(left_frame, text="Load Script", command=self.LoadScript)
        load_button.grid(row=2, sticky='s', pady=10)

        save_button = tk.Button(left_frame, text="Save Script", command=self.SaveScript)
        save_button.grid(row=3, sticky='s', pady=10)

        back_button = tk.Button(left_frame, text="Back",
                           command=lambda: controller.show_frame("StartPage"))
        back_button.grid(row=4, sticky='s', pady=(10,0))

        left_frame.grid_rowconfigure(1, weight=1)
        left_frame.grid_columnconfigure(0, weight=1)

        
        # Right Frame
        code_label = tk.Label(right_frame, text="Your code:")
        code_label.grid(sticky='w')

        self.code = tk.Text(right_frame, width=70, height=30, bg='#ffffff')
        self.code.grid(row=1, column=0, columnspan=4, rowspan=3, sticky='nsew', pady=(0,10))

        dir_button = tk.Button(right_frame, text="Destination Directory", command=self.SelectToDirectory)
        dir_button.grid(row=4, column=0, sticky='ew')

        self.dest_entry = tk.Entry(right_frame, bg='#ffffff', font=("Arial", 14))
        self.dest_entry.grid(row=4, column=1, columnspan=2, sticky='we')

        run_button = tk.Button(right_frame, text="Run Script", command=self.doScript)
        run_button.grid(row=4, column=3, sticky='se')

        right_frame.grid_rowconfigure(1, weight=3)
        right_frame.grid_columnconfigure(0, weight=1)
        right_frame.grid_columnconfigure(1, weight=2)
        right_frame.grid_columnconfigure(2, weight=2)

    def SaveScript(self):  # opens Save file dialog box and saves(overwrites) contents of the script window into file
        self.path = os.getcwd() + "\scripts"
        print("need to write save function")
        filename = filedialog.asksaveasfilename(initialdir=self.path, title="Select file", filetypes=(("text file", "*.txt"), ("all files", "*.*")))
        try:
            with open(filename, 'w') as f:
                text = self.code.get(0.0, tk.END)
                f.write(text)
                f.close()
        except:
            print("File could not be saved")

    def LoadScript(self):  # opens Open file dialog box and loads(overwrites) contents of file into the script window
        self.path = os.getcwd() + "\scripts"
        print("need to write Load function")
        self.code.delete(0.0, tk.END)
        filename = filedialog.askopenfilename(initialdir=self.path, title="Save file", filetypes=((".Txt", "*.txt"), ("all files", "*.*")))  # show an "Open" dialog box and return the path to the selected file
        try:
            with open(filename, 'r') as f:
                text = f.read()
                self.code.insert(0.0, text)
                f.close()
        except:
            print("File could not be loaded")

    def SelectToDirectory(self):# opens a directory selection dialog and sets sortDest
        user = getpass.getuser()  # gets username for default file path
        filename = filedialog.askdirectory(initialdir='C:/Users/%s' % user)  # show an "Open" dialog box and return the path to the selected file
        # print(filename) # debug
        if (filename != ""): #
            self.dest_entry.delete(0, tk.END) # delete contents of text window
            self.dest_entry.insert(0, filename) # print to sortDest text window
        else:
            print("dir not selected") # debug

    def doScript(self):  #
        Script = self.code.get(0.0, tk.END)  # get all text in box
        Dest = self.dest_entry.get()
        GoodToGo = True
        if not (re.match(r'[A-z]\:(\\[^\'"/?*|]+)*',Dest)):
            GoodToGo[0] = False
            print("select a destination")
        if (len(self.controller.files) == 0):
            GoodToGo[1] = False
            print("select some files")
        if (Script == ""):
            GoodToGo[1] = False
            print("write/load a script")
        if GoodToGo == True:
            Process = Interpreter.LexicalAnalyzer(Dest, self.controller.files)
            Process.parseTokens(Script)
        return

if __name__ == "__main__":
    app = SampleApp()
    app.mainloop()