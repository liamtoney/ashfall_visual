# MODULE containing foundational tools for ashfall forecast visualization

import os  # for running GMT commands
import xarray as xr  # for reading netCDF files

# This function is from Chai
# https://github.com/ccp137/DynamicViz/blob/master/utility.py
def read_gmt_boundary(filename):
    '''
    Read boundary data from text files that are extracted by GMT
    
    Input:
        filename is the filename for the boundary data file
    
    Output:
        lat_list is a list of latitudes
        lon_list is a list of longitude
    
    '''
    fid = open(filename,'r')
    lon_list, lat_list = [], []
    temp_lon, temp_lat = [], []
    for aline in fid:
        words = aline.split()
        if words[0] != '>':
            temp_lon.append(float(words[0]))
            temp_lat.append(float(words[1]))
        else:
            lon_list.append(temp_lon)
            lat_list.append(temp_lat)
            temp_lon, temp_lat = [], []
    fid.close()
    lon_list.append(temp_lon)
    lat_list.append(temp_lat)
    return lat_list, lon_list

def grab_GMT_features(latmin, latmax, lonmin, lonmax, res):
    '''
    Grab geographical feature data from GMT for a specified extent and resolution
    Requires the os module
    Also requires GMT to be installed, obviously...
    
    Input:
        latmin, latmax, lonmin, lonmax specify extent in decimal degrees
        res (a string) can be either f, h, i, l, or c depending upon desired resolution
    
    Output:
        feature_data is a dictionary containing coordinates of geo features (each feature is a list)
    
    '''
    # the projection (-J) info shouldn't make a difference here
    cmd = 'gmt pscoast -JB{0}/{2}/{2}/{3}/4.7i -R{0}/{1}/{2}/{3} -D{4} -W -M > temp.xy'.format(lonmin, lonmax,
                                                                                               latmin, latmax, res)
    os.system(cmd)
    
    feature_data = {}
    feature_data['latitude'], feature_data['longitude'] = read_gmt_boundary('temp.xy')
    
    # clean up
    os.system('rm gmt.history')
    os.system('rm temp.xy')
    
    return feature_data

def read_HYSPLIT_netCDF(filename):
    '''
    Read a netCDF file and add in volcano location info
    Requires the xarray package
    
    Input:
        filename is the filename and path for the netCDF file
    
    Output:
        model is an xarray.Dataset with all the netCDF info 
    
    '''
    # taken from https://volcano.si.edu/search_volcano.cfm
    src_locs = {'auckland':[-36.9, 174.87],\
                'mayor':[-37.28, 176.25],\
                'white':[-37.52, 177.18],\
                'haroharo':[-38.12, 176.5],\
                'tarawera':[-38.12, 176.5],\
                'taupo':[-38.82, 176],\
                'tongariro':[-39.157, 175.632],\
                'ngauruhoe':[-39.157, 175.632],\
                'ruapehu':[-39.28, 175.57],\
                'taranaki':[-39.3, 174.07]}
    volc_name = filename.split("_")[1]
    
    # open model and add in source location info
    model = xr.open_dataset(filename)
    model.attrs['volcano_location'] = src_locs[volc_name]

    return model