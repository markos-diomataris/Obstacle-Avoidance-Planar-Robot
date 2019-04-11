from robot import Robot
import numpy as np
from logger import Logger
import matplotlib.pyplot as plt
from pdb import set_trace
from scipy.stats import multivariate_normal


class PathPlanning:

    def __init__(self, R, O, T=0.01):
        self.R = R  # Robot
        self.O = O  # Obstacles
        self.L = Logger()
        self.integrator_ = self.R.state  # initial state of Robot
        self.differentiator_ = np.array([ self.R.fk()[0,3], self.R.fk()[1,3] ])  # initial position of tool
        self.Logic_ = 'Simple_Closed'
        self.T = T
        self.fig, self.ax = plt.subplots()
        self.X1= -1
        self.X2= 7
        self.Y1= -4
        self.Y2= 7
        self.ax.set_xlim((self.X1, self.X2))
        self.ax.set_ylim((self.Y1, self.Y2))
        self.drawStep = 25

    def reset(self):
        """
        Reset system: reset integrator, differentiator, and Robot
        to HOME position
        """

        self.R.reset()
        self.integrator_ = self.R.state
        self.differentiator_ = np.array([ self.R.fk()[0,3], self.R.fk()[1,3] ])  # initial position of tool

    def differentiator(self,input):
        ret = (input - self.differentiator_)/self.T
        self.differentiator_ = input
        return ret

    def integrator(self,input):
        self.integrator_ = input*self.T + self.integrator_
        return self.integrator_

    def logic(self,input):
        """
        <3 <3 <3 <3 <3 <3 <3 <3 <3 <3 <3 <3 <3 <3 <3 <3 <3 <3 <3 <3 <3 <3 <3
        Task Segmentation Logic
        This is the heart of the robot
        here we decide depending on the spcecified task
        the desired joint velocities
        Simple_Open: Open loop minimum energy calculation no big deal
        <3 <3 <3 <3 <3 <3 <3 <3 <3 <3 <3 <3 <3 <3 <3 <3 <3 <3 <3 <3 <3 <3 <3
        """
        np.set_printoptions(suppress=True)
        np.set_printoptions(precision=3)

        # Task 1: tool position
        Jac = self.R.Jacobian()[:2,:]
        # J1plus = np.linalg.pinv(self.R.Jacobian()) 
        J1plus = Jac.T @ np.linalg.inv(Jac @ Jac.T)
        T1 = J1plus @ input

        # Task 2: obstacle avoidance
        grads1 = np.zeros((self.R.n,self.R.n))
        grads2 = np.zeros((self.R.n,self.R.n))
        D1 = np.zeros(self.R.n)
        D2 = np.zeros(self.R.n)
        rv1 = multivariate_normal(self.O.bc(1), np.array([[self.O.R, 0],[0, self.O.R]]))
        rv2 = multivariate_normal(self.O.bc(2), np.array([[self.O.R, 0],[0, self.O.R]]))

        scale1 = np.ones(self.R.n)
        scale2 = np.ones(self.R.n)
        for i in range(1,self.R.n+1):
            pi = self.R.fk(i)[0:2,3]
            scale1[i-1] = rv1.pdf(pi)/rv1.pdf(self.O.bc(1))
            scale2[i-1] = rv2.pdf(pi)/rv2.pdf(self.O.bc(2))
            D1[i-1] = np.linalg.norm(pi - self.O.bc(1))
            D2[i-1] = np.linalg.norm(pi - self.O.bc(2))
            Jac_li = self.R.Jacobian(i)[:2,:]
            grad = (pi - self.O.bc(1)).T @ Jac_li
            grads1[:,i-1] = grad
            grad = (pi - self.O.bc(2)).T @ Jac_li
            grads2[:,i-1] = grad

        In = np.eye(self.R.n)
        kc = 20
        nearrest1 = np.argmin(D1)
        nearrest2 = np.argmin(D2)
        #grads1_norm = grads1/np.linalg.norm(grads1, ord=2, axis=1, keepdims=True)
        #T2 = kc * (In-J1plus@Jac) @ ((grads1 @ scale1) + (grads2 @ scale2))
        T2 = kc * (In-J1plus@Jac) @ ((grads1[:,nearrest1] * scale1[nearrest1]) + (grads2[:,nearrest2] * scale2[nearrest2]))

        # caluclate q dots 
        # combine tasks
        q_dot = T1  + T2

        return q_dot

    def trajectoryPlan(self,Pa,Pb,tf):
        """
        Calculate a straight line path from Pa to Pb
        according to a 2nd degree velocity profile
        v(t) = a*t^2 + b*t + c
        p(t) = integral_of v(t)
        returns: velocity_profile, position_profile, time(sec) (arrays)
        """

        time = np.linspace(0, tf, tf/self.T)
        # calculate polynomials
        a = 6*(Pa-Pb)/tf**3
        b = -a*tf
        c = 0
        d = Pa
        p = np.zeros((2,time.shape[0]))
        v = np.zeros((2,time.shape[0]))
        for i,t in enumerate(time): # FIX: create vectorized function
            p[:,i] = (a*t**3)/3 + (b*t**2)/2 + d
            v[:,i] = a*t**2 + b*t
        return v, p, time

    def move(self,Pb,tf):
        """
        Considering as starting position the current position
        first PathPlanning() is performed and then
        the input(s) is fed through the system
        the output is applied to the Robot
        """

        Pa = np.array([self.R.fk()[0,3], self.R.fk()[1,3]])  # initial position of tool (current)
        move_states = []
        v, p, time = self.trajectoryPlan(Pa,Pb,tf)
        for i in range(time.shape[0]):

            if self.Logic_ == 'Simple_Open':
                out = self.differentiator(p[:,i])
                out = self.logic(out)
                q = self.integrator(out)
                self.R.move(q)
                self.O.move()
                move_states.append(q)

            elif self.Logic_ == 'Simple_Closed':
                xd = p[:,i]
                xe = self.R.fk()[:2,3]
                e = xd - xe
                # Logger
                self.L.add('error',e)
                #
                K = 2 * np.eye(e.shape[0])  # FIX: calibrate K
                out = (K @ e) + v[:,i]
                out = self.logic(out)
                q = self.integrator(out)
                self.R.move(q)
                self.O.move()
                move_states.append(q)

            if i % self.drawStep == 0:
                self.draw()

        return move_states

    def draw(self,state=None):
        """
        Draw Robot  and obstacles in state 'state'
        !! Does not change the state of the robot or position of obstacles,
        just draws
        """

        if isinstance(state, np.ndarray):
            cache = self.R.state
            self.R.state = state

        points = []
        # plt.figure(self.fig.number)
        plt.cla()
        self.ax.set_xlim((self.X1, self.X2))
        self.ax.set_ylim((self.Y1, self.Y2))
        plt.grid()
        for i in range(self.R.n):
            # draw Robot
            points.append((self.R.fk(i)[0,3], self.R.fk(i+1)[0,3]))
            points.append((self.R.fk(i)[1,3], self.R.fk(i+1)[1,3]))
            self.ax.add_patch(plt.Circle((points[-2][0],points[-1][0]), 0.06, color='g', alpha=1))
            self.ax.add_patch(plt.Circle((points[-2][0],points[-1][0]), 0.04, color='r', alpha=1))
        # draw obstacles
        self.ax.add_patch(plt.Circle((self.O.bc(1)[0], self.O.bc(1)[1]), self.O.R, color='c', alpha=1))
        self.ax.add_patch(plt.Circle((self.O.bc(2)[0], self.O.bc(2)[1]), self.O.R, color='c', alpha=1))

        plt.plot(*points)
        plt.draw()
        plt.pause(0.1)
        if isinstance(state, np.ndarray):
            self.R.state = cache
        return points
