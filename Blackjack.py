# Mini-project #6 - Blackjack

try:
    import simplegui
except ImportError:
    import SimpleGUICS2Pygame.simpleguics2pygame as simplegui
import random

# load card sprite - 936x384 - source: jfitz.com
CARD_SIZE = (72, 96)
CARD_CENTER = (36, 48)
card_images = simplegui.load_image("http://storage.googleapis.com/codeskulptor-assets/cards_jfitz.png")

CARD_BACK_SIZE = (72, 96)
CARD_BACK_CENTER = (36, 48)
card_back = simplegui.load_image("http://storage.googleapis.com/codeskulptor-assets/card_jfitz_back.png")    

# initialize some useful global variables
in_play = False
outcome = ""
prompt = ""
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
            print ("Invalid card: ", suit, rank)

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
        self.hand = [] #Initialise empty list of cards

    def __str__(self):
        # return a string representation of a hand
        s = "Hand contains "
        for card in self.hand:
            s += str(card) + " "
        return s
            
    def add_card(self, card):
        self.hand.append(card)	# add a card object to a hand

    def get_value(self):
        # count aces as 1, if the hand has an ace, then add 10 to hand value if it doesn't bust
        value = 0
        ace_state = False
        for card in self.hand:
            if card.get_rank() == "A":
                ace_state = True
            value += VALUES[card.get_rank()]
        if ace_state:
            if value + 10 <= 21:
                return value + 10
            else: 
                return value
        else:
            return value
   
    def draw(self, canvas, pos): # draw a hand on the canvas, use the draw method for cards
        for card in self.hand:
            if pos == "p":
                card.draw(canvas, [100 * (self.hand.index(card) + 1),400])
            if pos == "d":
                if in_play:
                    canvas.draw_image(card_back, CARD_BACK_CENTER, CARD_BACK_SIZE,
                                      [100 + CARD_BACK_CENTER[0], 200 + CARD_BACK_CENTER[1]], 
                                      CARD_BACK_SIZE)
                card.draw(canvas, [100 * (self.hand.index(card) + 1),200])
            
        
# define deck class 
class Deck:
    def __init__(self):
        self.deck = [Card(suit,rank)for suit in SUITS for rank in RANKS]	# create a Deck object

    def shuffle(self):
        # shuffle the deck 
        random.shuffle(self.deck)   # use random.shuffle()

    def deal_card(self):
        return self.deck.pop()	# deal a card object from the deck
    
    def __str__(self):
        s = "Deck contains " # return a string representing the deck
        for card in self.deck:
            s += str(card) + " "
        return s
    
#define event handlers for buttons
def deal():
    global outcome, prompt, in_play, deck, player_hand, dealer_hand, score
    # your code goes here
    if in_play:
        outcome = "Dealer wins!" #Report player loss if deal pressed in middle of round
        score -= 1
    deck = Deck() #New deck every time deal is called
    deck.shuffle() #Shuffle Deck
    player_hand = Hand() #New hand for player
    for i in range(1,3): #Give player two cards
        player_hand.add_card(deck.deal_card())
    dealer_hand = Hand() #New hand for dealer
    for i in range(1,3): #Give dealer two cards
        dealer_hand.add_card(deck.deal_card())
    in_play = True
    prompt = "Hit or Stand?"


def hit():
    global outcome, prompt, in_play, score
    if in_play: # if the hand is in play, hit the player
        if player_hand.get_value() <= 21:
            player_hand.add_card(deck.deal_card())
            if player_hand.get_value()>21: # if busted, assign a message to outcome/prompt, update in_play and score
                outcome = "You have busted!" 
                prompt = "New Deal?"
                in_play = False
                score -= 1
                       
def stand():
    global outcome, prompt, in_play, score
    if player_hand.get_value()>21:
            outcome = "You have busted!" 
            prompt = "New Deal?"
    if in_play:
        while dealer_hand.get_value()<17: 
        # if hand is in play, repeatedly hit dealer until his hand has value 17 or more
            dealer_hand.add_card(deck.deal_card())
        if dealer_hand.get_value()>21: 
            # if busted, assign a message to outcome, update in_play and score
            outcome = "You have won!" 
            score += 1
        elif dealer_hand.get_value() >= player_hand.get_value():
            outcome = "Dealer wins!" 
            score -= 1
        else:
            outcome = "You have won!"
            score += 1
        prompt = "New Deal?"
        in_play = False

# draw handler    
def draw(canvas):
    # test to make sure that card.draw works, replace with your code below
    player_hand.draw(canvas, "p")
    dealer_hand.draw(canvas, "d")
    canvas.draw_text("Dealer", [100,160], 27, "Black", "sans-serif")
    canvas.draw_text("Player", [100,360], 27, "Black", "sans-serif")
    canvas.draw_text("Blackjack", [150,100],40,"Aqua", "sans-serif")
    canvas.draw_text(prompt, [250,360], 27,"Black", "sans-serif")
    canvas.draw_text(outcome, [250,160], 27, "Black", "sans-serif")
    canvas.draw_text("Score = " + str(score), [400,100], 27, "Black", "sans-serif")

# initialization frame
frame = simplegui.create_frame("Blackjack", 600, 600)
frame.set_canvas_background("Green")

#create buttons and canvas callback
frame.add_button("Deal", deal, 200)
frame.add_button("Hit",  hit, 200)
frame.add_button("Stand", stand, 200)
frame.set_draw_handler(draw)

# get things rolling
deal()
frame.start()
