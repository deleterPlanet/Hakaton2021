from tkinter import *
from tkinter import messagebox
from random import randint
from functools import partial
import time

class Const():
	WINDOW_W = 990 #размер поля в px
	WINDOW_H = 750 #размер поля в px
	CELL_SIZE = 15 #размер клетки в px
	START_SPEED = 10 #кол-во кадров в секунду
	APPLES_COUNT = 2  #макс. кол-во яблок на поле
	TRAPS_COUNT = 10  #макс. кол-во ловушек на поле
	BONUSES_COUNT = 30 #макс. кол-во бонусов на поле
	BONUS_TIME = 10 #кол-во секунд работы бонуса
	SLOWDOWN_TIME = 2 #во сколько раз замедляется время

class Items():
	def __init__(self, countA=2, countT=10, countB=3):
		self.apples = []
		self.traps = []
		self.bonuses = []
		self.appleColor = "orange red"
		self.trapColor = "white"
		self.crossColor = "red"
		self.bonusColors = {"short": "wheat3", "invincib": "gold", "time": "deep sky blue", "tp": "DeepPink2"}
		self.bonusesTypes = []
		self.bonusesStat = {"invincib": {"isRun": False, "startTime": 0}, "time": {"isRun": False, "startTime": 0}}
		self.applesCount = countA #макс. кол-во яблок на поле
		self.trapsCount = countT #макс. кол-во ловушек на поле
		self.bonusesCount = countB #макс. кол-во бонусов на поле
		self.checkAppleCount()
		self.checkTrapCount()
		self.checkBonusCount()

	def spawnApple(self): #генерация яблока
		appleX = randint(0, Const.WINDOW_W//Const.CELL_SIZE)
		appleY = randint(0, Const.WINDOW_H//Const.CELL_SIZE)
		if not ({"x": appleX, "y": appleY} in (self.apples + self.traps + self.bonuses + snake.body)):
			self.apples.append({"x": appleX, "y": appleY})

	def checkAppleCount(self):
		while len(self.apples) < self.applesCount:
			self.spawnApple()

	def spawnTrap(self): #генерация ловушки
		trapX = randint(0, Const.WINDOW_W//Const.CELL_SIZE)
		trapY = randint(0, Const.WINDOW_H//Const.CELL_SIZE)
		if not ({"x": trapX, "y": trapY} in (self.apples + self.traps + self.bonuses + snake.body)):
			self.traps.append({"x": trapX, "y": trapY})

	def checkTrapCount(self):
		while len(self.traps) < self.trapsCount:
			self.spawnTrap()

	def spawnBonus(self): #генерация бонуса
		bonusX = randint(0, Const.WINDOW_W//Const.CELL_SIZE)
		bonusY = randint(0, Const.WINDOW_H//Const.CELL_SIZE)
		types = list(self.bonusColors.keys()) #список доступных типов
		bonusType = types[randint(0, len(types)-1)]
		if not ({"x": bonusX, "y": bonusY} in (self.apples + self.traps + self.bonuses + snake.body)):
			self.bonuses.append({"x": bonusX, "y": bonusY})
			self.bonusesTypes.append(bonusType)

	def checkBonusCount(self):
		while len(self.bonuses) < self.bonusesCount:
			self.spawnBonus()

	def getBonus(self, bonusNum):
		type = self.bonusesTypes[bonusNum]
		if type == "short":
			snake.length = 1
		elif type == "tp":
			while {"x": snake.headPosX, "y": snake.headPosY} in snake.body:
				snake.headPosX = randint(0, Const.WINDOW_W//Const.CELL_SIZE)
				snake.headPosY = randint(0, Const.WINDOW_H//Const.CELL_SIZE)
		else:
			self.bonusesStat[type]["startTime"] = time.time()
			self.bonusesStat[type]["isRun"] = True

		del self.bonusesTypes[bonusNum]
		del self.bonuses[bonusNum]

	def checkBonusRun(self):
		now = time.time()
		for i in self.bonusesStat.keys():
			if self.bonusesStat[i]["isRun"] and now - self.bonusesStat[i]["startTime"] >= Const.BONUS_TIME:
				self.bonusesStat[i]["isRun"] = False
				print(i, "off")

class Snake():
	def __init__(self, x=0, y=0, speed=1):
		self.drc = "top" #направление змейки
		self.body = [] 
		self.length = 10 #максимальная длина змейки
		self.color = "green3" #"green4"
		self.speedX = 0
		self.speedY = -1
		self.newDrc = ""
		self.headPosX = x
		self.headPosY = y
		self.speed = speed
		self.body.append({"x": x, "y": y})

	def move(self): #перемещение змейки
		global pasCells
		self.headPosX += self.speedX
		self.headPosY += self.speedY
		self.body.insert(0, {"x": self.headPosX, "y": self.headPosY})
		pasCells += 1
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
					break


class EndGameWindow(Toplevel):
    def __init__(self, parent, results):
        super().__init__(parent)

        self.geometry('350x200')
        self["bg"] = "black"
        self.title("Конец игры")
        self.resizable(width=False, height=False)
        self.protocol("WM_DELETE_WINDOW", self.toMenu)

        self.lblResults = Label(self, text=results, font=("Arial", 20), fg="white", bg="black")
        self.lblResults.pack(side=TOP, padx=10, pady=10)
		
        self.btnRestart = Button(self, text="Заново", command=self.restart, font=("Arial", 20), fg="white", bg="black", bd=5, relief=RAISED)
        self.btnRestart.pack(side=LEFT, padx=10, pady=10)

        self.btnMenu = Button(self, text="Меню", command=self.toMenu, font=("Arial", 20), fg="white", bg="black", bd=5, relief=RAISED)
        self.btnMenu.pack(side=RIGHT, padx=10, pady=10)
        
    def restart(self):
        global points, pasCells, snake, startTime, items, inGame
        points = 0
        pasCells = 0
        snake = Snake(Const.WINDOW_W//(2*Const.CELL_SIZE), Const.WINDOW_H//(2*Const.CELL_SIZE), Const.START_SPEED)
        startTime = time.time()
        items = Items(Const.APPLES_COUNT, Const.TRAPS_COUNT, Const.BONUSES_COUNT)
        inGame = True
        self.destroy()
        loop()

    def toMenu(self):
        mainFrame.pack(expand=True)
        cnv.pack_forget()
        self.destroy()

class RuleWindow(Toplevel): #окно с правилами игры
    def __init__(self, parent):
        super().__init__(parent)

        self.geometry('978x544')
        self.title("Правила игры")
        self.resizable(width=False, height=False)

        self.cnv = Canvas(self, bg="black")
        self.cnv.pack(fill=BOTH, expand=True)
        self.drawRules()
        
    def drawRules(self): #отрисовка правил игры
    	self.img = PhotoImage(file="rules.png") 
    	self.cnv.create_image(0, 0, anchor='nw',image=self.img)
        
def death():
	global inGame, points, pasCells
	inGame = False
	now = time.time()
	res = "Время игры: " + str(int(now - startTime)) + " cек.\n" + "Набрано очков: " + str(points) + "\n" + "Пройдено клеток: " + str(pasCells)
	endGameWindow = EndGameWindow(window, res)
	endGameWindow.grab_set()

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
	elif code == 116:
		death()
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
	global points
	for i in range(len(items.apples)):
		if snake.headPosX == items.apples[i]["x"] and snake.headPosY == items.apples[i]["y"]:
			snake.length += 1
			points += 1
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
			if items.bonusesStat["invincib"]["isRun"]:
				del items.traps[i]
			else:
				death()
			break

def drawBonuses(): #отрисовка бонусов
	for i in range(len(items.bonuses)):
		x = items.bonuses[i]["x"]*Const.CELL_SIZE
		y = items.bonuses[i]["y"]*Const.CELL_SIZE
		cnv.create_rectangle(x, y, x+Const.CELL_SIZE, y+Const.CELL_SIZE, outline=items.bonusColors[items.bonusesTypes[i]], fill=items.bonusColors[items.bonusesTypes[i]])

def checkBonusContact(): #проверка на сбор бонуса
	for i in range(len(items.bonuses)):
		if snake.headPosX == items.bonuses[i]["x"] and snake.headPosY == items.bonuses[i]["y"]:
			items.getBonus(i)
			break

def drawTimers():
	now = time.time()
	timerPos = {"x": 0, "y": 0}
	for i in items.bonusesStat.keys():
		pasBonus = (now - items.bonusesStat[i]["startTime"])/Const.BONUS_TIME
		if items.bonusesStat[i]["isRun"] and pasBonus <= 1:
			x = timerPos["x"]*Const.CELL_SIZE
			y = timerPos["y"]*Const.CELL_SIZE
			timerPos["x"] += 3
			timer = int(pasBonus*360)
			cnv.create_arc(x, y, x+2*Const.CELL_SIZE, y+2*Const.CELL_SIZE, start=90, extent=360-timer, outline=items.bonusColors[i], fill=items.bonusColors[i])

def loop():
	global inGame
	cnv.delete("all")
	#работа с числами
	items.checkAppleCount()
	items.checkTrapCount()
	items.checkBonusCount()
	snake.move()
	#отрисовка элементов
	createMap()
	drawSnake()
	drawApples()
	drawTraps()
	drawBonuses()
	drawTimers()
	#проверки
	snake.checkBiteYourself()
	checkBorderContact()
	checkAppleContact()
	checkTrapContact()
	checkBonusContact()
	items.checkBonusRun()
	#запуск нового кадра
	fps = snake.speed
	if items.bonusesStat["time"]["isRun"]: fps //= Const.SLOWDOWN_TIME
	if inGame: window.after(1000//fps, loop)

def start(mod, event): #запуск игры
	global startTime, snake, items, inGame, isHardMod, points, pasCells
	#работа с информацией
	data = open("data.txt", "r")
	isFirstGame = int(data.readline().split("=")[-1])
	if isFirstGame: #если это первая игра
		data = open("data.txt", "w")
		data.write("isFirstGame=" + "0")
		data.close()
		if messagebox.askyesno(message="Не хотите сначала ознакомиться с правилами игры?", parent=window):
			help()
			return
	data.close()
	#работа с элементами экрана
	mainFrame.pack_forget()
	cnv.pack(fill=BOTH, expand=True)
	#обнуление переменных
	startTime = time.time()
	snake = Snake(Const.WINDOW_W//(2*Const.CELL_SIZE), Const.WINDOW_H//(2*Const.CELL_SIZE), Const.START_SPEED)
	items = Items(Const.APPLES_COUNT, Const.TRAPS_COUNT, Const.BONUSES_COUNT)
	inGame = True
	isHardMod = mod 
	points = 0
	pasCells = 0
	loop()

def help():  #окно с правилами игры
	rulesWindow = RuleWindow(window)
	rulesWindow.grab_set()

def createMap(): #создание сетки на поле
	for i in range(Const.WINDOW_W//Const.CELL_SIZE):
		x = (i+1)*Const.CELL_SIZE
		cnv.create_line(x, 0, x, Const.WINDOW_H, fill="gray50")
	for i in range(Const.WINDOW_H//Const.CELL_SIZE):
		y = (i+1)*Const.CELL_SIZE
		cnv.create_line(0, y, Const.WINDOW_W, y, fill="gray50")

def exit():
	if messagebox.askyesno(message="Вы точно хотите выйти из игры?", parent=window):
		window.destroy()

#создание элементов меню
window = Tk()
window.resizable(width=False, height=False)
window.protocol("WM_DELETE_WINDOW", exit)
window.geometry('990x750')
window["bg"] = "black"
window.title("Змейка (Хакатон 2021)")
window.bind("<KeyPress>", onKeyPressed)

cnv = Canvas(window, bg="black")

mainFrame = Frame(window, width=50, bg="black")
mainFrame.pack(expand=True)

btnStartEasy = Button(mainFrame, text="Статический режим", width=20, bg="black", fg="white", font=("Arial Bold", 20), bd=10, relief=GROOVE)
btnStartEasy.pack(side=TOP, padx=20, pady=20)
btnStartEasy.bind('<Button-1>', partial(start, False))

btnStartHard = Button(mainFrame, text="Динамический режим", width=20, bg="black", fg="white", font=("Arial Bold", 20), bd=10, relief=GROOVE)
btnStartHard.pack(side=TOP, padx=20, pady=20)
btnStartHard.bind('<Button-1>', partial(start, True))

btnHelp = Button(mainFrame, text="Правила игры", width=20, command=help, bg="black", fg="white", font=("Arial Bold", 20), bd=10, relief=GROOVE)
btnHelp.pack(side=TOP, padx=20, pady=20)

window.mainloop()