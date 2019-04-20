import select
import numpy as np
import time
import curses
import os, sys
from robot import Robot
from obstacles import Obstacles
from system import PathPlanning
import numpy as np
import matplotlib.pyplot as plt
import time

def poll_key(win):
    try:
        key = win.getkey()
        win.clear()
        win.addstr("Detected key: " + str(key) + "\n\n")
        if key == os.linesep:
            return
    except Exception as e:
        # No input
        pass

def main(win):
    win.nodelay(True)
    key=""
    win.clear()

    HOME = [np.pi/2, -np.pi/2, np.pi/2, -np.pi/2, 0, 0 , -np.pi/2, np.pi/2]
    R = Robot(np.array([1]*8), HOME)
    O = Obstacles(np.array([3,1]), 1, 4, speed=np.pi/200)
    P = PathPlanning(R, O, win)
    P.Logic_ = 'Simple_Closed'

    Pa = np.array([5,1])
    Pb = np.array([6,3])
    Pc = np.array([6,-1])

    while True:
        states = P.move(Pb, 3)
        states = P.move(Pc, 3)
        states = P.move(Pa, 3)

    P.L.plot_results()
if __name__ == '__main__':
    curses.wrapper(main)
