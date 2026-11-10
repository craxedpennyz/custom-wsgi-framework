import json
from wsgiref.simple_server import make_server

class Request:
    def __init__(self, environ):
        self.environ = environ

    @property
    def path(self):
        return self.environ.get("PATH_INFO", "/")

    @property
    def method(self):
        return self.environ.get("REQUEST_METHOD", "GET")

class Response:
    STATUS_MAP = {
    200: "200 OK",
    400: "400 Bad Request",
    404: "404 Not Found",
    500: "500 Internal Server Error"
    }

    def __init__(self, body, status_code=200, headers=None):
        if headers is None:
            headers = {"Content-Type": "application/json"}
        self.body = body
        self.status_code = status_code
        self.headers = headers
       

    @property
    def encode_body(self):
        if isinstance(self.body, (dict, list)):
            text = json.dumps(self.body)
        else:
            text = str(self.body)
        return text.encode('utf-8')

    @property
    def status_text(self):
        return self.STATUS_MAP.get(self.status_code, f"{self.status_code} Unknown")


def home_handler(req):
    return Response(body={"message": "Hello!"}, status_code=200)


def health_handler(req):
    return Response(body={"status": "online"}, status_code=200)


def not_found_handler(req):
    return Response(body={"error": "Endpoint does not exist"}, status_code=404)

routes = {"/": home_handler, "/health": health_handler}
    

def application(environ, start_response):
    
    req = Request(environ)

    # Select handler using req.path instead of raw environ
    handler = routes.get(req.path, not_found_handler)

    # Execute handler to get back a Response instance
    res = handler(req)

    # Encode the body to UTF-8 bytes
    bytes_data = res.encode_body

    # Format headers as WSGI expects: list of tuples [('Header-Name', 'Value')]
    header_list = [(k, str(v)) for k, v in res.headers.items()]
    header_list.append(("Content-Length", str(len(bytes_data))))

    # Call WSGI callback with status text string (e.g. "200 OK") and header list
    start_response(res.status_text, header_list)

    # Return body in list as required by WSGI spec
    return [bytes_data]

if __name__ == "__main__":
    server = make_server("localhost", 8888, application)
    print("Serving on http://localhost:8888...")
    server.serve_forever()