from random import randint

def moves():  # Ход игрока и компьютера
	global compMove, playerMove, res

	compMove = randint(0, 2)
	st = "Компьютер сделал свой ход. Сделайте и вы (введите 'К'/'Н'/'Б') "
	inp = input(st).lower()

	flag = True
	st = "Неправильный ввод. Повторите пожалуйста (введите 'К'/'Н'/'Б') "
	while True:  # Проверка на корректность ввода
		for i in answers.keys():
			if inp in answers[i] and i != "да":
				inp = i
				flag = False
		if not flag: break
		inp = input(st).lower()

	playerMove = playerVal.index(inp)
	res = ""

def findWinner():  # Поиск победителя
	global res, compPoints, playerPoints

	if playerMove == compMove:
		playerPoints += 1
		res = "очко игроку"
	elif playerMove == (compMove + 1)%3:
		res = "ничья"
	else:
		compPoints += 1
		res = "очко компьютеру"

def checkEndGame():  # Проверка на окончание игры
	global compPoints, playerPoints, inGame

	if compPoints == 3:
		print("победил компьютер")
		compPoints = playerPoints = 0
		inGame = input("начать заново? (д/н) ").lower() in answers["да"]
	elif playerPoints == 3:
		print("победил игрок")
		compPoints = playerPoints = 0
		inGame = input("начать заново? (д/н) ").lower() in answers["да"]
	else:
		print(res)

def rules():
	f = open("rules.txt", "r")
	rules = f.readline()
	rules += f.readline()
	print(rules)

def drawRules():
	ans = input("не хотите ли вы ознакомиться с правилами игры? (д/н) ")
	ans = ans.lower()
	isDraw = ans in answers["да"]
	if isDraw:
		rules()

compPoints = 0  # Очки компьютера
playerPoints = 0  # Очки игрока
compVal = ["камень", "ножницы", "бумага"]
playerVal = ["бумага", "камень", "ножницы"]
inGame = True
answers = {"камень": ["к", "r", "камень"],
	"ножницы": ["н", "y", "ножницы"],
	"бумага": ["б", ",", "<", "бумага"],
	"да": ["да", "д", "l"]
}

drawRules()

while inGame:
	moves()
	findWinner()
	checkEndGame()