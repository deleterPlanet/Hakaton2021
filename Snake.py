class Snake():
	def __init__(self, x, y, speed=1):
		self.drc = "top"  # Направление змейки
		self.body = [] 
		self.length = 1  # Максимальная длина змейки
		self.color = "green3"
		self.speedX = 0
		self.speedY = -1
		self.newDrc = ""
		self.headPosX = x
		self.headPosY = y
		self.speed = speed
		self.body.append({"x": x, "y": y})

	def move(self, pasCells):  # Перемещение змейки
		self.headPosX += self.speedX
		self.headPosY += self.speedY
		self.body.insert(0, {"x": self.headPosX, "y": self.headPosY})
		pasCells += 1
		# Анимация укорочения
		if len(self.body) > self.length:
			del self.body[-1]
		if len(self.body) > self.length:
			del self.body[-1]

		if self.newDrc != "":
			self.drc = self.newDrc
			self.newDrc = ""

	def checkBiteYourself(self, fun):
		for i in range(len(self.body)):
			for j in range(i+1, len(self.body)):
				if (self.body[i]["x"] == self.body[j]["x"]
						and self.body[i]["y"] == self.body[j]["y"]):
					fun()
					break