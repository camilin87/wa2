from sys import argv
from flask import Flask
from appcore import AppCore
from logging import basicConfig
from logging import INFO


app = Flask(__name__)
api_params = "/<api_key>/<latitude>/<longitude>/"
app_core = AppCore()

log_format_str = "%(asctime)s [%(levelname)s] %(message)s"
date_format_str = "%Y-%m-%d %H:%M:%S"
basicConfig(
    level=INFO,
    format=log_format_str,
    datefmt=date_format_str
)


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
