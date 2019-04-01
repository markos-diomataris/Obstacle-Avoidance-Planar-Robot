"""
Implementation of Robot class
"""
import numpy as np
import matplotlib.pyplot as plt

class Robot:
    def __init__(self,lengths, HOME):
        """
        l: list of connector lengths
        """
        
        self.HOME = HOME
        self.lengths = lengths
        self.n = lengths.shape[0]
        self.state = np.array(self.HOME)
        self.state_history = [self.state]

    def reset(self):
        """
        Erase state history and reset position
        !! Called ONLY by PathPlanning() class
        """

        self.state = np.array(self.HOME)
        self.state_history = [self.state]

    def move(self,state):
        self.state_history.append(state)
        self.state = state

    def fk(self,joint=None):
        """
        Calculate Forward Kinematics based on current state
        joint: if None we calculate the end effector's position
               else we calculate util 'joint'
        returns: 4 x 4 numpy array
        """
        
        if joint == 0:
            return np.eye(4)
        if not joint:
            joint = self.lengths.shape[0]
        assert (isinstance(joint, int) and joint >= 1 and joint <= self.lengths.shape[0]) , "fk(): joint value out of bounds"

        c = np.cos(np.sum(self.state[:joint]))
        s = np.sin(np.sum(self.state[:joint]))
        dx = np.sum(np.multiply(self.lengths[:joint], np.cos(np.cumsum(self.state[:joint]))))
        dy = np.sum(np.multiply(self.lengths[:joint], np.sin(np.cumsum(self.state[:joint]))))
        R = np.array([[c,-s, 0, dx],
                      [s, c, 0, dy],
                      [0, 0, 1, 0],
                      [0, 0, 0, 1]])
        return R

    def Jacobian(self,joint=None):
        """
        Calculate Jacobian matrix based on state
        returns: 6 x n numpy array
        """
        
        if not joint:
            joint = self.lengths.shape[0]
        assert (isinstance(joint, int) and joint >= 1 and joint <= self.lengths.shape[0]) , "fk(): joint value out of bounds"

        #  Caluclate Jacobian rows
        Jp1 = [np.sum(np.multiply(-self.lengths[row:], np.sin(np.cumsum(self.state)[row:]))) for row in range(joint)]
        Jp2 = [np.sum(np.multiply(self.lengths[row:], np.cos(np.cumsum(self.state)[row:]))) for row in range(joint)]
        Jp3 = [0 for _ in range(joint)]
        Jo1 = [0 for _ in range(joint)]
        Jo2 = [0 for _ in range(joint)]
        Jo3 = [1 for _ in range(joint)]
        return np.array([Jp1, Jp2, Jp3, Jo1, Jo2, Jo3]) 

