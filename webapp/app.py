from flask import Flask
from appcore import AppCore


app = Flask(__name__)
api_params = "/<api_key>/<latitude>/<longitude>/"
app_core = AppCore()
app_core.configure_logging()


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
    app.run(host='0.0.0.0', port=8080, debug=True)
