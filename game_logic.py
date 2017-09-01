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
    if card.suit == play.trump.suit: # If it's trump it should be higher than any other non trump card
        value += len(constants.SYMBOLS)
        return value
    elif card.suit != play.suit: # If the card is not even the current suit, it's worthless
        return 0
    else:
        return value

    # for i, s in enumerate(constants.SYMBOLS):
    #     if s == card.rank:
    #         value += i
    #         break
    #
    # return value

def determine_play_winner(play):
    max_card_value = 0
    winner = None
    for player, card in play.plays.items():
        card_val = card_value(play, card)
        print("{} card {} has value {}".format(player, card, card_val))
        if card_val > max_card_value:
            # print(max_card_value)
            max_card_value = card_val
            winner = player
    play.winner = winner
    return winner