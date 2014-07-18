from flask import Flask
from flask import jsonify
from datetime import datetime


app = Flask(__name__)


@app.errorhandler(404)
def page_not_found(error):
    return app.send_static_file('404.html'), 404


@app.route("/rd/<api_key>/<latitude>/<longitude>")
def retrieve_data(api_key, latitude, longitude):
    timestamp = "fixed"
    timestamp = datetime.utcnow().isoformat()

    return jsonify({
        "method": "rd",
        "api_key": api_key,
        "latitude": latitude,
        "longitude": longitude,
        "timestamp": timestamp
    })

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=8080, debug=True)
