from tkinter import *
from tkinter import messagebox

class Const():
	WINDOW_W = 990
	WINDOW_H = 750
	CELL_SIZE = 15
	START_SPEED = 10 #количество кадров в секунду

class Snake():
	drc = "top" #направление змейки
	body = [] 
	length = 1 #максимальная длина змейки
	color = "green3" #"green4"
	speedX = 0
	speedY = -1

	def __init__(self, x=0, y=0, speed=1):
		self.headPosX = x
		self.headPosY = y
		self.speed = speed
		self.body.append({"x": x, "y": y})

	def move(self): #перемещение змейки
		self.headPosX += self.speedX
		self.headPosY += self.speedY
		self.body.insert(0, {"x": self.headPosX, "y": self.headPosY})
		del self.body[-1]

def death():
	inGame = False
	messagebox.showinfo('Конец игры', 'Заново?')

def drawSnake(): #отрисовка змейки
	for i in range(snake.length):
		x = snake.body[i]["x"]*Const.CELL_SIZE
		y = snake.body[i]["y"]*Const.CELL_SIZE
		cnv.create_rectangle(x, y, x+Const.CELL_SIZE, y-Const.CELL_SIZE, outline=snake.color, fill=snake.color)

def onKeyPressed(event):
	code = event.keycode
	newDrc = ""
	newSpeedX = 0
	newSpeedY = 0
	if code == 112:
		help()
	elif code == 38 and snake.drc != "bottom": #вверх
		newDrc = "top"
		newSpeedY = -1
	elif code == 40 and snake.drc != "top": #вниз
		newDrc = "bottom"
		newSpeedY = 1
	elif code == 39 and snake.drc != "left": #вправо
		newDrc = "right"
		newSpeedX = 1
	elif code == 37 and snake.drc != "right": #влево
		newDrc = "left"
		newSpeedX = -1
	if newDrc != "":
		snake.drc = newDrc
		snake.speedX = newSpeedX
		snake.speedY = newSpeedY

def checkBorderContact():
	width = Const.WINDOW_W//Const.CELL_SIZE
	height = Const.WINDOW_H//Const.CELL_SIZE
	x = snake.headPosX
	y = snake.headPosY
	if x >= width or x < 0 or y >= height or y < 0:
		death()




def loop():
	cnv.delete("all")
	createMap()
	snake.move()
	drawSnake()
	checkBorderContact()
	if inGame: window.after(1000//snake.speed, loop)

def start(): #запуск игры
	mainFrame.pack_forget()
	cnv.pack(fill=BOTH, expand=1)
	loop()

def help():  #окно с правилами игры
	messagebox.showinfo('Правила игры', 'Текст')

def createMap(): #создание сетки на поле
	for i in range(Const.WINDOW_W//Const.CELL_SIZE):
		x = (i+1)*Const.CELL_SIZE
		cnv.create_line(x, 0, x, Const.WINDOW_H, fill="gray50")
	for i in range(Const.WINDOW_H//Const.CELL_SIZE):
		y = (i+1)*Const.CELL_SIZE
		cnv.create_line(0, y, Const.WINDOW_W, y, fill="gray50")

snake = Snake(Const.WINDOW_W//(2*Const.CELL_SIZE), Const.WINDOW_H//(2*Const.CELL_SIZE), Const.START_SPEED)
inGame = True
#создание элементов меню
window = Tk()
window.geometry('990x750')
window["bg"] = "black"
window.title("Змейка (Хакатон 2021)")
window.bind("<KeyPress>", onKeyPressed)

cnv = Canvas(window, bg="black")

mainFrame = Frame(window, width=50, bg="black")
mainFrame.pack(fill=BOTH, side=LEFT, expand=True)

btnStart = Button(mainFrame, text="Играть", width=20, command=start, bg="black", fg="white", font=("Arial Bold", 20), bd=10, relief=GROOVE)
btnStart.pack(side=TOP, padx=5, pady=5)

btnHelp = Button(mainFrame, text="Правила", width=20, command=help, bg="black", fg="white", font=("Arial Bold", 20), bd=10, relief=GROOVE)
btnHelp.pack(side=TOP, padx=5, pady=5)

window.mainloop()