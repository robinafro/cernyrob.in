import os
import json
import time
import math
import bcrypt
import base64

from flask import Flask, render_template, request, jsonify, make_response, redirect
from flask_session import Session
from gunicorn.app.base import Application

YEAR = 60 * 60 * 24 * 365

app = Flask(__name__)
app.config["SESSION_PERMANENT"] = True
app.config['SESSION_TYPE'] = 'filesystem'
Session(app)

data_dir = os.path.join(os.path.dirname(__file__), "Database")
ids_dir = os.path.join(os.path.dirname(__file__), "IDs")
log_dir = os.path.join(os.path.dirname(__file__), "Logs")

data_template = {
    "robin_clicker": {
        "clicks": 0,
        "clickmult": 1,
        "upgrades": [],
    },

    "user_data": {
        "username": None,
        "password": None,
        "salt": None,
    }
}

def log(msg):
    filename = os.path.join(log_dir, f"log.txt")
    content = ""
    with open(filename, "r") as file:
       content = file.read()
    with open(filename, "w") as file:
       file.write(content + " | " + msg)

def current_time():
    return str(math.floor(time.time()))

def save_data(key, data):
    if key == 0:
        return
    
    filename = os.path.join(data_dir, f"{key}.json")
    with open(filename, "w") as file:
        json.dump(data, file)

def load_data(key):
    if key == 0:
        return data_template
    
    filename = os.path.join(data_dir, f"{key}.json")
    if os.path.exists(filename):
        with open(filename, "r") as file:
            return json.load(file)
    else:
        return data_template

def get_user_from_cookie(cookie):
    filename = os.path.join(ids_dir, f"{cookie}.txt")
    if os.path.exists(filename):
        with open(filename, "r") as file:
            return file.read()
    else:
        return None
    
def set_user_to_cookie(cookie, user):
    filename = os.path.join(ids_dir, f"{cookie}.txt")
    with open(filename, "w") as file:
       file.write(user)

def get_cookie_from_user(username):
    for cookie in os.listdir(ids_dir):
        with open(os.path.join(ids_dir, cookie), "r") as file:
            usr = file.read()
            if usr == username:
                return cookie.replace(".txt", "")
    return None

@app.route('/get_player_data')
def get_player_data():
    return jsonify(player_data=load_data(request.cookies.get('id'))["robin_clicker"])

@app.route('/add_click')
def add_click():
    response = make_response(jsonify(status="success"))
    cookie = request.cookies.get('id')

    if cookie is None:
        tm = current_time()
        response.set_cookie('id', tm, max_age=YEAR)
        cookie = tm

    data = load_data(cookie)
    clicker_data = data["robin_clicker"]

    clicker_data["clicks"] += clicker_data["clickmult"]

    save_data(cookie, data)

    return response

@app.route('/')
def index():
    response = make_response(render_template('index.html'))
    
    # if request.cookies.get('id') is None:
    #     response.set_cookie('id', current_time(), max_age=YEAR)

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
            cookie_value = get_cookie_from_user(username)
            cookie_value_was_none = cookie_value is None

            if cookie_value is None:
                cookie_value = current_time() # cookie value might be set to the current time even if the user is not new
            
            user_data = load_data(cookie_value)

            if cookie_value_was_none:
                salt = bcrypt.gensalt()
                hashed_password_bytes = bcrypt.hashpw(password.encode('utf-8'), salt)
                hashed_password = base64.b64encode(hashed_password_bytes).decode('utf-8')

                user_data["user_data"]["username"] = username
                user_data["user_data"]["password"] = hashed_password
                user_data["user_data"]["salt"] = salt.decode('utf-8')

                if not (request.cookies.get('id') is None):
                    original_data = load_data(request.cookies.get('id'))
                    original_data["user_data"] = user_data["user_data"]
                    user_data = original_data
                
                save_data(cookie_value, user_data)

                log("Registered user '"+username+"'")
                log("User data: "+str(user_data["user_data"]))
                log("Actual user data: "+str(load_data(cookie_value)["user_data"]))
            else:
                log("Attempt to log in "+username+" with password "+password)
                log("User data: "+str(user_data["user_data"]))

                salt = user_data["user_data"]["salt"].encode('utf-8')
                stored_hashed_password = user_data["user_data"]["password"]

                if stored_hashed_password != base64.b64encode(bcrypt.hashpw(password.encode('utf-8'), salt)).decode('utf-8'):
                    return 'Incorrect password.'

            response.set_cookie('id', cookie_value, max_age=YEAR)
            set_user_to_cookie(cookie_value, username)

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

    data = load_data(request.cookies.get('id') or 0)["robin_clicker"]

    response = make_response(render_template('clicker.html', player_data=json.dumps(data)))

    # if request.cookies.get('id') is None:
    #     response.set_cookie('id', tm, max_age=YEAR)

    return response

if not os.path.exists(data_dir):
    os.mkdir(data_dir)

if __name__ == '__main__':
    class StandaloneApplication(Application):
        def init(self, parser, opts, args):
            return {
                'bind': '0.0.0.0:8000',
                'workers': 4,
                'worker_class': 'gevent',
            }

        def load(self):
            return app

    print("Booting server...")

    StandaloneApplication().run()

