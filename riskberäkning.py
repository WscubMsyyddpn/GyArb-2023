import random as r
from math import comb
import datetime as dt
import matplotlib.pyplot as plt



#KORTLEK
deck = [
# 2  3  4  5  6  7  8  9  10  J   Q   K   A
	2, 3, 4, 5, 6, 7, 8, 9, 10, 10, 10, 10, 11,
	2, 3, 4, 5, 6, 7, 8, 9, 10, 10, 10, 10, 11,
	2, 3, 4, 5, 6, 7, 8, 9, 10, 10, 10, 10, 11,
	2, 3, 4, 5, 6, 7, 8, 9, 10, 10, 10, 10, 11
	]
#ANTAL SPEL
i = 1_000_000_00
#ANTAL VARV PER SPEL
k = 100
#gransvarde I PROCENT
gransvarde = 100
#HAND VÄRD 21
blackjack = 21
#ESS VÄRD 11
ace = 11
#RESULTAT
win = 0; draw = 0; loss = 0
#SKAPA GRAF
fig, ax = plt.subplots()

# värde av kort för att avgöra en viss hands gynnsamma utfall
dictFO = {
# value:  n
	11   :   52,
	12   :   36,
	13   :   32,
	14   :   28,
	15   :   24,
	16   :   20,
	17   :   16,
	18   :   12,
	19   :   8,
	20   :   4,
	21   :   0
}

# blandar kortleken
def hit():
	cardHit = deck[r.choice(deck)]
	return cardHit

# kontrollerar om en hand är "soft"
def soft(hand):
	ifSoft = True
	if sum(hand) >= 17:
		while ifSoft == True:
			for a in range(len(hand)):
				if hand[a] == 11:
					hand[a] = 1
					ifSoft = False
					break
				else:
					ifSoft = False
	
	return hand


def result(pResult,dResult):
	global win
	global loss
	global draw

	p = int(pResult[-1])
	d = int(dResult[-1])

	if p > d and p <= blackjack or d > blackjack and p <= blackjack:
		win += 1
	elif p == d and p <= blackjack:
		draw += 1
	elif p > blackjack or p < d:
		loss += 1
	
	return win


def game():
	playerHand = []
	dealerHand = []

	playerHand.append(hit())
	dealerHand.append(hit())
	playerHand.append(hit())
	dealerHand.append(hit())


	# spelarens handlingar
	def playerGame(playerHand):
		while sum(playerHand) <= 10:
			playerHand.append(hit())

		while True:
			if sum(playerHand) <= blackjack:	
				n = dictFO[sum(playerHand)]
				po = comb(len(deck), 1)
				fo = comb(n,1)
				pHit = (fo/po)

				if (pHit * 100) >= gransvarde:
					playerHand.append(hit())
				else: 
					break
			else:
				break
		
		return sum(playerHand)
	

	# dealerns handlingar
	def dealerGame(dealerHand):
		while sum(dealerHand) <= 17:
			if ace in dealerHand:
				dealerHand.append(hit())
				dealerHand = soft(dealerHand)
			else:
				if sum(dealerHand) > 17:
					dealerHand.append(hit())
				else:
					break
		
		return sum(dealerHand)
	
	# initierar spelarens sedan dealerns tur
	pGame = playerGame(playerHand)
	dGame = dealerGame(dealerHand)

	return pGame, dGame


def main():
	global gransvarde
	global win
	winProcentList = []

	#STARTTID
	t1 = dt.datetime.now()

	for repetition in range(k):
		
		pResult = []
		dResult = []


		for iteration in range(i):
			player, dealer = game()
			pResult.append(player)
			dResult.append(dealer)
			
			w = result(pResult, dResult)
		
	
		winProcent = ((w / i) * 100)
		winProcentList.append(winProcent)


		win = 0
		gransvarde -= 1

	# checkar vilken gransvarde som ger flest vinster
	maxElement = max(winProcentList)
	maxIndex = winProcentList.index(maxElement)
	
	winProcentList.reverse() #vänder på listan. Grafen blir lättare att tolka

	#GRAF DESIGN
	barColour = [("green" if p == maxElement else "red") for p in winProcentList]
	#plt.title(f"Gränsvärde")
	plt.xlabel(f"GRÄNSVÄRDE")
	plt.ylabel(f"ANDEL VINSTER")

	
	#RITA GRAF
	plt.bar(range(k), winProcentList, width = 0.3, color = barColour)
	ax.axhline(y=maxElement, color = "black", linestyle="--")


	#SLUTTID
	t2 = dt.datetime.now()

	#PROGRAMTID
	runtime = (t2-t1)

	#PRINT
	print("Highest win procentage:", maxElement)
	print("Gransvarde for highest win procentage:", (100 - (maxIndex)))
	print("Runtime:", runtime)
	print(i)


	#VISA GRAF
	plt.show()

main()