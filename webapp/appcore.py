from flask import jsonify
from flask import abort
from wa.factory.apifactory import ApiFactory
from wa.factory.enginefactory import EngineFactory
from wa.api.freeforall import FreeForAll
from wa.extapi.citkeys import CitKeys


class AppCore(object):
    def __init__(self):
        self.disable_debug = False

    def retrieve_data_test(self, api_key, latitude_str, longitude_str):
        if self._disable_debug():
            abort(404)
            return
        result = ApiFactory.create_dummy_response(float(latitude_str), float(longitude_str))
        return jsonify(result.__dict__)

    def _disable_debug(self):
        def _disable_uwsgi_debug():
            try:
                from uwsgi import opt
                return "true" == opt["disable_debug"].decode()
            except:
                return False
        return self.disable_debug or _disable_uwsgi_debug()

    def retrieve_data_staging(self, api_key, latitude_str, longitude_str):
        if self._disable_debug():
            abort(404)
            return
        key_validator = FreeForAll()
        api_key_reader = CitKeys()
        return self._retrieve_data(
            api_key, latitude_str, longitude_str, key_validator, api_key_reader
        )

    def retrieve_data_production(self, api_key, latitude_str, longitude_str):
        return self._retrieve_data(api_key, latitude_str, longitude_str)

    def _retrieve_data(
        self, api_key, latitude_str, longitude_str, key_validator=None, api_key_reader=None
    ):
        data_retriever_controller = self._create_controller(key_validator, api_key_reader)
        api_response = data_retriever_controller.get(api_key, latitude_str, longitude_str)
        return jsonify(api_response.__dict__)

    def _create_controller(self, key_validator, api_key_reader):
        data_retriever = EngineFactory.create_data_retriever(api_key_reader)
        return ApiFactory.create_data_retriever_controller(data_retriever, key_validator)
