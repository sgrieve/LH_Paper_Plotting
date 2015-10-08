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

Script to generate Figure 5 from Grieve et al. (2015)

Input data is generated using LH_Driver.cpp

Parameters to be modified are highlighted by comments

@author: SWDG
"""

def mm_to_inch(mm):
    return mm*0.0393700787

import matplotlib.pyplot as plt
from matplotlib import rcParams
import MuddPyStatsTools as mpy
import numpy as np
import string
    
# Set up fonts for plots
rcParams['font.family'] = 'sans-serif'
rcParams['font.sans-serif'] = ['arial']
rcParams['font.size'] = 10
rcParams['xtick.direction'] = 'out'
rcParams['ytick.direction'] = 'out'

#================ modifyable parameters start here ====================

#paths to the data and to save the figure to
path = 'C:/Users/Stuart/Dropbox/LH_Paper/or/' #path to the folder contaning the hilltopdata files
filename = 'OR_PaperData.txt'#names of the hilltopdata file
figpath = 'C:/Users/Stuart/Desktop/FR/final_figures_revision/' #path to save the final figure

#plot style parameters
xmaxes = [250,200,300]
ymaxes = [52,200,90]
xsteps = [50,100,100]
ysteps = [10,40,30]
v_line_lims = [5,0,0]

#plot labels
Methods = ['Hilltop Flow Routing','Slope-Area','Drainage Density']
fig_labels = list(string.ascii_lowercase)[:3] #generate subplot labels

#number of bins in the histograms
nbins = 20

#================ modifyable parameters end here ====================

fig = plt.figure()

#load the paperdata file to get the LH data
with open(path+filename,'r') as f:
    f.readline()
    data = f.readlines()

    lh_ = []
    SA = []
    SA_Plot =[]
    DD = []        
    for d in data:       
        split = d.split()        
        lh = float(split[2])
        sa_lh = float(split[9])        
        dd = float(split[11])        
        
        if (sa_lh > 2.0):           
            SA.append(sa_lh)
            if (sa_lh < 400.):
                SA_Plot.append(sa_lh)
        if (lh > 2.0):           
            lh_.append(lh)
        if (dd > 2.0):           
            DD.append(dd)

Calc_Data = [lh_,SA,DD]
Plot_Data = [lh_,SA_Plot,DD]

for subplot_count, (Method,xmax,ymax,xstep,ystep,labels,v_line_lim) in enumerate(zip(Methods,xmaxes,ymaxes,xsteps,ysteps,fig_labels,v_line_lims)):

    LH = Calc_Data[subplot_count]
        
    #get the median absolute devaition
    MAD = mpy.calculate_MedianAbsoluteDeviation(LH)
    
    #set up the 4 subplots
    ax = plt.subplot(3,1,subplot_count + 1)
    
    #Add a title with the location name
    ax.text(.5,.9,Method, horizontalalignment='center', transform=ax.transAxes,fontsize=12)
    
    #plot the histogram and get the patches so we can colour them
    n,bins,patches = plt.hist(Plot_Data[subplot_count],bins=nbins,color='k',linewidth=0)
    
    #get the median -/+ median devaition
    MinMAD = np.median(LH)-MAD
    MaxMAD = np.median(LH)+MAD

    #color the bins that fall within +/- MAD of the median    
    #http://stackoverflow.com/questions/6352740/matplotlib-label-each-bin
    for patch, rightside, leftside in zip(patches, bins[1:], bins[:-1]):
        if rightside < MinMAD:        
            patch.set_alpha(0.4)
        elif leftside > MaxMAD:
            patch.set_alpha(0.4)
    
    #Insert dashed red line at median
    plt.vlines(np.median(LH),0,ymax-v_line_lim,label='Median', color='r',linewidth=1,linestyle='dashed')

    #set x axis limits    
    plt.xlim(0,xmax)
    plt.ylim(0,ymax)

    #format the ticks to only appear on the bottom and left axes 
    plt.tick_params(axis='x', which='both', top='off',length=2)
    plt.tick_params(axis='y', which='both', right='off',length=2)
    
    #configure tick spacing based on the defined spacings given
    ax.xaxis.set_ticks(np.arange(0,xmax+1,xstep))
    ax.yaxis.set_ticks(np.arange(0,ymax+1,ystep))
    
    #annotate the plot with the median and MAD and the subplot label
    plt.annotate('Median = '+str(int(round(np.median(LH),0)))+' m\nMAD = '+str(int(round(MAD,0)))+' m', xy=(0.6, 0.7), xycoords='axes fraction', fontsize=10, horizontalalignment='left', verticalalignment='top')
    plt.annotate(labels, xy=(0.95, 0.95), xycoords='axes fraction', fontsize=10, horizontalalignment='left', verticalalignment='top')

#spacing of the plots
plt.subplots_adjust(hspace = 0.25,left=0.2)

#x and y axis labels
fig.text(0.5, 0.05, 'Hillslope length (m)', ha='center', va='center', size=12)
fig.text(0.06, 0.5, 'Count', ha='center', va='center', rotation='vertical', size=12)

# title
fig.text(0.55, 0.925, 'Oregon Coast Range', ha='center', va='center', size=14)


#set the size of the plot to be saved. These are the JGR sizes:
#quarter page = 95*115
#half page = 190*115 (horizontal) 95*230 (vertical)
#full page = 190*230
fig.set_size_inches(mm_to_inch(95), mm_to_inch(200))
    
plt.savefig(figpath+'Figure_5.png', dpi = 500) #change to *.tif for submission
