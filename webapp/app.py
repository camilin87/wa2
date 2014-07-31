from flask import Flask
from flask import jsonify
from wa.factory.apifactory import ApiFactory


app = Flask(__name__)


@app.errorhandler(404)
def page_not_found(error):
    return app.send_static_file('404.html'), 404


@app.route("/t/<api_key>/<latitude>/<longitude>")
def retrieve_data(api_key, latitude, longitude):
    return jsonify(ApiFactory.create_dummy_response(float(latitude), float(longitude)).__dict__)

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=8080, debug=True)
