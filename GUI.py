from tkinter import *
from tkinter import filedialog

#Create Window:
window = Tk()
window.title("Data-Mining")
window.geometry('400x200')
folder_path = StringVar()

#Functions:
def browser_button():
    global folder_path
    path = filedialog.askdirectory()
    folder_path.set(path)
    return path

def get_num_of_bins():
    inputValue = binstxt.get("1.0","end -1c")
    return inputValue


#Labels:
loadlbl = Label(window, text="Select folder to load files:", font=("Times", 12))
loadlbl.grid(column=0, row=0)
binslbl = Label(window, text="Discretization Bins:", font=("Times", 12))
binslbl.grid(column=0, row=1)

#Textboxes:
browsertxt = Entry(window, width=25, textvariable=folder_path)
browsertxt.grid(column=1, row=0)
binstxt = Text(window, height=1,width=19)
binstxt.grid(column=1, row=1)

#Buttons:
buttombtn = Button(window, text="Browser...", command=lambda: browser_button())
buttombtn.grid(column=2, row=0)
binsbtn = Button(window, text="Submit",command=lambda: get_num_of_bins())
binsbtn.grid(column=2, row=1)
cleanbtn = Button(window, text="Clean")
cleanbtn.grid(column=0, row=3)
discretizationbtn = Button(window, text="Discretization")
discretizationbtn.grid(column=0, row=4)
buildbtn = Button(window, text="Build")
buildbtn.grid(column=0, row=5)
classifybtn = Button(window, text="Classify")
classifybtn.grid(column=0, row=6)
accuracybtn = Button(window, text="Accuracy")
accuracybtn.grid(column=0, row=7)
exitbtn = Button(window, text="Exit")
exitbtn.grid(column=0, row=8)


window.mainloop()