import constants
from models import Card

EMOJI_DICT = {
    "H":"❤️",
    "D":"♦️",
    "C":"♣",
    "S":"♠"
}

class EmojiCardView(object):

    def __init__(self, card):
        self.value = str(card.symbol) + EMOJI_DICT[card.suit]
        # self.emoji = 

    def __str__(self):
        return self.value

class View(object):

    def __init__(self, width, height):
        self.width = width
        self.height = height

class TextView(View):
    pass

class TextCardView(TextView):
    def __init__(width, height):
        self.__super__(width, height)    

class TextGameView(TextView):

    def __init__(self, game, width, height):
        self.game = game

        # Sanity check parameters TODO
        self.__super__()
        self.width = width
        self.height = height

    def display(self):
        corner_char = "*"
        lining_hor = "-"
        lining_ver = "|"

        inner_width = (self.width - 2)
        inner_height = (self.height - 2)

        string = corner_char + inner_width * lining_hor + corner_char + "\n"
        string += inner_height * (lining_ver + ' ' * inner_width + lining_ver + "\n")
        string += corner_char + inner_width * lining_hor + corner_char + "\n"

        print(string)


class CardView(object):

    def __init__():
        pass


class GameView(object):

    def __init__(self, game):
        pass
