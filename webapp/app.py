from sys import argv
from flask import Flask
from appcore import AppCore

app = Flask(__name__)
api_params = "/<api_key>/<latitude>/<longitude>/"
app_core = AppCore()


@app.errorhandler(404)
def page_not_found(error):
    return app.send_static_file('404.html'), 404


@app.route("/t" + api_params)
def retrieve_data_test(api_key, latitude, longitude):
    return app_core.retrieve_data_test(api_key, latitude, longitude)


@app.route("/s" + api_params)
def retrieve_data_staging(api_key, latitude, longitude):
    return app_core.retrieve_data_staging(api_key, latitude, longitude)


@app.route("/p" + api_params)
def retrieve_data_production(api_key, latitude, longitude):
    return app_core.retrieve_data_production(api_key, latitude, longitude)


if __name__ == '__main__':
    if "disable_debug" in argv:
        app_core.disable_debug = True
    app.run(host='0.0.0.0', port=8080, debug=True)
