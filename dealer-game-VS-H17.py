## använd gv från förra koden
## en del som kör kort räkning, dvs, håller koll på varje kort som spelats och beräknar sannolikheten därifrån
## en del som  kör utan korträkning som spelar som dealern eller att spelaren kör slumpmässigt eller utan att ta ett nytt kort.

import random 
from math import comb
import datetime as dt
import matplotlib.pyplot as plt

# ANTAL SPEL
num_games = 1_000_000_000
# ANTAL KORTLEKAR
num_decks = 8
# GRÄNSVÄRDE I PROCENT
gransvarde = 74
# HAND VÄRD 21
twentyone = 21
# ESS
ace = 11
# NÄR KORTLEKEN BLANDAS
reshuffle_index = 80
# RESULTAT
win_count = 0; draw_count = 0; loss_count = 0; blackjack_count = 0
#SKAPA GRAF
fig, ax = plt.subplots()


# hanterar om en hand är "soft"
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

# blandar kortleken och skapar en kopia av standardleken.
def deck_shuffle():
  std_deck = [
  # 2  3  4  5  6  7  8  9  10  J   Q   K   A
  2, 3, 4, 5, 6, 7, 8, 9, 10, 10, 10, 10, 11,
  2, 3, 4, 5, 6, 7, 8, 9, 10, 10, 10, 10, 11,
  2, 3, 4, 5, 6, 7, 8, 9, 10, 10, 10, 10, 11,
  2, 3, 4, 5, 6, 7, 8, 9, 10, 10, 10, 10, 11
  ]
  
  std_deck *= num_decks

  random.shuffle(std_deck)

  return std_deck[:]

# beräknar resultatet av en runda blackjack
def result(player_result,dealer_result):
  global win_count
  global draw_count
  global loss_count

  # tilldelar resultat av senaste rundan till variablerna p och d
  p = int(player_result[-1])
  d = int(dealer_result[-1])

  if (p > d and p <= twentyone) or (d > twentyone and p <= twentyone):
    win_count += 1
  elif p == d and p <= twentyone:
    draw_count += 1
  elif p > twentyone or p < d:
    loss_count += 1
  
  return win_count, draw_count, loss_count

# blackjack med korträkning
def blackjack_simulation_card_counting():
  global blackjack_count

  player_hand = []
  dealer_hand = []

  # delar ut kort
  player_hand.append(deck.pop(0))
  dealer_hand.append(deck.pop(0))
  player_hand.append(deck.pop(0))
  dealer_hand.append(deck.pop(0))

  # checkar om man fått en blackjack
  if player_hand in [[11, 10], [10, 11]]:
    blackjack_count += 1

  # SPELAREN
  def player_action_card_counting(player_hand):
    while sum(player_hand) <= twentyone:
      while sum(player_hand) <= 10:
        player_hand.append(deck.pop(0))
      
      # checkar hur många gynnsamma kort som finns i kortleken
      n = deck.count(ace)
      upperLimit = twentyone - sum(player_hand)
      for card in range(2, (upperLimit + 1)):
        n += deck.count(card)

      # beräknar sannolikheten att inte gå bust vid hit
      po = comb(len(deck), 1)
      fo = comb(n, 1)
      pHit = (fo/po)


      if (pHit * 100) >= gransvarde:
        player_hand.append(deck.pop(0))
        if sum(player_hand) > twentyone:

          if ace in player_hand and sum(player_hand) <= 17:
            player_hand = soft(player_hand)
            
      else:
        break

    return sum(player_hand)

  # DEALERN
  def dealer_action_card_counting(dealer_hand):
    while sum(dealer_hand) < 17:
        dealer_hand.append(deck.pop(0))
        if ace in dealer_hand:
          dealer_hand = soft(dealer_hand)

    if sum(dealer_hand) == 17 and ace in dealer_hand:
      dealer_hand.append(deck.pop(0))
      if ace in dealer_hand:
        dealer_hand = soft(dealer_hand)

    return sum(dealer_hand)

  player_game = player_action_card_counting(player_hand)
  dealer_game = dealer_action_card_counting(dealer_hand)

  return player_game, dealer_game

# blackjack där spelaren spelar som dealern med reglerna H17
def blackjack_simulation_H17():
  global blackjack_count

  player_hand = []
  dealer_hand = []

  # delar ut kort
  player_hand.append(deck.pop(0))
  dealer_hand.append(deck.pop(0))
  player_hand.append(deck.pop(0))
  dealer_hand.append(deck.pop(0))


  # checkar om man fått en blackjack
  if player_hand in [[11, 10], [10, 11]]:
    blackjack_count += 1

  # SPELAREN
  def player_action_H17(player_hand):
    while sum(player_hand) < 17:
        player_hand.append(deck.pop(0))
        if ace in player_hand:
          player_hand = soft(player_hand)

    if sum(player_hand) == 17 and ace in player_hand:
      player_hand.append(deck.pop(0))
      if ace in player_hand:
        player_hand = soft(player_hand)

    return sum(player_hand)

  # DEALERN
  def dealer_action_H17(dealer_hand):
    while sum(dealer_hand) < 17:
        dealer_hand.append(deck.pop(0))
        if ace in dealer_hand:
          dealer_hand = soft(dealer_hand)

    if sum(dealer_hand) == 17 and ace in dealer_hand:
      dealer_hand.append(deck.pop(0))
      if ace in dealer_hand:
        dealer_hand = soft(dealer_hand)

    return sum(dealer_hand)

  player_game = player_action_H17(player_hand)
  dealer_game = dealer_action_H17(dealer_hand)

  return player_game, dealer_game


def main():
  # deklarera globala variabler
  global switch
  global deck

  player_result = []
  dealer_result = []
  game_result = []


  switch = True # True (räknar kort), False (spelar som dealern (H17))

  # STARTTID
  t1 = dt.datetime.now()

  # blandar kortleken
  deck = deck_shuffle()

  for iteration in range(num_games):
    if switch == True:
      player, dealer = blackjack_simulation_card_counting()
    elif switch == False:
      player, dealer = blackjack_simulation_H17()
    

    # blandar om kortleken
    if len(deck) < reshuffle_index:
      deck = deck_shuffle()

    player_result.append(player)
    dealer_result.append(dealer)

    win, draw, loss = result(player_result, dealer_result)

    


  
  win_procent = ((win/num_games) * 100)
  draw_procent = ((draw/num_games) * 100)
  loss_procent = ((loss/num_games) * 100)

  game_result.extend([win, draw, loss])


  # RITA GRAF
  bar_colour = ["#002000","#202020","#200000"]
  bar_label = ["Wins", "Draws", "Losses"]
  bar_container = ax.bar(bar_label, game_result, width = 0.75, color = bar_colour)
  ax.bar_label(bar_container, label_type = "edge", color = "black")
  ax.spines["top"].set_visible(False)
  ax.spines["right"].set_visible(False)
  
  # SLUTTID
  t2 = dt.datetime.now()

  # PROGRAMTID
  runtime = (t2-t1)

  print(f"Win percentage: {win_procent}")
  print(f"Draw percentage: {draw_procent}")
  print(f"Loss percentage: {loss_procent}")
  print(f"Number of Blackjacks: {blackjack_count}")
  print(f"Number of games {'{:,}'.format(num_games).replace(',', ' ')}")
  print(f"Runtime: {runtime}")


  # SPARA GRAF

  if switch == True:
    plt.savefig("epic graph card counting")
  elif switch == False:
    plt.savefig("epic graph Player-H17")

  # VISA GRAF
  plt.show()

main()
