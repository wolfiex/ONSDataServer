'''
Publish Mapbox tilesets and Data API requests.

ONSVisual - Innovate
Dan Ellis 2021
'''

# app.py
import mimetypes
from flask import Flask, g, jsonify, abort, request, render_template
from flask_cors import CORS,cross_origin
from flask_caching import Cache

app = Flask('ONSVisualApp')
cors = CORS(app, resources={r"*": {"origins": "*"}})
app.config['CORS_HEADERS'] = 'Content-Type'
cache = Cache(app)


@app.route('/')
def main():
    return 'The ONS Visual API is running.'









''' Tilesets'''



# @frontend.before_request
# def before_request():
#     """Ensure database is connected for each request """




from .ember import Tileset
from io import StringIO  

# fl = '/Users/danielellis/ONStileBuilder/tiles/countries.mbtiles'
# t = Tileset(fl)
# t.summary
__tloc__ = '/Users/danielellis/Desktop/ONSDataDownloads/mbtiles/'
__tiles__ = {
    'countries': 
        __tloc__ + 'CountiesUA.mbtiles',
    'oa11': __tloc__ + 'Output_Areas__December_2011__Boundaries_EW_BGC.mbtiles'
    

}

#load each tileset
print('------------------------------------------------------')
print('tileset')
print('------------------------------------------------------')
for t in __tiles__: 
    print('---',t,'---')
    __tiles__[t] = Tileset(__tiles__[t])
    # print(__tiles__[t].summary)
    for l in __tiles__[t].metadata.json['vector_layers']:
        print(l)
 
print('------------------------------------------------------')


@app.route('/mbtiles')
def mbtiles():
    return 'Specify a tileset.'

@app.route('/mbtiles/<tileset>/<z>/<x>/<y>', methods=['GET'])
@cache.cached(timeout=300)
@cross_origin(origin='*',headers=['Content-Type','Authorization'])
def get_tile_value(tileset,z,x,y):
    ''' Returns the Tile data from the DataBase'''
    # print(x,y,z,__tiles__[tileset].get_tile(int(z),int(y),int(x)))
    # return __tiles__[tileset].get_tile(int(z),int(y),int(y))
    tile = __tiles__[tileset].get_tile(int(z),int(x),int(y))
    print(tile)
    if not tile:
        abort(404)
    # else:
        # return tile

    return  app.response_class(
            StringIO(tile.__str__()).read(),
            mimetype="application/vnd.mapbox-vector-tile"
            # mimetype='image/png'
        )

@app.route('/tilebounds/<tileset>', methods=['GET'])
def get_tile_bounds(tileset):
    ''' Returns the Tile boundaries and centre'''
    return jsonify(dict(bounds=__tiles__[tileset].metadata.bounds,centre=__tiles__[tileset].metadata.centre))


''' Centroids'''

import pandas as pd
import numpy as np
__cloc__ = '/Users/danielellis/Desktop/ONSDataDownloads/centroids/WGS84_simplified/'

# Lower_Layer_Super_Output_Areas_\(December_2011\)_Population_Weighted_Centroids.csv

centroids = {
    '2011':
        {
           'lsoa' : r'Lower_Layer_Super_Output_Areas_(December_2011)_Population_Weighted_Centroids',
           'msoa' : r'Middle_Layer_Super_Output_Areas_(December_2011)_Population_Weighted_Centroids',
           'oa'   : r'Output_Areas__December_2011__Population_Weighted_Centroids'
        },
    '2001':
        {
           'lsoa' : r'Lower_Layer_Super_Output_Areas_(December_2001)_Population_Weighted_Centroids',
           'msoa' : r'Middle_Layer_Super_Output_Areas_(December_2001)_Population_Weighted_Centroids',
           'oa'   : r'Output_Areas__December_2001__Population_Weighted_Centroids'
        }
}

print('Loading centroids')

for year in centroids:
    yearselect = centroids[year]
    for level in yearselect:
        yearselect[level] = pd.read_csv(__cloc__+yearselect[level]+'.csv')

print('Centroids Loaded')



@app.route('/centroids/<year>/<area>/<polygon>', methods=['GET'])
def fetch_centroids(year,area,polygon):
    ''' Extracts the data from centroids.  '''
    polygon = np.array(eval(polygon)).astype(float).astype(int)*1e5

    bmx = polygon.max(axis=1)
    bmn = polygon.min(axis=1)

    data = centroids[year][area]
    print (data,bmn,bmx)

    data = data[(data[['Lon','Lat']] < bmx).all(axis=1) ]
    data = data[(data[['Lon','Lat']] > bmn).all(axis=1)]

    print(data)
    # print( data[(data[['Lon','Lat']] < bmx).all(axis=1) & (data[['Lon','Lat']] > bmn).all(axis=1)] )

    # select = data[data.Lat > bmn[1] & data.Lon > bmn[0] * data.Lat < bmx[1] * data.Lon < bmx[0]]


    if len(polygon)==2:bbox=True

    return select






    print(polygon)






    return jsonify(dict(bounds=__tiles__[tileset].metadata.bounds,centre=__tiles__[tileset].metadata.centre))









'''
from  . import inpolygon
from p_tqdm import p_map

import numpy as np
lenpoly = 10

polygon = [[np.sin(x)+0.5,np.cos(x)+0.5] for x in 
np.linspace(0,2*np.pi,lenpoly)[:-1]]

print('----',polygon)
# random points set of points to test 
N = 50
# making a list instead of a generator to help debug
points = zip(np.random.random(N)*8,np.random.random(N)*2)
# print('=======',list(points))
polygon = np.array(polygon)


result = [inpolygon.ray_tracing(point[0], point[1], polygon) for point in points]

print(result)


'''




# tileset = MbtileSet(mbtiles='/Users/danielellis/ONStileBuilder/tiles/merged.mbtiles')
# zoom, col, row = 6, 9, 40
# tile = tileset.get_tile(zoom, col, row)
# binary_png = tile.get_png()
# text_json = tile.get_json()












# import sqlite3
# conn = sqlite3.connect('postcodes.db',check_same_thread=False)
# cursor = conn.cursor()




# ######## HOME ############
# @app.route('/')
# def main():
#     return 'This is the geography selector.'

# ######## Data fetch ############
# @app.route('/postcode/<match>/<limit>', methods=['GET'])
# def pfind(match,limit):
#     r = conn.execute(r'SELECT POST,IDLSOA from POSTAREA WHERE PSELECT LIKE "{}%" LIMIT {};'.format(match.replace(' ','').upper(),int(limit))).fetchall()
#     return jsonify(r)  # serialize and use JSON headers

# @app.route('/name/<match>/<limit>', methods=['GET'])
# def nfind(match,limit):
#     r = conn.execute(r'SELECT * from NAMELIST WHERE NAME LIKE "{}%" LIMIT {};'.format(match.replace(' ','').upper(),int(limit))).fetchall()
#     return jsonify(r)  # serialize and use JSON headers




# @app.route('/lad/<value>', methods=['GET'])
# def ladfind(value):
#     r = conn.execute(r'SELECT CODE from LAD WHERE ID = %d;'%int(value)).fetchone()
#     return jsonify(r)  # serialize and use JSON headers





# run app
app.run(port=5002,debug=True)