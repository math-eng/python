# Implementation of classic arcade game Pong

import simplegui
import random

# initialize globals - pos and vel encode vertical info for paddles
WIDTH = 600
HEIGHT = 400       
BALL_RADIUS = 20
PAD_WIDTH = 8
PAD_HEIGHT = 80
HALF_PAD_WIDTH = PAD_WIDTH / 2
HALF_PAD_HEIGHT = PAD_HEIGHT / 2
paddle_speed = 3

# helper function that spawns a ball by updating the 
# ball's position vector and velocity vector
# if right is True, the ball's velocity is upper right, else upper left
def ball_init(right):
    global ball_pos, ball_vel # these are vectors stored as lists
    ball_pos = [WIDTH / 2, HEIGHT / 2]
    ball_vel = [random.randrange(120, 240) / 60, -random.randrange(60, 180) / 60]
    if not right:
        ball_vel[0] *= -1

def paddle_vertices(paddle_center):
    upper_left = (paddle_center[0] - HALF_PAD_WIDTH, paddle_center[1] - HALF_PAD_HEIGHT)
    upper_right = (paddle_center[0] + HALF_PAD_WIDTH, paddle_center[1] - HALF_PAD_HEIGHT)
    lower_right = (paddle_center[0] + HALF_PAD_WIDTH, paddle_center[1] + HALF_PAD_HEIGHT + 1)
    lower_left = (paddle_center[0] - HALF_PAD_WIDTH, paddle_center[1] + HALF_PAD_HEIGHT + 1)
    return [upper_left, upper_right, lower_right, lower_left]

def ball_hit_paddle(paddle_pos):
    global ball_pos
    return ball_pos[1] >= paddle_pos - HALF_PAD_HEIGHT and ball_pos[1] <= paddle_pos + HALF_PAD_HEIGHT

# define event handlers
    
def new_game():
    global paddle1_pos, paddle2_pos, paddle1_vel, paddle2_vel  # these are floats
    global score1, score2  # these are ints
    global paddle_speed
    score1 = 0
    score2 = 0
    paddle1_pos = HEIGHT / 2
    paddle2_pos = HEIGHT / 2
    paddle1_vel = 0.0
    paddle2_vel = 0.0
    ball_init(random.choice([True, False]))

def draw(c):
    global score1, score2, paddle1_pos, paddle2_pos, ball_pos, ball_vel
 
    # update paddle's vertical position, keep paddle on the screen
    paddle1_pos += paddle1_vel
    if paddle1_pos < HALF_PAD_HEIGHT or paddle1_pos >= HEIGHT - HALF_PAD_HEIGHT - 1:
        paddle1_pos -= paddle1_vel
    paddle2_pos += paddle2_vel
    if paddle2_pos < HALF_PAD_HEIGHT or paddle2_pos >= HEIGHT - HALF_PAD_HEIGHT - 1:
        paddle2_pos -= paddle2_vel
    
    # draw mid line and gutters
    c.draw_line([WIDTH / 2, 0],[WIDTH / 2, HEIGHT], 1, "White")
    c.draw_line([PAD_WIDTH, 0],[PAD_WIDTH, HEIGHT], 1, "White")
    c.draw_line([WIDTH - PAD_WIDTH, 0],[WIDTH - PAD_WIDTH, HEIGHT], 1, "White")
    
    # draw paddles
    c.draw_polygon(paddle_vertices([HALF_PAD_WIDTH, paddle1_pos]), 1, "White", "White")
    c.draw_polygon(paddle_vertices([WIDTH - HALF_PAD_WIDTH, paddle2_pos]), 1, "White", "White")
    
    # update ball
    ball_pos[0] += ball_vel[0]
    ball_pos[1] += ball_vel[1]
    if (ball_pos[1] - BALL_RADIUS <= 0) or (ball_pos[1] + BALL_RADIUS >= HEIGHT - 1):
        ball_vel[1] *= -1
    if ball_pos[0] - BALL_RADIUS <= PAD_WIDTH - 1:
        if ball_hit_paddle(paddle1_pos):
            ball_vel[0] *= -1.1
            ball_vel[1] *= 1.1
        else:
            score2 += 1
            ball_init(True)
    elif ball_pos[0] + BALL_RADIUS >= WIDTH - 1 - PAD_WIDTH:
        if ball_hit_paddle(paddle2_pos):
            ball_vel[0] *= -1.1
            ball_vel[1] *= 1.1
        else:
            score1 += 1
            ball_init(False)
        
    # draw ball and scores
    c.draw_circle(ball_pos, BALL_RADIUS, 1, "White", "White")
    c.draw_text(str(score1), (WIDTH / 4, 30), 36, "White")
    c.draw_text(str(score2), (WIDTH * 3 / 4, 30), 36, "White")
        
        
def keydown(key):
    global paddle1_vel, paddle2_vel
    global down_key1, down_key2
    if key == simplegui.KEY_MAP['w']:
        paddle1_vel = -paddle_speed
        down_key1 = 'w'
    elif key == simplegui.KEY_MAP['s']:
        paddle1_vel = paddle_speed
        down_key1 = 's'
    elif key == simplegui.KEY_MAP['up']:
        paddle2_vel = -paddle_speed
        down_key2 = 'up'
    elif key == simplegui.KEY_MAP['down']:
        paddle2_vel = paddle_speed
        down_key2 = 'down'
    else:
        print "Control keys are 'w', 's' for player 1 and 'up', 'down' for player 2"
   
def keyup(key):
    global paddle1_vel, paddle2_vel
    if (key == simplegui.KEY_MAP['w'] or key == simplegui.KEY_MAP['s']) and key == simplegui.KEY_MAP[down_key1]:
        paddle1_vel = 0
    elif (key == simplegui.KEY_MAP['up'] or key == simplegui.KEY_MAP['down']) and key == simplegui.KEY_MAP[down_key2]:
        paddle2_vel = 0


# create frame
frame = simplegui.create_frame("Pong", WIDTH, HEIGHT)
frame.set_draw_handler(draw)
frame.set_keydown_handler(keydown)
frame.set_keyup_handler(keyup)
frame.add_button("Restart", new_game)

# start game
new_game()

# start frame
frame.start()