from models import Player, Card, FudgeGame, Round, Play, GameException, FudgeHand, Score
from logging import log, log_play
from player_controllers import SimpleAIPlayer

import game_logic


class GameController(object):

    def __init__(self, player_controllers, nr_rounds=2):
        self.player_controllers = player_controllers
        self.nr_rounds = nr_rounds

        self._player_register = dict()
        for ctrl in self.player_controllers:
            self._player_register[ctrl.player] = ctrl

    def finish_round(self):
        if not self.game_round:
            raise GameException("Round is not finished")
        else:
            self.rounds_hist.append(self.game_round)

    def start_game(self):

        self.game = FudgeGame(list(self._player_register.keys()), self.nr_rounds)
        final_score = Score(self.game.players)

        while not self.game.is_finished():
            game_round = self.game.new_round()
            log("New round started! Trump card is {}".format(game_round.trump))

            # Deal cards to players
            for player_contr in self.player_controllers:

                player = player_contr.player
                player.hand = game_round.deck.draw_cards(game_round.round_nr)

                # Ask the player controllers for moves
                bid = player_contr.request_bid()
                game_round.record_bid(player, bid)

                log("{} bids {}".format(player, bid))

            for i in range(game_round.round_nr):
                
                play = game_round.new_play()
                for player in play.next_player():
                    while True:  # Keep requesting moves until valid move is played
                        player_ctrl = self._player_register[player]
                        card = player_ctrl.request_move(self.game)  # Request move from player
                        # print("Player wants to play " + str(card))
                        if game_logic.is_valid_play(player, play, card):
                            log_play(player, card)

                            card.value = game_logic.card_value(play, card)

                            # Mave the card from the player into the game field
                            player.remove_card(card)
                            # Record move
                            play.record_play(player, card)
                            break

                # Determine winner of play
                game_logic.determine_play_winner(play)
                log("Player {} won the play.".format(play.winner))

            print("ROUND FINISHED")

            # Round finished, update score model
            scores = game_logic.determine_scores(game_round)
            for k, v in scores.items():
                k.score += v

            print("ROUND SCORES")
            print(scores)

            final_score += scores

        print("FINAL SCORE : ")
        print(final_score)

    def display(self):
        pass

        # Call display on all the views ...
