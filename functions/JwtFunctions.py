import jwt
from flask import current_app

def generateJWT(userId, userEmail):
    secretKey = current_app.config['SECRETKEY']
    token = jwt.encode({"id": userId, "email": userEmail}, secretKey)
    return token

def decodeJWT(token):
    payload = jwt.decode(token, 'oieg9834gsnovjwe8f', algorithms=["HS256"])
    return payload
