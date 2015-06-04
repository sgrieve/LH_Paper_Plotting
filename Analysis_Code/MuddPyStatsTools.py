"""
Copyright (C) 2013 Simon M. Mudd 2014

Developer can be contacted by simon.m.mudd _at_ ed.ac.uk

This program is free software;
you can redistribute it and/or modify it under the terms of the
GNU General Public License as published by the Free Software Foundation;
either version 2 of the License, or (at your option) any later version.

This program is distributed in the hope that it will be useful,
but WITHOUT ANY WARRANTY;
without even the implied warranty of
MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.
See the GNU General Public License for more details.

You should have received a copy of the
GNU General Public License along with this program;
if not, write to:
Free Software Foundation, Inc.,
51 Franklin Street, Fifth Floor,
Boston, MA 02110-1301
USA
"""

# -*- coding: utf-8 -*-
# Some statistics tools

from scipy.stats import gaussian_kde
from numpy.random import normal
from numpy import arange
import numpy as np

# this calculates the MedianAbsoluteDeviation, 
# which is a robust way (that is, resistant to outliers)
# of quantifying dispersion
# see http://seismo.berkeley.edu/~kirchner/eps_120/Toolkits/Toolkit_02.pdf
# SMM 23/10/2014
def calculate_MedianAbsoluteDeviation(data):
    
    # get the median
    med = np.median(data) 
    
    # get the residuals
    resids = np.abs(data-med)
    
    # get the median of the residuals
    med_resids = np.median(resids)
    
    return med_resids
    
# this uses the gaussian kernal, a non-parametric way to estimate the
#  probability density function of a random variable. 
# (see: http://en.wikipedia.org/wiki/Kernel_density_estimation)
# to get the maximum probability
# SMM 23/10/2014
def calculate_MaxProbGaussKDE(data,Nbins=100):

    k = gaussian_kde(data) #calculates the kernel density
    m = k.dataset.min() #lower bound kernal
    M = k.dataset.max() #upper bound kernal
    
    # seperate the data into bins
    x = arange(m,M,(M-m)/Nbins) 
    
    # now find the maxium probability
    v = k.evaluate(x) 
    
    # call a function to get the indices into the maximum elements
    maxelem = maxelements(v.tolist())
    
    #print "indices of maximum: "
    #print maxelem
    n_maxelem = len(maxelem)
    
    posmax = []
    for i in range(n_maxelem):
        #print "This max is: " + str(x[maxelem[i]])
        posmax.append(x[maxelem[i]])
        
    return posmax
    
 
# Return list of position(s) of largest element
# from http://stackoverflow.com/questions/3989016/how-to-find-positions-of-the-list-maximum 
def maxelements(seq):
    
    max_indices = []
    if seq:
        max_val = seq[0]
        for i,val in ((i,val) for i,val in enumerate(seq) if val >= max_val):
            if val == max_val:
                max_indices.append(i)
            else:
                max_val = val
                max_indices = [i]

    return max_indices 