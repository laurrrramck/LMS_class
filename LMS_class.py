# -*- coding: utf-8 -*-
"""
Created on Thu Nov  2 12:57:24 2023

@author: 2393967m
"""
import numpy as np
import pylab as pl

class FIR_filter:
    def __init__(self, _coefficients):
        self.ntaps = len(_coefficients)
        self.coefficients = _coefficients
        self.buffer = np.zeros(self.ntaps)
        
    def filter(self, v):
        for j in range (self.ntaps-1):
            self.buffer[self.ntaps-j-1] = self.buffer[self.ntaps-j-2]
        self.buffer[0] = v
        return np.inner(self.buffer, self.coefficients)
    
    def lms(self, error, mu = 0.01):
        for j in range(self.ntaps):
            self.coefficients[j]= self.coefficients[j]+ error *mu * self.buffer[j]
            
            