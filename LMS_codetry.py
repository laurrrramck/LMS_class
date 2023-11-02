# -*- coding: utf-8 -*-
"""
Created on Thu Nov  2 13:04:58 2023

@author: 2393967m
"""

import numpy as np
import pylab as pl
import LMS_class

fs = 1000
NTAPS = 500
LEARNING_RATE = 0.001
fnoise = 50

ecg = np.loadtxt("ECGnoise.dat")
pl.figure(1)
pl.plot(ecg)

f = LMS_class.FIR_filter(np.zeros(NTAPS))

y = np.empty(len(ecg))
for i in range (len(ecg)):
    ref_noise = np.sin(2.0*np.pi*fnoise/fs * i );
    canceller = f.filter(ref_noise)
    output_signal = ecg[i] - canceller 
    f.lms(output_signal, LEARNING_RATE)
    y[i] = output_signal
    
    
    
pl.figure(2)
pl.plot(y)
pl.show()
