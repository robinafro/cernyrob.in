import os
import platform
import json
import time
import math
import bcrypt
import base64

from flask import Flask, render_template, request, jsonify, make_response, redirect
from flask_session import Session
from flask_limiter import Limiter
from flask import request
from urllib.parse import urlparse, urlunparse

import database
import callme

YEAR = 60 * 60 * 24 * 365
RATE_LIMIT = 1 / 25 # CPS

app = Flask(__name__)
app.config["SESSION_PERMANENT"] = True
app.config['SESSION_TYPE'] = 'filesystem'
app.config['SERVER_NAME'] = 'cernyrob.in'

def custom_key_func():
    # Get the "id" cookie from the client's request
    client_id = request.cookies.get("id")
    return f"client:{client_id}" if client_id else "client:anonymous"

limiter = Limiter(custom_key_func, app=app)

Session(app)

log_dir = os.path.join(os.path.dirname(__file__), "Logs")

if not os.path.exists(log_dir):
    os.makedirs(log_dir)

rate_limit = {}

###################

def log(msg):
    filename = os.path.join(log_dir, f"log.txt")
    content = ""

    if os.path.exists(filename):
        with open(filename, "r") as file:
            content = file.read()
        with open(filename, "w") as file:
            file.write(content + " | " + msg)

def current_time():
    return str(math.floor(time.time()))

@app.route('/get_player_data', methods=['GET'])
def get_player_data():
    return jsonify(player_data=database.load_data(request.cookies.get('id'))["robin_clicker"])

@app.route('/add_click', methods=['GET'])
@limiter.limit("30 per second")
def add_click():
    response = None
    cookie = request.cookies.get('id')
    tm = current_time()

    if cookie is None:
        cookie = tm

    if rate_limit.get(cookie) is None:
        rate_limit[cookie] = 0

    rate_limited = time.time() - rate_limit[cookie] < RATE_LIMIT

    clicker_data = database.increment(cookie, "clicks", 0 if rate_limited else "clickmult")["robin_clicker"]
    
    response = make_response(jsonify(status=("rate_limited" if rate_limited else "success"), player_data=clicker_data))
    if request.cookies.get('id') is None:
        response.set_cookie('id', cookie, max_age=YEAR, domain=('.'+app.config['SERVER_NAME']))

    rate_limit[cookie] = time.time()

    return response

@app.route('/', subdomain="")
def index():
    response = make_response(render_template('index.html'))

    return response

@app.route('/auth/', methods=['POST'])
def auth():
    if request.method == 'POST':
        username = request.form.get('username')
        password = request.form.get('password')
        redirect = request.form.get('redirect')

        # Make sure there are no spaces in the username or password, that they are not empty, and if the length is within 3 to 20 characters
        if not ((not (username is None)) and (not (password is None)) and (not (username.find(' ') != -1)) and (not (password.find(' ') != -1)) and (not (username == '')) and (not (password == '')) and (len(username) >= 3) and (len(username) <= 20) and (len(password) >= 3) and (len(password) <= 20)):
            return 'Invalid username or password.'

        if False: # disabled, will delete soon
            return 'OK'
        else:
            response = make_response('OK')
            cookie_value = database.get_cookie_from_user(username)
            cookie_value_was_none = cookie_value is None

            if cookie_value is None:
                cookie_value = current_time()
            
            user_data = database.load_data(cookie_value)

            if cookie_value_was_none:
                salt = bcrypt.gensalt()
                hashed_password_bytes = bcrypt.hashpw(password.encode('utf-8'), salt)
                hashed_password = base64.b64encode(hashed_password_bytes).decode('utf-8')

                user_data["user_data"]["username"] = username
                user_data["user_data"]["password"] = hashed_password
                user_data["user_data"]["salt"] = salt.decode('utf-8')

                if (not (request.cookies.get('id') is None)) and database.get_user_from_cookie(request.cookies.get('id')) is None:
                    original_data = database.load_data(request.cookies.get('id'))
                    original_data["user_data"] = user_data["user_data"]
                    user_data = original_data
                
                database.save_data(cookie_value, user_data)

                print("Registered user '"+username+"'")
                print("User data: "+str(user_data["user_data"]))
                print("Actual user data: "+str(database.load_data(cookie_value)["user_data"]))
            else:
                print("Attempt to log in "+username+" with password "+password)
                print("User data: "+str(user_data["user_data"]))

                salt = user_data["user_data"]["salt"].encode('utf-8')
                stored_hashed_password = user_data["user_data"]["password"]

                if stored_hashed_password != base64.b64encode(bcrypt.hashpw(password.encode('utf-8'), salt)).decode('utf-8'):
                    return 'Incorrect password.'

            response.set_cookie('id', cookie_value, max_age=YEAR, domain=('.'+app.config['SERVER_NAME']))
            database.set_user_to_cookie(cookie_value, username)

            return response

@app.route('/login/<redirect>/')
def login(redirect):
    processed_redirect = redirect
    page = redirect
    subdomain = ""

    if redirect.find(".") != -1:
        subdomain = redirect.split(".")[0] + "."
        page = redirect.split(".")[1]
    
    processed_redirect = "http://" + subdomain + app.config['SERVER_NAME'] + "/" + page
    
    return make_response(render_template('login.html', redirect=processed_redirect))

@app.route('/clicker/')
def clicker():
    tm = current_time()

    data = database.load_data(request.cookies.get('id') or 0)["robin_clicker"]

    response = make_response(render_template('clicker.html', player_data=json.dumps(data)))

    return response

@app.route('/', subdomain="test")
def test():
    return "Test subdomain"

@app.before_request
def redirect_to_non_www():
    urlparts = urlparse(request.url)
    if urlparts.netloc == ('www.' + app.config['SERVER_NAME'] or "cernyrob.in"):
        urlparts_list = list(urlparts)
        urlparts_list[1] = app.config['SERVER_NAME'] or "cernyrob.in"
        return redirect(urlunparse(urlparts_list), code=301)

callme.init(app)

if __name__ == '__main__':
    if platform.system() == "Linux":
        from gunicorn.app.base import Application

        app.config['SERVER_NAME'] = 'cernyrob.in'

        class StandaloneApplication(Application):
            def init(self, parser, opts, args):
                return {
                    'bind': '0.0.0.0:8000',
                    'workers': 4,
                    'worker_class': 'gevent',
                }

            def load(self):
                return app

        print("Booting server using Gunicorn...")

        StandaloneApplication().run()
    else:
        app.config['SERVER_NAME'] = 'localhost'

        app.run(debug=True, host='0.0.0.0', port=80)
