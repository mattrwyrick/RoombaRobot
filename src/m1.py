"""
The Python Capstone Project.

CSSE 120 - Introduction to Software Development.
Team members: Trevor Bednarek, Bill Metcalf, Matt Wyrick (all of them).

The primary author of this module is: Trevor Bednarek.
"""
# DONE: Put the names of ALL team members in the above where indicated.
#       Put YOUR NAME in the above where indicated.

import m0
import m2
import m3
import m4

import tkinter
from tkinter import ttk
import new_create
from new_create import BUMP_LEFT, BUMP_RIGHT
import time


class DataContainer1():
    """ A container for the data shared across the application. """

    def __init__(self):
        """ Initializes instance variables (fields). """
        self.speed = None
        self.darkness = None
        self.distance = None
        self.port = None
        self.robot = None
        self.root = None
        self.kill_function = False

def main():
    """
    Tests functions in this module.
    Intended to be used internally by the primary author of this module.
    """
    print('-------------------------------')
    print('Testing functions in module m1:')
    print('-------------------------------')
    data = DataContainer1
    port = 'sim'
    robot = new_create.Create(port)
    data.port = port
    data.robot = robot
    root = tkinter.Tk()
    a = play_song(root, data)
    b = move_until(root, data)
    c = follow_line(root, data)
    a.mainloop()
    b.mainloop()
    c.mainloop()


def my_frame(root, dc):
    """
    Constructs and returns a Frame (on the given root window)
    that contains this module's widgets.
    Also sets up callbacks for this module's widgets.

    Preconditions:
      :type root: tkinter.Tk
      :type dc: m0.DataContainer
    """

    frame = ttk.Frame(root, padding=(20, 20))
    frame.grid()

    button_simulator = ttk.Button(frame, text='Connect using Simulator')
    button_port = ttk.Button(frame, text='Connect using Port')
    button_disconnect = ttk.Button(frame, text='Disconnect')
    label = ttk.Label(frame, text='Enter the port:')
    port_entry = ttk.Entry(frame, width=10)
    dc.port = port_entry.get()

    button_simulator.grid(column=1, row=1)
    button_port.grid(column=2, row=1)
    label.grid(column=3, row=1)
    port_entry.grid(column=4, row=1)
    button_disconnect.grid(column=2, row=3)

    button_simulator['command'] = lambda: simulator(dc)
    button_port['command'] = lambda: input_port(dc)
    button_disconnect['command'] = lambda: disconnect(dc)

    dc.port = port_entry

    dc.current_frame = frame

def simulator(dc):
    """
    Connects the robot using the simulator
    """
    try:
        dc.port = 'sim'
        dc.robot = new_create.Create(dc.port)
    except:
        print("Error: Cannot connect to simulator.")

def input_port(dc):
    """
    Connects the robot using a port specified by the user.
    Prints an error if the user entered a wrong port.
    """
    port = dc.port.get()
    print(port)
    try:
        dc.robot = new_create.Create(int(port))
    except:
        print("Error: Wrong port entered.")

def disconnect(dc):
    """
    Shutsdown the robot
    """
    print('Shutting down')
    dc.robot.shutdown()


