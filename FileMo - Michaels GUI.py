import Interpreter
import getpass, os
from tkinter import *
from tkinter.filedialog import *

class MainGui():
    # class var
    sortDest = "\0"
    sortFiles = []
    DestSet = False
    # Note: everything with a self. is also a class var and requires self. to access

    def __init__(self, master):
        # initialize
        self.user = getpass.getuser() # gets username for use in default file path
        self.path = os.getcwd() # Gets current directory path for save / load
        self.path = self.path + "\scripts" # save / load to script dir

        # window setup
        master.grid_rowconfigure(0, weight=1)
        master.grid_rowconfigure(99, weight=1)
        master.grid_columnconfigure(0, weight=1)
        master.grid_columnconfigure(99, weight=1)
        master.title("FileMo")  # set window title

        # Spacers
        Label(master, text="").grid(row=0, column=0, padx=20) # creates some space above and left
        Label(master, text="").grid(row=99, column=99, padx=20) # creates some space below and right
        Label(master, text="").grid(row=4, column=0, padx=20) # creates some between script window and buttons
        Label(master, text="").grid(row=0, column=2, padx=20) # creates some between Cheat sheet and script window

        # Script input window
        Label(master, text="Source Code Input:").grid(row=2, column=3, sticky=W, )  # create label for window
        self.ScriptEntry = Text(master, width=120, height=15)
        self.ScriptEntry.grid(row=3, column=3, columnspan=2, sticky=E)  # create input box, set size

        # Selected Directory Window
        self.DestDirEntry = Text(master, width=80, height=1)  # create input box, set size
        self.DestDirEntry.grid(row=1, column=4, columnspan=2, sticky=E)
        self.DestDirEntry.insert(0.0, "This Box is read only, use the \"Sort To:\" button to set the sort destination")
        self.DestDirEntry.config(state=DISABLED) # make read only

        # Buttons
        Button(master, width=20, text="Run Script", command=self.doScript).grid(row=5, column=4, sticky=E)  # run button
        Button(master, width=13, text="Sort To:", command=self.SelectToDirectory).grid(row=1, column=3, sticky=E) # select dir
        Button(master, width=50, text="File Selector", command=self.SelectGui).grid(row=1, column=1, sticky=N) # file selector
        Button(master, width=20, text="Save Script", command=self.SaveScript).grid(row=5, column=3, sticky=W)  # save button
        Button(master, width=20, text="Load Script", command=self.LoadScript).grid(row=5, column=3, sticky=E)  # load button

        # cheatsheet window
        Label(master, text="Cheat Sheet:").grid(row=2, column=1, sticky=W, )  # create label for window
        self.CheatWindow = Text(master, width=50, height=18).grid(row=3, column=1, rowspan=3, sticky=E)  # create input box, set size
        #todo: fill sheet with a cheats
        return

    def doScript(self):  #
        strin = self.ScriptEntry.get(0.0, END)  # get all text in box
        Process = Interpreter.LexicalAnalyzer(self.sortDest, self.sortFiles)
        Process.parseTokens(strin)
        return

    def SelectToDirectory(self):# opens a directory selection dialog and sets sortDest
        user = getpass.getuser()  # gets username for default file path
        filename = askdirectory(initialdir='C:/Users/%s' % user)  # show an "Open" dialog box and return the path to the selected file
        # print(filename) # debug
        if (filename != ""): #
            # print("dir selected") # debug
            self.DestSet = True # set destination as selected
            self.sortDest = filename # set the destination
            self.DestDirEntry.config(state=NORMAL) # make Directory Display writable
            self.DestDirEntry.delete(0.0, END) # delete contents of text window
            self.DestDirEntry.insert(0.0, filename) # print to sortDest text window
            self.DestDirEntry.config(state=DISABLED) # make Directory Display read only
        else:
            print("dir not selected") # debug
            #todo: add warning

    def SaveScript(self): # opens Save file dialog box and saves(overwrites) contents of the script window into file
        print("need to write save function")
        filename = asksaveasfilename(initialdir=self.path, title = "Select file",filetypes = (("text file","*.txt"),("all files","*.*"))) #todo: figure out how this works
        with open(filename, 'w') as f:
            text = self.ScriptEntry.get(0.0, END)
            f.write(text)

            f.close()


    def LoadScript(self): # opens Open file dialog box and loads(overwrites) contents of file into the script window
        print("need to write Load function")
        self.ScriptEntry.delete(0.0, END)
        filename = askopenfilename(initialdir=self.path, title = "Save file",filetypes = ((".Txt","*.txt"),("all files","*.*")))  # show an "Open" dialog box and return the path to the selected file
        with open(filename, 'r') as f:
            text = f.read()
            self.ScriptEntry.insert("insert linestart", text)
            f.close()
    # File Select widow---------------------------------------------------------------
    def SelectGui(self): # creates a file selection and display window # not final selector, will improve later(probably)

        # window setup
        selgui = Toplevel(self.master)
        selgui.wm_title("File Select") #window name
        selgui.grab_set()  # prevent user from interacting from main window while open

        # spacers
        Label(selgui, text="").grid(row=0, column=0, padx=20) # create space above List
        Label(selgui, text="").grid(row=5, column=4, padx=20) # create space below buttons

        # selected veiw
        self.list = Listbox(selgui, width=80, height=20) # create listbox
        self.list.grid(row=1, column=1) # set listbox grid

        #buttons
        Button(selgui, width=35, text="Add File", command=self.FileSelect).grid(row=2, column=1, sticky=W)  # create addfile button
        Button(selgui, width=35, text="Add Folder", command=self.DirSelect).grid(row=2, column=1, sticky=E)  # create adddir button
        Button(selgui, width=70, text="Remove Item", command=self.FileDeselect).grid(row=3, column=1, rowspan=2, sticky=N)  # create remove item button
        return

    def FileSelect(self): # opens a file selector dialog and adds item to list and display
        filename = askopenfilename(initialdir= 'C:/Users/%s' % self.user)  # shows a Open file dialog box and sets filename to the selected path
        self.sortFiles.append(filename) # add filename to end of sortFiles list
        self.list.insert(END, filename) # add filename to end of listbox

    def DirSelect(self): # opens a directory selection dialog and adds it to list and display (prompts user to add contents to list instead?)
        filename = askdirectory(initialdir='C:/Users/%s' % self.user) # shows a Open directory dialog box and sets filename to the selected path
        self.sortFiles.append(filename)  # add filename to end of sortFiles list
        self.list.insert(END, filename) # add filename to end of listbox

    def FileDeselect(self): # removes highlighted listbox item from display and sortFiles list
        sel = self.list.get(self.list.curselection()) # get name of selected item from listbox
        self.sortFiles.remove(sel) # remove item from sortFiles list
        self.list.delete(self.list.curselection()) # remove item from listbox

# runs GUI
root = Tk()
my_gui = MainGui(root)
root.mainloop()
