import numpy as np
import matplotlib.pyplot as plt

from obspy.io.segy.core import _read_segy

from scipy import signal

from DASLowFreqProcessing import spool,terra_io,lfproc

import warnings
warnings.simplefilter('ignore')

class data:
    '''
    Handles the initial processing and plotting of DAS and sweep data
    Requires DASLowFreqProcessing modules
    '''
    
    def __init__(self):
        self.DASdata = np.empty(0)
        self.sweep = np.empty(0)
        self.dist = np.empty(0)
        
    def read_sweep(self, npoint: int, sweep: str, datapath: str) -> None:
        '''
        npoint: nth trigger point
        Read in the sweep data given the sweep filename and datapath
        Assumes the sweep data file is in segy format
        '''
        self.npoint = npoint
        
        sweepname = datapath + sweep
        self.st = _read_segy(sweepname)
        
        # read beginning and end time from the data as np.datetime64 objects
        self.bgtime = np.datetime64(str(self.st[0].stats.starttime)[0:-1])
        self.edtime = np.datetime64(str(self.st[0].stats.endtime)[0:-1])
        
    def read_data(self, datapath: str) -> None:
        #Read in the DAS data with matching time with the sweep data
        sp = terra_io.create_spool(datapath)
        sp.get_time_segments()

        self.DASdata = sp.get_patch(self.bgtime,self.edtime)[0]
        self.DASdata = self.DASdata.tran.velocity_to_strain_rate()
        
        # resample the sweep data to match DAS data's sampling rate
        self.sweep = signal.resample(self.st[0].data/max(self.st[0].data), self.DASdata.data.shape[0])
        
        # store distance and time data
        self.dist = self.DASdata.coords['distance']
        self.time = self.DASdata.coords['time']

    def plot_sweep(self, drivelevel = False) -> None:
        '''
        Plot the sweep data for time vs amplitude unless user specifies it to plot for time vs drive level
        '''

        if drivelevel:
            plt.figure(figsize = (10,5))
            plt.plot(self.time, self.sweep)
            
            plt.ylabel("Amplitude")

            plt.show()
            
        else:
            fig = plt.figure(figsize=(10,5))
            ax = fig.add_subplot(1,1,1)
            ax.plot(self.st[0].times("matplotlib"), self.st[0].data)

            ax.xaxis_date()
            fig.autofmt_xdate()
            
            plt.ylabel("Drive Level (kN)")

        plt.title(f"Sweep at Trigger Point {self.npoint}")
        plt.xlabel("Time (UTC)")
        plt.show()
        
    def plot(self, data, scale = 0.01) -> None:    # here can fix the correlated data
        '''
        Plots the DAS data using waterfall scaled at scale
        '''
        
        plt.figure(figsize = (7,7))
        plt.imshow(data, cmap = 'seismic', interpolation = 'nearest', aspect = 'auto', extent = (1.54, 1023.3091457785043, 0.06, 0))
        plt.colorbar()
               
    def correlate(self) -> None:
        '''
        Cross-correlate stores DAS and sweep data
        '''
        self.corr_data = np.empty(self.DASdata.data.shape)
        for i in range(self.DASdata.data[0].shape[0]):
            self.corr_data[:,i] = signal.correlate(self.DASdata.data[:,i], self.sweep, mode='same')
        
    def plot_powerspec(self, pspec: np.array, m: int) -> None:
        '''
        Plot the power spectrum of the array taken as an input
        specify the max frequency extent using m
        '''
        
        #create the min and max values
        vmin = np.percentile(np.log(pspec),5)
        vmax = np.percentile(np.log(pspec),95)

        plt.figure(figsize=(7,7))
        plt.imshow(np.log10(pspec), aspect='auto',cmap='seismic', extent=(1,1023.3091457785043,m,0))
        plt.clim(vmin= vmin,vmax=vmax)
        plt.colorbar(label = "Strain Rate($\log_{10}(1/s^2)$)")
        plt.xlabel("Distance (m)")
        plt.ylabel("Frequency (Hz)")
        
        plt.show()