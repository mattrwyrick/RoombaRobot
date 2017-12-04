"""
The Python Capstone Project. abc

CSSE 120 - Introduction to Software Development.
Team members:Bill and Trevor (all of them).

The primary author of this module is: Matt Wyrick.
"""
from urllib.robotparser import RobotFileParser

"1,2,4 & 5 -"
# Done: Put the names of ALL team members in the above where indicated.
#       Put YOUR NAME in the above where indicated.

import m0
import m1
import m2
import m4


import tkinter
from tkinter import ttk
import new_create
import time
from tkinter import *

class DataContainer3():
    """ A container for the data shared across the application. """

    def __init__(self):
        """ Initializes instance variables (fields). """
        self.entry_for_distance = None
        self.label_for_distance = None
        self.distance = None

        self.entry_for_velocity = None
        self.label_for_velocity = None
        self.velocity = None

        self.entry_for_talk = None

        self.print_talk = True
        self.port = None
        self.robot = None

        self.ir = 255








def main():
    """
    Tests functions in this module.
    Intended to be used internally by the primary author of this module.
    """
    print('-------------------------------')
    print('Testing functions in module m3:')
    print('-------------------------------')


    data = DataContainer3
    port = 'sim'
    robot = new_create.Create(port)
    data.port = port
    data.robot = robot
    root = tkinter.Tk()


    a = my_frame(root, data)
    a.mainloop()




def Matts_Frame(root, data):
    """
    Constructs and returns a Frame (on the given root window)
    that contains this module's widgets.
    Also sets up callbacks for this module's widgets.

    Preconditions:
      :type root: tkinter.Tk
      :type dc: m0.DataContainer
    """


    'INITIAL FRAMES'
    frame = ttk.Frame(root, padding=(40, 40))
    frame.grid()

    print_talk()

    'RADIO FRAMES'
    radio_frame = ttk.Frame(frame, borderwidth=10, relief='groove')
    radio1 = ttk.Radiobutton(radio_frame, text='Forward', value='Forward')
    data.radio1 = radio1
    radio2 = ttk.Radiobutton(radio_frame, text='Backward', value='Backward')
    data.radio2 = radio2
    radio3 = ttk.Radiobutton(radio_frame, text='Left', value='Left')
    data.radio3 = radio3
    radio4 = ttk.Radiobutton(radio_frame, text='Right', value='Right')
    data.radio4 = radio4

    radio_observer = tkinter.StringVar()
    for radio in [radio1, radio2, radio3, radio4]:
        radio['variable'] = radio_observer

    c = 0
    for widget in [radio_frame]:
        widget.grid(row=0, column=c, padx=20)
        c = c + 1
    for radio in [radio1, radio2, radio3, radio4]:
        radio.grid(sticky='w')


    'DISTANCE & VELOCITY'
    entry_d = ttk.Entry(frame, width=8)
    entry_d.grid()
    data.entry_for_distance = entry_d

    label_d = ttk.Label(frame, text="Enter a Distance")
    label_d.grid()
    data.label_for_distance = label_d

    entry_v = ttk.Entry(frame, width=8)
    entry_v.grid()
    data.entry_for_velocity = entry_v

    label_v = ttk.Label(frame, text="Enter a Velocity")
    label_v.grid()
    data.label_for_velocity = label_v


    'TKINTER BUTTONS'
    buttonv = ttk.Button(frame, text='Submit velocity')
    buttonv.grid()
    buttonv['command'] = lambda: test_direction(data, radio_observer)

    button_hours = ttk.Button(frame, text="Work Hours")
    button_hours.grid()
    button_hours['command'] = lambda: work_hours()

    button_hours = ttk.Button(frame, text="Light Show")
    button_hours.grid(column=2, row=1)
    button_hours['command'] = lambda: light_show(data)

#     button_userdrive = ttk.Button(frame, text="Enable Udrive")
#     button_userdrive.grid(column=2, row=2)
#     button_userdrive['command'] = lambda: user_control(data)

    label_talk = ttk.Label(frame, text='Talk Menu on Console')
    label_talk.grid(column=2, row=0)



    button_ir = ttk.Button(frame, text='Robot listen')
    button_ir.grid(column=2, row=3)
    button_ir['command'] = lambda: robot_listen(data, frame)

    label_num = ttk.Label(frame, text='Enter 0-7')
    label_num.grid(column=2, row=4)

    entry_talk = ttk.Entry(frame, width=8)
    entry_talk.grid(column=2, row=5)
    data.entry_for_talk = entry_talk

    button_talk = ttk.Button(frame, text="Robot Talk")
    button_talk.grid(column=2, row=6)
    button_talk['command'] = lambda: robot_talk(data, frame)

#     button_endl = ttk.Button(frame, text="Stop Listening")
#     button_endl.grid(column=2, row=2)
#     button_endl['command'] = lambda: end_listening(data)

    data.current_frame = frame



