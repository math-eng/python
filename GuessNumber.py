# template for "Guess the number" mini-project
# input will come from buttons and an input field
# all output for the game will be printed in the console

import simplegui
import math
import random

# initialize global variables used in your code
low = 0
high = 100
count = 7
number = 10

# define helper functions
def init():
    global low, high, count, number
    count = math.ceil(math.log(high - low) / math.log(2))
    number = random.randrange(low, high)
    print "New game. Range is from", low, "to", high
    print "Number of remaining guesses is", count
    print

# define event handlers for control panel
    
def range100():
    # button that changes range to range [0,100) and restarts
    global low, high, count, number
    low = 0
    high = 100
    init() 

def range1000():
    # button that changes range to range [0,1000) and restarts
    global low, high, count, number
    low = 0
    high = 1000
    init()
    
def get_input(guess):
    # main game logic goes here
    global count
    count -= 1
    print "Guess was ", guess
    print "Number of remaining guesses is ", count
    guessed = int(guess)
    if guessed < number and count > 0:
        print "Higher!"
    elif guessed > number and count > 0:
        print "Lower!"
    elif guessed == number:
        print "Correct!"
    else:
        print "You ran out of guesses. The number was ", number

    print
    
    if guessed == number or count == 0:
        init()

    
# create frame
frame = simplegui.create_frame("Guess the number", 300, 200)

# register event handlers for control elements
frame.add_button("Range: 0 - 100", range100, 200)
frame.add_button("Range: 0 - 1000", range1000, 200)
frame.add_input("Enter a guess", get_input, 200)

init()
# start frame
frame.start()

# always remember to check your completed program against the grading rubric