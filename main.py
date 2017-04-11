from models import Card, Deck, Round, Player, Game

import game_logic
import constants

class GameLogger(object):

    def log_card_play(self, player, card):
        print("Player {} played {}".format(player, card))

    def log(self, msg):
        print(msg)

class GameEngine(object):

    def __init__(self):
        pass

    def start_new_game(self):

        logger = GameLogger()
        
        # Create default players
        players = list()
        for i in range(4):
            players.append(Player("player_" + str(i)))

        # Start game
        n_rounds = 2
        game = Game(players, n_rounds)
        logger.log("New game started : {}".format(game))

        while not game.finished():

            game_round = game.new_round()
            logger.log("New round started! Trump card is {}".format(game_round.trump))

            # Deal cards to players
            for player in game_round.next_player():
                player.cards = game_round.deck.draw_cards(game_round.round_nr)
                bid = player.request_bid()

                game_round.record_bid(player, bid)

                logger.log("{} bids {}".format(player, bid))

            for play in game_round.next_play():
                print("NEW PLAY")
                for player in play.next_player():

                    valid_move = False
                    while not valid_move: # Keep requesting moves until valid move is played
                    
                        card = player.request_move(game) # Request move from player
                        logger.log("{} attempts to play {}".format(player, card))
                        if play.suit is None or play.suit == card.suit:

                            logger.log("{} plays {}".format(player, card))
                            valid_move = True

                            # Mave the card from the player into the game field
                            played_card = player.remove_card(card)
                            # Record move
                            play.record_play(player, card)
                            valid_move = True
                        else:
                            # Check if player has suit
                            if player.has_suit(play.suit):
                                # logger.log("Cannot play card: Wrong suit.")
                                break
                            else:
                                logger.log("Player does not have {}.".format(play.suit)) 
                                logger.log("{} plays {}.".format(player, card))

                                # Mave the card from the player into the game field
                                played_card = player.remove_card(card)
                                # Record move
                                play.record_play(player, card)
                                valid_move = True

                # Determine winner of play
                game_logic.determine_play_winner(play)

                logger.log("Player {} won the play.".format(play.winner))
                
        # Round finished
        scores = game_logic.determine_scores(game_round)
        print(scores)

    def new_round():

            # Generate new trump card
            trump = random.sample(self.deck, 1)

            # Assign players new cards

if __name__ == '__main__':
    ge = GameEngine()

    ge.start_new_game()