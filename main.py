from tkinter import *
from tkinter import messagebox
from random import randint
from functools import partial
import time
# Подключение своих модулей
import Const as c
import Items as i
import Snake as s
import EndGameWindow as egw
import RuleWindow as rw
        
def death():
	global inGame, points, pasCells

	inGame = False
	now = time.time()
	res = "Время игры: " + str(int(now - startTime)) + " cек.\n"
	res += "Набрано очков: " + str(points) + "\n"
	res += "Пройдено клеток: " + str(pasCells)

	endGameWindow = egw.EndGameWindow(window, res, restart, toMenu)
	endGameWindow.grab_set()

def drawSnake(): #отрисовка змейки
	for i in range(len(snake.body)):
		x = snake.body[i]["x"]*Const.CELL_SIZE
		y = snake.body[i]["y"]*Const.CELL_SIZE

		cnv.create_oval(x, y, x+Const.CELL_SIZE, y+Const.CELL_SIZE,
			outline=snake.color, fill=snake.color)

def onKeyPressed(event):  # Отслеживание нажатий клавиш
	global isCells
	code = event.keycode
	newSpeedX = 0
	newSpeedY = 0

	if code == 112:
		help()
	elif code == 67: # Переключение отображения сетки
		isCells = not isCells
	elif code == 38 and snake.drc != "bottom":  # Вверх
		snake.newDrc = "top"
		newSpeedY = -1
	elif code == 40 and snake.drc != "top":  # Вниз
		snake.newDrc = "bottom"
		newSpeedY = 1
	elif code == 39 and snake.drc != "left":  # Вправо
		snake.newDrc = "right"
		newSpeedX = 1
	elif code == 37 and snake.drc != "right":  # Влево
		snake.newDrc = "left"
		newSpeedX = -1

	if newSpeedX + newSpeedY != 0:
		snake.speedX = newSpeedX
		snake.speedY = newSpeedY

def checkBorderContact():  # Проверка на выход из поля игры
	width = Const.WINDOW_W//Const.CELL_SIZE
	height = Const.WINDOW_H//Const.CELL_SIZE
	x = snake.headPosX
	y = snake.headPosY
	if x >= width or x < 0 or y >= height or y < 0:
		death()

def drawApples():  # Отрисовка яблок
	for i in range(len(items.apples)):
		x = items.apples[i]["x"]*Const.CELL_SIZE
		y = items.apples[i]["y"]*Const.CELL_SIZE
		cnv.create_oval(x, y, x+Const.CELL_SIZE, y+Const.CELL_SIZE,
			outline=items.appleColor, fill=items.appleColor)

def checkAppleContact():  # Проверка на сбор яблока
	global points, background, startBgAnim

	for i in range(len(items.apples)):
		if (snake.headPosX == items.apples[i]["x"]
				and snake.headPosY == items.apples[i]["y"]):
			snake.length += 1
			points += 1
			background = "background_apple.png"
			startBgAnim = time.time()

			if isHardMod: snake.speed += 2
			del items.apples[i]
			break

def drawTraps():  # Отрисовка ловушек
	for i in range(len(items.traps)):
		x = items.traps[i]["x"]*Const.CELL_SIZE
		y = items.traps[i]["y"]*Const.CELL_SIZE

		cnv.create_rectangle(x, y, x+Const.CELL_SIZE, y+Const.CELL_SIZE,
			outline=items.trapColor, fill=items.trapColor)

		# Отрисовка креста в ловушке
		cnv.create_line(x, y, x+Const.CELL_SIZE, y+Const.CELL_SIZE,
			fill=items.crossColor)
		cnv.create_line(x+Const.CELL_SIZE, y, x, y+Const.CELL_SIZE,
			fill=items.crossColor)

def checkTrapContact():  # Проверка на столкновение с ловушкой
	for i in range(len(items.traps)):
		if (snake.headPosX == items.traps[i]["x"]
				and snake.headPosY == items.traps[i]["y"]):

			if items.bonusesStat["invincib"]["isRun"]:
				del items.traps[i]
			else:
				death()
			break

def drawBonuses():  # Отрисовка бонусов
	for i in range(len(items.bonuses)):
		x = items.bonuses[i]["x"]*Const.CELL_SIZE
		y = items.bonuses[i]["y"]*Const.CELL_SIZE
		cnv.create_image(x, y, anchor=NW,
			image=items.bonusImgs[items.bonusesTypes[i]])

def checkBonusContact():  # Проверка на сбор бонуса
	for i in range(len(items.bonuses)):
		if (snake.headPosX == items.bonuses[i]["x"]
				and snake.headPosY == items.bonuses[i]["y"]):
			items.getBonus(i, snake)
			break

def drawTimers():
	now = time.time()
	timerPos = {"x": 0, "y": 0}
	for i in items.bonusesStat.keys():
		pasBonus = (now - items.bonusesStat[i]["startTime"])
		pasBonus /= Const.BONUS_TIME
		if items.bonusesStat[i]["isRun"] and pasBonus <= 1:
			x = timerPos["x"]*Const.CELL_SIZE
			y = timerPos["y"]*Const.CELL_SIZE
			timerPos["x"] += 3
			timer = int(pasBonus*360)
			cnv.create_arc(x, y, x+2*Const.CELL_SIZE, y+2*Const.CELL_SIZE,
				start=90, extent=360-timer,
				outline=items.bonusColors[i], fill=items.bonusColors[i])
			cnv.create_image(x+0.5*Const.CELL_SIZE, y+0.5*Const.CELL_SIZE,
				anchor=NW, image=items.bonusImgs[i])

