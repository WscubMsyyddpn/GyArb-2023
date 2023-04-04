from math import comb

deck = [
# 2  3  4  5  6  7  8  9  10  J   Q   K   A
	2, 3, 4, 5, 6, 7, 8, 9, 10, 10, 10, 10, 11,
	2, 3, 4, 5, 6, 7, 8, 9, 10, 10, 10, 10, 11,
	2, 3, 4, 5, 6, 7, 8, 9, 10, 10, 10, 10, 11,
	2, 3, 4, 5, 6, 7, 8, 9, 10, 10, 10, 10, 11]

numberWorthTen = deck.count(10)   
numberAce = deck.count(11)

possibleOutcomes = comb(len(deck), 2)
favorableOutcomes = comb(numberAce, 1) * comb(numberWorthTen, 1)

pBlackjack = (favorableOutcomes/possibleOutcomes)

print(pBlackjack)
