from models import Player, Card, FudgeGame, Round, Play, GameException, FudgeHand, Score
from logging import log, log_play
from player_controllers import SimpleAIPlayer

import game_logic


class GameController(object):
    def finish_round(self):
        if not self.game_round:
            raise GameException("Round is not finished")
        else:
            self.rounds_hist.append(self.game_round)

    def play_new_round(self):
        pass

    def start_game(self, nr_players=4, nr_rounds=2):

        # Initialize player controllers
        self.player_ais = dict()
        for i in range(nr_players):
            player = Player("player_" + str(i))
            player_ctrl = SimpleAIPlayer(player)

            self.player_ais[player] = player_ctrl

        self.game = FudgeGame(list(self.player_ais.keys()), nr_rounds)
        final_score = Score(self.game.players)

        while not self.game.is_finished():
            game_round = self.game.new_round()
            log("New round started! Trump card is {}".format(game_round.trump))

            # Deal cards to players
            for player, player_ctrl in self.player_ais.items():

                player.hand = game_round.deck.draw_cards(game_round.round_nr)

                # Ask the player controllers for moves
                bid = player_ctrl.request_bid()
                game_round.record_bid(player, bid)

                log("{} bids {}".format(player, bid))

            for i in range(game_round.round_nr):
                
                play = game_round.new_play()
                for player in play.next_player():
                    while True:  # Keep requesting moves until valid move is played
                        player_ai = self.player_ais[player]
                        card = player_ai.request_move(self.game)  # Request move from player
                        # print("Player wants to play " + str(card))
                        if game_logic.is_valid_play(player, play, card):
                            log_play(player, card)

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
            print("ROUND SCORES")
            print(scores)

            final_score += scores

        print("FINAL SCORE : ")
        print(final_score)

    def display(self):
        pass

        # Call display on all the views ...
