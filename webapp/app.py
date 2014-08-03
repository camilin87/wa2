from sys import argv
from flask import Flask
from flask import jsonify
from wa.factory.apifactory import ApiFactory
from wa.factory.enginefactory import EngineFactory
from wa.api.freeforall import FreeForAll
from wa.extapi.citkeys import CitKeys


disable_debug = False
app = Flask(__name__)


@app.errorhandler(404)
def page_not_found(error):
    return app.send_static_file('404.html'), 404


@app.route("/t/<api_key>/<latitude>/<longitude>/")
def retrieve_data_test(api_key, latitude, longitude):
    if _disable_debug():
        abort(404)
        return
    return jsonify(ApiFactory.create_dummy_response(float(latitude), float(longitude)).__dict__)


@app.route("/s/<api_key>/<latitude>/<longitude>/")
def retrieve_data_staging(api_key, latitude, longitude):
    if _disable_debug():
        abort(404)
        return
    key_validator = FreeForAll()
    api_key_reader = CitKeys()
    return _retrieve_data(api_key, latitude, longitude, key_validator, api_key_reader)


def _disable_debug():
    def _disable_uwsgi_debug():
        try:
            from uwsgi import opt
            return "true" == opt["disable_debug"].decode()
        except:
            return False
    return disable_debug or _disable_uwsgi_debug()


@app.route("/p/<api_key>/<latitude>/<longitude>/")
def retrieve_data_production(api_key, latitude, longitude):
    return _retrieve_data(api_key, latitude, longitude)


def _retrieve_data(api_key, latitude, longitude, key_validator=None, api_key_reader=None):
    data_retriever_controller = _create_controller(key_validator, api_key_reader)
    api_response = data_retriever_controller.get(api_key, latitude, longitude)
    return jsonify(api_response.__dict__)


def _create_controller(key_validator, api_key_reader):
    data_retriever = EngineFactory.create_data_retriever(api_key_reader)
    return ApiFactory.create_data_retriever_controller(data_retriever, key_validator)


if __name__ == '__main__':
    if "disable_debug" in argv:
        disable_debug = True
    app.run(host='0.0.0.0', port=8080, debug=True)
