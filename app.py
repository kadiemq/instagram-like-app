from flask.helpers import url_for
from werkzeug.utils import redirect
from utils.Middleware import Middleware, isAuthenticated
from flask import Flask, render_template, request
from config import unprotectedUrls


app = Flask(__name__)
app.wsgi_app = Middleware(app.wsgi_app)


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
        print(request.form)
    return render_template('signup.html')


@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        print(request.form)
    return render_template('login.html')


if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0')
