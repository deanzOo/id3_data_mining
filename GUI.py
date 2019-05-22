from tkinter import *
from tkinter import filedialog

#Functions:
def UploadAction():
    filename = filedialog.askopenfile(initialdir = '/',title = "Select file",filetypes = (("csv files","*.csv"),("all files","*.*")))
    print("Selected:",filename)

#Create Window
window = Tk()
window.title("Data-Mining")
window.geometry('400x200')

#Create Labels
loadlbl = Label(window, text="Select folder to load files:", font= ("Times", 12))
loadlbl.grid(column = 0, row = 0)


binslbl = Label(window, text="Discretization Bins:", font= ("Times", 12))
binslbl.grid(column = 0, row = 1)

#Bottoms:
buttombtn = Button(window, text = "Browser...",command = UploadAction)
buttombtn.grid (column = 2,row = 0)

binsbtn = Button(window, text = "Submit")
binsbtn.grid (column = 2,row = 1)

cleanbtn = Button(window, text = "Clean")
cleanbtn.grid (column = 0,row = 3)

discretizationbtn = Button(window, text = "Discretization")
discretizationbtn.grid (column = 0,row = 4)

buildbtn = Button(window, text = "Build")
buildbtn.grid (column = 0,row = 5)

classifybtn = Button(window, text = "Classify")
classifybtn .grid (column = 0,row = 6)

accuracybtn = Button(window, text = "Accuracy")
accuracybtn  .grid (column = 0,row = 7)

exitbtn = Button(window, text = "Exit")
exitbtn.grid (column = 0,row = 8)

#TextBoxes:
browsertxt = Entry (window, width = 25)
browsertxt.grid(column = 1, row = 0)

binstxt = Entry (window, width = 25)
binstxt.grid(column = 1, row = 1)
window.mainloop()