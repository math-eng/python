# template for "Stopwatch: The Game"
import simplegui

# define global variables
time_tenth_sec = 0
number_of_hit = 0
number_of_stop = 0

# define helper function format that converts time
# in tenths of seconds into formatted string A:BC.D
def format(t):
    D = str(t % 10)
    A = str(int(t / 10 / 60))
    BC = str((int(t / 10)) % 60)
    if len(BC) < 2:
        BC = "0" + BC
    return A + ":" + BC + "." + D
    
# define event handlers for buttons; "Start", "Stop", "Reset"
def start():
    timer.start()
    
def stop():
    global number_of_hit, number_of_stop
    if timer.is_running():
        number_of_stop += 1
        if time_tenth_sec % 10 == 0:
            number_of_hit += 1
    timer.stop()
    
def reset():
    global time_tenth_sec, number_of_hit, number_of_stop
    timer.stop()
    time_tenth_sec = 0
    number_of_hit = 0
    number_of_stop = 0

# define event handler for timer with 0.1 sec interval
def timer_handler():
    global time_tenth_sec
    time_tenth_sec += 1

# define draw handler
def draw_handler(canvas):
    canvas.draw_text(format(time_tenth_sec), (60, 120), 72, "White")
    canvas.draw_text(str(number_of_hit) + "/" + str(number_of_stop), (240, 25), 32, "Green")

# create frame
frame = simplegui.create_frame("Stopwatch", 300, 200)
timer = simplegui.create_timer(100, timer_handler)

# register event handlers
frame.set_draw_handler(draw_handler)
start_button = frame.add_button("Start", start, 100)
stop_button = frame.add_button("Stop", stop, 100)
reset_button = frame.add_button("Reset", reset, 100)

# start frame
frame.start()


# Please remember to review the grading rubric