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

Script to generate Figure 9 from Grieve et al. (2015)

Input data is generated using LH_Driver.cpp

Parameters to be modified are highlighted by comments

@author: SWDG
"""

def mm_to_inch(mm):
    return mm*0.0393700787

import matplotlib.pyplot as plt
from matplotlib import rcParams
from matplotlib import container
    
# Set up fonts for plots
rcParams['font.family'] = 'sans-serif'
rcParams['font.sans-serif'] = ['arial']
rcParams['font.size'] = 12
rcParams['xtick.direction'] = 'out'
rcParams['ytick.direction'] = 'out'

#hard coded data
# hfr, sa, dd (measurement,MAD)
NC = ([89,17],[6,1],[39,10])
OR = ([123,50],[28,14],[58,33])
GM = ([103,26],[112,56],[42,14])
CR = ([104,35],[177,173],[33,13])

figpath = 'C:/Users/Stuart/Desktop/FR/final_figures_revision/'

fig = plt.figure()

ax = plt.gca()

fmt_str = ['ko','bo','ro']
labels = ['Hilltop flow routing','Slope-area','Drainage density']
locations = ['Coweeta', 'Oregon Coast\nRange', 'Gabilan Mesa', 'Sierra Nevada']
xlabel_indexes = [1, 4, 7, 10]

for i in range(3):
    plt.errorbar(i,NC[i][0],yerr=NC[i][1],fmt=fmt_str[i],label=labels[i])
    plt.errorbar(i+3,OR[i][0],yerr=OR[i][1],fmt=fmt_str[i])
    plt.errorbar(i+6,GM[i][0],yerr=GM[i][1],fmt=fmt_str[i])
    plt.errorbar(i+9,CR[i][0],yerr=CR[i][1],fmt=fmt_str[i])

#plot vertical lines between locations
plt.vlines(2.5,0,350, color='k',linewidth=1,linestyle='dashed')
plt.vlines(5.5,0,500, color='k',linewidth=1,linestyle='dashed')
plt.vlines(8.5,0,500, color='k',linewidth=1,linestyle='dashed')

#set plot limit
plt.ylim(0,400)
plt.xlim(-0.5,11.5)

#remove the errorbars from the legend
handles, labels = ax.get_legend_handles_labels()   
handles = [h[0] if isinstance(h, container.ErrorbarContainer) else h for h in handles]  
plt.legend(handles, labels, loc=2, numpoints=1,scatterpoints=1)

#format the ticks to only appear on the bottom and left axes 
plt.tick_params(axis='x', which='both', top='off',length=0)
plt.tick_params(axis='y', which='both', right='off',length=2)

plt.ylabel('Hillslope Length (m)',size=12)

#Label the xaxis with the study locations
plt.xticks(range(12))
xlabels = [item.get_text() for item in ax.get_xticklabels()]

for loc,ind in zip(locations,xlabel_indexes):
    xlabels[ind] = loc
 
ax.set_xticklabels(xlabels)

#set the size of the plot to be saved. These are the JGR sizes:
#quarter page = 95*115
#half page = 190*115 (horizontal) 95*230 (vertical)
#full page = 190*230
fig.set_size_inches(mm_to_inch(190), mm_to_inch(115))
   
plt.savefig(figpath+'Figure_9.png', dpi = 500) #change to *.tif for submission
