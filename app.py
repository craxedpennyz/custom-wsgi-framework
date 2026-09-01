import json
from wsgiref.simple_server import make_server

def home_handler(environ):
    return "200 OK", {"message": "Hello!"}


def health_handler(environ):
    return "200 OK", {"status": "online"}


def not_found_handler(environ):
    return "404 Not Found", {"error": "Endpoint does not exist"}

routes = {"/": home_handler, "/health": health_handler}


def application(environ, start_response):
    

    path = environ.get("PATH_INFO", "/")
    handler = routes.get(path, not_found_handler)

    status, response = handler(environ)

    json_data = json.dumps(response)
    bytes_data = json_data.encode('utf-8')

    headers = [("Content-Type", "application/json"), ("Content-Length", str(len(bytes_data)))]

    start_response(status, headers)

    return [bytes_data]

if __name__ == "__main__":
    server = make_server("localhost", 8888, application)
    print("Serving on http://localhost:8888...")
    server.serve_forever()