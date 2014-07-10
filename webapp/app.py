from bottle import route
from bottle import run
from bottle import error
from bottle import static_file
from os.path import dirname
from os.path import realpath
from os.path import join

current_dir = dirname(realpath(__file__))
static_files = join(current_dir, "./static/files/")

@error(404)
def error_404(error):
    return static_file("404.html", root=static_files)

@route("/rd/<api_key:re:[a-zA-Z0-9]{1,100}>/<latitude:float>/<longitude:float>")
def retrieve_data(api_key, latitude, longitude):
    return "rd/" + api_key + "/" + str(latitude) + "/" + str(longitude)

run(host='0.0.0.0', port=8080, debug=True)