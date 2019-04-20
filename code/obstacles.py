"""
Implemntation of Obstacle class
"""

import numpy as np
import sys

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
        self.speed = speed
        self.direction = np.array([.0,.0])

    def bc(self,b):
        y = 1 if b == 1 else -1
        return self.HOME + self.D/2 * np.array([0,y])

    def minDistance(self,p):
        """
        Calulate minimum distance of a point p from our "balls"
        """
        d1 = np.linalg.norm(self.bc1 - p)
        d2 = np.linalg.norm(self.bc2 - p)
        return np.min(d1, d2)

    def move(self, inp):
        if inp == "KEY_UP":
            self.direction = np.array([0,1])
        if inp == "KEY_DOWN":
            self.direction = np.array([0,-1])
        if inp == "KEY_RIGHT":
            self.direction = np.array([1,0])
        if inp == "KEY_LEFT":
            self.direction = np.array([-1,0])
        if inp == "s":
            self.direction = np.zeros(2)
        if inp == "q":
            sys.exit(0)
        self.HOME = self.HOME + self.speed * self.direction

