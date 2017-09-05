from views import EmojiCardView

def log_play(player, card):
    print(" {} played {}  (v={})".format(player, EmojiCardView(card), card.value))

def log(msg):
    print(msg)