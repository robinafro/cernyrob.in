import os
import json
import time
import math

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

data_template = {
    "robin_clicker": {
        "clicks": 0,
        "clickmult": 1,
        "upgrades": [],
    },

    "user_data": {
        "username": None,
        "password": None,
    }
}

def current_time():
    return str(math.floor(time.time()))

def save_data(key, data):
    filename = os.path.join(data_dir, f"{key}.json")
    with open(filename, "w") as file:
        json.dump(data, file)

def load_data(key):
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
    for filename in os.listdir(ids_dir):
        with open(os.path.join(ids_dir, filename), "r") as file:
            cookie = file.read()
            if cookie == username:
                return cookie
    return False

@app.route('/get_player_data')
def get_player_data():
    return jsonify(player_data=load_data(request.cookies.get('id'))["robin_clicker"])

@app.route('/add_click')
def add_click():
    data = load_data(request.cookies.get('id'))
    clicker_data = load_data(request.cookies.get('id'))["robin_clicker"]

    clicker_data["clicks"] += clicker_data["clickmult"]

    save_data(request.cookies.get('id'), data)

    return jsonify(status="success")

@app.route('/')
def index():
    response = make_response(render_template('index.html'))
    
    # if request.cookies.get('id') is None:
    #     response.set_cookie('id', current_time(), max_age=YEAR)

    return response

@app.route('/auth/', methods=['POST', 'GET'])
def auth():
    if request.method == 'POST':
        username = request.form.get('username')
        password = request.form.get('password')
        redirect = request.form.get('redirect')

        if not (request.cookies.get('id') is None):
            return 'OK'
        else:
            response = render_template('auth.html')
            cookie_value = get_cookie_from_user(username)
            cookie_value_was_none = cookie_value is None

            if cookie_value is None:
                cookie_value = current_time()
            
            user_data = load_data(cookie_value)

            if cookie_value_was_none:
                user_data["user_data"]["username"] = username
                user_data["user_data"]["password"] = password

                save_data(cookie_value, user_data)
            else:
                if user_data["user_data"]["username"] != username:
                    return 'Incorrect username or password.', 401
                elif user_data["user_data"]["password"] != password:
                    return 'Incorrect username or password.', 401

            set_user_to_cookie(cookie_value, username)
            response.set_cookie('id', cookie_value, max_age=YEAR)

            return response
    else:
        return 'OK'

@app.route('/login/')
def login():
    if request.cookies.get('id') is None:
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

