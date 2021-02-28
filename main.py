from tkinter import *
from tkinter import messagebox
from random import randint

class Const():
	WINDOW_W = 990 #размер поля в px
	WINDOW_H = 750 #размер поля в px
	CELL_SIZE = 15 #размер клетки в px
	START_SPEED = 3 #кол-во кадров в секунду
	APPLES_COUNT = 2  #максимальное кол-во яблок на поле
	TRAPS_COUNT = 2  #максимальное кол-во ловушек на поле

class Items():
	apples = []
	appleColor = "orange red"
	trapColor = "white"
	crossColor = "red"
	traps = []

	def __init__(self, countA=2, countT=2):
		self.applesCount = countA #максимальное кол-во яблок на поле
		self.trapsCount = countT #максимальное кол-во ловушек на поле
		self.checkAppleCount()
		self.checkTrapCount()

	def spawnApple(self):
		appleX = randint(0, Const.WINDOW_W//Const.CELL_SIZE)
		appleY = randint(0, Const.WINDOW_H//Const.CELL_SIZE)
		if not ({"x": appleX, "y": appleY} in self.apples or {"x": appleX, "y": appleY} in self.traps):
			self.apples.append({"x": appleX, "y": appleY})

	def checkAppleCount(self):
		while len(self.apples) < self.applesCount:
			self.spawnApple()

	def spawnTrap(self):
		trapX = randint(0, Const.WINDOW_W//Const.CELL_SIZE)
		trapY = randint(0, Const.WINDOW_H//Const.CELL_SIZE)
		if not ({"x": trapX, "y": trapY} in self.apples or {"x": trapX, "y": trapY} in self.traps):
			self.traps.append({"x": trapX, "y": trapY})

	def checkTrapCount(self):
		while len(self.traps) < self.trapsCount:
			self.spawnTrap()

class Snake():
	drc = "top" #направление змейки
	body = [] 
	length = 10 #максимальная длина змейки
	color = "green3" #"green4"
	speedX = 0
	speedY = -1
	newDrc = ""

	def __init__(self, x=0, y=0, speed=1):
		self.headPosX = x
		self.headPosY = y
		self.speed = speed
		self.body.append({"x": x, "y": y})

	def move(self): #перемещение змейки
		self.headPosX += self.speedX
		self.headPosY += self.speedY
		self.body.insert(0, {"x": self.headPosX, "y": self.headPosY})
		if len(self.body) > self.length: #"анимация" укорочения
			del self.body[-1]
		if len(self.body) > self.length: #"анимация" укорочения
			del self.body[-1]
		if self.newDrc != "":
			self.drc = self.newDrc
			self.newDrc = ""

	def checkBiteYourself(self):
		for i in range(len(self.body)):
			for j in range(i+1, len(self.body)):
				if self.body[i]["x"] == self.body[j]["x"] and self.body[i]["y"] == self.body[j]["y"]:
					death()

def death():
	inGame = False
	messagebox.showinfo('Конец игры', 'Заново?')

def drawSnake(): #отрисовка змейки
	for i in range(len(snake.body)):
		x = snake.body[i]["x"]*Const.CELL_SIZE
		y = snake.body[i]["y"]*Const.CELL_SIZE
		cnv.create_rectangle(x, y, x+Const.CELL_SIZE, y+Const.CELL_SIZE, outline=snake.color, fill=snake.color)

def onKeyPressed(event): #отслеживание нажатий клавиш
	code = event.keycode
	newSpeedX = 0
	newSpeedY = 0
	if code == 112:
		help()
	elif code == 38 and snake.drc != "bottom": #вверх
		snake.newDrc = "top"
		newSpeedY = -1
	elif code == 40 and snake.drc != "top": #вниз
		snake.newDrc = "bottom"
		newSpeedY = 1
	elif code == 39 and snake.drc != "left": #вправо
		snake.newDrc = "right"
		newSpeedX = 1
	elif code == 37 and snake.drc != "right": #влево
		snake.newDrc = "left"
		newSpeedX = -1
	if newSpeedX + newSpeedY != 0:
		snake.speedX = newSpeedX
		snake.speedY = newSpeedY

def checkBorderContact(): #проверка на выход из поля игры
	width = Const.WINDOW_W//Const.CELL_SIZE
	height = Const.WINDOW_H//Const.CELL_SIZE
	x = snake.headPosX
	y = snake.headPosY
	if x >= width or x < 0 or y >= height or y < 0:
		death()

def drawApples(): #отрисовка яблок
	for i in range(len(items.apples)):
		x = items.apples[i]["x"]*Const.CELL_SIZE
		y = items.apples[i]["y"]*Const.CELL_SIZE
		cnv.create_rectangle(x, y, x+Const.CELL_SIZE, y+Const.CELL_SIZE, outline=items.appleColor, fill=items.appleColor)

def checkAppleContact(): #проверка на сбор яблока
	for i in range(len(items.apples)):
		if snake.headPosX == items.apples[i]["x"] and snake.headPosY == items.apples[i]["y"]:
			snake.length += 1
			if isHardMod: snake.speed += 2
			del items.apples[i]
			break

def drawTraps(): #отрисовка ловушек
	for i in range(len(items.traps)):
		x = items.traps[i]["x"]*Const.CELL_SIZE
		y = items.traps[i]["y"]*Const.CELL_SIZE
		cnv.create_rectangle(x, y, x+Const.CELL_SIZE, y+Const.CELL_SIZE, outline=items.trapColor, fill=items.trapColor)
		#отрисовка креста в ловушке
		cnv.create_line(x, y, x+Const.CELL_SIZE, y+Const.CELL_SIZE, fill=items.crossColor)
		cnv.create_line(x+Const.CELL_SIZE, y, x, y+Const.CELL_SIZE, fill=items.crossColor)

def checkTrapContact(): #проверка на столкновение с ловушкой
	for i in range(len(items.traps)):
		if snake.headPosX == items.traps[i]["x"] and snake.headPosY == items.traps[i]["y"]:
			death()

def loop():
	cnv.delete("all")
	items.checkAppleCount()
	items.checkTrapCount()
	snake.move()
	createMap()
	drawSnake()
	drawApples()
	drawTraps()
	snake.checkBiteYourself()
	checkBorderContact()
	checkAppleContact()
	checkTrapContact()
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
items = Items(Const.APPLES_COUNT, Const.TRAPS_COUNT)
inGame = True
isHardMod = True

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