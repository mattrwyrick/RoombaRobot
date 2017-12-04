"""
The Python Capstone Project.

CSSE 120 - Introduction to Software Development.
Team members: Bill Trevor Matt (all of them).

The primary author of this module is: Bill.
"""
# DONE: Put the names of ALL team members in the above where indicated.
#       Put YOUR NAME in the above where indicated.

import m0
import m1
import m3
import m4

import tkinter
from tkinter import ttk
import new_create
import random as rng
import time

class DataContainer():
    """ A container for the data shared across the application. """

    def __init__(self):
        """ Initializes instance variables (fields). """
        # Add     self.FOO = BLAH     here as needed.
        self.robot = new_create.Create('sim')
        self.port = None
        self.remote_speed_entry = None

class dc_wp():
    def __init__(self):
        self.count = 0
        self.points = []
        self.width = 700
        self.height = 600
        self.total_angle = 0
        self.x = 0
        self.y = 0

class dc2():
    def __init__(self):
        self.speed_lable = None
        self.turn_lable = None
        self.speed = 0
        self.turn = 0

def main():
    """
    Tests functions in this module.
    Intended to be used internally by the primary author of this module.
    """
    print('-------------------------------')
    print('Testing functions in module m2:')
    print('-------------------------------')
    dc = DataContainer()
    root = tkinter.Tk()
    frame = waypoints_frame(root, dc)
    frame.grid()

    root.mainloop()

def complex_movements_frame(root, dc):
    """
    This constructs the frame for complex movements. You input a side length and number of sides,
    and then the robot drives in a path of a regular polygon with those parameters
    """
    frame = ttk.Frame(root)
    frame.grid()
    length_entry = ttk.Entry(frame)
    sides_entry = ttk.Entry(frame)
    length_title = ttk.Label(frame, text='Enter side length')
    sides_title = ttk.Label(frame, text='Enter side count')
    sides_title.grid(row=0, column=0)
    sides_entry.grid(row=0, column=1)
    length_title.grid(row=1, column=0)
    length_entry.grid(row=1, column=1)
    go_button = ttk.Button(frame, text='Go')
    go_button['command'] = lambda:move_complex(sides_entry, length_entry, dc)
    go_button.grid(row=2, column=0)

    dc.current_frame = frame

def move_complex(sides_entry, length_entry, dc):
    """
    Moves the robot in a regular polygon path
    """
    sides = int(sides_entry.get())
    length = int(length_entry.get())
    angle = 180 - (sides - 2) * 180 / sides
    time_ = length / 50

    for _ in range(sides):
        dc.robot.driveDirect(50, 50)
        time.sleep(time_)
        print(time_)
        dc.robot.stop()
        dc.robot.driveDirect(15, -15)
        dc.robot.waitAngle(angle * (-1))
        dc.robot.stop()
        time.sleep(time_)  # I've got no idea why this has to be here, but it doesn't work without it

def waypoints_frame(frame, dc_r):
    """
    Creates a canvas that allows the input of 'waypoints,' the robot then moves to
    each of the specified waypoints after a button press
    """
    dc = dc_wp()
    main_frame = ttk.Frame(frame)
    main_frame.grid()
    bottom_frame = ttk.Frame(main_frame)
    bottom_frame.grid()
    canvas = tkinter.Canvas(main_frame, width=dc.width, height=dc.height, background='lightgrey')
    canvas.grid()
    canvas.create_line(dc.width / 2, 0, dc.width / 2, dc.height, fill='grey')
    canvas.create_line(0, dc.height / 2, dc.width, dc.height / 2, fill='grey')
    canvas.create_oval(dc.width / 2 - 13, dc.height / 2 - 13, dc.width / 2 + 13, dc.height / 2 + 13, fill='blue', width=3)
    canvas.create_text(dc.width / 2, dc.height / 2, text='R')
    go_button = ttk.Button(bottom_frame, text='Go')
    go_button.grid()

    dc = dc_wp()

    canvas.bind('<Button-1>', lambda event: click(event, dc))
    go_button['command'] = lambda:go(main_frame, dc, dc_r, canvas)

    main_frame.grid()

    dc_r.current_frame = main_frame

def click(event, dc):
    """
    gets the mouse clicks in the waypoints canvas and creates the circles
    representing the waypoints
    """
    dc.count += 1
    canvas = event.widget
    canvas.create_oval(event.x - 10, event.y - 10, event.x + 10, event.y + 10, fill='green', width=3)
    canvas.create_text(event.x, event.y, text=str(dc.count))
    dc.points += [[event.x - dc.width / 2, (event.y - (dc.height / 2)) * (-1)]]  # want the grid theoretically with origin at center of canvas
#     print(dc.points)

def go(frame, dc, dc_r, canvas):
    """
    Drives the robot to each waypoint
    """
#     frame.destroy()
    n_points = len(dc.points)
    x_tot = 0
    y_tot = 0
    c_direction = 1
    direction = None

    for k in range(0, n_points):
        print("Next Point:", dc.points[k])
        # get the x,y coordinants of next waypoint, assume start facing in +y axis
        x_dist = dc.points[k][0]
        y_dist = dc.points[k][1]

        # turn to face the proper direction for x axis movement
        if x_dist > x_tot:
            direction = 2
        else:
            direction = 4

        while not c_direction == direction:
            dc_r.robot.driveDirect(-15, 15)
            dc_r.robot.waitAngle(90)
            dc_r.robot.stop()
            c_direction -= 1
            if c_direction == 0:
                c_direction = 4
            time.sleep(1)


        dc_r.robot.driveDirect(50, 50)
        time.sleep(abs((x_dist - x_tot) / 50))

        dc_r.robot.stop()
        x_tot = x_dist

        # now the y
        if y_dist > y_tot:
            direction = 1
        else:
            direction = 3
        while not c_direction == direction:
            dc_r.robot.driveDirect(-15, 15)
            dc_r.robot.waitAngle(90)
            dc_r.robot.stop()
            c_direction -= 1
            if c_direction == 0:
                c_direction = 4
            time.sleep(1)

        dc_r.robot.driveDirect(50, 50)
        time.sleep(abs((y_dist - y_tot) / 50))
        dc_r.robot.stop()
        y_tot = y_dist
        print("X total:", x_tot, "\tY total:", y_tot)