def drawBackground():
	global img, background

	img = PhotoImage(file=background) 
	cnv.create_image(0, 0, anchor=NW, image=img)
	if time.time() - startBgAnim >= Const.ANIM_TIME:
		background = "background.png"

def restart():
	beforeGame()
	loop()

def toMenu():
	mainFrame.pack(expand=True)
	cnv.pack_forget()

def loop():
	global inGame

	cnv.delete("all")

	# Работа с числами
	items.checkAppleCount(snake)
	items.checkTrapCount(snake)
	items.checkBonusCount(snake)
	snake.move(pasCells)

	# Отрисовка элементов
	drawBackground()
	if isCells: createMap()
	drawApples()
	drawBonuses()
	drawSnake()
	drawTraps()
	drawTimers()

	# Проверки
	snake.checkBiteYourself(death)
	checkBorderContact()
	checkAppleContact()
	checkTrapContact()
	checkBonusContact()
	items.checkBonusRun()

	# Запуск нового кадра
	fps = snake.speed
	if items.bonusesStat["time"]["isRun"]: fps //= Const.SLOWDOWN_TIME
	if inGame: window.after(1000//fps, loop)

def start(mod, event):  #З апуск игры
	global startTime, snake, items, inGame, isHardMod, points, pasCells
	global background, startBgAnim

	# Работа с информацией
	data = open("data.txt", "r")
	isOpenRules = int(data.readline().split("=")[-1])
	if not isOpenRules:
		data = open("data.txt", "w")
		data.write("isOpenRules=" + "1")
		data.close()
		msg = "Не хотите сначала ознакомиться с правилами игры?"
		if messagebox.askyesno(message=msg, parent=window):
			help()
			return
	data.close()

	# Работа с элементами экрана
	mainFrame.pack_forget()
	cnv.pack(fill=BOTH, expand=True)

	isHardMod = mod
	beforeGame()

	loop()

def beforeGame():  # Обнуление переменных
	global points, pasCells, snake, startTime, items, inGame
	global startBgAnim, background, isCells

	background = "background.png"
	startTime = time.time()
	startBgAnim = 0
	snake = s.Snake(Const.WINDOW_W//(2*Const.CELL_SIZE),
			Const.WINDOW_H//(2*Const.CELL_SIZE), Const.START_SPEED)
	items = i.Items(Const.APPLES_COUNT, Const.TRAPS_COUNT,
			Const.BONUSES_COUNT, snake)
	isCells = True
	inGame = True
	points = 0
	pasCells = 0

def help():  # Окно с правилами игры
	rulesWindow = rw.RuleWindow(window)
	rulesWindow.grab_set()
	data = open("data.txt", "w")
	data.write("isOpenRules=" + "1")
	data.close()

def createMap():  # Создание сетки на поле
	for i in range(Const.WINDOW_W//Const.CELL_SIZE):
		x = (i+1)*Const.CELL_SIZE
		cnv.create_line(x, 0, x, Const.WINDOW_H, fill="gray70")

	for i in range(Const.WINDOW_H//Const.CELL_SIZE):
		y = (i+1)*Const.CELL_SIZE
		cnv.create_line(0, y, Const.WINDOW_W, y, fill="gray70")

def exit():
	msg = "Вы точно хотите выйти из игры?"
	if messagebox.askyesno(message=msg, parent=window):
		window.destroy()

Const = c.Const()

# Создание элементов меню
window = Tk()
window.resizable(width=False, height=False)
window.protocol("WM_DELETE_WINDOW", exit)
window.geometry('975x720')
window["bg"] = "black"
window.title("Змейка (Хакатон 2021)")
window.bind("<KeyPress>", onKeyPressed)

cnv = Canvas(window, bg="black")

mainFrame = Frame(window, width=50, bg="black")
mainFrame.pack(expand=True)

btnStartEasy = Button(mainFrame, text="Статический режим", width=20,
				bg="black", fg="white", font=("Arial Bold", 20), bd=10,
				relief=GROOVE)
btnStartEasy.pack(side=TOP, padx=20, pady=20)
btnStartEasy.bind('<Button-1>', partial(start, False))

btnStartHard = Button(mainFrame, text="Динамический режим", width=20,
				bg="black", fg="white", font=("Arial Bold", 20), bd=10,
				relief=GROOVE)
btnStartHard.pack(side=TOP, padx=20, pady=20)
btnStartHard.bind('<Button-1>', partial(start, True))

btnHelp = Button(mainFrame, text="Правила игры", width=20, command=help,
			bg="black", fg="white", font=("Arial Bold", 20), bd=10,
			relief=GROOVE)
btnHelp.pack(side=TOP, padx=20, pady=20)

window.mainloop()