def move_until(root, dc):
    """
     Move autonomously, by going until a specified sensor 
    reaches a specified threshold.  Sensors should include the bump 
    sensors and the 4 cliff sensors, at the least. In particular, the 
    user can set the speed and which bumpers to use (both, just-left 
    or just-right).  Then, the user tells the robot to start, at which 
    point the robot moves until the relevant bumper(s) are pressed.
    Likewise, the user can set the speed, which of the four cliff 
    sensors to use, and a darkness level.  Then, the user tells the 
    robot to start, at which point the robot moves until the specified 
    sensor sees sufficient darkness.
    """
    frame = ttk.Frame(root, padding=(20, 20))
    radio_bumper_frame = ttk.Frame(frame, borderwidth=10, relief='groove')
    radio_sensor_frame = ttk.Frame(frame, borderwidth=10, relief='groove')
    frame.grid()
    radio_bumper_frame.grid()
    radio_sensor_frame.grid()

    button_start_bumper = ttk.Button(frame, text='Start with Bump Sensors')
    button_start_sensor = ttk.Button(frame, text='Start with Cliff Sensors')

    label_speed = ttk.Label(frame, text='Set the speed:')
    entry_speed = ttk.Entry(frame, width=10)
    dc.speed = entry_speed

    label_speed_bumper = ttk.Label(radio_bumper_frame, text='Select a bumper or bumpers to use:')
    radio_bumper_left = ttk.Radiobutton(radio_bumper_frame, text='Left Bumper', value='left')
    radio_bumper_right = ttk.Radiobutton(radio_bumper_frame, text='Right Bumper', value='right')
    radio_bumper_both = ttk.Radiobutton(radio_bumper_frame, text='Both Bumpers', value='both')

    label_darkness = ttk.Label(frame, text='Set the darkness level:')
    entry_darkness = ttk.Entry(frame, width=10)
    dc.darkness = entry_darkness

    label_sensor = ttk.Label(radio_sensor_frame, text='Select a sensor to use:')
    radio_left = ttk.Radiobutton(radio_sensor_frame, text='Left Sensor', value='left')
    radio_front_left = ttk.Radiobutton(radio_sensor_frame, text='Front Left Sensor', value='fleft')
    radio_front_right = ttk.Radiobutton(radio_sensor_frame, text='Front Right Sensor', value='fright')
    radio_right = ttk.Radiobutton(radio_sensor_frame, text='Right Sensor', value='right')

    radio_bumper_observer = tkinter.StringVar()
    for radio in [radio_bumper_left, radio_bumper_right, radio_bumper_both]:
        radio['variable'] = radio_bumper_observer

    radio_sensor_observer = tkinter.StringVar()
    for radio in [radio_left, radio_front_left, radio_front_right, radio_right]:
        radio['variable'] = radio_sensor_observer

    button_start_bumper.grid()
    button_start_sensor.grid()
    label_speed.grid(column=1, row=2)
    entry_speed.grid(column=2, row=2)
    label_speed_bumper.grid()
    radio_bumper_left.grid()
    radio_bumper_right.grid()
    radio_bumper_both.grid()
    label_darkness.grid(column=1, row=3)
    entry_darkness.grid(column=2, row=3)
    label_sensor.grid()
    radio_left.grid()
    radio_front_left.grid()
    radio_front_right.grid()
    radio_right.grid()


    button_start_bumper['command'] = lambda: go_until_dark_bumper(dc, radio_bumper_observer)
    button_start_sensor['command'] = lambda: go_until_dark_sensor(dc, radio_sensor_observer)

    c = 0
    for widget in [radio_bumper_frame]:
        widget.grid(row=0, column=c, padx=20)
        c += 1
    for radio in [radio_bumper_left, radio_bumper_right]:
        radio.grid()

    for widget in [radio_sensor_frame]:
        widget.grid(row=0, column=c, padx=10)
        c += 1
    for radio in [radio_left, radio_front_left, radio_front_right, radio_right]:
        radio.grid(sticky='w')

    dc.entry_speed = entry_speed
    dc.label_speed_bumper = label_speed_bumper
    dc.radio_bumper_left = radio_bumper_left
    dc.radio_bumper_right = radio_bumper_right
    dc.radio_bumper_both = radio_bumper_both
    dc.entry_darkness = entry_darkness
    dc.label_sensor = label_sensor
    dc.radio_left = radio_left
    dc.radio_front_left = radio_front_left
    dc.radio_front_right = radio_front_right
    dc.radio_right = radio_right

    dc.current_frame = frame

