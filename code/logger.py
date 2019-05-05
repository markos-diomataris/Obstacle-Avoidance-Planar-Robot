import numpy as np
import matplotlib.pyplot as plt
import sys

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

        plt.subplot(211)
#        plt.plot(self.data['error'],'--', linewidth=1)
        mean = np.array(self.data['error'])
        plt.plot(np.sqrt(mean[:,0]**2 + mean[:,1]**2), linewidth=2)
        plt.title('Mean error: ' + '%.2f' %(np.mean(self.data['error'])))
        plt.grid()

        plt.subplot(212)
        m = np.array(self.data['min_dist']).min(axis=1)
        data = np.array(self.data['min_dist'])
        plt.plot(data[:,0],label='obstacle 1',linewidth=2)
        plt.plot(data[:,1],label='obstacle 2',linewidth=2)
        plt.plot(np.zeros(data.shape[0]), color='r')
        plt.title('Mean Minimum Distance: ' + '%.2f' %(m.mean()),y=0.85)
        plt.legend()
        plt.grid()
#        plt.savefig(sys.argv[2])


#        plt.subplot(312)
#        plt.plot(self.data['state'])
#        plt.title('state')
#        plt.grid()


        plt.show()
