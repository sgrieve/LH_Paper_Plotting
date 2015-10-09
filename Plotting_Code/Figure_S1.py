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


Loads 4 hillshade rasters in flt format, draped a floodplain mask over them 
and tiles the images with correct UTM coordinates and labels them.

Inputs: 4 flt format floodplain masks
        
        4 hillshade files of the study areas in flt format
        
See the method Make_The_Figure() to understand how to supply these input files.
    

Created on Fri May 29 13:22:19 2015

@author: Stuart Grieve
"""


def mm_to_inch(mm):
    return mm*0.0393700787

def Mask_Hillshades(files,masks):
    
    import matplotlib.pyplot as plt
    import numpy as np
    import matplotlib.cm as cmx
    from matplotlib import rcParams
    import raster_plotter_simple as raster
            
    # Set up fonts for plots
    rcParams['font.family'] = 'sans-serif'
    rcParams['font.sans-serif'] = ['arial']
    rcParams['font.size'] = 12
    rcParams['xtick.direction'] = 'out'
    rcParams['ytick.direction'] = 'out'
        
    fig = plt.figure()
    
    labels = ['a','b','c','d']
    
    for i in range(1,5):
        
        ax = plt.subplot(2,2,i)
        
        #get data
        hillshade, hillshade_header = raster.read_flt(files[i-1])
        mask, mask_header = raster.read_flt(masks[i-1])
       
        #ignore nodata values    
        hillshade = np.ma.masked_where(hillshade == -9999, hillshade)    
        mask = np.ma.masked_where(mask == -9999, hillshade)    
        
        x_max = hillshade_header[0]
        x_min = 0
        y_max = hillshade_header[1] 
        y_min = 0
        
        #plot the hillshade on the axes
        plt.imshow(hillshade, vmin=0, vmax=255, cmap=cmx.gray) 
        plt.imshow(mask,cmap=cmx.Reds)
            
        #place axis ticks around the outside of each plot
        if (i == 1): #top left  
            ax.xaxis.tick_top() 
            plt.tick_params(axis='x', which='both', bottom='off',length=2)
            plt.tick_params(axis='y', which='both', right='off',length=2)
        if (i == 2): #top right        
            ax.xaxis.tick_top()
            ax.yaxis.tick_right()
            plt.tick_params(axis='x', which='both', bottom='off',length=2)
            plt.tick_params(axis='y', which='both', left='off',length=2)
        if (i == 3): #bottom left        
            plt.tick_params(axis='x', which='both', top='off',length=2)
            plt.tick_params(axis='y', which='both', right='off',length=2) 
            plt.ylabel('Northing (m)', size=14,color='white') #create an invisible label here to create the padding for the real label later on
            ax.yaxis.labelpad = 10
        if (i == 4): #bottom right
            ax.yaxis.tick_right()        
            plt.tick_params(axis='x', which='both', top='off',length=2)
            plt.tick_params(axis='y', which='both', left='off',length=2)
    
        # now get the tick marks    
        n_target_tics = 4
        xlocs,ylocs,new_x_labels,new_y_labels = raster.format_ticks_for_UTM_imshow(hillshade_header,x_max,x_min,y_max,y_min,n_target_tics)  
        plt.xticks(xlocs, new_x_labels, rotation=60)
        plt.yticks(ylocs, new_y_labels) 
        
        plt.annotate(labels[i-1], xy=(0.92, 0.96), backgroundcolor='white', xycoords='axes fraction', fontsize=10, horizontalalignment='left', verticalalignment='top')
    
        x_center = int(x_max/2.)    
        y_center = int(y_max/2.)    
        
        plt.xlim(x_center-2000,x_center+2000)    
        plt.ylim(y_center+2000,y_center-2000)        
        
    
    fig.text(0.5, 0.02, 'Easting (m)', ha='center', va='center', size=14)
    fig.text(0.02, 0.5, 'Northing (m)', ha='center', va='center', rotation='vertical', size=14)
    
    plt.tight_layout()  
    
    #quarter page = 95*115
    #half page = 190*115 (horizontal) 95*230 (vertical)
    #full page = 190*230
    fig.set_size_inches(mm_to_inch(190), mm_to_inch(200))
        
    plt.savefig('Figure_S1.png', dpi = 250)
   
    
def Make_The_Figure():
    """
    All filenames and paths to data are modifed here in this wrapper
    """

    Hillshade_files = ['NC_HS.flt','OR_HS.flt','GM_HS.flt','CR2_HS.flt']    
    Mask_files = ['NC_FloodPlain.flt','OR_FloodPlain.flt','GM_FloodPlain.flt','CR2_FloodPlain.flt',]

    Mask_Hillshades(Hillshade_files,Mask_files)
        
    
Make_The_Figure()    
    