from tkinter import *
from tkinter import filedialog
from ProcessCSV import *

class MainWindow():

    def __init__(self,parent):
        self.parent = parent
        parent.title ("Data-Mining")
        parent.geometry('400x200')
        self.folder_path = StringVar()
        self.p = ProcessCSV()

        # Labels:
        self.loadlbl = Label(parent, text="Select folder to load files:", font=("Times", 12))
        self.loadlbl.grid(column=0, row=0)
        self.binslbl = Label(parent, text="Discretization Bins:", font=("Times", 12))
        self.binslbl.grid(column=0, row=1)

        # Textboxes:
        self.browsertxt = Entry(parent, width=25, textvariable=self.folder_path)
        self.browsertxt.grid(column=1, row=0)
        self.binstxt = Text(parent, height=1, width=19)
        self.binstxt.grid(column=1, row=1)

        # Buttons:
        self.buttombtn = Button(parent, text="Browser...", command=lambda: self.p.open_files(self.browser_button()))
        self.buttombtn.grid(column=2, row=0)
        self.cleanbtn = Button(parent, text="Clean", command=lambda: self.p.clean_up() )
        self.cleanbtn.grid(column=0, row=3)
        self.discretizationbtn = Button(parent, text="Discretization" ,command=lambda: self.p.discretisize(self.get_num_of_bins()))
        self.discretizationbtn.grid(column=0, row=4)
        self.buildbtn = Button(parent, text="Build")
        self.buildbtn.grid(column=0, row=5)
        self.classifybtn = Button(parent, text="Classify")
        self.classifybtn.grid(column=0, row=6)
        self.accuracybtn = Button(parent, text="Accuracy")
        self.accuracybtn.grid(column=0, row=7)
        self.exitbtn = Button(parent, text="Exit")
        self.exitbtn.grid(column=0, row=8)

    def browser_button(self):
        self.folder_path
        path = str(filedialog.askdirectory())
        self.folder_path.set(path)
        return path

    def get_num_of_bins(self):
        inputValue = self.binstxt.get("1.0", "end -1c")
        return float(inputValue)




if __name__ == "__main__":
    root = Tk()
    MainWindow(root)
    root.mainloop()
