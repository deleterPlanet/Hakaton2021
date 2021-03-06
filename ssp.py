from random import randint

def moves(): #ход игрока и компьютера
	global compMove, playerMove, res
	compMove = randint(0, 2)
	inp = input("Компьютер сделал свой ход. Сделайте и вы (введите 'камень'/'ножницы'/'бумага') ").lower()
	while not (inp in ["камень", "ножницы", "бумага"]): #проверка на корректность ввода
		inp = input("Неправильный ввод. Повторите пожалуйста (введите 'камень'/'ножницы'/'бумага') ").lower()
	playerMove = playerVal.index(inp)
	res = ""

def findWinner(): #поиск победителя
	global res, compPoints, playerPoints
	if playerMove == compMove:
		playerPoints += 1
		res = "очко игроку"
	elif playerMove == (compMove + 1)%3:
		res = "ничья"
	else:
		compPoints += 1
		res = "очко компьютеру"

def checkEndGame(): #проверка на окончание игры
	global compPoints, playerPoints, inGame
	if compPoints == 3:
		print("победил компьютер")
		compPoints = playerPoints = 0
		inGame = input("начать заново? (да/нет) ").lower() in ["да", "д", "y", "yes"]
	elif playerPoints == 3:
		print("победил игрок")
		compPoints = playerPoints = 0
		inGame = input("начать заново? (да/нет) ").lower() in ["да", "д", "y", "yes"]
	else:
		print(res)

compPoints = 0 #очки компьютера
playerPoints = 0 #очки игрока
compVal = ["камень", "ножницы", "бумага"]
playerVal = ["бумага", "камень", "ножницы"]
inGame = True
while inGame:
	moves()
	findWinner()
	checkEndGame()