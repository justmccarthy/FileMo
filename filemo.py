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


class StartPage(tk.Frame):

    def __init__(self, parent, controller):
        tk.Frame.__init__(self, parent)
        self.controller = controller

        label = tk.Label(self, text="This is the start page")
        label.pack(side="top", fill="x", pady=10)

        self.selected_list = tk.Listbox(self, selectmode="multiple", height=20, width=50, bg='#ffffff')
        self.selected_list.pack(padx=15, fill='both')

        file_button = tk.Button(self, text="Select files",
                                command=self.openFiles)
        file_button.pack()

        file_button = tk.Button(self, text="Remove selected",
                                command=self.removeFile)
        file_button.pack()

        next_button = tk.Button(self, text="Next",
                                command=lambda: controller.show_frame("CodePage"))
        next_button.pack()

    def openFiles(self):
        temp = askopendirnames()
        self.controller.files = list(temp)
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

        load_button = tk.Button(left_frame, text="Load Script", command=None)
        load_button.grid(row=2, sticky='s', pady=10)

        save_button = tk.Button(left_frame, text="Save Script", command=None)
        save_button.grid(row=3, sticky='s', pady=10)

        back_button = tk.Button(left_frame, text="Back",
                           command=lambda: controller.show_frame("StartPage"))
        back_button.grid(row=4, sticky='s', pady=(10,0))

        left_frame.grid_rowconfigure(1, weight=1)
        left_frame.grid_columnconfigure(0, weight=1)

        
        # Right Frame
        code_label = tk.Label(right_frame, text="Your code:")
        code_label.grid(sticky='w')

        code = tk.Text(right_frame, width=70, height=30, bg='#ffffff')
        code.grid(row=1, column=0, columnspan=4, rowspan=3, sticky='nsew', pady=(0,10))

        dir_button = tk.Button(right_frame, text="Destination Directory", command=None)
        dir_button.grid(row=4, column=0, sticky='ew')

        dest_entry = tk.Entry(right_frame, bg='#ffffff', font=("Arial", 14))
        dest_entry.grid(row=4, column=1, columnspan=2, sticky='we')

        run_button = tk.Button(right_frame, text="Run Script",
                           command=lambda: controller.show_frame("StartPage"))
        run_button.grid(row=4, column=3, sticky='se')

        right_frame.grid_rowconfigure(1, weight=3)
        right_frame.grid_columnconfigure(0, weight=1)
        right_frame.grid_columnconfigure(1, weight=2)
        right_frame.grid_columnconfigure(2, weight=2)

if __name__ == "__main__":
    app = SampleApp()
    app.mainloop()