from bottle import route, template, run, static_file, request, response, view

@route("/static/<filename:path>")
def send_static(filename):
    response.content_type = mimetypes.guess_type(filename)
    return static_file(filename, root="./static")

@route("/")
@view("index")
def index():
    pass

if __name__ == "__main__":
    run(server="waitress", host='0.0.0.0', reloader=True, port=8080, debug=True)
