# implementation of card game - Memory

import simplegui
import random

# global variables
FONT_SIZE = 80
FONT_POS = [6, 80]
DECK = range(0, 8)
DECK.extend(range(0, 8))

# helper function to initialize globals
def init():
    global num_of_turns, exposed, flipped, DECK
    random.shuffle(DECK)
    num_of_turns = 0
    exposed = [False for k in DECK]
    flipped = []
    label.set_text("Moves = 0")

     
# define event handlers
def mouseclick(pos):
    # add game state logic here
    global num_of_turns
    index = pos[0] // 50
    if not exposed[index]:
        flipped.append(index)
        exposed[index] = True
        num_of_turns += 1
        if num_of_turns % 2 == 0:
            label.set_text("Moves = " + str(num_of_turns // 2))
        if len(flipped) == 3:
            if DECK[flipped[0]] != DECK[flipped[1]]:
                exposed[flipped[0]] = False
                exposed[flipped[1]] = False
            flipped.pop(0)
            flipped.pop(0)


# cards are logically 50x100 pixels in size    
def draw(canvas):
    global DECK
    for k in range(len(DECK)):
        if exposed[k]:
            pos = list(FONT_POS)
            pos[0] += k * 50
            canvas.draw_text(str(DECK[k]), pos, FONT_SIZE, "White")
        else:
            canvas.draw_polygon([[50 * k, 0], [50 * (k + 1), 0],
                                 [50 * (k + 1), 100], [50 * k, 100]],
                                1, "White", "Green")


# create frame and add a button and labels
frame = simplegui.create_frame("Memory", 800, 100)
frame.add_button("Restart", init)
label = frame.add_label("Moves = 0")

# initialize global variables
init()

# register event handlers
frame.set_mouseclick_handler(mouseclick)
frame.set_draw_handler(draw)

# get things rolling
frame.start()


# Always remember to review the grading rubric