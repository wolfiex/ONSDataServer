'''
Processing ONS geographies: Centroids
Dan Ellis, 2021
'''

import pandas as pd
import glob, os, re

from p_tqdm import p_map
from pyproj import Proj, transform


loc = '/Users/danielellis/Desktop/ONSDataDownloads/geojson/'



if __name__ == '__main__':
    # create copies

    fls = glob.glob(loc+'*.geojson')
    # print(fls)
    def process(fl):
        gg = fl.replace('geojson','mbtiles')
        print(f'tippecanoe -zg -o { gg } --drop-densest-as-needed {fl}')

        os.popen(f'tippecanoe -z15 -Z4 -o { gg } --no-feature-limit --no-tile-size-limit --generate-id --drop-densest-as-needed {fl} --force').read()

    p_map(process, fls) 






