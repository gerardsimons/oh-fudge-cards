import constants
from models import Card

EMOJI_DICT = {
    "H":"❤️",
    "D":"♦️",
    "C":"♣",️
    "S":"♠"️
}

class CardEmoji():

    def __init__(card):
        self.emoji = EMOJI_DICT[card.suit]

class CardView():

    def __init__():
        pass


class GameView():

    def __init__(self, game):
        
