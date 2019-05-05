import select
import numpy as np
import time
import curses
import os, sys
from robot import Robot
from obstacles import Obstacles
from system import PathPlanning, prompt
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
    #setup interactive window
    win.nodelay(True)
    key=""
    win.clear()
    win.addstr(prompt)
    #setup simulation
    HOME = [np.pi/2, -np.pi/2, np.pi/2, -np.pi/2, 0, 0 , -np.pi/2, np.pi/2]
    R = Robot(np.array([1]*8), HOME)
    O = Obstacles(np.array([3,1]), 1, 4, speed=np.pi/200, manual=manual)
    P = PathPlanning(R, O, win)
    P.Logic_ = 'Simple_Closed'
#    P.Logic_ = 'Simple_Open'
    #setup path triangle points
    Pa = np.array([5,1])
    Pb = np.array([6,3])
    Pc = np.array([6,-1])
    if not manual:
        for _ in range(3):
            try:
                P.move(Pb, 3)
                P.move(Pc, 3)
                P.move(Pa, 3)
            except:
                break
    else:
        while True:
            try:
                P.move(Pb, 3)
                P.move(Pc, 3)
                P.move(Pa, 3)
            except:
                break

    P.L.plot_results()
    input()
if __name__ == '__main__':
    if len(sys.argv) != 2:
        print("usage: python run.py [manual|auto]")
        sys.exit(0)
    elif sys.argv[1] == 'manual':
        manual=True
    elif sys.argv[1] == 'auto':
        manual=False
    else:
        print("usage: python run.py [manual|auto]")
        sys.exit(0)
    curses.wrapper(main)