def go_until_dark_bumper(dc, observer):
    """
    Determines how far the robot goes based on what bumper sensor the 
    user selected. The robot goes at a certain speed based on what they 
    enter. If nothing was entered the robot goes  at 10 cm/s.
    """
    bump_sensor = new_create.Sensors.bumps_and_wheel_drops

    speed = 0
    if dc.speed.get() == '':
        speed = 10
    else:
        speed = float(dc.speed.get())

    if speed > 50:
        speed = 50

    if speed < -50:
        speed = -50

    while True:
        dc.robot.go(speed, 0)
        if observer.get() == 'both':
            reading = dc.robot.getSensor(bump_sensor)
            if reading[3] == 1 or reading[4] == 1:
                break
        if observer.get() == 'left':
            reading = dc.robot.getSensor(bump_sensor)
            if reading[3] == 1:
                break
        else:
            reading = dc.robot.getSensor(bump_sensor)
            if reading[4] == 1:
                break
    dc.robot.stop()
    print('Robot has hit a wall')


def go_until_dark_sensor(dc, observer):
    """
    Determines how far the robot goes based on what cliff sensors the 
    user selected. The robot goes at a certain speed based on what they 
    enter. If nothing was entered the robot goes  at 10 cm/s. Also, the 
    darkness is set to 100 if there was no darkness set.
    """
    front_left_sensor = new_create.Sensors.cliff_front_left_signal
    front_right_sensor = new_create.Sensors.cliff_front_right_signal
    left_sensor = new_create.Sensors.cliff_left_signal
    right_sensor = new_create.Sensors.cliff_right_signal

    speed = 0
    if dc.speed.get() == '':
        speed = 10
    else:
        speed = float(dc.speed.get())

    if speed > 50:
        speed = 50

    if speed < -50:
        speed = -50

    darkness = 0
    if dc.darkness.get() == '':
        darkness = 100
    else:
        darkness = float(dc.darkness.get())

    if darkness < 0:
        darkness = 0

    if observer.get() == 'left':
        dark_sensor(dc, darkness, speed, front_left_sensor)
    elif observer.get() == 'fleft':
        dark_sensor(dc, darkness, speed, left_sensor)
    elif observer.get() == 'fright':
        dark_sensor(dc, darkness, speed, front_right_sensor)
    else:
        dark_sensor(dc, darkness, speed, right_sensor)
    dc.robot.stop()

def dark_sensor(dc, threshold, velocity, sensor):
    """
    Uses a robot, dc, that goes at a certain velocity using one of
    four sensors. The robot moves until it reaches the threshold.
    """
    while True:
        dc.robot.go(velocity, 0)
        reading = dc.robot.getSensor(sensor)
        if reading < threshold:
            break
        time.sleep(0.05)
    dc.robot.stop()


def follow_line(root, dc):
    """
    The user is able to click a button that makes the robot follow 
    a line.
    """
    frame = ttk.Frame(root, padding=(20, 20))
    frame.grid()

    button_follow = ttk.Button(frame, text='Follow Black Line')
    button_stop = ttk.Button(frame, text='Stop')
#     label_darkness = ttk.Label(frame, text='Darkness: ')
#     entry_darkness = ttk.Entry(frame, width=10)
#     dc.darkness = entry_darkness

    button_follow.grid(column=0, row=1)
#     label_darkness.grid(column=1, row=1)
#     entry_darkness.grid(column=2, row=1)
    button_stop.grid(column=3, row=1)

    button_follow['command'] = lambda: curvy_black_line(dc)
    button_stop['command'] = lambda: stop_button(dc)

#     dc.entry_darkness = entry_darkness

    dc.current_frame = frame

def curvy_black_line(dc):
    """
    The robot follows a line for a certain period of time.
    
#     """
#     darkness = 0
#     if dc.darkness.get() == '':
#         darkness = 100
#     else:
#         darkness = float(dc.darkness.get())
#
#     if darkness < 0:
#         darkness = 0
    dc.is_following = True
    darknessl = new_create.Sensors.cliff_front_left_signal
    darknessr = new_create.Sensors.cliff_front_right_signal

    while dc.is_following:
