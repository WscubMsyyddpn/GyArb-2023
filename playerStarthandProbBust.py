#TABELL SOM ÖVERSTÄMMER
#https://debitcardcasino.ca/2019/01/11/dealer-bust-rate-blackjack/

import matplotlib.pyplot as plt

#KORTVÄRDEN I EN KORTLEK
cardList = [1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 10, 10, 10]
card1 = 2
#HANTERAR DATA
data = []

#SKAPAR GRAF
fig, ax = plt.subplots()
#CELLTEXT
column= ("Värde av Hand", "Chans att gå bust")
#CELLFÄRG
topRowColour = ["forestgreen","forestgreen"]
color = [["w" if i%2 == 0 else "gainsboro" for j in range(2)] for i in range(11)]

#GÖM AXLARNA
fig.patch.set_visible(False)
ax.axis('off')
ax.axis('tight')
plt.rcParams["font.family"] = "Calibri"

for x in range(20):
	sumHand = 0
	bust = 0

	for card2 in cardList:
		sumHand  = card1 + card2
		if sumHand  > 21:
			bust += 1

	if card1 > 11:
		bustProcent = str(int(round(bust/13,2) * 100)) + "%"
		dataRun = [card1, bustProcent]
		data.append(dataRun)

	card1 += 1

data.insert(0, ["11 or lower", 0])




#RITAR TABELL
table = ax.table(cellText=data, colLabels=column, loc="center", cellLoc="center", colColours=topRowColour, colWidths=[0.4,0.4], cellColours=color)
table.set_fontsize(20)
table.scale(1,2)
table.auto_set_column_width(col=list(range(len(column))))

plt.savefig("probability to bust on start hand")
plt.show()
