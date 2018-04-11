# MODULE containing foundational tools for ashfall forecast visualization

import os

# this function is from Chai
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

def grab_gmt_boundaries(latmin, latmax, lonmin, lonmax, res):
    '''
    Grab geographical boundary data from GMT for a specified extent and resolution
    Requires the os module to be imported
    Also requires GMT to be installed, obviously...
    
    Input:
        latmin, latmax, lonmin, lonmax specify extent in decimal degrees
        res (a string) can be either f, h, i, l, or c depending upon desired resolution
    
    Output:
        boundary_data is a dictionary containing coordinates of geo features (each feature is a list)
    
    '''
    # the projection (-J) info shouldn't make a difference here
    cmd = 'gmt pscoast -JB{0}/{2}/{2}/{3}/4.7i -R{0}/{1}/{2}/{3} -D{4} -W -M > temp.xy'.format(lonmin, lonmax,
                                                                                               latmin, latmax, res)
    os.system(cmd)
    
    boundary_data = {}
    # this function is from Chai
    # https://github.com/ccp137/DynamicViz/blob/master/utility.py
    boundary_data['latitude'], boundary_data['longitude'] = read_gmt_boundary('temp.xy')
    
    # clean up
    os.system('rm gmt.history')
    os.system('rm temp.xy')
    
    return boundary_data