import random as r
from math import comb, ceil
import datetime as dt
import matplotlib.pyplot as plt

# KORTLEK
deck = [
# 2  3  4  5  6  7  8  9  10  J   Q   K   A
  2, 3, 4, 5, 6, 7, 8, 9, 10, 10, 10, 10, 11,
  2, 3, 4, 5, 6, 7, 8, 9, 10, 10, 10, 10, 11,
  2, 3, 4, 5, 6, 7, 8, 9, 10, 10, 10, 10, 11,
  2, 3, 4, 5, 6, 7, 8, 9, 10, 10, 10, 10, 11
]
# ANTAL SPEL
numGames = 10000
# ANTAL VARV (1 varv motsvarat ett gränsvärde)
numTurns = 100
# ANTAL KORTLEKAR
numDeck = 4
# GRÄNSVÄRDE I PROCENT
gransvarde = 100
# HANDVÄRDe 21
twentyone = 21
# ESS
ace = 11
# WHEN TO RESHUFFLE
reshuffleIndex = 70
# RESULTAT
winCount = 0; drawCount = 0; lossCount = 0
#SKAPA GRAF
fig, ax = plt.subplots()
# värde av kort för att avgöra en viss hands gynnsamma utfall, gäller när cc = False
dictFO = {
# värde:  n
   11  :  52,
   12  :  36,
   13  :  32,
   14  :  24,
   16  :  20,
   17  :  16,
   18  :  12,
   19  :  8,
   20  :  4,
   21  :  0
}

# blandar kortlek
def deckShuffle():
	stdDeck = [
	# 2  3  4  5  6  7  8  9  10  J   Q   K   A
	2, 3, 4, 5, 6, 7, 8, 9, 10, 10, 10, 10, 11,
	2, 3, 4, 5, 6, 7, 8, 9, 10, 10, 10, 10, 11,
	2, 3, 4, 5, 6, 7, 8, 9, 10, 10, 10, 10, 11,
	2, 3, 4, 5, 6, 7, 8, 9, 10, 10, 10, 10, 11
	]
	stdDeck *= numDeck

	r.shuffle(stdDeck)

	return stdDeck[:]

# tar ett "slumpmässigt" kort
def hit():
	cardHit = deck[r.choice(deck)]
	return cardHit

# hanterar händer med ess
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

# beräknar utfallet från en runda Blackjack
def result(pResult,dResult):
	global winCount
	global drawCount
	global lossCount


	p = int(pResult[-1])
	d = int(dResult[-1])

	if p > d and p <= twentyone or d > twentyone and p <= twentyone:
		winCount += 1
	elif p == d and p <= twentyone:
		drawCount += 1
	elif p > twentyone or p < d:
		lossCount += 1
	
	return winCount, drawCount, lossCount


# räkning av kort
def cardCountingGame():
	playerHand = []
	dealerHand = []

 	 # kort delas ut till spelaren och dealern
	playerHand.append(deck.pop(0))
	dealerHand.append(deck.pop(0))
	playerHand.append(deck.pop(0))
	dealerHand.append(deck.pop(0))

  	# spelarens drag
	def playerActionCC(playerHand):
		while sum(playerHand) <= twentyone:
			while sum(playerHand) <= 10:
				playerHand.append(deck.pop(0))
			
      		# beräknar sannolikheten att INTE gå bust
			n = deck.count(11)
			for card in range(2, (twentyone - sum(playerHand) + 1)):
				n += deck.count(card)
			po = comb(len(deck), 1)
			fo = comb(n, 1)
			pHit = (fo/po)

     		# jämfört sannolikheten med gränsvärde och fattar ett beslut
			if (pHit * 100) >= gransvarde:
				playerHand.append(deck.pop(0))
				if sum(playerHand) > twentyone:
					if ace in playerHand:
						playerHand = soft(playerHand)				
			else:
				break
			
		return sum(playerHand)

  	# dealerns drag
	def dealerActionCC(dealerHand):
		if sum(dealerHand) <= 17:
			while (sum(dealerHand) < 17) or (sum(dealerHand) == 17 and ace in dealerHand):
				dealerHand.append(deck.pop(0))
				if ace in dealerHand:
					dealerHand = soft(dealerHand)
		
		return sum(dealerHand)

	pGameCC = playerActionCC(playerHand)
	dGameCC = dealerActionCC(dealerHand)

	return pGameCC, dGameCC


