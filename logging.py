from views import EmojiCardView

def log_play(player, card):
    print(" {} played {}".format(player, EmojiCardView(card)))

def log(msg):
    print(msg)