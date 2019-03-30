from robot import Robot
from system import PathPlanning
import numpy as np
import matplotlib.pyplot as plt
import time

plt.ion()

R = Robot(np.ones(8))
P = PathPlanning(R)
for i in range(3):
    P.move(np.array([7,3]), 3)
    P.move(np.array([7,-1]), 3)
    P.move(np.array([5,1]), 3)
for s in P.R.state_history[::20]:
    R.draw(s)

input()
