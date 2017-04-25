from models import Player, Card, Game, Round, Play
from logging import log, log_play
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
        self.game_round = Round(len(self.rounds_hist) + 1, self.game.players, self.player_start_i)
        self.rounds_hist.append(self.game_round)
        log("New round started! Trump card is {}".format(self.game_round.trump))

        # Deal cards to players
        for player, player_ctrl in self.player_ais.items():
            player.cards = self.game_round.deck.draw_cards(self.game_round.round_nr)

            # Ask the player controllers for moves
            bid = player_ctrl.request_bid()
            self.game_round.record_bid(player, bid)

            log("{} bids {}".format(player, bid))


        for i in range(self.game_round.round_nr):
            # play = None
            last_play = self.game.last_play()
            if last_play:

                # Find player start i
                start_i = 0
                # winner = last_play.winner
                for i, player in enumerate(self.players):
                    if player == last_play.winner:
                        start_i = i
                        break

                print("{} won the last round, so he starts.".format(self.players[start_i]))
                play = Play(self.game_round.trump, self.game.players, start_i)


            else:
                play = Play(self.game_round.trump, self.game.players, self.player_start_i)
                # self.plays.append(p)

            print("NEW PLAY")
            for player in play.next_player():
                valid_play = False

                while not valid_play:  # Keep requesting moves until valid move is played
                    player_ai = self.player_ais[player]
                    card = player_ai.request_move(self.game)  # Request move from player
                    if game_logic.is_valid_play(player, play, card):
                        log_play(player, card)

                        # Mave the card from the player into the game field
                        player.remove_card(card)
                        # Record move
                        play.record_play(player, card)
                        break

            self.game_round.plays.append(play)
            # Determine winner of play
            game_logic.determine_play_winner(play)
            log("Player {} won the play.".format(play.winner))

        print("ROUND FINISHED")

    def start_game(self, nr_players=4, nr_rounds=2):

        # Initialize player controllers
        self.player_ais = dict()
        for i in range(nr_players):
            player = Player("player_" + str(i))
            player_ctrl = SimpleAIPlayer(player, )

            self.player_ais[player] = player_ctrl

        self.game = Game(self.player_ais.keys(), nr_rounds)

        while True: # The main loop
            if not self.game.is_finished():
                self.play_new_round()

                # Round finished, update score model
                scores = game_logic.determine_scores(self.game_round)
                print(scores)

                # return

            self.display()

    def display(self):
        pass

        # Call display on all the views ...

