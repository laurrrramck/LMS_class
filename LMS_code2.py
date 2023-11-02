# -*- coding: utf-8 -*-
"""
Created on Thu Nov  2 13:30:46 2023

@author: 2393967m
"""

import numpy as np
import matplotlib.pyplot as plt
import scipy as sp
import scipy.signal as signals

class FIRfilter:
    def __init__(self,_coefficients):
        self._coefficients = _coefficients
        self.ntaps = len(self._coefficients)
        self.buffer = np.zeros(self.ntaps)
        self.offset = 0
    
  #  def dofilter(self,v):
  #      self.buffer = np.roll(self.buffer,1)
  #      self.buffer[0] = v
   #     if self.offset == self.ntaps:
     #       self.offset = 0
   #     else: self.offset += 1
  #      product = np.multiply(self.buffer,self._coefficients)
   #     value = np.sum(product)
   #     return value
    
    def doFilterAdaptive(self,signal,noise,learningRate):
        f = FIRfilter(np.zeros(self.ntaps))
        y = np.empty(len(signal))
        for i in range(len(signal)):
            ref_noise = np.sin(2.0*np.pi*noise/1000 * i );
            canceller = f.filter(ref_noise)
            error = signal[i] - canceller
       
        for j in range (self.ntaps):
            self.coefficients[j] = self.coefficients[j]+error*learningRate*self.buffer[j]   #changes coefficients
            y[j] = error
        return y

class ECG:
    def __init__(self, time, samples):
            if time != 0:
                self.time = time
            else:
                self.time = []
            if samples != 0:
                self.samples = samples
            else:
                self.samples = []

def plot_filter(ECG_in, ECG_out, ls, hs):
    plt.figure()
    plt.subplot(221)
    plt.plot(ECG_in.time, ECG_in.samples)
    plt.xlabel("Time (s)")
    plt.ylabel("Signal Amplitude")
    plt.subplot(222)
    plt.plot(ECG_out.time, ECG_out.samples)
    plt.xlabel("Time (s)")
    plt.ylabel("Signal Amplitude")
    plt.subplot(223)
    plt.plot(ECG_in.time[ls:hs], ECG_in.samples[ls:hs])
    plt.xlabel("Time (s)")
    plt.ylabel("Signal Amplitude")
    plt.subplot(224)
    plt.plot(ECG_out.time[ls:hs], ECG_out.samples[ls:hs])
    plt.xlabel("Time (s)")
    plt.ylabel("Signal Amplitude")
    plt.show()
    return


def menu():

    return

def FIR_coeff(fs, lpf, nf):
    nw = 10 # number of bins to cut above and below notch cut-off
    lpf = int(lpf)
    nf = int(nf)
    ntaps = int(fs*2) #number of taps = sample rate
    xbs = np.ones(ntaps, np.float32) #create array of 1's
    xbs[nf-nw:nf+nw] = 0 # set notch frequencies to 0
    xlp = [0]*ntaps
    xlp[0:lpf] = np.sinc(np.linspace(0, 1, lpf)) #create sinc function array
    xf = [1]*ntaps #create array of ones
    xf = np.multiply(xf, xbs) # multiply by band stop array
    xf = np.multiply(xf, xlp) # multiply by sinc array
    xf[0] = 0
    xf = np.append(xf, np.flip(xf))
    plt.plot(xf)
    plt.show()
    xt = np.abs(np.fft.ifft(xf))
    xt = np.fft.ifft(xf) 
    return xt

        
def main():
    selection = input('\n---Choose Input File---\n1: Clean ECG\n2: Noisy ECG\n')
    if selection == '1':
        ECGdata = 'ECGclear.dat'
    elif selection == '2':
        ECGdata = 'ECGnoise.dat'

    with open(ECGdata, 'r') as data:
        ECG_in = ECG([],[])
        for line in data:
            line_temp = line.split()
            ECG_in.time.append (float(line.split()[0])) 
            ECG_in.samples.append (float(line.split()[1]))

    h = FIR_coeff(1000, 150, 50)
    myFIR = FIRfilter(h)
    ECG_out = ECG(ECG_in.time,[])
    
    for s in ECG_in.samples:
        ECG_out.samples.append(myFIR.doFilterAdaptive(s, h, 0.001))
    
    plot_filter(ECG_in, ECG_out, 2000, 5000)
    return


if __name__ == "__main__":
    main()


 
        
    
         
         
         
         
         
         
         
         
         
         
         
         
#returns clean ecg