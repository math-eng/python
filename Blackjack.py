# Mini-project #6 - Blackjack

import simplegui
import random

# load card sprite - 949x392 - source: jfitz.com
CARD_SIZE = (73, 98)
CARD_CENTER = (36.5, 49)
card_images = simplegui.load_image("http://commondatastorage.googleapis.com/codeskulptor-assets/cards.jfitz.png")

CARD_BACK_SIZE = (71, 96)
CARD_BACK_CENTER = (35.5, 48)
card_back = simplegui.load_image("http://commondatastorage.googleapis.com/codeskulptor-assets/card_back.png")    

# initialize some useful global variables
in_play = False
outcome = ""
score = 0

# define globals for cards
SUITS = ('C', 'S', 'H', 'D')
RANKS = ('A', '2', '3', '4', '5', '6', '7', '8', '9', 'T', 'J', 'Q', 'K')
VALUES = {'A':1, '2':2, '3':3, '4':4, '5':5, '6':6, '7':7, '8':8, '9':9, 'T':10, 'J':10, 'Q':10, 'K':10}


# define card class
class Card:
    def __init__(self, suit, rank):
        if (suit in SUITS) and (rank in RANKS):
            self.suit = suit
            self.rank = rank
        else:
            self.suit = None
            self.rank = None
            print "Invalid card: ", suit, rank

    def __str__(self):
        return self.suit + self.rank

    def get_suit(self):
        return self.suit

    def get_rank(self):
        return self.rank

    def draw(self, canvas, pos):
        card_loc = (CARD_CENTER[0] + CARD_SIZE[0] * RANKS.index(self.rank), 
                    CARD_CENTER[1] + CARD_SIZE[1] * SUITS.index(self.suit))
        canvas.draw_image(card_images, card_loc, CARD_SIZE, [pos[0] + CARD_CENTER[0], pos[1] + CARD_CENTER[1]], CARD_SIZE)
        
# define hand class
class Hand:
    def __init__(self):
        # create Hand object
        self.hand = []

    def __str__(self):
        # return a string representation of a hand
        if len(self.hand) == 0:
            return ""
        else:
            return " ".join([str(card) for card in self.hand])

    def add_card(self, card):
        # add a card object to a hand
        self.hand.append(card)

    def get_value(self):
        # count aces as 1, if the hand has an ace, then add 10 to hand value if it doesn't bust
        # compute the value of the hand, see Blackjack video
        if len(self.hand) == 0:
            return 0
        else:
            rank = [card.get_rank() for card in self.hand]
            val = sum([VALUES[r] for r in rank])
            if ('A' in rank) and val + 10 <= 21:
                return val + 10
            else:
                return val
   
    def draw(self, canvas, pos):
        # draw a hand on the canvas, use the draw method for cards
        for i in range(0, min(5, len(self.hand))):
            self.hand[i].draw(canvas, (pos[0] + i * (CARD_SIZE[0] + 20), pos[1]))
        if len(self.hand) > 5:
            for i in range(5, len(self.hand)):
                self.hand[i].draw(canvas, (pos[0] + (i - 5) * (CARD_SIZE[0] + 20),
                                           pos[1] + CARD_SIZE[1] + 10))

# define deck class 
class Deck:
    def __init__(self):
        # create a Deck object
        self.deck = [Card(s, r) for s in SUITS for r in RANKS]

    def shuffle(self):
        # add cards back to deck and shuffle
        # use random.shuffle() to shuffle the deck
        self.deck = [Card(s, r) for s in SUITS for r in RANKS]
        random.shuffle(self.deck)

    def deal_card(self):
        # deal a card object from the deck
        return self.deck.pop()
    
    def __str__(self):
        # return a string representing the deck
        return " ".join([str(card) for card in self.deck])

#define event handlers for buttons
def deal():
    global deck, outcome, in_play, score, deck, player, dealer

    if not in_play:
        deck = Deck()
        deck.shuffle()
        player, dealer = Hand(), Hand()
        for i in range(0, 2):
            player.add_card(deck.deal_card())
            dealer.add_card(deck.deal_card())

        in_play = True
        outcome = ""
    else:
        in_play = False
        outcome = "You lost!"
        score -= 1

def hit():
    # replace with your code below
    # if the hand is in play, hit the player
    # if busted, assign a message to outcome, update in_play and score
    global deck, in_play, outcome, score, player
    if in_play:
        player.add_card(deck.deal_card())
        val = player.get_value()
        if val > 21:
            outcome = "You have busted"
            in_play = False
            score -= 1
    else:
        outcome = "Click Deal to start a new game!"

def stand():
    # replace with your code below
    # if hand is in play, repeatedly hit dealer until his hand has value 17 or more
    # assign a message to outcome, update in_play and score
    global deck, in_play, outcome, score, dealer
    if in_play:
        while dealer.get_value() < 17:
            dealer.add_card(deck.deal_card())
        dval = dealer.get_value()
        if dval > 21:
            outcome = "Dealer has busted. You win!"
            score += 1
        elif dval >= player.get_value():
            outcome = "You lost!"
            score -= 1
        else:
            outcome = "You win!"
            score += 1
        in_play = False
    else:
        outcome = "Click Deal to start a new game!"

# draw handler    
def draw(canvas):
    global dealer, player, score, outcome
    # test to make sure that card.draw works, replace with your code below
    # draw game title
    canvas.draw_text("Blackjack", [80, 50], 50, "Blue")
    # draw score
    canvas.draw_text("Score  " + str(score), [400, 50], 30, "Black")
    # draw dealer
    canvas.draw_text("Dealer", [50, 100], 30, "Black")
    dealer.draw(canvas, [50, 120])
    if in_play:
        canvas.draw_image(card_back, CARD_BACK_CENTER, CARD_BACK_SIZE,
                          [50 + CARD_BACK_CENTER[0], 120 + CARD_BACK_CENTER[1]],
                          CARD_BACK_SIZE)
    # draw dealer message
    canvas.draw_text(outcome, [200, 100], 30, "Black")
    # draw player
    canvas.draw_text("Player", [50, 360], 30, "Black")
    player.draw(canvas, [50, 380])
    # draw player message
    if in_play:
        canvas.draw_text("Hit or stand?", [200, 360], 30, "Black")
    else:
        canvas.draw_text("New deal?", [200, 360], 30, "Black")


# initialization frame
frame = simplegui.create_frame("Blackjack", 600, 600)
frame.set_canvas_background("Green")

#create buttons and canvas callback
frame.add_button("Deal", deal, 200)
frame.add_button("Hit",  hit, 200)
frame.add_button("Stand", stand, 200)
frame.set_draw_handler(draw)

deal()

# get things rolling
frame.start()


# remember to review the gradic rubric