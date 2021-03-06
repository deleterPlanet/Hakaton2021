from tkinter import *

class RuleWindow(Toplevel):  # Окно с правилами игры
    def __init__(self, parent):
        super().__init__(parent)

        self.geometry('978x544')
        self.title("Правила игры")
        self.resizable(width=False, height=False)

        self.cnv = Canvas(self, bg="black")
        self.cnv.pack(fill=BOTH, expand=True)
        self.drawRules()
        
    def drawRules(self):
    	self.img = PhotoImage(file="rules.png") 
    	self.cnv.create_image(0, 0, anchor=NW,image=self.img)