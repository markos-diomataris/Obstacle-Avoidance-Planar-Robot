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

def main(win):
        win.nodelay(True)
        key=""
        win.clear()
        win.addstr("Detected key:")
       i=0
        while 1:
            try:
               key = win.getkey()
               win.clear()
               win.addstr("Detected key: " + str(i))
               win.addstr(str(key))
               if key == os.linesep:
                  break
            except Exception as e:
               # No input
               pass
        win.addstr("Exitting...")
        sys.exit(0)

if __name__ == '__main__':
    curses.wrapper(main)
