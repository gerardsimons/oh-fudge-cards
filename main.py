from models import Card, Deck, Round, Player, Game
from views import EmojiCardView, TextGameView
from controllers import GameController

import game_logic
import constants

def automated_game():
    ge = GameController()

    # This usually comes from the user
    ge.start_game()




if __name__ == '__main__':
    automated_game()