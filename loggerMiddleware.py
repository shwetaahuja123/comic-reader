from werkzeug.wrappers import Request, Response
import jwt

savedUuids = {}
class LoggerMiddleware(object):
    def __init__(self, app):
        self.app = app

    def __call__(self, environ, start_response):
        # not Flask request - from werkzeug.wrappers import Request
        request = Request(environ)

        if request.path == '/register' or request.path == '/health' or request.path == '/login':
            return self.app(environ, start_response)

        if not('Authorization' in request.headers):
            res = Response(u'Authorization failed', mimetype='text/plain', status=401)
            return res(environ, start_response)

        bearerToken = request.headers['Authorization']

        token = bearerToken[len('Bearer '):]
        key = "secret1"
        if token in savedUuids:
            decoded = jwt.decode(token, key, algorithms="HS256" )
            email = decoded['email']
            return self.app(environ, start_response)

        res = Response(u'Authorization failed', mimetype='text/plain', status=401)
        return res(environ, start_response)