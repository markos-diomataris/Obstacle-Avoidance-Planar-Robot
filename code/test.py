from robot import Robot
from system import PathPlanning
import numpy as np
import matplotlib.pyplot as plt
import time

plt.ion()

HOME = [np.pi/2, -np.pi/2, np.pi/2, -np.pi/2, 0, 0 , -np.pi/2, np.pi/2]
R = Robot(np.ones(8),HOME)
P = PathPlanning(R)
P.Logic_ = 'Simple_Closed'

while True:
    print('asdf')
    states = P.move(np.array([np.random.randint(0,6),np.random.randint(0,6)]), 2)
    for s in states[::20]: 
        P.draw(s)

input()
