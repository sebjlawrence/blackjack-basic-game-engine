
#Libraries-------------------------

import random

#Constants-------------------------

RANKS = ['2', '3', '4', '5', '6', '7', '8', '9', '10', 'J', 'Q', 'K', 'A']
SUITS = ['Hearts', 'Spades', 'Clubs', 'Diamonds']
VALUES = {'2':2, '3':3, '4':4, '5':5, '6':6, '7':7, '8':8, '9':9, '10':10, 'J':10, 'Q':10, 'K':10, 'A':1}
#Aces are low by default
MAX_SPLITS = 3
#Four hands are the maximum, following common casino rules

#Classes---------------------------

class Shoe:
    def __init__(self, mindecks = 6 ):
        self.mindecks = mindecks
        self.reshuffle()

    def deal_card(self):
        return self.cards.pop()

    def is_low(self):
        low = False
        if len(self.cards) < (0.25 * self.mindecks * 52):
            low = True
        return low

    def reshuffle(self):
        deck = [[rank, suit] for rank in RANKS for suit in SUITS]
        self.cards = deck * self.mindecks
        random.shuffle(self.cards)
        

class Hand:
    def __init__(self):
        self.cards = []

    def add_card(self, card):
        self.cards.append(card)

    def total_value(self):
        #hand is soft if there is one or more aces
        totalVal = 0
        aces = 0
        soft = False
        for card in self.cards:
            valueChar = card[0]
            value = VALUES[valueChar]
            totalVal += value
            if value == 1:
                aces += 1
        if aces > 0 and totalVal <= 11:
            totalVal += 10
            soft = True
        return totalVal, soft

    def is_bust(self):
        bust = False
        busted, x = self.total_value()
        if busted > 21:
            bust = True
        return bust

    def is_blackjack(self):
        bj = False
        blackj, x = self.total_value()
        if blackj == 21 and len(self.cards) == 2:
            bj = True
        return bj


#Functions-----------------------

def begin_play(my_Shoe):
    player = Hand()
    dealer = Hand()
    dealer.add_card(my_Shoe.deal_card())
    player.add_card(my_Shoe.deal_card())
    dealer.add_card(my_Shoe.deal_card())
    player.add_card(my_Shoe.deal_card())
    return player, dealer


def dealer_behaviour(dealer_hand, my_Shoe):
    
    bust = False
    
    total, soft = dealer_hand.total_value()     
    while total < 17 or (total == 17 and soft):
        dealer_hand.add_card(my_Shoe.deal_card())
        total, soft = dealer_hand.total_value()
    
    if dealer_hand.is_bust():
        bust = True

    return total, bust




def play_hand(my_Shoe, strategy, player_hand, up_card, splits=0):

    player_choice = strategy(player_hand, up_card)

    if player_choice == 'split':
        if len(player_hand.cards) != 2:
            raise ValueError(f'Can only split on two cards: {player_hand.cards}')

        card1, card2 = player_hand.cards
        if VALUES[card1[0]] != VALUES[card2[0]]:
            raise ValueError(f'Can only split a pair: {player_hand.cards}')
        if splits >= MAX_SPLITS:
            raise ValueError(f'Split limit reached: {player_hand.cards}')

        results = []
        for card in player_hand.cards:
            new_hand = Hand()
            new_hand.add_card(card)
            new_hand.add_card(my_Shoe.deal_card())

            if card[0] == 'A':
                # Split aces get one card each and no further decisions
                total, soft = new_hand.total_value()
                results.append((False, 1, total))
            else:
                results += play_hand(my_Shoe, strategy, new_hand, up_card, splits + 1)

        return results

    # Base case: play this hand normally
    double = 1

    if player_choice == 'double':
        double = 2
        player_hand.add_card(my_Shoe.deal_card())

    while player_choice == 'hit' and not player_hand.is_bust():
        player_hand.add_card(my_Shoe.deal_card())
        if not player_hand.is_bust():
            player_choice = strategy(player_hand, up_card)
            if player_choice == 'double':
                raise ValueError('Can not double after already hitting.')

    player_total, soft = player_hand.total_value()
    player_bust = player_hand.is_bust()

    return [(player_bust, double, player_total)]


def play_round(my_Shoe, strategy):

    score = 0

    if my_Shoe.is_low():
        my_Shoe.reshuffle()

    player_hand, dealer_hand = begin_play(my_Shoe)

    if dealer_hand.is_blackjack() and player_hand.is_blackjack():
        score = 0

    elif dealer_hand.is_blackjack():
        score = -1

    elif player_hand.is_blackjack():
        score = 1.5

    else:
        up_card = VALUES[dealer_hand.cards[0][0]]
        if up_card == 1:
            up_card = 11

        results = play_hand(my_Shoe, strategy, player_hand, up_card)

        # The dealer only plays if at least one hand is still live
        dealer_needed = any(not bust for bust, double, total in results)
        if dealer_needed:
            dealer_total, dealer_bust = dealer_behaviour(dealer_hand, my_Shoe)

        for player_bust, double, player_total in results:
            if player_bust:
                score += -1 * double
            elif dealer_bust:
                score += 1 * double
            elif dealer_total > player_total:
                score += -1 * double
            elif dealer_total < player_total:
                score += 1 * double
            # equal totals: push, score unchanged

    return score

