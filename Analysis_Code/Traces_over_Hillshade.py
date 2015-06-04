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

Method to plot a traces shapefile generated using Trace_Process_1_1.py over a 
hillshade of a landscape.
 
Parameters that need modified are highlighed with comments

Requires the python shapefile library availibile here: URL

@author: SWDG
"""

def mm_to_inch(mm):
    return mm*0.0393700787
    
def col_to_utm_x(XLL,ColIndex):
    return XLL + ColIndex

def row_to_utm_y(YLL,NRows,RowIndex):
    return YLL+(NRows-RowIndex)

import matplotlib.pyplot as plt
import numpy as np
import matplotlib.cm as cmx
from matplotlib import rcParams
import raster_plotter_simple as raster
import shapefile as shp
    
# Set up fonts for plots
rcParams['font.family'] = 'sans-serif'
rcParams['font.sans-serif'] = ['arial']
rcParams['font.size'] = 8
rcParams['xtick.direction'] = 'out'
rcParams['ytick.direction'] = 'out'

#================ modifyable parameters start here ====================

#paths to data here   
data_path = 'X:\\Figure_Code\\'
hillshade_file = 'OR_Clip_HS.flt'
trace_file = 'Traces_Aspect.shp'

#set plot limits
xmin_plot = 680
xmax_plot = 1290
ymin_plot = 285
ymax_plot = 780

#================ modifyable parameters end here ====================

#Load hillshaded DEM
hillshade, hillshade_header = raster.read_flt(data_path + hillshade_file)

#ignore nodata values    
hillshade = np.ma.masked_where(hillshade == -9999, hillshade) 

#get the dimensions of the raster to plot
x_max = hillshade_header[0]
x_min = 0
y_max = hillshade_header[1] 
y_min = 0
xll = hillshade_header[2] 
yll = hillshade_header[3]  
 
#create figure
fig = plt.figure() 
 

   
ax = plt.gca()

#plot the hillshade
plt.imshow(hillshade, vmin=0, vmax=255, cmap=cmx.gray) 

#place axis ticks around the bottom and left of the plot
plt.tick_params(axis='x', which='both', top='off',length=2)
plt.tick_params(axis='y', which='both', right='off',length=2)
   
# now get the tick marks    
n_target_tics = 5
xlocs,ylocs,new_x_labels,new_y_labels = raster.format_ticks_for_UTM_imshow(hillshade_header,x_max,x_min,y_max,y_min,n_target_tics)  
plt.xticks(xlocs, new_x_labels)
plt.yticks(ylocs, new_y_labels) 

x_center = int(x_max/2.)    
y_center = int(y_max/2.)    
   
#load trace shapefile
sf = shp.Reader(data_path + trace_file)

for shape in sf.shapes():
    x=[]
    y=[]
    for point in shape.points:
        #convert shapeile data into raster coords
        x.append(point[0]-xll)
        y.append((-1*point[1]) + yll + hillshade_header[1])
    ax.plot(x,y,'r-',linewidth=0.5,alpha=1)
    
#load channels
sf = shp.Reader(data_path + 'Chans.shp')

for shape in sf.shapes():
    x=[]
    y=[]
    for point in shape.points:
        #convert shapeile data into raster coords
        x.append(point[0]-xll)
        y.append((-1*point[1]) + yll + hillshade_header[1])
    plt.plot(x,y,'b-',linewidth=2)           

#set plot limits
plt.xlim(xmin_plot,xmax_plot)
plt.ylim(ymin_plot,ymax_plot)

#make white space for labels and ticks
plt.subplots_adjust(left = 0.2, hspace=0.05)

#label the axes with eating and northing
#fig.text(0.5, 0.02, 'Easting (m)', ha='center', va='center', size=9)
#fig.text(0.06, 0.45, 'Northing (m)', ha='center', va='center', rotation='vertical', size=9)
  
plt.xlabel('Easting (m)',fontsize=10)  
plt.ylabel('Northing (m)',fontsize=10)  
  
#plt.show()

#quarter page = 95*115
#half page = 190*115 (horizontal) 95*230 (vertical)
#full page = 190*230
fig.set_size_inches(mm_to_inch(95), mm_to_inch(115))
    
plt.savefig('Traces_over_Hillshade.png', dpi = 500) #change to *.tif for submission
