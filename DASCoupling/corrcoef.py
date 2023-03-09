import numpy as np
import matplotlib.pyplot as plt

from scipy import stats

import warnings
warnings.simplefilter('ignore')

class corrcoef():
    '''
    Calculates the correlation coefficients
    Does not require DASLowFreqProcessing modules
    '''
    
    def __init__(self, data: np.array, buf = 4):
        self.buf = buf
        self.data = data
        self.init_matrix = np.empty((self.data.shape[1]-self.buf, self.buf))
        self.corr_matrix = np.empty(0)
        self.median = 0

    def pearson(self):
        '''
        Calculates the correlation coefficients using Pearson
        '''
        
        # compare buf number of neiboring channels
        for i in range(self.data.shape[1]-self.buf):
            for j in range(1,self.buf):
                self.init_matrix[i,j] = stats.pearsonr(self.data[:,i], self.data[:,i+j])[0]

        self.corr_matrix = np.zeros(self.init_matrix.shape[0])
        
        # take the median of the coefficients calculated above and assign the median for each channel
        for i in range(self.init_matrix.shape[0]):
            self.corr_matrix[i] = np.median(self.init_matrix[i,:])

        # store the median of all coefficient values
        self.median = np.median(self.corr_matrix)

    def spearman(self):
        '''
        Calculates the correlation coefficients using Spearman
        '''
        
        # compare buf number of neiboring channels
        for i in range(self.data.shape[1]-self.buf):
            for j in range(1,self.buf):
                self.init_matrix[i,j] = stats.spearmanr(self.data[:,i], self.data[:,i+j], axis = None, nan_policy = 'omit')[0]

        self.corr_matrix = np.zeros(self.init_matrix.shape[0])
        
        # take the median of the coefficients calculated above and assign the median for each channel
        for i in range(self.init_matrix.shape[0]):
            self.corr_matrix[i] = np.median(self.init_matrix[i,:])

        # store the median of all coefficient values
        self.median = np.median(self.corr_matrix)

    def stats(self):
        '''
        Print the mean and median of all stores correlation coefficient values
        '''
        print(f"Mean: {np.mean(self.corr_matrix)}, median = {np.median(self.corr_matrix)}")

    def find_bad(self, thresh: int) -> np.array:
        '''
        Find the indices of correlation coefficients where the value is less than the threshhold value as a numpy array
        '''
        self.bad = np.array(np.where(self.corr_matrix < thresh))
        return self.bad

    def plot_corr(self):
        '''
        Plot all correlation coefficients
        '''
        plt.title(f"Correlation Coefficient at moving window {self.buf}")
        plt.plot(self.corr_matrix)

        plt.xlabel("Channel Number")
        plt.ylabel("Correlation Coefficient")

        plt.show()

    def plot_hist(self):
        '''
        Plot the histogram of all correlation coefficients
        '''
        plt.title(f"Correlation Coefficient at moving window {self.buf}")
        plt.hist(self.corr_matrix)

        plt.xlabel("Correlation Coefficient")
        plt.ylabel("Occurences")

        plt.show()