def test_direction(data, radio_observer):

    "DISTANCE & VELOCITY"
    entry = data.entry_for_distance
    contents_entry_for_distance = entry.get()
    entry = data.entry_for_velocity
    contents_entry_for_velocity = entry.get()

    if contents_entry_for_distance == '':
        data.distance = 10
    else:
        data.distance = int(contents_entry_for_distance)
    if contents_entry_for_velocity == '':
        data.velocity = 10
    else:
        data.velocity = int(contents_entry_for_velocity)
    if data.velocity > 50:
        data.velocity = 50

    data.velocity = abs(data.velocity)
    format_string = '{} centimeters traveled'
    answer = format_string.format(data.distance)
    data.label_for_distance['text'] = answer

    format_string = '{} meters/second'
    answer = format_string.format(data.velocity)
    data.label_for_velocity['text'] = answer


    "RADIOS"
    # No Entry
    if radio_observer.get() == '':
        move(data)

    # Forward
    if radio_observer.get() == "Forward":
        move(data)

    # Backward
    if radio_observer.get() == "Backward":
        data.velocity = data.velocity * -1
        data.distance = data.distance * -1
        move(data)

    # Left
    if radio_observer.get() == "Left":
        data.robot.driveDirect(-15, 15)
        time.sleep(1.35)
        data.robot.stop()
        move(data)

    # Right
    if radio_observer.get() == "Right":
        data.robot.driveDirect(15, -15)
        time.sleep(1.35)
        data.robot.stop()
        move(data)

def move(data):

    get_time = 1 / (int(data.velocity) / int(data.distance))
    data.robot.driveDirect(data.velocity, data.velocity)
    time.sleep(get_time)
    data.robot.stop()


def work_hours():

    inputFile = open("workhours.txt", "r")
    line = inputFile.read()
    inputFile.close()
    print(line)


def light_show(data):

    for i in range(12):
        data.robot.setLEDs(0, 225, 0, 1)
        data.robot.driveDirect(-50, 50)
        time.sleep(.5)
        data.robot.setLEDs(225, 225, 1, 0)
        data.robot.driveDirect(-25, 25)
        time.sleep(.5)
        data.robot.setLEDs(100, 100, 2, 1)
        data.robot.driveDirect(50, -50)
        time.sleep(.5)
        data.robot.setLEDs(175, 225, 2, 2)
        data.robot.driveDirect(25, -25)
        time.sleep(.5)
    data.robot.stop()
    data.robot.setLEDs(0, 0, 0, 0)

def robot_talk(data, frame):


    entry = int(data.entry_for_talk.get())

    # match numbers to actual button led set
    if entry == 0:
        'POWER button'
        data.robot.setLEDs(225, 225, 0, 1)

    if entry == 1:
        'SPOT button'
        data.robot.setLEDs(0, 225, 0, 1)

    if entry == 2:
        'Clean button'
        data.robot.setLEDs(225, 225, 1, 0)

    if entry == 3:
        'MAX button'
        data.robot.setLEDs(225, 225, 0, 0)

    if entry == 4:
        'LEFT button'
        data.robot.setLEDs(0, 225, 0, 0)

    if entry == 5:
        'FORWARD button'
        data.robot.setLEDs(0, 225, 1, 0)

    if entry == 6:
        'RIGHT button'
        data.robot.setLEDs(0, 225, 1, 1)

    if entry == 7:
        'PAUSE button'
        data.robot.setLEDs(225, 225, 1, 1)

    if entry == '':
        data.robot.setLEDs(0, 0, 0, 0)






def robot_listen(data, frame):
    '255 indicates no bytes'

    ir = new_create.Sensors.ir_byte
    ir_value = data.robot.getSensor(ir)

    while ir_value == 255:
        ir_value = data.robot.getSensor(ir)
        time.sleep(.2)


    if ir_value == 129:
        'left button'
        data.robot.playNote(50, 30)
        data.robot.setLEDs(0, 225, 0, 0)

    if ir_value == 130:
        'forward button'
        data.robot.playNote(50, 30)
        data.robot.setLEDs(0, 225, 1, 0)

    if ir_value == 131:
        'right button'
        data.robot.playNote(50, 30)
        data.robot.setLEDs(0, 225, 1, 1)

    if ir_value == 132:
        'spot button'
        data.robot.playNote(50, 30)
        data.robot.setLEDs(0, 225, 0, 1)

    if ir_value == 133:
        'max button'
        data.robot.playNote(50, 30)
        data.robot.setLEDs(225, 225, 0, 0)

    if ir_value == 136:
        'clean button'
        data.robot.playNote(50, 30)
        data.robot.setLEDs(225, 225, 1, 0)

    if ir_value == 137:
        'pause button'
        data.robot.playNote(50, 30)
        data.robot.setLEDs(225, 225, 1, 1)

    if ir_value == 138:
        'power button'
        data.robot.playNote(50, 30)
        data.robot.setLEDs(225, 225, 0, 1)
    time.sleep(2)
    data.robot.setLEDs(0, 0, 0, 0)

# def end_listening(data):
#     data.robot.driveDirect(0, 0)
#     time.sleep(.1)

def print_talk():
  print("------------------------")
  print("Robot Talk Entry (0-7)")
  print("")
  print("0 = POWER")
  print("1 = SPOT")
  print("2 = CLEAN")
  print("3 = MAX")
  print("4 = LEFT")
  print("5 = FORWARD")
  print("6 = RIGHT")
  print("7 = PAUSE")
  print("------------------------")






# ----------------------------------------------------------------------
# If this module is running at the top level (as opposed to being
# imported by another module), then call the 'main' function.
# ----------------------------------------------------------------------
if __name__ == '__main__':
    main()
