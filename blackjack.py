#!/usr/bin/env python

"""
File: blackjack.py
Author: Jay Hartt
Date: 2021-02-09
Python Version: 3.9
"""

import random
import time
import subprocess
import os


def clear():
    subprocess.call('clear' if os.name == 'posix' else 'cls')


clear()


class Card:
    def __init__(self, suit, rank):
        self.suit = suit
        self.rank = rank

    def __str__(self):
        return "{} of {}".format(self.rank, self.suit)

    def dealer_card(self):
        if self.rank.isnumeric():
            return int(self.rank)
        else:
            if self.rank == "A":
                return 11
            else:
                return 10


class Deck:
    def __init__(self):
        self.cards = []

    def new_deck(self):
        suits = ["Spades", "Clubs", "Hearts", "Diamonds"]
        ranks = ["2", "3", "4", "5", "6", "7", "8", "9", "10", "J", "Q", "K", "A"] * 4
        if len(self.cards) < 25:
            for suit in suits:
                for rank in ranks:
                    self.cards.append(Card(suit, rank))
        random.shuffle(self.cards)


class Hand:
    def __init__(self):
        self.stand = False
        self.hand = []
        self.total = 0

    def get_card(self):
        self.hand.append(deck.cards.pop())

    def show_hand(self):
        for card in self.hand:
            print(" "*4 + str(card))

    def get_total(self):
        ace = False
        for card in self.hand:
            if card.rank.isnumeric():
                self.total += int(card.rank)
            else:
                if card.rank == "A":
                    ace = True
                    self.total += 11
                else:
                    self.total += 10
        if ace and self.total > 21:
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

    def eat_float(self):
        if self.chips < 1:
            self.chips = int(self.chips)
            return self.chips


dealer = Hand()
player = Hand()
deck = Deck()
bank = Bank()


def set_table():
    deck.new_deck()
    if dealer.hand == [] and player.hand == []:
        player.get_card()
        dealer.get_card()
        player.get_card()
        dealer.get_card()


def show_dealer():
    dealer.total = 0
    print("\n ** Dealer's Hand **")
    if player.stand:
        dealer.show_hand()
        print("\n Dealer Shows: " + str(dealer.score()))
    else:
        print("     - Hidden -\n" + "    " + str(dealer.hand[1]))
        print("\n Dealer Shows: " + str(dealer.hand[1].dealer_card()))


def show_player():
    player.total = 0
    print("\n ** Player's Hand ** ")
    player.show_hand()
    print("\n Player Has: " + str(player.score()))


def display():
    clear()
    print("\n You bet " + str(bank.bet) + " chips")
    show_dealer()
    show_player()


def wager():
    bank.eat_float()
    print("\nYou have " + str(bank.chips) + " chips!")
    if bank.chips <= 0:
        time.sleep(0.8)
        print("\nSorry, Game Over")
        exit()
    while True:
        try:
            bank.bet = int(input("\nPlease place your bet: "))
            if bank.bet <= 0:
                clear()
                print("\n> Must be positive integer")
                continue
            elif bank.bet > bank.chips:
                clear()
                print("\nSorry, you only have " + str(bank.chips) + " chips.")
                continue
        except ValueError:
            clear()
            print("\n> Must be positive integer")
            continue
        if bank.chips >= bank.bet:
            set_table()
            check_win()
    return bank.bet


def options():
    choose = input("\n(H)it, (S)tand, (D)ouble ").lower()
    if choose == 'h':
        player.get_card()
        check_win()
    elif choose == 's':
        player.stand = True
        show_dealer()
        while True:
            if dealer.total < 17:
                dealer.get_card()
                display()
                continue
            else:
                check_win()
    elif choose == 'd':
        if bank.chips >= bank.bet * 2:
            bank.bet *= 2
            player.get_card()
            check_win()
        else:
            print("\nSorry, not enough chips to double")


def new_hand():
    dealer.hand = []
    player.hand = []
    while True:
        again = input("\nPlay another hand? (Y/n) ").lower()
        clear()
        if again == "y":
            player.stand = False
            wager()
        elif again == "n":
            print("Thanks for playing!")
            exit()
        else:
            continue


def check_win():
    display()
    while True:
        if player.total == 21:
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


def greeter():
    print("\nWelcome to Python Blackjack!")
    while True:
        try:
            bank.chips = int(input("\nHow many chips would you like to buy?\n"))
            if bank.chips <= 0:
                clear()
                print("\n> Must be positive integer")
                continue
            clear()
            wager()
        except ValueError:
            clear()
            print("\n> Must be positive integer")
            continue


if __name__ == "__main__":
    greeter()
