import os
import json
import time
import math
import bcrypt
import base64

from flask import Flask, render_template, request, jsonify, make_response, redirect
from flask_session import Session

import database

YEAR = 60 * 60 * 24 * 365
RATE_LIMIT = 1 / 25 # CPS

app = Flask(__name__)
app.config["SESSION_PERMANENT"] = True
app.config['SESSION_TYPE'] = 'filesystem'
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

@app.route('/get_player_data')
def get_player_data():
    return jsonify(player_data=database.load_data(request.cookies.get('id'))["robin_clicker"])

@app.route('/add_click')
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
        response.set_cookie('id', cookie, max_age=YEAR)

    rate_limit[cookie] = time.time()

    return response

@app.route('/')
def index():
    response = make_response(render_template('index.html'))

    return response

@app.route('/auth/', methods=['POST'])
def auth():
    if request.method == 'POST':
        username = request.form.get('username')
        password = request.form.get('password')
        redirect = request.form.get('redirect')

        if False: # disabled
            return 'OK'
        else:
            response = make_response('OK')
            cookie_value = database.get_cookie_from_user(username)
            cookie_value_was_none = cookie_value is None

            if cookie_value is None:
                cookie_value = current_time() # cookie value might be set to the current time even if the user is not new
            
            user_data = database.load_data(cookie_value)

            if cookie_value_was_none:
                salt = bcrypt.gensalt()
                hashed_password_bytes = bcrypt.hashpw(password.encode('utf-8'), salt)
                hashed_password = base64.b64encode(hashed_password_bytes).decode('utf-8')

                user_data["user_data"]["username"] = username
                user_data["user_data"]["password"] = hashed_password
                user_data["user_data"]["salt"] = salt.decode('utf-8')

                if not (request.cookies.get('id') is None):
                    original_data = database.load_data(request.cookies.get('id'))
                    original_data["user_data"] = user_data["user_data"]
                    user_data = original_data
                
                database.save_data(cookie_value, user_data)

                log("Registered user '"+username+"'")
                log("User data: "+str(user_data["user_data"]))
                log("Actual user data: "+str(database.load_data(cookie_value)["user_data"]))
            else:
                log("Attempt to log in "+username+" with password "+password)
                log("User data: "+str(user_data["user_data"]))

                salt = user_data["user_data"]["salt"].encode('utf-8')
                stored_hashed_password = user_data["user_data"]["password"]

                if stored_hashed_password != base64.b64encode(bcrypt.hashpw(password.encode('utf-8'), salt)).decode('utf-8'):
                    return 'Incorrect password.'

            response.set_cookie('id', cookie_value, max_age=YEAR)
            database.set_user_to_cookie(cookie_value, username)

            return response

@app.route('/login/')
def login():
    if request.cookies.get('id') is None or True:
        return make_response(render_template('login.html')) # return the login screen. the client will later send their login credentials
    else:
        return make_response(render_template('auth_redirect.html'))

@app.route('/clicker/')
def clicker():
    tm = current_time()

    data = database.load_data(request.cookies.get('id') or 0)["robin_clicker"]

    response = make_response(render_template('clicker.html', player_data=json.dumps(data)))

    # if request.cookies.get('id') is None:
    #     response.set_cookie('id', tm, max_age=YEAR)

    return response

if __name__ == '__main__':
    if os.name == "posix":
        from gunicorn.app.base import Application

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
        app.run(debug=True, host='0.0.0.0', port=80)