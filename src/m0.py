"""
The Python Capstone Project.

This file contains data SHARED by the other modules in this project.

CSSE 120 - Introduction to Software Development.
Team members: PUT-YOUR-NAMES_HERE (all of them).
"""
# TODO: Put the names of ALL team members in the above where indicated.

import m1
import m2
import m3
import m4

import tkinter
from tkinter import ttk
import new_create

# ----------------------------------------------------------------------
# TODO: TEAM-PROGRAM this module so that it runs your entire program,
#       incorporating parts from m1 .. m4.
# ----------------------------------------------------------------------


class DataContainer():
    """ A container for the data shared across the application. """
    def __init__(self):
        """ Initializes instance variables (fields). """
        # Add     self.FOO = BLAH     here as needed.
        self.robot = None
        self.port = None
        self.remote_speed_entry = None
        self.current_frame = None
        self.row_n = 0
        self.root = None
        self.is_following = True

def main():
    """ Runs the MAIN PROGRAM. """
    print('----------------------------------------------')
    print('Integration Testing of the INTEGRATED PROGRAM:')
    print('----------------------------------------------')
    dc = DataContainer()
    dc.root = tkinter.Tk()
    mainframe = ttk.Frame(dc.root)
    mainframe.grid()

    # Add new frame methods into the line below,and the text for its button another line down
    frames = [[m1.my_frame, m2.tele_frame, m2.waypoints_frame, m2.rand_notes_frame, m1.play_song, m1.follow_line, m1.move_until, m2.complex_movements_frame, m3.Matts_Frame],
              ['Connect', 'Remote', 'Waypoints', 'Random Notes', 'Play Song', 'Follow Line', 'Move Until Sensor', 'Complex Movements', "Matt's Frame"]]
    buttons = []

    for k in range(len(frames[0])):
        buttons += [ttk.Button(mainframe, text=frames[1][k], width=18)]
        create_button(buttons, k, frames[0][k], dc.root, dc)

    m1.my_frame(dc.root, dc)
    dc.root.mainloop()

def create_button(buttons, k, command, root, dc):
    buttons[k]['command'] = lambda: button_command(root, dc, command)
    buttons[k].grid(row=dc.row_n, column=k % 5)
    if (k + 1) % 5 == 0:
        dc.row_n += 1


def button_command(root, dc, command):
    dc.current_frame.destroy()
    command(root, dc)



# ----------------------------------------------------------------------
# If this module is running at the top level (as opposed to being
# imported by another module), then call the 'main' function.
# ----------------------------------------------------------------------
if __name__ == '__main__':
    main()
