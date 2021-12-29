'''
Processing ONS geographies: Centroids
Dan Ellis, 2021
'''

import pandas as pd
import glob, os, re

from p_tqdm import p_map
from pyproj import Proj, transform

v84 = Proj(proj="latlong",towgs84="0,0,0",ellps="WGS84")
v36 = Proj(proj="latlong", k=0.9996012717, ellps="airy",
        towgs84="446.448,-125.157,542.060,0.1502,0.2470,0.8421,-20.4894")

vgrid = Proj(init="world:bng")


def ENtoLL84(easting, northing):
    """Returns (longitude, latitude) tuple
    """
    vlon36, vlat36 = vgrid(easting, northing, inverse=True)
    return transform(v36, v84, vlon36, vlat36)

def LL84toEN(longitude, latitude):
    """Returns (easting, northing) tuple
    """
    vlon36, vlat36 = transform(v84, v36, longitude, latitude)
    return vgrid(vlon36, vlat36)




files = glob.glob("/Users/danielellis/Desktop/ONSDataDownloads/centroids/NE/*.csv")

def remake(fl):
    ''' 
    A function to read in the centroid files and convert them to WGS84
    '''
    
    df = pd.read_csv(fl)
    df = df[df.columns[[0,1,3]]]
    df.columns = 'X Y ID'.split()
    df['X'] = df['X'].astype(int)   
    df['Y'] = df['Y'].astype(int)
    df.sort_values(by=['X','Y'], inplace=True)
    df.to_csv(fl.replace('NE','NE_processed'), index=False)

    # this bit is MUCH slower - comment out if unnecessary
    lat = []
    lon = []
    for i,element in df.iterrows():
        ln, lt = ENtoLL84(element['X'], element['Y'])
        lat.append(lt)
        lon.append(ln)

    df['Lat'] = lat
    df['Lon'] = lon
    df.drop(['X','Y'], axis=1, inplace=True)
    df.to_csv(fl.replace('NE','WGS84'), index=False)


    # simplify 
    df['Lat'] = (df['Lat']*1e5).astype(int)
    df['Lon'] = (df['Lon']*1e5).astype(int)
    df.to_csv(fl.replace('NE','WGS84_simplified'), index=False)





if __name__ == '__main__':
    # create copies
    p_map(remake, files)

