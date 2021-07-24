from functions.databaseFunctions.FetchData import fetchData
from functions.databaseFunctions.ConnectDB import connect_db
from functions.JwtFunctions import decodeJWT
from flask.wrappers import Response
from werkzeug.wrappers import Request
from flask import Flask

unprotectedPaths = ['/login', '/signup']

class Middleware:
    def __init__(self, wsgi, app):
        self.wsgi = wsgi
        self.app = app


    def __call__(self, environ, start_response):
        request = Request(environ)
        cookies = request.cookies
        path = request.path

        with self.app.app_context():
            environ['isAuthenticated'] = isAuthenticated(cookies)

        return self.wsgi(environ, start_response)


def isAuthenticated(cookies):
    if (len(cookies)) > 0 :
        if 'jwt' in cookies:
            payload = decodeJWT(cookies['jwt'])
            connection = connect_db()
            data = fetchData(connection, columns='*', table='users', conditions={'id': payload['id'], 'email': payload['email']})
            if len(data) < 1: raise ValidationError('Something is wrong.')
            print(data)

            return payload
    else:
        return False
