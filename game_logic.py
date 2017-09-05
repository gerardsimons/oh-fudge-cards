import constants

from collections import defaultdict

from models import Score

def determine_scores(game_round):

    wins_dict = defaultdict(int)

    for play in game_round.plays:
        wins_dict[play.winner] += 1

    player_scores = Score(game_round.players)
    for p, bid in game_round.bids.items():
        if bid == wins_dict[p]:
            player_scores.add_points(p, 10 + bid)

    return player_scores

def is_valid_play(player, play, card):
    if play.suit is None or play.suit == card.suit:
        return True
    elif not player.has_suit(play.suit):
        return True
        
    return False

def card_value(play, card):
    value = int(card)

    # print("Card suit = {}".format(card.suit))
    # print("Play suit = {}".format(play.suit))

    if card.suit == play.trump.suit: # If it's trump it should be higher than any other non trump card
        value += len(constants.SYMBOLS)
        return value
    elif card.suit != play.suit and play.suit is not None: # If the card is not even the current suit, it's worthless
        return 0
    else: # Otherwise just return the default value
        return value



def determine_play_winner(play):
    '''
    Assumes card values have been computed!
    :param play: The play for which to assess the card values depending on the play's trump and the cards played by the players.
    :return:
    '''
    max_card_value = 0
    winner = None
    for player, card in play.plays.items():
        if card.value > max_card_value:
            max_card_value = card.value
            winner = player

    assert winner is not None

    play.winner = winner
    return winner