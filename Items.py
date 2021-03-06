from tkinter import *
from random import randint
import time
import Const as c

Const = c.Const()

class Items():
	def __init__(self, countA, countT, countB, snake):
		self.apples = []
		self.traps = []
		self.bonuses = []
		self.appleColor = "light goldenrod"
		self.trapColor = "white"
		self.crossColor = "red"
		self.bonusColors = {
			"short": "wheat3", "invincib": "gold",
			"time": "deep sky blue", "tp": "DeepPink2"
		}
		self.bonusImgs = {"short": "", "invincib": "", "time": "", "tp": ""}
		self.bonusesTypes = []
		self.bonusesStat = {
			"invincib": {"isRun": False, "startTime": 0},
			"time": {"isRun": False, "startTime": 0}
		}
		self.applesCount = countA  # Макс. кол-во яблок на поле
		self.trapsCount = countT  # Макс. кол-во ловушек на поле
		self.bonusesCount = countB  # Макс. кол-во бонусов на поле
		self.checkAppleCount(snake)
		self.checkTrapCount(snake)
		self.checkBonusCount(snake)
		self.loadImgs()

	def loadImgs(self):
		for i in self.bonusImgs.keys():
			self.bonusImgs[i] = PhotoImage(file=i + ".png")

	def spawnApple(self, snake):  #Генерация яблока
		appleX = randint(0, Const.WINDOW_W//Const.CELL_SIZE-1)
		appleY = randint(0, Const.WINDOW_H//Const.CELL_SIZE-1)
		cells = self.apples + self.traps + self.bonuses + snake.body
		if not ({"x": appleX, "y": appleY} in cells):
			self.apples.append({"x": appleX, "y": appleY})

	def checkAppleCount(self, snake):
		while len(self.apples) < self.applesCount:
			self.spawnApple(snake)

	def spawnTrap(self, snake):  # Генерация ловушки
		trapX = randint(0, Const.WINDOW_W//Const.CELL_SIZE-1)
		cells = self.apples + self.traps + self.bonuses + snake.body
		trapY = randint(0, Const.WINDOW_H//Const.CELL_SIZE-1)
		if not ({"x": trapX, "y": trapY} in cells):
			self.traps.append({"x": trapX, "y": trapY})

	def checkTrapCount(self, snake):
		while len(self.traps) < self.trapsCount:
			self.spawnTrap(snake)

	def spawnBonus(self, snake):  # Генерация бонуса
		bonusX = randint(0, Const.WINDOW_W//Const.CELL_SIZE-1)
		bonusY = randint(0, Const.WINDOW_H//Const.CELL_SIZE-1)
		types = list(self.bonusColors.keys())  # Список доступных типов
		bonusType = types[randint(0, len(types)-1)]
		cells = self.apples + self.traps + self.bonuses + snake.body
		if not ({"x": bonusX, "y": bonusY} in cells):
			self.bonuses.append({"x": bonusX, "y": bonusY})
			self.bonusesTypes.append(bonusType)

	def checkBonusCount(self, snake):
		while len(self.bonuses) < self.bonusesCount:
			self.spawnBonus(snake)

	def getBonus(self, bonusNum, snake):
		global background, startBgAnim

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
		background = "background_" + type + ".png"
		startBgAnim = time.time()

		del self.bonusesTypes[bonusNum]
		del self.bonuses[bonusNum]

	def checkBonusRun(self):
		now = time.time()
		for i in self.bonusesStat.keys():
			bonusTime = now - self.bonusesStat[i]["startTime"]
			if self.bonusesStat[i]["isRun"] and bonusTime >= Const.BONUS_TIME:
				self.bonusesStat[i]["isRun"] = False
				print(i, "off")