#         canvas.destroy()


def tele_frame(root, dc):
    """
    Basically creates a remote control used to drive the robot.
    Makes two slide bars, one for forwards/backward speed, and the other for
    turning speed
    """
    frame = ttk.Frame(root, relief='raised', padding=(5, 5))

    # holds speed and turn values, also make title
    dc_2 = dc2()
    title = ttk.Label(frame, text='Remote Driving', padding=(0, 5))
    title.grid(column=1, row=0)

    # create the two scales
    speed_scale = ttk.Scale(frame, from_=50, to=-50, value=0, length=150, orient=tkinter.VERTICAL)
    turn_scale = ttk.Scale(frame, from_=-50, to=50, value=0, length=150)
    turn_scale.grid(column=1, row=2)
    speed_scale.grid(column=1, row=3)

    # create the lables for the scales
    speed_lable = ttk.Label(frame, text='0')
    turn_lable = ttk.Label(frame, text='0')
    speed_lable.grid(column=2, row=3)
    turn_lable.grid(column=2, row=2)
    dc_2.speed_lable = speed_lable
    dc_2.turn_lable = turn_lable

    # create the buttons
    go_button = ttk.Button(frame, text='Go')
    stop_button = ttk.Button(frame, text='Stop')
    reset_button = ttk.Button(frame, text='Reset')
    straighten_button = ttk.Button(frame, text='Straighten')
    go_button.grid(column=0, row=1)
    stop_button.grid(column=1, row=1)
    reset_button.grid(column=2, row=1)
    straighten_button.grid(column=0, row=2)
    go_button['command'] = lambda: set_speed(dc_2.speed, dc, dc_2)
    stop_button['command'] = lambda: stop(dc)
    reset_button['command'] = lambda: reset(speed_scale, speed_lable, turn_scale, turn_lable, dc, dc_2)
    straighten_button['command'] = lambda: straighten(dc, dc_2, turn_scale)

    # set up the commands for the scales
    speed_scale['command'] = lambda x: set_speed(x, dc, dc_2)
    turn_scale['command'] = lambda x: set_turn(x, dc, dc_2)

    frame.grid()
    dc.current_frame = frame

def set_speed(x, dc, dc2):
    speed = round(float(x))
    dc2.speed_lable['text'] = str(speed)
    dc2.speed = speed
    drive(dc, dc2)

def set_turn(x, dc, dc2):
    turn = round(float(x))
    dc2.turn_lable['text'] = str(turn)
    dc2.turn = turn
    drive(dc, dc2)

def stop(dc):
    dc.robot.stop()

def straighten(dc, dc2, turn_s):
    dc2.turn = 0
    dc2.turn_lable['text'] = 0
    turn_s['value'] = 0
    drive(dc, dc2)


def reset(speed_s, speed_l, turn_s, turn_l, dc, dc2):
    speed_s['value'] = 0
    speed_l['text'] = 0
    turn_s['value'] = 0
    turn_l['text'] = 0
    dc2.speed = 0
    dc2.turn = 0
    stop(dc)

def drive(dc, dc2):
    left = right = dc2.speed

    if dc2.speed > 0:
        if dc2.turn >= 0:
            if dc2.turn < dc2.speed:
                right -= dc2.turn
            else:
                right = 0
                left += dc2.turn - dc2.speed
                if left > 50:
                    left = 50
        else:
            if abs(dc2.turn) < dc2.speed:
                left -= abs(dc2.turn)
            else:
                left = 0
                right += abs(dc2.turn) - dc2.speed
                if right > 50:
                    right = 50
    else:  # fix from here
        if dc2.turn >= 0:
            if abs(dc2.turn) < abs(dc2.speed):
                right += dc2.turn
            else:
                right = 0
                left -= dc2.turn + dc2.speed
                if abs(left) > 50:
                    left = -50
        else:
            if abs(dc2.turn) < abs(dc2.speed):
                left -= dc2.turn
            else:
                left = 0
                right -= abs(dc2.turn) - abs(dc2.speed)
                if abs(right) > 50:
                    right = -50
    dc.robot.driveDirect(left, right)

def rand_notes_frame(root, dc):
    """
    Plays an inputed amount of random notes
    """
    frame = ttk.Frame(root, padding=(4, 10))
    play_b = ttk.Button(frame, text='play')
    title = ttk.Label(frame, text='Play n random notes')
    title.grid(row=0)
    play_b.grid(row=2)

    count_e = ttk.Entry(frame)
    count_e.grid(row=1)

    n_notes = count_e

    play_b['command'] = lambda: play_random(n_notes, dc)

    frame.grid()
    dc.current_frame = frame

def play_random(entry, dc):
    n = int(entry.get())
    for k in range(n):
        r = rng.randrange(31, 127)
        dc.robot.playNote(r, 50)
        print('played note', k, r)
        time.sleep(1)

# ----------------------------------------------------------------------
# If this module is running at the top level (as opposed to being
# imported by another module), then call the 'main' function.
# ----------------------------------------------------------------------
if __name__ == '__main__':
    main()
