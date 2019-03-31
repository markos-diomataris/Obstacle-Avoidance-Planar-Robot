from robot import Robot
from system import PathPlanning
import numpy as np
import matplotlib.pyplot as plt
import time

plt.ion()

HOME = [np.pi/2, -np.pi/2, np.pi/2, -np.pi/2, 0, 0 , -np.pi/2, np.pi/2]
R = Robot(np.ones(8),HOME)
P = PathPlanning(R)
for i in range(3):
    P.move(np.array([7,3]), 3)
    P.move(np.array([7,-1]), 1)
    P.move(np.array([5,1]), 1)
for s in P.R.state_history[::20]:
    R.draw(s)

input()
