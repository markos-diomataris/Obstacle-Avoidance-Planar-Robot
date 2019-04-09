"""
Implemntation of Obstacle class
"""

import numpy as np
from pdb import set_trace


class Obstacles:

    def __init__(self, HOME, R, D, speed=np.pi/400):
        """
        HOME: position of initial center of mass of our "balls" (numy array)
        R: Radius of our "balls" (0.2l<=R<=0.5l)
        D: Distance of our "balls" (l<=D<=1.8l)
        """
        self.HOME = HOME
        self.R = R
        self.D = D
        # Ball centers
        self.phase = 0
        self.speed = speed

    def bc(self,b):
        y = 1 if b == 1 else -1
        return self.HOME + np.sin(self.phase) * np.array([0,1])+ self.D/2 * np.array([0,y]) + np.cos(self.phase) * np.array([1,0])

    def minDistance(self,p):
        """
        Calulate minimum distance of a point p from our "balls"
        """
        d1 = np.linalg.norm(self.bc1 - p)
        d2 = np.linalg.norm(self.bc2 - p)
        return np.min(d1, d2)

    def move(self):
      self.phase += self.speed

