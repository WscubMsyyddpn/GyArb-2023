## beräknar det terotetiska bästa sättet att spela med hjälp av sannolikheten. Spela igenom x antal spel på varje procent (0 till 100) och använd resultaten i nästkommande kod ##

import random
from math import comb
import datetime
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
num_games = 100_000_000
# ANTAL VARV (1 varv motsvarat ett gränsvärde)
num_turns = 100
# GRÄNSVÄRDE I PROCENT
gransvarde = 0
# HAND VÄRD 21
twentyone = 21
# ESS
ace = 11
# RESULTAT
win_count = 0; draw_count = 0; loss_count = 0
#SKAPA GRAF
fig, ax = plt.subplots()
# värde av kort för att avgöra en viss hands gynnsamma utfall, gäller när cc = False
dict_FO = {
# värde:  n
   11  :  52,
   12  :  36,
   13  :  32,
   14  :  28,
   15  :  24,
   16  :  20,
   17  :  16,
   18  :  12,
   19  :  8,
   20  :  4,
   21  :  0
}

def hit():
  card_hit = deck[random.choice(deck)]
  return card_hit

def soft(hand):
  if_soft = True
  if sum(hand) >= 17:
    while if_soft == True:
      for element in range(len(hand)):
        if hand[element] == 11:
          hand[element] = 1
          if_soft = False
          break
        else:
          if_soft = False
  
  return hand


def result(pResult,dResult):
  global win_count
  global draw_count
  global loss_count

  p = int(pResult[-1])
  d = int(dResult[-1])

  if (p > d and p <= twentyone) or (d > twentyone and p <= twentyone):
    win_count += 1
  elif p == d and p <= twentyone:
    draw_count += 1
  elif p > twentyone or p < d:
    loss_count += 1
  
  return win_count

def blackjack_simulation():
  player_hand = []
  dealer_hand = []
  
  # kort delas ut till spelaren och dealern
  player_hand.append(hit())
  dealer_hand.append(hit())
  player_hand.append(hit())
  dealer_hand.append(hit())


  def player_action(player_hand):
    while sum(player_hand) <= twentyone:

      while sum(player_hand) <= 10:
        player_hand.append(hit())
      
      favourable_outcomes = comb(dict_FO[sum(player_hand)], 1)
      possible_outcomes = comb(len(deck), 1)
      p_no_bust = favourable_outcomes/possible_outcomes
      
      if p_no_bust * 100 >= gransvarde:
        player_hand.append(hit())
        if sum(player_hand) > twentyone:
          if ace in player_hand and sum(player_hand) <= 17:
            player_hand = soft(player_hand)

      
      else:
        break
        
    
    return sum(player_hand)

  def dealer_action(dealer_hand):
    while sum(dealer_hand) < 17:
        dealer_hand.append(hit())
        if ace in dealer_hand:
          dealer_hand = soft(dealer_hand)

    if sum(dealer_hand) == 17 and ace in dealer_hand:
      dealer_hand.append(hit())
      if ace in dealer_hand:
        dealer_hand = soft(dealer_hand)

    return sum(dealer_hand)

  player_game = player_action(player_hand)
  dealer_game = dealer_action(dealer_hand)

  return player_game, dealer_game


def main():
  global gransvarde
  global win_count
  
  win_rates = []

  # STARTTID
  t1 = datetime.datetime.now()


  for repetition in range(num_turns):
    player_result = []
    dealer_result = []

    for iteration in range(num_games):
      player, dealer = blackjack_simulation()

      player_result.append(player)
      dealer_result.append(dealer)

      win = result(player_result, dealer_result)

    win_percent = ((win/num_games))# * 100)
    win_rates.append(win_percent)

    win_count = 0
    gransvarde += 1

  max_rate = max(win_rates)
  max_index = win_rates.index(max_rate) + 1

  # GRAF DESIGN
  bar_colour = [("red" if p == max_rate else "black") for p in win_rates]
  plt.xlabel(f"GRANSVARDE")
  plt.ylabel(f"ANDEL VINSTER")
  
  # RITA GRAF
  ax.bar(range(num_turns), win_rates, width = 0.50, color = bar_colour)


  # SLUTTID
  t2 = datetime.datetime.now()

  # PROGRAMTID
  runtime = (t2-t1)

  #PRINT
  print(f"Highest win procentage:", max_rate)
  print(f"Index for highest win procentage:", (max_index))
  print(f"Runtime:", runtime)
  print(win_rates)

  # VISA GRAF
  plt.show()

main()