#         dc.robot.driveDirect(5, 5)
        left_front = dc.robot.getSensor(darknessl)
        right_front = dc.robot.getSensor(darknessr)


#         time.sleep(.1)


        if right_front > 400:
            dc.robot.driveDirect(0, 8)
            time.sleep(.2)
            dc.robot.stop()

        if left_front > 400:
            dc.robot.driveDirect(8, 0)
            time.sleep(.2)
            dc.robot.stop()

#         time.sleep(.01)

        dc.root.update()

def stop_button(dc):
    """
    Stops the robot when necessary
    """
    dc.robot.stop()
    dc.is_following = False


def play_song(root, dc):
    """
    The user is able to click a button and the robot plays a song.
    """
    frame = ttk.Frame(root, padding=(10, 10))
    frame.grid()

    button_song = ttk.Button(frame, text='Play Song')
    button_song.grid(column=1, row=1)

    button_song['command'] = lambda: song(dc)

    dc.current_frame = frame

def song(dc):
    """
    The robot plays a song based on a certain pattern of notes.
    """

    """
    1, 1, 2, 3
    """
    while True:
        if dc.robot.getSensor('SONG_PLAYING') == 0:
            break
    dc.robot.playSong([(88, 20), (83, 20), (71, 20), (88, 20), (83, 20), (71, 20), (88, 19), (83, 20)])

    while True:
        if dc.robot.getSensor('SONG_PLAYING') == 0:
            break
    dc.robot.playSong([(88, 20), (83, 20), (71, 20), (88, 20), (83, 20), (71, 20), (88, 19), (83, 20)])

    while True:
        if dc.robot.getSensor('SONG_PLAYING') == 0:
            break
    dc.robot.playSong([(96, 20), (83, 20), (71, 20), (96, 20), (83, 20), (71, 20), (96, 19), (83, 20)])

    while True:
        if dc.robot.getSensor('SONG_PLAYING') == 0:
            break
    dc.robot.playSong([(98, 20), (83, 20), (71, 20), (96, 20), (83, 20), (71, 20), (96, 19), (83, 20)])

    """
    1, 1, 2, 3
    """
    while True:
        if dc.robot.getSensor('SONG_PLAYING') == 0:
            break
    dc.robot.playSong([(88, 20), (83, 20), (71, 20), (88, 20), (83, 20), (71, 20), (88, 19), (83, 20)])

    while True:
        if dc.robot.getSensor('SONG_PLAYING') == 0:
            break
    dc.robot.playSong([(88, 20), (83, 20), (71, 20), (88, 20), (83, 20), (71, 20), (88, 19), (83, 20)])

    while True:
        if dc.robot.getSensor('SONG_PLAYING') == 0:
            break
    dc.robot.playSong([(96, 20), (83, 20), (71, 20), (96, 20), (83, 20), (71, 20), (96, 19), (83, 20)])

    while True:
        if dc.robot.getSensor('SONG_PLAYING') == 0:
            break
    dc.robot.playSong([(98, 20), (83, 20), (71, 20), (96, 20), (83, 20), (71, 20), (96, 19), (83, 20)])

    """
    1, 1, 2, 3
    """
    while True:
        if dc.robot.getSensor('SONG_PLAYING') == 0:
            break
    dc.robot.playSong([(88, 20), (83, 20), (71, 20), (88, 20), (83, 20), (71, 20), (88, 19), (83, 20)])

    while True:
        if dc.robot.getSensor('SONG_PLAYING') == 0:
            break
    dc.robot.playSong([(88, 20), (83, 20), (71, 20), (88, 20), (83, 20), (71, 20), (88, 19), (83, 20)])

    while True:
        if dc.robot.getSensor('SONG_PLAYING') == 0:
            break
    dc.robot.playSong([(96, 20), (83, 20), (71, 20), (96, 20), (83, 20), (71, 20), (96, 19), (83, 20)])

    while True:
        if dc.robot.getSensor('SONG_PLAYING') == 0:
            break
    dc.robot.playSong([(98, 20), (83, 20), (71, 20), (96, 20), (83, 20), (71, 20), (96, 19), (83, 20)])

    """
    1, 1, 2, 3
    """
    while True:
        if dc.robot.getSensor('SONG_PLAYING') == 0:
            break
    dc.robot.playSong([(88, 20), (83, 20), (71, 20), (88, 20), (83, 20), (71, 20), (88, 19), (83, 20)])

    while True:
        if dc.robot.getSensor('SONG_PLAYING') == 0:
            break
    dc.robot.playSong([(88, 20), (83, 20), (71, 20), (88, 20), (83, 20), (71, 20), (88, 19), (83, 20)])

    while True:
        if dc.robot.getSensor('SONG_PLAYING') == 0:
            break
    dc.robot.playSong([(96, 20), (83, 20), (71, 20), (96, 20), (83, 20), (71, 20), (96, 19), (83, 20)])

    while True:
        if dc.robot.getSensor('SONG_PLAYING') == 0:
            break
    dc.robot.playSong([(98, 20), (83, 20), (71, 20), (96, 20), (83, 20), (71, 20), (96, 19), (83, 20)])

    """
    1, 1, 2, 3 if possible play notes in background
    """
    while True:
        if dc.robot.getSensor('SONG_PLAYING') == 0:
            break
    dc.robot.playSong([(88, 20), (83, 20), (71, 20), (88, 20), (83, 20), (71, 20), (88, 19), (83, 20)])

    while True:
        if dc.robot.getSensor('SONG_PLAYING') == 0:
            break
    dc.robot.playSong([(88, 20), (83, 20), (71, 20), (88, 20), (83, 20), (71, 20), (88, 19), (83, 20)])

    while True:
        if dc.robot.getSensor('SONG_PLAYING') == 0:
            break
    dc.robot.playSong([(96, 20), (83, 20), (71, 20), (96, 20), (83, 20), (71, 20), (96, 19), (83, 20)])

    while True:
        if dc.robot.getSensor('SONG_PLAYING') == 0:
            break
    dc.robot.playSong([(98, 20), (83, 20), (71, 20), (96, 20), (83, 20), (71, 20), (96, 19), (83, 20)])

    """
    1, 1, 2, 3 if possible play notes in background
    """
    while True:
        if dc.robot.getSensor('SONG_PLAYING') == 0:
            break
    dc.robot.playSong([(88, 20), (83, 20), (71, 20), (88, 20), (83, 20), (71, 20), (88, 19), (83, 20)])

    while True:
        if dc.robot.getSensor('SONG_PLAYING') == 0:
            break
    dc.robot.playSong([(88, 20), (83, 20), (71, 20), (88, 20), (83, 20), (71, 20), (88, 19), (83, 20)])

    while True:
        if dc.robot.getSensor('SONG_PLAYING') == 0:
            break
    dc.robot.playSong([(96, 20), (83, 20), (71, 20), (96, 20), (83, 20), (71, 20), (96, 19), (83, 20)])

    while True:
        if dc.robot.getSensor('SONG_PLAYING') == 0:
            break
    dc.robot.playSong([(98, 20), (83, 20), (71, 20), (96, 20), (83, 20), (71, 20), (96, 19), (83, 20)])

    """
    D6, E5, C5, E6, E5, C5, B5, A5
    """
    while True:
        if dc.robot.getSensor('SONG_PLAYING') == 0:
            break
    dc.robot.playSong([(98, 20), (88, 20), (84, 20), (100, 20), (88, 20), (84, 20), (83, 19), (81, 20)])

    """
    4, 4, 4
    A5#, G5, D5, A5#, G5, D5, A5#, G5
    """
    while True:
        if dc.robot.getSensor('SONG_PLAYING') == 0:
            break
    dc.robot.playSong([(82, 20), (91, 20), (86, 20), (82, 20), (91, 20), (86, 20), (82, 19), (91, 20)])

    while True:
        if dc.robot.getSensor('SONG_PLAYING') == 0:
            break
    dc.robot.playSong([(82, 20), (91, 20), (86, 20), (82, 20), (91, 20), (86, 20), (82, 19), (91, 20)])

    while True:
        if dc.robot.getSensor('SONG_PLAYING') == 0:
            break
    dc.robot.playSong([(82, 20), (91, 20), (86, 20), (82, 20), (91, 20), (86, 20), (82, 19), (91, 20)])

    """
    E6, G5, E5, E6, G5, E5, A5#, G5
    """
    while True:
        if dc.robot.getSensor('SONG_PLAYING') == 0:
            break
    dc.robot.playSong([(100, 20), (91, 20), (88, 20), (100, 20), (91, 20), (88, 20), (82, 19), (91, 20)])

    """
    4, 4, 4
    A5#, G5, D5, A5#, G5, D5, A5#, G5
    """
    while True:
        if dc.robot.getSensor('SONG_PLAYING') == 0:
            break
    dc.robot.playSong([(82, 20), (91, 20), (86, 20), (82, 20), (91, 20), (86, 20), (82, 19), (91, 20)])

    while True:
        if dc.robot.getSensor('SONG_PLAYING') == 0:
            break
    dc.robot.playSong([(82, 20), (91, 20), (86, 20), (82, 20), (91, 20), (86, 20), (82, 19), (91, 20)])

    while True:
        if dc.robot.getSensor('SONG_PLAYING') == 0:
            break
    dc.robot.playSong([(82, 20), (91, 20), (86, 20), (82, 20), (91, 20), (86, 20), (82, 19), (91, 20)])

    """
    5
    D5, A5#, G5, C5#
    """
    while True:
        if dc.robot.getSensor('SONG_PLAYING') == 0:
            break
    dc.robot.playSong([(86, 20), (82, 20), (91, 20), (85, 20)])

    """
    4
    """
    while True:
        if dc.robot.getSensor('SONG_PLAYING') == 0:
            break
    dc.robot.playSong([(82, 20), (91, 20), (86, 20), (82, 20), (91, 20), (86, 20), (82, 19), (91, 20)])

    """
    5
    """
    while True:
        if dc.robot.getSensor('SONG_PLAYING') == 0:
            break
    dc.robot.playSong([(86, 20), (82, 20), (91, 20), (85, 20)])

    """
    A5#, G5, C5#, A5#, G5, C5#, C6#, G5
    """
    while True:
        if dc.robot.getSensor('SONG_PLAYING') == 0:
            break
    dc.robot.playSong([(82, 20), (91, 20), (85, 20), (82, 20), (91, 20), (85, 20), (97, 19), (91, 20)])

    """
    G5, C6#, A5#, G5, C6#, A5#, G5, C6#
    """
    while True:
        if dc.robot.getSensor('SONG_PLAYING') == 0:
            break
    dc.robot.playSong([(91, 20), (97, 20), (82, 20), (91, 20), (97, 20), (82, 20), (91, 19), (97, 20)])

    """
    A5#, G5, C6#, A5#, G5, C6#, A5#, G5
    """
    while True:
        if dc.robot.getSensor('SONG_PLAYING') == 0:
            break
    dc.robot.playSong([(82, 20), (91, 20), (97, 20), (82, 20), (91, 20), (97, 20), (82, 19), (91, 20)])


# ----------------------------------------------------------------------
# If this module is running at the top level (as opposed to being
# imported by another module), then call the 'main' function.
# ----------------------------------------------------------------------
if __name__ == '__main__':
    main()




