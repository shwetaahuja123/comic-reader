from werkzeug.wrappers import Request, Response
savedUuids = {}
class LoggerMiddleware(object):
    def __init__(self, app):
        self.app = app

    def __call__(self, environ, start_response):
        # not Flask request - from werkzeug.wrappers import Request
        request = Request(environ)

        if request.path == '/login':
            return self.app(environ, start_response)

        print('request.headers: ',type(request.headers))
        if not('Authorization' in request.headers):
            res = Response(u'Authorization failed', mimetype='text/plain', status=401)
            return res(environ, start_response)

        bearerToken = request.headers['Authorization']

        print('path: %s, url: %s' % (request.path, request.url))

        token = bearerToken[len('Bearer '):]
        print(token)
        if token in savedUuids:
            print('Is Authenticated User')
            return self.app(environ, start_response)

        # just do here everything what you need
        print('Is NOT Authenticated User')
        res = Response(u'Authorization failed', mimetype='text/plain', status=401)
        return res(environ, start_response)