import numpy as np
import matplotlib.pyplot as plt


class Logger:

    def __init__(self):
        self.data = dict()
        self.data['error'] = []
        self.data['state'] = []
        self.data['pos'] = []

    def add(self, field, value):
        self.data[field].append(value)

    def plot_results(self):
        plt.figure()
        plt.plot(self.data['error'])
