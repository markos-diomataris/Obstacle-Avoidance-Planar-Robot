from robot import Robot
from obstacles import Obstacles
from system import PathPlanning
import numpy as np
import matplotlib.pyplot as plt
import time

plt.ion()

HOME = [np.pi/2, -np.pi/2, np.pi/2, -np.pi/2, 0, 0 , -np.pi/2, np.pi/2]
R = Robot(np.array([1]*8), HOME)
O = Obstacles(np.array([4,1]), 0.5, 2)
P = PathPlanning(R, O)

P.Logic_ = 'Simple_Closed'
Pa = np.array([3,1])
Pb = np.array([7,3])
Pc = np.array([7,-1])
while True:
    #px , py = np.random.randint(0,6), np.random.randint(0,6)
    states = P.move(Pb, 3)
    states = P.move(Pc, 3)
    states = P.move(Pa, 3)
input()
