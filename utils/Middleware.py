from flask.wrappers import Response
from werkzeug.wrappers import Request

unprotectedPaths = ['/login', '/signup']

class Middleware:
    def __init__(self, app):
        self.app = app


    def __call__(self, environ, start_response):
        request = Request(environ)
        cookies = request.cookies
        path = request.path

        environ['isAuthenticated'] = isAuthenticated(cookies)

        return self.app(environ, start_response)


def isAuthenticated(cookies):
    if (len(cookies)) > 0 :
        return {'first_name': 'test_firstname',
                'last_name': 'test_lastname',
                'username': 'test_username',
                'email': 'test@gmail.com'
        }

    else:
        return False
