import geojson
import geopandas as gpd
from mapbox import Directions
from shapely.geometry import LineString

from access_token import TOKEN


def gps_point_to_routes(points_from_file='points.geojson', dump_to='routes.geojson'):
    get_direct = Directions(access_token=TOKEN)

    with open(points_from_file, 'r') as cat:
        data = geojson.load(cat).copy()

    end_points = data['features']

    resp = get_direct.directions(walkway_bias=1,
                                 alley_bias=1,
                                 profile='mapbox/walking',
                                 features=end_points,
                                 geometries='geojson')

    if resp.status_code in [200, 202]:
        new_data = resp.json()

        if (code := new_data['code']) == 'Ok':

            geom = new_data['routes'][-1]['geometry']
            line = LineString(geom['coordinates'])
            route_df = gpd.GeoDataFrame(geometry=[line])
            route_df.to_file(dump_to, driver='GeoJSON', encoding="utf-8")

            return route_df.to_dict()
        else:
            return {'error': f'code status Mapbox Direction API for {code}'}
    else:
        return {'error': f'code status Mapbox Direction API for {resp.status_code}'}


if __name__ == '__main__':
    res = gps_point_to_routes('points.geojson')
    print(res.get('error', 'ok'))
