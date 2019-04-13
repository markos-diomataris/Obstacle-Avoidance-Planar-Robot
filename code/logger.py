import numpy as np
import matplotlib.pyplot as plt


class Logger:

    def __init__(self):
        self.data = dict()
        self.data['error'] = []
        self.data['state'] = []
        self.data['pos'] = []
        self.data['min_dist'] = []

    def add(self, field, value):
        self.data[field].append(value)

    def plot_results(self):
        plt.figure()

        plt.subplot(311)
        plt.plot(self.data['error'])
        plt.title('error')
        plt.grid()

        plt.subplot(312)
        plt.plot(self.data['state'])
        plt.title('state')
        plt.grid()

        plt.subplot(313)
        plt.plot(self.data['min_dist'])
        plt.title('Obstacles distance: ' + str(np.mean(self.data['min_dist'])))
        plt.grid()