# ej räkning av kort
def noCardCountingGame():
	playerHand = []
	dealerHand = []
	
  # kort delas ut till spelaren och dealern
	playerHand.append(hit())
	dealerHand.append(hit())
	playerHand.append(hit())
	dealerHand.append(hit())

  	# spelarens drag
	def playerAction(playerHand):
		while sum(playerHand) <= twentyone:
			while sum(playerHand) <= 10:
				playerHand.append(hit())
			
      		# beräknar sannolikheten att INTE gå bust
			n = dictFO[sum(playerHand)]
			po = comb(len(deck), 1)
			fo = comb(n, 1)
			pHit = (fo/po)

      		# jämfört sannolikheten med gränsvärde och fattar ett beslut
			if (pHit * 100) >= gransvarde:
				playerHand.append(hit())
				if sum(playerHand) > twentyone:
					if ace in playerHand:
						playerHand = soft(playerHand)		
			else:
				break
	
		return sum(playerHand)


  	# dealerns drag
	def dealerAction(dealerHand):
		if sum(dealerHand) <= 17:
			while (sum(dealerHand) < 17) or (sum(dealerHand) == 17 and ace in dealerHand):
				dealerHand.append(hit())
				if ace in dealerHand:
					dealerHand = soft(dealerHand)
			
		return sum(dealerHand)
	

	pGame = playerAction(playerHand)
	dGame = dealerAction(dealerHand)

	return pGame, dGame


def main():
	# deklarera globala variabler
	global gransvarde
	global winCount
	global cc
	global deck

	winProcentList = []
	
	cc = False # card count (True = på) (False = av)

  	# STARTTID
	t1 = dt.datetime.now()


	for repetition in range(numTurns):
		pResult = [] # spelarens resultat lagras
		dResult = [] # dealerns resultat lagras

    	# blandar kortleken
		if cc == True:
			deck = deckShuffle()

		for iteration in range(numGames):
			if cc == True:
				player, dealer = cardCountingGame()
			elif cc == False:
				player, dealer = noCardCountingGame()
			

			pResult.append(player)
			dResult.append(dealer)

      		# antalet vinster, oavgjort, förluster
			win, draw, loss = result(pResult, dResult)

      		# blandar om kortleken
			if cc == True:
				if (float(len(deck)) / (52 * numDeck)) * 100 < reshuffleIndex:
					deck = deckShuffle()
		
    	# beräknar och lagrar andelen vinster
		winProcent = ((win/numGames) * 100)
		winProcentList.append(winProcent)

    	# nollställer antalet vinster för nästa gränsvärde
		winCount = 0
		# minskar gränsvärdet med en procentenhet
		gransvarde -= 1

	# avgör vilket gränsvärde gav flest andel vinster
	maxElement = max(winProcentList)
	maxIndex = winProcentList.index(maxElement)

	# GRAF DESIGN
	barColour = [("green" if p == maxElement else "red") for p in winProcentList]
	plt.title("GRÄNSVÄRDE")
	plt.xlabel(f"RISKFAKTOR (100% --> 0 %)")
	plt.ylabel("VINSTER I PROCENT")
	
	# RITA GRAF
	plt.bar(range(numTurns), winProcentList, width = 0.4, color = barColour)

	# SLUTTID
	t2 = dt.datetime.now()

	# PROGRAMTID
	runtime = (t2-t1)

	#PRINT
	print(f"Highest win procentage:", maxElement)
	print(f"Index for highest win procentage:", (100 - (maxIndex)))
	print(f"Runtime:", runtime)
	print(f"Number of wins:", win)
	print(f"Number of wins:", draw)
	print(f"Number of wins:", loss)


	# VISA GRAF
	plt.show()

main()
