# -*- coding: utf-8 -*-
"""
Created on Thu Nov  2 11:23:48 2023

@author: 2393967m
"""

import numpy as np
import matplotlib.pyplot as plt 
import scipy as sp
import scipy.signal as signal

data = np.loadtxt("ECGnoise.dat")

M = 200
Fs = 500

y = data[:,1]
t = data[:,0]


k1 = int(45/Fs) * M
k2 = int(55/Fs) * M

X = np.ones(M)

X[k1: k2+1] = 0
X[M-k2:M-k1+1] = 0

x = np.fft.ifft(X)
x = np.real(x)

h = np.zeros(M)

h[0:int(M/2)] = x[int(M/2):M]
h[int(M/2):M] = x[0:int(M/2)]

h = h*np.hamming(M)

y2 = signal.lfilter(h,1,y)

plt.plot(y2)