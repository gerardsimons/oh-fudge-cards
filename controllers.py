from models import Player, Card, Game, Round
from logging import log
from player_controllers import SimpleAIPlayer

import game_logic

class GameController(object):
    
    def __init__(self):
        self.player_start_i = 0
        self.rounds_hist = list()

    def new_round(self):
        return game_round

    def finish_round(self):
        if not self.current_round:
            raise GameException("Round is not finished")
        else:
            self.rounds_hist.append(self.game_round)

    def play_new_round(self):
        self.player_start_i += 1
        self.player_start_i = self.player_start_i % len(self.game.players)
        game_round = Round(len(self.rounds_hist) + 1, self.game.players, self.player_start_i)
        self.rounds_hist.append(game_round)
        log("New round started! Trump card is {}".format(game_round.trump))

        # Deal cards to players
        for player, player_ctrl in zip(self.game.players, self.player_ctrls):
            player.cards = game_round.deck.draw_cards(game_round.round_nr)

            # Ask the player controllers for moves
            bid = player_ctrl.request_bid()
            game_round.record_bid(player, bid)

            log("{} bids {}".format(player, bid))

        for play in self.next_play():
            print("NEW PLAY")
            for player in play.next_player():
                while True: # Keep requesting moves until valid move is played
                
                    card = player.request_move(game) # Request move from player
                    if play.suit is None or play.suit == card.suit:

                        # Mave the card from the player into the game field
                        played_card = player.remove_card(card)

                        # Record move
                        logger.log_play(player, card)
                        play.record_play(player, card)
                        break
                    else:

                        # Check if player has suit
                        if player.has_suit(play.suit):
                            continue
                        else:
                            logger.log("Player does not have {}.".format(play.suit)) 
                            logger.log_play(player, card)

                            # Mave the card from the player into the game field
                            played_card = player.remove_card(card)
                            # Record move
                            play.record_play(player, card)
                            break

            # Determine winner of play
            game_logic.determine_play_winner(play)

            logger.log("Player {} won the play.".format(play.winner))

        return game_round

    def start_game(self, nr_players=4, nr_rounds=2):

        # Initialize player controllers
        self.player_ctrls = list()
        players = list()
        for i in range(nr_players):
            player = Player("player_" + str(i))
            player_ctrl = SimpleAIPlayer(player, )

            players.append(player)
            self.player_ctrls.append(player_ctrl)

        self.game = Game(players, nr_rounds)
        # logger.log("New game started : {}".format(game))
        
        while True: # The main loop

            if not self.game.is_finished():
                game_round = self.play_new_round()

                # Round finished, update score model
                scores = game_logic.determine_scores(game_round)
                print(scores)

            self.display()

    def display(self):
        pass

        # Call display on all the views ...

    def next_play(self):
        
        for i in range(self.game.round_nr):
            last_play = self.last_play()
            if last_play:

                # Find player start i
                start_i = 0
                # winner = last_play.winner
                for i, player in enumerate(self.players):
                    if player == last_play.winner:
                        start_i = i
                        break

                print("{} won the last round, so he starts.".format(self.players[start_i]))
                p = Play(self.trump, self.players, start_i)
            else:                
                p = Play(self.trump, self.players, self.player_start_i)
                self.plays.append(p)
            yield p
