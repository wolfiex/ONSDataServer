'''
Publish Mapbox tilesets and Data API requests.

ONSVisual - Innovate
Dan Ellis 2021
'''

# app.py
from flask import Flask, jsonify, request, render_template
from flask_cors import CORS
app = Flask('ONSVisualApp')
cors = CORS(app, resources={r"/*": {"origins": "*"}})
app.config['CORS_HEADERS'] = 'Content-Type'

from .ember import Tileset

fl = '/Users/danielellis/ONStileBuilder/tiles/merged.mbtiles'
t = Tileset(fl)
t.summary







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
# app.run(port=5002,debug=True)