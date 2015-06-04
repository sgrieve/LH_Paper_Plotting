# -*- coding: utf-8 -*-
"""
Copyright (C) 2015 Stuart W.D Grieve 2015

Developer can be contacted by s.grieve _at_ ed.ac.uk

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

Script to perform fitting of LH and Relief data from *_HilltopData.csv generated
by LH_Driver.cpp

Plots the data and calculates the best fit S_c value given the erosion rate, 
diffusivity and material densities.

Parameters and paths to be modified are highlighted by comments. 

@author: SWDG
"""

def mm_to_inch(mm):
    return mm*0.0393700787
    
def LH_Rel(k,Sc):
    """
    This is a bit messy. To use the scipy optimizer we need to declare a fn with independent variables
    (LH,pr,pr,Diff,erosion rate) as a tuple followed by the parameter to be optimised, Sc, as the second
    input argument.
    
    We have the values of all of the independent variables so we want to create a series of numpy arrays
    of the same dimensions as LH, filled with the parameter values which have been published.
    
    This FN is implementing equation 10 from Grieve et al 2015, based on work in Roering 2007
    """
    
    x = k[0]    
    DD = k[1]
    EE = k[2]
    pr = k[3]
    ps = k[4]   
        
    A = (2.*EE*pr)/(DD*Sc*ps)                                
    return (Sc * (-1. + np.sqrt(1 + A**2. * x**2.) + np.log(3.) - np.log(2. + np.sqrt(1. + A**2. * x**2.))))/A    

def r_squared(modeled, measured):
   
    mean_measured = np.mean(measured)  
   
    sqr_err_w_line=[]
    sqr_err_mean = []    
   
    for measure,mod in zip(measured,modeled):
        sqr_err_w_line.append((mod-measure)**2)
        sqr_err_mean.append((measure-mean_measured)**2)
    
    r_sq = 1-(np.sum(sqr_err_w_line)/np.sum(sqr_err_mean))
    
    return r_sq

def fill_array(array, value):
    """
    Quick wrapper to replace the np.ndarray.full_like function which is not present in numpy 1.6
    """
    
    New_Array = array.copy()
    New_Array.fill(value)
    
    return New_Array


import matplotlib.pyplot as plt
import numpy as np
from matplotlib import rcParams
import scipy.optimize as optimization
    
# Set up fonts for plots
rcParams['font.family'] = 'sans-serif'
rcParams['font.sans-serif'] = ['arial']
rcParams['font.size'] = 10
rcParams['xtick.direction'] = 'out'
rcParams['ytick.direction'] = 'out'

#================ modifyable parameters start here ====================

path = 'C:/Users/Stuart/Desktop/FR/' #path to the folder contaning the hilltopdata files
Filename = 'CR2_HilltopData.csv'
figpath = path #path to save the final figures

#soil and rock density data
#roering 2007 has a ratio of 1.5 to 2 but does not double rho_s  
#hillel 1980 fundamentals of soil physics says soil ranges between 1.1 and 1.6
pr = 2.4 *1000 #kg/m^3  (2.4 is in g/cm^3)
ps = 1.4 *1000 

#diffusivity and erosion rate data published for the sites
DD = 0.0086
EE = 0.25

#plot style parameters
xmax = 400
ymax = 300
xstep = 100
ystep = 100

#plot labels
location = 'Sierra Nevada'


#initial Sc guess - we need to see the fitting with a sane value
#optimizer has been tested and is NOT sensitive to this param. Just choose something vaguely sane
init_Sc = 0.8

#================ modifyable parameters end here ====================

fig = plt.figure()

#load the lh and relief data from the hilltopdata file
with open(path + Filename,'r') as f:
    f.readline()
    data = f.readlines()

LH_Data = []
R_Data = []

#get the data and remove any values below 2 as these are probably artifacts
for d in data:
    if 'fail' not in d and len(d.split(','))>10: #len is used to skip incomplete data when processing plots on files that have ont finished running
        split = d.split(',')
        relief = float(split[4])
        lh = float(split[5])            
        slope = float(split[8])                                
        EucDist = float(split[13])            
        if (lh > 2.0):
            if (relief > 2.0):                   
                if (slope < 1.2):                        
                    if (EucDist/lh > 0.9999 and EucDist/lh < 1.0001):                        
                        LH_Data.append(lh)
                        R_Data.append(relief)
                                                
#convert the lists into arrays
LH_Data = np.array(LH_Data[:])
R_Data = np.array(R_Data[:])

#create the subplot and put the location name at the top
ax = plt.gca()
ax.text(.5,.9,location, horizontalalignment='center', transform=ax.transAxes, fontsize=16)

#create the parameter arrays
EE_array = fill_array(LH_Data,EE)
DD_array = fill_array(LH_Data,DD)
Pr_array = fill_array(LH_Data,pr)
Ps_array = fill_array(LH_Data,ps)

#just want the params from the fit, dont need the covariance matrix, _    
params, _ = optimization.curve_fit(LH_Rel, (LH_Data,DD_array,EE_array,Pr_array,Ps_array), R_Data, init_Sc)
    
#get the optimized Sc
Sc = params[0]

#generate the best fit line using the S_c value
modeled_y = []

for data in LH_Data:        
    modeled_y.append(LH_Rel((data,DD_array[0],EE_array[0],Pr_array[0],Ps_array[0]),params[0]))

#get the r_squared of the fit
r_sq = r_squared(R_Data,modeled_y)

#sort the modeled data by LH, so that it can be plotted as a line    
sorted_data =  sorted(zip(LH_Data, modeled_y))
LH_Sorted = [x[0] for x in sorted_data]
R_Sorted = [x[1] for x in sorted_data]

#plot the raw data and the line
plt.scatter(LH_Data, R_Data, s=5, marker="o", c='k', edgecolors='none')
plt.plot(LH_Sorted,R_Sorted,'r-')

#annotate the figure with the r squared and critical slope value    
plt.annotate('$\mathregular{R^2}$= '+str(round(r_sq,2)), xy=(0.1, 0.8), xycoords='axes fraction', fontsize=12,
        horizontalalignment='left', verticalalignment='bottom')
plt.annotate('$\mathregular{S_c}$= '+str(round(Sc,2)), xy=(0.1, 0.73), xycoords='axes fraction', fontsize=12,
        horizontalalignment='left', verticalalignment='bottom')
   
#set the x and y max based on the input params
plt.xlim(0,xmax)
plt.ylim(0,ymax)

#configure tick spacing based on the defined spacings given
ax.xaxis.set_ticks(np.arange(0,xmax+1,xstep))
ax.yaxis.set_ticks(np.arange(0,ymax+1,ystep))

#format the ticks to only appear on the bottom and left axes    
plt.tick_params(axis='x', which='both', top='off',length=2)
plt.tick_params(axis='y', which='both', right='off',length=2)

    
#adjust the spacing between the 4 plots
plt.subplots_adjust(hspace = 0.3)

#add in the x and y labels
fig.text(0.5, 0.02, 'Hillslope length (m)', ha='center', va='center', size=12)
fig.text(0.06, 0.5, 'Relief (m)', ha='center', va='center', rotation='vertical', size=12)

plt.show()

#set the size of the plot to be saved. These are the JGR sizes:
#quarter page = 95*115
#half page = 190*115 (horizontal) 95*230 (vertical)
#full page = 190*230
fig.set_size_inches(mm_to_inch(190), mm_to_inch(115))
    
plt .savefig(figpath + 'LH_Relief_Fit.png', dpi = 500) #change to *.tif for submission