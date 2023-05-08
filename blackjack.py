#!/usr/bin/env python

import random
import time
import subprocess
import os


def console():
    subprocess.call('clear' if os.name == 'posix' else 'cls')


console()


class Card:

    def __init__(self, suit, rank):
        self.suit = suit
        self.rank = rank

    def __str__(self):
        return "{} of {}".format(self.rank, self.suit)

    def dealer_card(self):
        if self.rank in "JQK":
            return 10
        elif self.rank == "A":
            return 11
        else:
            return int(self.rank)


class Deck:

    def __init__(self):
        self.cards = []

    def new_deck(self):
        suits = ["Spades", "Clubs", "Hearts", "Diamonds"]
        ranks = ["2", "3", "4", "5", "6", "7", "8", "9", "10", "J", "Q", "K", "A"] * 4
        if len(self.cards) < 25:
            self.cards.clear()
            for suit in suits:
                for rank in ranks:
                    self.cards.append(Card(suit, rank))
        random.shuffle(self.cards)


class Hand:

    def __init__(self):
        self.hand = []
        self.total = 0

    def get_card(self):
        self.hand.append(deck.cards.pop())

    def show_hand(self):
        for card in self.hand:
            print(" "*4 + str(card))

    def get_total(self):
        ace = 0
        for card in self.hand:
            if card.rank in "JQK":
                self.total += 10
            elif card.rank == "A":
                ace += 1
                self.total += 11
            else:
                self.total += int(card.rank)
        for a in range(ace):
            if self.total > 21:
                self.total -= 10

    def score(self):
        self.get_total()
        return self.total


class Bank:

    def __init__(self):
        self.chips = 0
        self.bet = 0

    def win(self):
        self.chips += self.bet

    def lose(self):
        self.chips -= self.bet

    def blackjack(self):
        self.chips += self.bet * 1.5


def set_table():
    deck.new_deck()
    if dealer.hand == [] and player.hand == []:
        for card in range(2):
            dealer.get_card()
            player.get_card()
    player.stand = False
    player.double = True


def display():
    dealer.total = 0
    player.total = 0

    console()
    print("\n You bet " + str(int(bank.bet)) + " chips")

    print("\n ** Dealer's Hand **")
    if player.stand:
        dealer.show_hand()
        print("\n Dealer Shows: " + str(dealer.score()))
    else:
        print(" "*5 + "- Hidden -\n" + " "*4 + str(dealer.hand[1]))
        print("\n Dealer Shows: " + str(dealer.hand[1].dealer_card()))

    print("\n ** Player's Hand ** ")
    player.show_hand()
    print("\n Player Has: " + str(player.score()))


def balance():
    print("\nYou have " + str(int(bank.chips)) + " chips!")
    if bank.chips <= 0:
        time.sleep(0.8)
        print("\nSorry, Game Over")
        exit()


def auto_deal():
    player.stand = True
    display()
    while True:
        if dealer.total < 17 and player.total <= 21:
            dealer.get_card()
            display()
            continue
        else:
            check_win()


def wager():
    balance()
    while True:
        try:
            bank.bet = int(input("\nPlease place your bet: "))
            if bank.bet <= 0:
                console()
                print("\n> Must be a positive integer.")
                continue
            elif bank.bet > bank.chips:
                console()
                print("\nSorry, you only have " + str(int(bank.chips)) + " chips.")
                continue
        except ValueError:
            console()
            print("\n> That's not an integer!")
            continue
        if bank.chips >= bank.bet:
            set_table()
            check_win()
    return bank.bet


def options():
    while True:
        choose = input("\n(H)it, (S)tand, (D)ouble ").lower()
        if choose == 'h':
            player.double = False
            player.get_card()
            check_win()
        elif choose == 's':
            auto_deal()
        elif choose == 'd':
            if player.double:
                if bank.chips >= bank.bet * 2:
                    bank.bet *= 2
                    player.get_card()
                    display()
                else:
                    print("\nSorry, not enough chips.")
                    time.sleep(1)
                    continue
            else:
                print("\nCan't double down after 'hit'")
                time.sleep(1)
                continue
        else:
            print ("\nInvalid entry.")
            time.sleep(1)
            continue


def check_win():
    display()
    while True:
        if player.total == 21 != dealer.total:
            player.stand = True
            display()
            print("\nBLACKJACK! YOU WIN!")
            bank.blackjack()
            break
        elif player.total > 21:
            player.stand = True
            display()
            print("\nBUSTED! YOU LOSE.")
            bank.lose()
            break
        elif dealer.total > 21:
            print("\nDEALER BUSTS! YOU WIN!")
            bank.win()
            break
        elif 17 <= dealer.total > player.total:
            print("\nDEALER HITS " + str(dealer.total) + ", YOU LOSE.")
            bank.lose()
            break
        elif player.total > dealer.total >= 17:
            print("\nDEALER HITS " + str(dealer.total) + ", YOU WIN!")
            bank.win()
            break
        elif player.total == dealer.total >= 17:
            print("\nDEALER PUSHES " + str(player.total) + ", DRAW!")
            break
        else:
            options()
    new_hand()


def new_hand():
    dealer.hand = []
    player.hand = []
    while True:
        again = input("\nPlay another hand? (Y/n) ").upper()
        console()
        if again == "Y":
            player.stand = False
            wager()
        elif again == "N":
            print("Thanks for playing!")
            time.sleep(0.8)
            exit()
        else:
            continue


def greeter():
    print("\nWelcome to Python Blackjack!")
    while True:
        try:
            bank.chips = int(input("\nHow many chips would you like to buy?\n"))
            if bank.chips <= 0:
                console()
                print("\n> Must be a positive integer.")
                continue
            console()
            wager()
        except ValueError:
            console()
            print("\n> That's not an integer!")
            continue


if __name__ == "__main__":
    deck = Deck()
    bank = Bank()
    dealer = Hand()
    player = Hand()
    greeter()
