'''
An edited version of the ember library for checking MapTiles. 

'''

from dataclasses import dataclass
import json
import mimetypes
import sqlite3


class TileNotFound(ValueError):
    pass


class Metadata:
    """
    Key/value store for settings for a tileset's settings.
    <https://github.com/mapbox/mbtiles-spec/blob/master/1.3/spec.md#metadata>
    """

    def __init__(self, items):
        self.items = items

    def __getattr__(self, attr):
        return self.items.get(attr, None)


    @property
    def zoom(self):
        return self.items['minzoom'],self.items['maxzoom']

    @property
    def bounds(self):
        return list(map(float, self.items["bounds"].split(",")))

    @property
    def center(self):
        return list(map(float, self.items["center"].split(",")))

    @property
    def json(self):
        return json.loads(self.items["json"])


class Tileset:
    filename: str
    metadata: Metadata

    def __init__(self, filename):
        self.filename = filename

        conn = sqlite3.connect(
            f"file:{self.filename}?mode=ro",
            uri=True,
            detect_types=sqlite3.PARSE_DECLTYPES,
        )
        cursor = conn.execute("SELECT * FROM metadata")
        self.metadata = Metadata(dict(cursor))
        conn.close()

    @property
    def summary (self):
        print('center:',self.metadata.center)
        print('bounds:',self.metadata.bounds)
        print('zoom:',self.metadata.zoom)
        print(self.metadata.json)

    def available(self,limit=10):
        conn = sqlite3.connect(
            f"file:{self.filename}?mode=ro",
            uri=True,
            detect_types=sqlite3.PARSE_DECLTYPES,
        )
        cursor = conn.execute(
            """
            select * from tiles limit %d
            """%limit)

        print('Available tiles\n',cursor.fetchall())

    def get_tile(self, z: int, x: int, y: int):
        conn = sqlite3.connect(
            f"file:{self.filename}?mode=ro",
            uri=True,
            detect_types=sqlite3.PARSE_DECLTYPES,
        )
        cursor = conn.execute(
            """
            SELECT
                tile_data
            FROM
                tiles
            WHERE
                zoom_level = ?
                AND
                tile_column = ?
                AND
                tile_row = ?
            """,
            (z, x, y),
        )
        tile_data = cursor.fetchone()

        



        conn.close()

        # return tile_data
        if tile_data is None:
            raise TileNotFound(f"tile z = {z}, x = {x}, y = {y} not found")

        return tile_data[0]
        


        
        # return tile_data[0]

    def media_type(self):
        if self.metadata.format == "jpg":
            return "image/jpeg"
        elif self.metadata.format == "pbf":
            return "application/vnd.mapbox-vector-tile"
        elif self.metadata.format == "png":
            return "image/png"
        elif self.metadata.format == "webp":
            return "image/webp"
        else:
            mimetypes.init()
            try:
                return mimetypes.types_map[f".{self.metadata.format}"]
            except KeyError:
                return "text/plain"  # TODO: Use a better fallback.