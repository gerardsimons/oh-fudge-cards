class SimpleAIPlayer(object):

    def __init__(self, player):
        self.player = player

    def request_bid(self): 
        # A player would need more information than this 
        # in order to make a sensible bid
        return 1

    # def deal_cards(self, cards):
    #     self.cards = cards

    def request_move(self, game):

        # Check which cards match the leading suit
        if not self.player.cards:
            raise ValueError("Player does not have any cards left")
        return self.player.cards[0]
    
        # return False