from robot import Robot
from obstacles import Obstacles
from system import PathPlanning
import numpy as np
import matplotlib.pyplot as plt
import time

plt.ion()

HOME = [np.pi/2, -np.pi/2, np.pi/2, -np.pi/2, 0, 0 , -np.pi/2, np.pi/2]
R = Robot(np.ones(8),HOME)
O = Obstacles(np.array([5,1]), 0.5, 2)
P = PathPlanning(R, O)
P.Logic_ = 'Simple_Closed'

while True:
    px , py = np.random.randint(0,6), np.random.randint(0,6)
    print('Moving to {},{}'.format(px, py))
    states = P.move(np.array([px,py]), 2)
 
input()
