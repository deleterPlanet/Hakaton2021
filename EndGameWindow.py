from tkinter import *

class EndGameWindow(Toplevel):
    def __init__(self, parent, results, restart, toMenu):
        super().__init__(parent)

        self.geometry('350x200')
        self["bg"] = "black"
        self.title("Конец игры")
        self.resizable(width=False, height=False)
        self.protocol("WM_DELETE_WINDOW", self.toMenu)

        self.lblResults = Label(self, text=results, font=("Arial", 20),
                            fg="white", bg="black")
        self.lblResults.pack(side=TOP, padx=10, pady=10)
		
        self.btnRestart = Button(self, text="Заново", font=("Arial", 20),
                            command=self.restart, fg="white", bg="black",
                            bd=5, relief=RAISED)
        self.btnRestart.pack(side=LEFT, padx=10, pady=10)

        self.btnMenu = Button(self, text="Меню", font=("Arial", 20),
                            command=self.toMenu, fg="white", bg="black",
                            bd=5, relief=RAISED)
        self.btnMenu.pack(side=RIGHT, padx=10, pady=10)

        self.newGame = restart
        self.openMenu = toMenu
        
    def restart(self):
        self.newGame()
        self.destroy()

    def toMenu(self):
        self.openMenu()
        self.destroy()