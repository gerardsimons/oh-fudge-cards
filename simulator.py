import json
import os

import click
import time

from controllers import GameController
from encoders import ComplexJSONEncoder
from models import Player
from player_controllers import FullyRandomPlayer


@click.command()
@click.argument('output', nargs=1, type=click.Path(exists=True))
@click.option('--rounds', default=10, help='Number of rounds per game.')
@click.option('--games', default=1, help='Number of games to play')
def automated_game(output, rounds, games):

    for game_i in range(games):

        players = list()
        for i in range(4):
            player_ctrl = FullyRandomPlayer(Player("player_" + str(i)))
            players.append(player_ctrl)

        ge = GameController(players, nr_rounds=rounds)
        ge.start_game()

        time_stamp = str(int(time.time() * 1000)) # Millisecond accuracy I think
        new_file = open(os.path.join(output, 'game_{}.json'.format(time_stamp)), mode='w')
        json.dump(ge.repr_json(), new_file, cls=ComplexJSONEncoder, indent=4)

if __name__ == '__main__':
    automated_game()