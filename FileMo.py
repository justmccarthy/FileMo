import os, getpass, Interpreter
import tkinter as tk
from tkinter import *
from tkinter import filedialog
from tkinter import messagebox
# from tkfilebrowser import askopendirnames, askopenfilenames # not in python installations by default

class SampleApp(tk.Tk):

    def __init__(self):
        tk.Tk.__init__(self)

        self.files = []
        self.destFile = ""
        self.script = ""
        self.destFlag = False

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

    
    def get_page(self, page_name):
        return self.frames[page_name]
    
    # Raise specified frame and reset geometry
    def show_frame(self, page_name):
        '''Show a frame for the given page name'''
        for frame in self.frames.values():
            frame.grid_remove()
        frame = self.frames[page_name]
        frame.grid()
        frame.tkraise()
        frame.winfo_toplevel().geometry("")
        frame.update_idletasks()
        x = (frame.winfo_screenwidth() - frame.winfo_reqwidth()) / 2
        y = (frame.winfo_screenheight() - frame.winfo_reqheight()) / 3
        self.geometry("+{}+{}".format(int(x), int(y)))

# Frame for selecting files to be sorted
class StartPage(tk.Frame):

    def __init__(self, parent, controller):
        tk.Frame.__init__(self, parent)
        self.controller = controller

        f1 = tk.Frame(self)
        f2 = tk.Frame(self)
        f3 = tk.Frame(self)

        self.grid_rowconfigure(0, weight=0)
        self.grid_rowconfigure(1, weight=1)
        self.grid_rowconfigure(2, weight=0)
        
        self.grid_columnconfigure(0, weight=0)
        self.grid_columnconfigure(1, weight=1)
        self.grid_columnconfigure(2, weight=0)

        f3.grid_rowconfigure(0, weight=1)

        f3.grid_columnconfigure(0, weight=1)


        label = tk.Label(self, text="Select files to be sorted")
        label.grid(row=0, column=1, sticky = "s")

        # Add multiselected delete: add back (selectmode="multiple",)
        self.selected_list = tk.Listbox(f3, bg='#ffffff', width = 40, height = 30)
        self.selected_list.grid(row = 0, column = 0, sticky= "nsew")

        file_button = tk.Button(f1, text="Select File(s)",
                                command=self.addFiles)
        file_button.grid(row=0, column=0, pady = 10)

        file_button = tk.Button(f1, text="Select Folder",
                                command=self.addFolders)
        file_button.grid(row=1, column=0, pady = 10)

        file_button = tk.Button(f2, text="Remove Selected",
                                command=self.removeFile)
        file_button.grid(row=0, column=0, pady = 10)

        file_button = tk.Button(f2, text="Clear List",
                                command=self.clearFiles)
        file_button.grid(row=1, column=0, pady = 10)

        next_button = tk.Button(self, text="Next",
                                command=lambda: controller.show_frame("CodePage"))
        next_button.grid(row=2, column=1, pady = 10)

        f1.grid(row=1, column=0, padx = 10)
        f2.grid(row=1, column=2, padx = 10, sticky = "e")
        f3.grid(row=1, column=1, sticky = "nsew")

        label = tk.Label(self, text="")
        #label.pack

    # Select individual files to be sorted
    def addFiles(self):
        user = getpass.getuser()
        filelist = tk.filedialog.askopenfilename(initialdir='C:/Users/%s' % user, multiple=True)
        for filename in filelist:
            if filename not in self.controller.files:
                try:
                    self.selected_list.insert('end', (filename))
                    self.controller.files.append(filename)
                except:
                    print("could not add: " + filename)

    # Select folders to be sorted
    def addFolders(self):
        user = getpass.getuser().lower()
        folder = filedialog.askdirectory(initialdir='C:/Users/' + user)
        if (folder == ''):
            return
        confirm = messagebox.askyesno('Confirm', 'Are you sure you want to sort from: ' + folder + '?')
        if not confirm:
            return
        self.addFolder(folder)

    # add folder to list calls self recursively for sub folders
    def addFolder(self, folder):
        try:
            filelist = os.scandir(folder)
        except:
            messagebox.showwarning("Access Denied", "Can't Access " + folder)
            return
        for filename in filelist:
            if os.path.isfile(folder + '/' + filename.name):
                if filename not in self.controller.files:
                    try:
                        self.selected_list.insert('end', (folder + '/' + filename.name))
                        self.controller.files.append(folder + '/' + filename.name)
                    except:
                        print("could not add: " + folder + '/' + filename.name)
            elif os.path.isdir(folder + '/' + filename.name):
                self.addFolder(folder + '/' + filename.name)

    # Remove selected files
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

    def clearFiles(self):
        self.controller.files.clear()
        try:
            self.selected_list.delete(0,'end')
        except:
            print("Error removing file from files list")


