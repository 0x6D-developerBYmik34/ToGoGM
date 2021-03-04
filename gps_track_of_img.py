import math
from functools import partial
from numbers import Number
from typing import List, Tuple

import cv2
import numpy as np
from geopandas import GeoDataFrame
from shapely.geometry import Point

from diff_bet_adj import num_sub_dif_bet_adj
from to_twentyfive_points import to_25


def lat_long_spher_to_merc(lon: float, lat: float) -> Tuple[float, float]:
    if lat > 89.5:
        lat = 89.5
    elif lat < -89.5:
        lat = -89.5

    rad_lat = math.radians(lat)
    rad_long = math.radians(lon)

    a = 6378137.0
    x_out = a * rad_long
    y_out = a * math.log(math.tan(math.pi / 4 + rad_lat / 2))
    return x_out, y_out


def distance(p1, p2):
    """
    This function computes the distance between 2 points defined by
     P1 = (x1,y1) and P2 = (x2,y2)
    """
    return ((p1[0] - p2[0]) ** 2 + (p1[1] - p2[1]) ** 2) ** 0.5


def optimized_path(coordinates: List[List[int]], start=None) -> List[List[int]]:
    """
    This function finds the nearest point to a point
    coordinates should be a list in this format coordinates = [ [x1, y1], [x2, y2] , ...]
    """
    if start is None:
        start = coordinates[0]

    pass_by = [p for p in coordinates if p != start]
    out_path: List[List[int]] = [start]

    while pass_by:
        distance_to_final = partial(distance, out_path[-1])
        nearest = min(pass_by, key=distance_to_final)

        out_path.append(nearest)
        pass_by.remove(nearest)
    else:
        return out_path


def img_to_points(file_in_this_dir: str,
                  original_point: Tuple[Number, Number],
                  meters=6, dump_to='points.geojson'):

    img = cv2.imread(file_in_this_dir)
    gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)

    corners = cv2.goodFeaturesToTrack(np.float32(gray), 100, 0.0001, 10)
    corners = np.int0(corners)

    squeezed = corners.squeeze().tolist()
    path = optimized_path(squeezed)

    print(path)

    # x = np.array([i[0] for i in path])
    # y = np.array([i[1] for i in path])
    x = (i[0] for i in path)
    y = (i[1] for i in path)

    # Координаты в системе координат EPSG:3857
    x_orig, y_orig = lat_long_spher_to_merc(*original_point)

    mx = num_sub_dif_bet_adj(x_orig, (i * meters for i in x))
    my = num_sub_dif_bet_adj(y_orig, (i * -meters for i in y))

    mxy = list(zip(mx, my))

    print(len(mxy))

    mxy = [Point(res) for res in to_25(mxy)]

    print(len(mxy))

    picture_df = GeoDataFrame(
        {'id': range(len(mxy))},
        crs="EPSG:3857",
        geometry=mxy
    )

    picture_df['geometry'] = picture_df['geometry'].to_crs(epsg=4326)

    picture_df.to_file(dump_to, driver='GeoJSON', encoding="utf-8")


if __name__ == '__main__':
    img_to_points('images/3g.png', (44.50473, 48.70324), meters=12)
