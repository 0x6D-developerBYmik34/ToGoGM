from flask import Flask
from flask import request, make_response, json
import geojson

from gps_points_to_track import gps_point_to_routes
from gps_track_of_img import img_to_points

app = Flask(__name__)

keys_cord = ('lat', 'lng')


@app.route('/togogm/api/v0.1/routes_from_img/<string:name_image_file>', methods=['GET'])
def get_markers_of_img(name_image_file='1g.jpg'):
    try:
        latlng = tuple(float(request.args[k]) for k in keys_cord)
    except KeyError:
        return {
            'error': 'required arguments(lat, long) are missing or not specified'
        }

    if meters := int(request.args.get('scatter')):
        img_to_points('images/' + name_image_file, latlng, meters=meters)
    else:
        img_to_points('images/' + name_image_file, latlng)

    data = gps_point_to_routes()

    resp = make_response(geojson.dumps(data))

    resp.headers['Content-Type'] = "application/json; charset=utf-8"

    return resp


if __name__ == '__main__':
    app.run(debug=True)
