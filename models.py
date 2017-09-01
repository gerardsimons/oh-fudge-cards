import random
import constants

from cardsource import Card, Hand, Deck


class FudgeCard(object):
    RANKS = Card.RANKS.replace('X', '')  # no jokers in blackjack
    VALUES = {
        '2': 2,
        '3': 3,
        '4': 4,
        '5': 5,
        '6': 6,
        '7': 7,
        '8': 8,
        '9': 9,
        'T': 10,
        'J': 10,
        'Q': 10,
        'K': 10,
        'A': 11
    }

    def __int__(self):
        return self.VALUES[self.rank]

    def __eq__(self, other):
        """
        Checks if 2 cards have the same rank
        """
        if not isinstance(other, FudgeCard):
            other = FudgeCard(other)

        return self.VALUES[self.rank] == self.VALUES[other.rank]


class GameException(Exception):
    pass

class FudgeGame(object):
    
    def __init__(self, players, n_rounds):
        self.n_rounds = n_rounds
        self.round_nr = 0
        self.players = players
        self.player_start_i = random.randint(0, len(players) - 1) # Assign first player randomly
        
        self.rounds = list()

    def is_finished(self):
        return len(self.rounds) >= self.n_rounds

    def last_play(self):
        last_round = self.last_round()
        if last_round:
            return last_round.last_play()
        else:
            return None

    def last_round(self):
        if len(self.rounds):
            return self.rounds[len(self.rounds) - 1]

    def new_round(self):
        new_round = Round(len(self.rounds) + 1, self.players, self.player_start_i)
        self.rounds.append(new_round)
        return new_round


class Round(object):

    def __init__(self, round_nr, players, player_start_i):
        self.round_nr = round_nr

        self.deck = FudgeDeck()
        self.deck.shuffle()
        self.trump = self.deck.pop()
        self.players = players
        self.player_start_i = player_start_i

        self.bids = dict()
        self.plays = list()

    def next_player(self):
        for player in self.players:
            yield player

    def last_play(self):
        if self.plays:
            return self.plays[len(self.plays) - 1]

    def new_play(self):
        last_play = self.last_play()
        if last_play:

            # Find last winner index
            start_i = 0
            for i, player in enumerate(self.players):
                if player == last_play.winner:
                    start_i = i
                    break

            play = Play(self.trump, self.players, start_i)
        else:
            play = Play(self.trump, self.players, self.player_start_i)

        self.plays.append(play)
        return play
            # self.plays.append(p)


    def record_bid(self, player, bid):
        self.bids[player] = bid



class Play(object):

    def __init__(self, trump, players, player_start_i):
        if not players:
            raise ValueError("Invalid number of players for play")

        # self.players = players
        self.trump = trump
        self.players = players[player_start_i:] + players[:player_start_i]
        self.plays = dict()
        self.suit = None
        self.winner = None

    def next_player(self):
        for player in self.players:
            yield player

    def is_complete(self):
        for player in self.players:
            if player not in self.plays:
                return False

        return True

    def record_play(self, player, card):
        # if player is not self.expected_player:
            # raise ValueError("Player's play is out of order") # TODO: Make custom exception
        # else:

        # TODO: Check that play is not out of turn
        self.plays[player] = card
            # expected_player = 
        if self.suit is None:
            self.suit = card.suit

    def __str__(self):
        string = ""
        for c in self.cards:
            string += str(c)

        return string

class Player(object):

    def __init__(self, name):
        self.score = 0
        self.hand = FudgeHand()
        self.name = name

    def __str__(self):
        return "Player '{}'".format(self.name)

    def remove_card(self, card):
        # print("Remove card ...")
        self.hand.take_card(card)

    def get_cards_suit(self, suit):
        suit_cards = list()
        for c in self.cards:
            if c.suit == suit:
                suit_cards.append(c)

        return suit_cards

    def has_suit(self, suit):
        return self.hand.has_suit(suit)

    def give_card(self, card):
        self.hand.append(card)


class Score(object):

    def __init__(self, players):
        self.scores = dict()

        for p in players:
            self.scores[p] = 0

    def add_points(self, player, points):
        self.scores[player] += points

    def __str__(self):
        # string = "PLAYER SCORES:\n"
        string = "---------------------------\n"
        for p, score in self.scores.items():
            string += "\t{} : {}\n".format(p, score)
        string += "---------------------------\n"
        return string

    def __add__(self, x):
        for i, k in self.scores.items():
            try:
                self.scores[i] += x.scores[i]
            except IndexError as e:
                raise ValueError("Other score does not contain player {}".format(i))
        return self

class FudgeDeck(Deck):

    def draw_cards(self, index):
        if index < 1 or index > len(self):
            raise ValueError("Invalid number of cards to draw")
        hand = FudgeHand()

        for _ in range(index):
            hand.append(self.pop())

        return hand

class FudgeHand(Hand):

    def __init__(self, cards=[]):
        self._cards = cards

    def has_suit(self, suit):

        for c in self._cards:
            if c.suit == suit:
                return True

        return False

    def take_card(self, card):
        for i, c in enumerate(self._cards):
            if c == card:
                del self._cards[i]
                return

        raise ValueError("No such card in this hand")