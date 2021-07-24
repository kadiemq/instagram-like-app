from functions.JwtFunctions import generateJWT
from threading import Condition
from functions.databaseFunctions.FetchData import fetchData
from functions.SanitizeString import sanitize_email, sanitize_general_string
from flask.helpers import make_response, url_for
from werkzeug.utils import redirect
from functions.Middleware import Middleware, isAuthenticated
from flask import Flask, render_template, request
from config import unprotectedUrls
from functions.databaseFunctions.ConnectDB import connect_db
import bcrypt
import json

app = Flask(__name__)
app.config.from_object('SETTINGS')
app.wsgi_app = Middleware(app.wsgi_app, app)


@app.before_request
def before_request():
    isAuthenticated = request.environ['isAuthenticated']

    if request.path not in unprotectedUrls and not isAuthenticated:
        return redirect('/login')

    if request.path in unprotectedUrls and isAuthenticated:
        return redirect('/')


@app.route('/')
def index():
    return render_template('index.html')


@app.route('/signup', methods=['GET', 'POST'])
def signup():
    if request.method == 'POST':
        
        connection = connect_db()
        
        try:
            
            email = sanitize_email(request.form.get('email'))
            username = sanitize_general_string(request.form.get('username'))
            first_name = sanitize_general_string(request.form.get('first_name'))
            last_name = sanitize_general_string(request.form.get('last_name'))
            password = sanitize_general_string(request.form.get('password')).encode()
            password = bcrypt.hashpw(password, bcrypt.gensalt()).decode()

            cursor = connection.cursor()
            query = 'INSERT INTO users(first_name, last_name, username, email, password) VALUES (%s, %s, %s, %s, %s)'
            values = (first_name, last_name, username, email, password)
            cursor.execute(query, values)
            connection.commit()
            cursor.close()
            connection.close()
            return redirect('/login')

        except ValueError as error:
            return render_template('signup.html', error_msg=error)


    return render_template('signup.html')


@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        connection = connect_db()
        try:
            email_or_username = sanitize_general_string(request.form.get('username'))
            password = sanitize_general_string(request.form.get('password'))

            data = fetchData(connection, columns='*', table='users', conditionsOr={'username': email_or_username, 'email': email_or_username})
            if len(data) < 1: raise ValueError('Wrong email or username')

            if bcrypt.checkpw(password.encode(), data[0]['password'].encode()):
                jwtToken = generateJWT(data[0]['id'], data[0]['email'])
                
                resp = make_response(redirect('/'))
                resp.set_cookie('jwt', jwtToken)

                return resp
            else:
                raise ValueError('Wrong Password')
                


        except ValueError as error:
            return render_template('login.html', error_msg=error)        

    return render_template('login.html')


if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0')
