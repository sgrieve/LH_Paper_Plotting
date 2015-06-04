"""
Copyright (C) 2013 Stuart W.D Grieve and Simon M. Mudd 2013

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
"""
##=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-
## Functions to read raster data in *.flt or *.asc format into numpy arrays
## and a function to create correct UTM tick labels for these raster files
##                     
## flt reading Built around code from http://pydoc.net/Python/PyTOPKAPI/0.2.0/pytopkapi.arcfltgrid/
##=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-
## SWDG 19/06/2013
## modified SMM 09/08/2013
##=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-

def round_to_n(x, n):
    if n < 1:
        raise ValueError("number of significant digits must be >= 1")
    # Use %e format to get the n most significant digits, as a string.
    format = "%." + str(n-1) + "e"
    as_string = format % x
    return float(as_string)


def read_headers(input_file):
    """
    Read the headers of a raster, returning the header info in a list with the 
    following structure:
        
        [ncols, nrows, xllcorner, yllcorner, cellsize, NODATA_value, byteorder]
                
    """

    with open(input_file+'.hdr','r') as f:   
        return [float(h) if not h.isalpha() else h for h in [l.split()[1] for l in f.readlines()]]  #isdigit() does not catch floats      

def read_bin(filename):
    """
    Method to read the binary data from an flt file, called by the wrapper.
    """
    import sys
    import numpy as np

    with open(filename + '.flt', "rb") as f:
        raster_data = np.fromstring(f.read(), 'f')

    if sys.byteorder == 'big':
        raster_data = raster_data.byteswap()  #ensures data is little endian

    return raster_data
    
def read_flt(input_file):
    """
    Wrapper method to read the header and data of a *.flt file. Pass in a filename
    amd it returns the data as a 2D numpy array and the header data as a list.
    """

    if input_file.endswith('.flt') or input_file.endswith('.hdr'):
        input_file = input_file[:-4]    
    else:
        print 'Incorrect filename'
        return 0,0 #exits module gracefully
    
    headers = read_headers(input_file)
    
    #read the data as a 1D array and reshape it to the dimensions in the header
    raster_array = read_bin(input_file).reshape(headers[1], headers[0]) 
    raster_array = raster_array.reshape(headers[1], headers[0]) #rows, columns

    return raster_array, headers

def read_ascii_raster(ascii_raster_file):
    """
    Wrapper method to read the header and data of a *.asc file. Pass in a filename
    amd it returns the data as a 2D numpy array and the header data as a list.
    """
    import numpy as np
    
    with open(ascii_raster_file) as f:
        header_data = [float(f.next().split()[1]) for x in xrange(6)] #read the first 6 lines
         
    raster_data = np.genfromtxt(ascii_raster_file, delimiter=' ', skip_header=6)
    raster_data = raster_data.reshape(header_data[1], header_data[0]) #rows, columns
    
    return raster_data, header_data

def format_ticks_for_UTM_imshow(hillshade_header,x_max,x_min,y_max,y_min,n_target_tics):
    """
    Method to create correctly formatted UTM ticks for plotting the raster files.
    Pass in the header list, x and y dimensions and the number of ticks required
    for each axis.
    
    Returns the locations and labels of the new ticks which can be fed into matplotlib.
    
    SMM
    """
    import numpy as np    
   
    xmax_UTM = hillshade_header[2]+x_max*hillshade_header[4]
    xmin_UTM = hillshade_header[2]+x_min*hillshade_header[4]
      
    # need to be careful with the ymax_UTM since the rows go from the top
    # but the header index is to bottom corner    
    
    #convert coordinates to UTM
    ymax_from_bottom = hillshade_header[1]-y_min
    ymin_from_bottom = hillshade_header[1]-y_max
    ymax_UTM = hillshade_header[3]+ymax_from_bottom*hillshade_header[4]
    ymin_UTM = hillshade_header[3]+ymin_from_bottom*hillshade_header[4]
        
    dy_fig = ymax_UTM-ymin_UTM
    dx_fig = xmax_UTM-xmin_UTM
    
    dx_spacing = dx_fig/n_target_tics
    dy_spacing = dy_fig/n_target_tics
    
    if (dx_spacing>dy_spacing):
        dy_spacing = dx_spacing
    
    str_dy = str(dy_spacing)
    str_dy = str_dy.split('.')[0]
    n_digits = str_dy.__len__()
    nd = int(n_digits)
        
    first_digit = float(str_dy[0])
    
    dy_spacing_rounded = first_digit*pow(10,(nd-1))
 
    str_xmin = str(xmin_UTM)
    str_ymin = str(ymin_UTM)
    str_xmin = str_xmin.split('.')[0]
    str_ymin = str_ymin.split('.')[0]
    xmin_UTM = float(str_xmin)
    ymin_UTM = float(str_ymin)
    
    n_digx = str_xmin.__len__() 
    n_digy = str_ymin.__len__() 
    
    front_x = str_xmin[:(n_digx-nd+1)]
    front_y = str_ymin[:(n_digy-nd+1)]
           
    round_xmin = float(front_x)*pow(10,nd-1)
    round_ymin = float(front_y)*pow(10,nd-1)
        
    # now we need to figure out where the xllocs and ylocs are
    xUTMlocs = np.zeros(2*n_target_tics)
    yUTMlocs = np.zeros(2*n_target_tics)
    xlocs = np.zeros(2*n_target_tics)
    ylocs = np.zeros(2*n_target_tics)
    
    new_x_labels = []
    new_y_labels = []
    
    for i in range(0,2*n_target_tics):
        xUTMlocs[i] = round_xmin+(i)*dy_spacing_rounded
        yUTMlocs[i] = round_ymin+(i)*dy_spacing_rounded
                  
        xlocs[i] = (xUTMlocs[i]-hillshade_header[2])/hillshade_header[4]
        
        # need to account for the rows starting at the upper boundary
        ylocs[i] = hillshade_header[1]-((yUTMlocs[i]-hillshade_header[3])/hillshade_header[4])
        
        new_x_labels.append( str(xUTMlocs[i]).split(".")[0] )
        new_y_labels.append( str(yUTMlocs[i]).split(".")[0] )
   
    return xlocs,ylocs,new_x_labels,new_y_labels