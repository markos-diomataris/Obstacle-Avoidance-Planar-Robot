"""
Implemntation of Obstacle class
"""

import numpy as np
from pdb import set_trace


class Obstacles:

    def __init__(self, HOME, R, D):
        """
        HOME: position of initial center of mass of our "balls" (numy array)
        R: Radius of our "balls" (0.2l<=R<=0.5l)
        D: Distance of our "balls" (l<=D<=1.8l)
        """
        self.HOME = HOME
        self.R = R
        self.D = D
        # Ball centers
        self.bc1 = HOME + D/2 * np.array([0,1])
        self.bc2 = HOME + D/2 * np.array([0,-1])
        pass

    def minDistance(self,p):
        """
        Calulate minimum distance of a point p from our "balls"
        """
        d1 = np.linalg.norm(self.bc1 - p)
        d2 = np.linalg.norm(self.bc2 - p)
        return np.min(d1, d2) 

    def move(self):
        pass


