import random
import constants

class Card(object):

    def __init__(self, symbol, suit):
        self.symbol = symbol
        self.suit = suit

    def __str__(self):
        return "{}{}".format(self.symbol, self.suit)


class GameException(Exception):
    pass

class Game(object):
    
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

        self.deck = Deck.gen_full_deck() # Recreate the deck
        self.trump = self.deck.draw_card()
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

    def is_complete():
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


class DeckEmptyException(Exception):
    pass

class Deck(object):

    def __init__(self, cards):
        self.cards = cards

    @classmethod
    def gen_full_deck(cls):
        cards = list()
        for suit in constants.SUITS:
            for symbol in constants.SYMBOLS:
                # print(suit)
                c = Card(symbol, suit)
                cards.append(c)

        return Deck(cards)

    def draw_cards(self, N):
        if N < 1:
            raise ValueError("Invalid number of cards requested")
        if len(self.cards) == 0:
            raise DeckEmptyException("Deck is empty")
        if N > len(self.cards):
            raise ValueError("More cards requested than are present in the deck")
        drawn = [self.cards.pop(random.randrange(len(self.cards))) for _ in range(N)]
        return drawn

    def draw_card(self):
        return self.draw_cards(1)[0]

    def __str__(self):
        string = ""
        for c in self.cards:
            string += str(c)

        return string

class Player(object):

    def __init__(self, name):
        self.score = 0
        self.cards = None
        self.name = name

    def __str__(self):
        return "Player '{}'".format(self.name)

    def remove_card(self, card):
        for i, c in enumerate(self.cards):
            if c == card:
                del self.cards[i]
                return 

        raise ValueError("Player does not hold card")

    def get_cards_suit(self, suit):
        suit_cards = list()
        for c in self.cards:
            if c.suit == suit:
                suit_cards.append(c)

        return suit_cards

    def has_suit(self, suit):
        for c in self.cards:
            if c.suit == suit:
                return True




class Score(object):

    def __init__(self, players):
        self.scores = dict()

        for p in players:
            self.scores[p] = 0

    def add_points(self, player, points):
        self.scores[player] += points

    def __str__(self):
        string = "PLAYER SCORES:\n"
        for p, score in self.scores.items():
            string += "\t{} : {}\n".format(p, score)

        return string