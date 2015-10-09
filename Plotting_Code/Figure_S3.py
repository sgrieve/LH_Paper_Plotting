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

datapath = 'X:/SA_DATA/'
figpath = ''

filenames = ['NC_2_SA_Data.txt','NC_28_SA_Data.txt','NC_34863_SA_Data.txt',
             'OR_3_SA_Data.txt','OR_7_SA_Data.txt','OR_6775_SA_Data.txt',
             'GM_11_SA_Data.txt','GM_111_SA_Data.txt','GM_1418_SA_Data.txt',
             'CR_1_SA_Data.txt','CR_177_SA_Data.txt','CR_644550_SA_Data.txt']

labels = list(string.ascii_lowercase)[:4]
headings = ['Lower Bound', 'Median', 'Upper Bound']

fig = plt.figure()

for i,filename in enumerate(filenames):

    ax = plt.subplot(4,3,i+1)
    with open(datapath+filename,'r') as f:
        data = f.readlines()
    
    slope = []
    area = []
        
    for d in data:
        split = d.split()
        area.append(split[0])    
        slope.append(split[1])
    
    
    LH = int(filename.split('_')[1])  
    
    plt.ylim(0.03,1.2)
    plt.xlim(0.8,1000000)
    
    if i < 3:
        plt.title(headings[i])
           
    #format the ticks to only appear on the bottom and left axes 
    plt.tick_params(axis='x', which='both', top='off',length=2)
    plt.tick_params(axis='y', which='both', right='off',length=2)     
    plt.tick_params(axis='x', which='minor', bottom='off',length=2)
    plt.tick_params(axis='y', which='minor', left='off',length=2)
    
    ax.set_yscale('log', nonposy='clip')
    ax.set_xscale('log', nonposx='clip')
    
    for label in ax.get_xticklabels()[1::2]:
        label.set_visible(False)    
    
      
    if (i == 0):
        ax.axes.get_xaxis().set_ticklabels([])
    elif (i == 3):
        ax.axes.get_xaxis().set_ticklabels([])
    elif (i == 6):
        ax.axes.get_xaxis().set_ticklabels([])
    elif (i == 9):
        pass
    elif (i == 10):
        ax.yaxis.set_visible(False)
    elif (i == 11):
        ax.yaxis.set_visible(False)    
    else:
        ax.axes.get_xaxis().set_ticklabels([])
        ax.axes.get_yaxis().set_ticklabels([])

    plt.plot(area,slope,'b.')
   
    plt.vlines(LH,0.03,1.5, color='k',linewidth=1,linestyle='dashed')
    
    
    if i == 2:     
        plt.annotate(labels[0], xy=(0.9, 0.95), xycoords='axes fraction', fontsize=10, horizontalalignment='left', verticalalignment='top')
    if i == 5:     
        plt.annotate(labels[1], xy=(0.9, 0.95), xycoords='axes fraction', fontsize=10, horizontalalignment='left', verticalalignment='top')
    if i == 8:     
        plt.annotate(labels[2], xy=(0.9, 0.95), xycoords='axes fraction', fontsize=10, horizontalalignment='left', verticalalignment='top')
    if i == 11:     
        plt.annotate(labels[3], xy=(0.9, 0.95), xycoords='axes fraction', fontsize=10, horizontalalignment='left', verticalalignment='top')

    
    
    
#x and y axis labels
fig.text(0.5, 0.04, 'Drainage area (m$^2$)', ha='center', va='center', size=12)
fig.text(0.06, 0.5, 'Slope (m/m)', ha='center', va='center', rotation='vertical', size=12)
        
fig.subplots_adjust(hspace=0.05, wspace=0.05)
    
#set the size of the plot to be saved. These are the JGR sizes:
#quarter page = 95*115
#half page = 190*115 (horizontal) 95*230 (vertical)
#full page = 190*230
fig.set_size_inches(mm_to_inch(190), mm_to_inch(230))
 
#plt.show()
   
plt.savefig(figpath+'Figure_S3.png', dpi = 500) #change to *.tif for submission