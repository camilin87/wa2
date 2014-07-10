from bottle import route, run

@route("/rd/<api_key:re:[a-zA-Z0-9]{1,100}>/<latitude:float>/<longitude:float>")
def retrieve_data(api_key, latitude, longitude):
    return "rd/" + api_key + "/" + str(latitude) + "/" + str(longitude)

run(host='0.0.0.0', port=8080, debug=True)