from flask import Flask
from flask import jsonify
from wa.factory.apifactory import ApiFactory
from wa.factory.enginefactory import EngineFactory


app = Flask(__name__)


@app.errorhandler(404)
def page_not_found(error):
    return app.send_static_file('404.html'), 404


@app.route("/t/<api_key>/<latitude>/<longitude>/")
def retrieve_data_test(api_key, latitude, longitude):
    return jsonify(ApiFactory.create_dummy_response(float(latitude), float(longitude)).__dict__)


@app.route("/s/<api_key>/<latitude>/<longitude>/")
def retrieve_data_staging(api_key, latitude, longitude):
    return retrieve_data_production(api_key, latitude, longitude)


@app.route("/p/<api_key>/<latitude>/<longitude>/")
def retrieve_data_production(api_key, latitude, longitude):
    data_retriever_controller = ApiFactory.create_data_retriever_controller(
        EngineFactory.create_data_retriever()
    )
    api_response = data_retriever_controller.get(api_key, latitude, longitude)
    return jsonify(api_response.__dict__)

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=8080, debug=True)
