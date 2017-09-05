import random


class FullyRandomPlayer(object):

    def __init__(self, player):
        self.player = player

    def request_bid(self): 
        # A player would need more information than this 
        # in order to make a sensible bid
        print("Player {} holds {} cards".format(self.player.name, len(self.player.hand)))
        return random.randint(0, len(self.player.hand))

    # def deal_cards(self, cards):
    #     self.cards = cards

    def request_move(self, game):

        # Check which cards match the leading suit
        if not self.player.hand:
            raise ValueError("Player does not have any cards left")
        return random.sample(self.player.hand._cards, 1)[0]
    
    def repr_json(self):
        return dict(name=self.player.name, controller_type=type(self).__name__)