# Frame for managing scripts and executing code
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

        load_button = tk.Button(left_frame, text="Load Script", command=self.loadScript)
        load_button.grid(row=2, sticky='s', pady=10)

        save_button = tk.Button(left_frame, text="Save Script", command=self.saveScript)
        save_button.grid(row=3, sticky='s', pady=10)

        back_button = tk.Button(left_frame, text="Back",
                           command=lambda: controller.show_frame("StartPage"))
        back_button.grid(row=4, sticky='s', pady=(10,0))

        left_frame.grid_rowconfigure(1, weight=1)
        left_frame.grid_columnconfigure(0, weight=1)

        
        # Right Frame
        code_label = tk.Label(right_frame, text="Your code:")
        code_label.grid(row = 0, column = 0, sticky='w')

        self.code = tk.Text(right_frame, width=70, height=30, bg='#ffffff')
        self.code.grid(row=1, column=0, columnspan=4, rowspan=3, sticky='nsew', pady=(0,10))

        dir_button = tk.Button(right_frame, text="Destination Directory", command=self.getDestDir)
        dir_button.grid(row=4, column=0, sticky='ew', padx = (0, 10))

        self.saveDes = BooleanVar()
        self.saveDes.set(False)

        self.saveCode = BooleanVar()
        self.saveCode.set(False)
        
        self.cbDes = Checkbutton(right_frame, text="Remember Destination Directory", variable = self.saveDes)
        self.cbDes.grid(row = 5, column = 0, sticky = 'w')
        self.cbDes.select()

        self.cbCode = Checkbutton(right_frame, text="Remember Written Code", variable = self.saveCode)
        self.cbCode.grid(row = 0, column = 2, sticky ='e', columnspan = 2)
        self.cbCode.select()
        
        self.dest_entry = tk.Entry(right_frame, textvariable=self.controller.destFile, state='readonly', bg='#ffffff')
        self.dest_entry.grid(row=4, column=1, columnspan=2, sticky='we')

        run_button = tk.Button(right_frame, text="Run Script", command = self.runScript)
        run_button.grid(row=4, column=3, rowspan=2, sticky='ns', padx = (10, 0))

        right_frame.grid_rowconfigure(1, weight=3)
        right_frame.grid_columnconfigure(0, weight=1)
        right_frame.grid_columnconfigure(1, weight=2)
        right_frame.grid_columnconfigure(2, weight=2)


    # Set destination directoy
    def getDestDir(self):
        user = getpass.getuser()
        self.controller.destFile = filedialog.askdirectory(initialdir='C:/Users/%s' % user, title = "Select Destination Dir")
        self.dest_entry.configure(state="normal")
        self.dest_entry.delete(0, 'end')
        self.dest_entry.insert(0, self.controller.destFile)
        self.dest_entry.configure(state="readonly")
        # Check if destination selection was canceled
        if self.controller.destFile:
            return
        else:
            self.controller.destFlag = True

    # Save script as a local file
    def saveScript(self):
        try:
            path = os.getcwd() + "\scripts"
            filename = filedialog.asksaveasfilename(initialdir = path, initialfile = 'script.txt', title = "Select save file", filetypes = (("text files", "*.txt"), ("all files", "*.*")))
            with open(filename, 'w') as f:
                scriptCode = self.code.get(0.0, 'end')
                f.write(scriptCode)
                f.close()
        except FileNotFoundError:
            print("File selection was canceled")
            return

    # Load local script file
    def loadScript(self):
        try:
            path = os.getcwd() + "\scripts"
            self.code.delete(0.0, 'end')
            filename = filedialog.askopenfilename(initialdir = path, title = "Select script to load", filetypes = (("text files", "*.txt"), ("all files", "*.*")))
            with open(filename, 'r') as f:
                scriptCode = f.read()
                self.code.insert(0.0, scriptCode)
                f.close()
        except FileNotFoundError:
            print("File selection was canceled")
            return

    # Execute script
    def runScript(self):
        self.controller.script = str(self.code.get(1.0, 'end'))
        if self.controller.script.isspace():
            print("No code has been writen") # Added popup error message for this
        elif self.controller.destFile == '':
            print("A destination has not been set") # Added popup error message for this
        elif len(self.controller.files) == 0:
            print("Select some files to be sorted")  # Added popup error message for this
        else:
            Process = Interpreter.LexicalAnalyzer(self.controller.destFile, self.controller.files)
            Script = self.code.get(0.0, tk.END)  # get all text in box
            Process.parseTokens(Script)
            self.controller.show_frame("StartPage")
            clr = self.controller.get_page("StartPage")
            clr.clearFiles()
            if (self.saveCode.get() == False):
                self.code.delete(1.0, "end")
            if (self.saveDes.get() == False):
                self.controller.destFile = ""
                self.dest_entry.configure(state="normal")
                self.dest_entry.delete(0, 'end')
                self.dest_entry.insert(0, self.controller.destFile)
                self.dest_entry.configure(state="readonly")
            



if __name__ == "__main__":
    app = SampleApp()
    app.mainloop()
