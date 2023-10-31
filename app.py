import os
import json
import time
import math

from flask import Flask, render_template, request, jsonify, make_response
from flask_session import Session
from gunicorn.app.base import Application

YEAR = 60 * 60 * 24 * 365

app = Flask(__name__)
app.config["SESSION_PERMANENT"] = True
app.config['SESSION_TYPE'] = 'filesystem'
Session(app)

data_dir = os.path.join(os.path.dirname(__file__), "Database")

data_template = {
    "clicks": 0,
    "clickmult": 1,
    "upgrades": [],
}

def current_time():
    return str(math.floor(time.time()))

def save_data(ip_address, data):
    filename = os.path.join(data_dir, f"{ip_address}.json")
    with open(filename, "w") as file:
        json.dump(data, file)

def load_data(ip_address):
    filename = os.path.join(data_dir, f"{ip_address}.json")
    if os.path.exists(filename):
        with open(filename, "r") as file:
            return json.load(file)
    else:
        return data_template

@app.route('/get_player_data')
def get_player_data():
    return jsonify(player_data=load_data(request.cookies.get('id')))

@app.route('/add_click')
def add_click():
    data = load_data(request.cookies.get('id'))

    data["clicks"] += data["clickmult"]

    save_data(request.cookies.get('id'), data)

    return jsonify(status="success")

@app.route('/')
def index():
    response = make_response(render_template('index.html'))
    
    if request.cookies.get('id') is None:
        response.set_cookie('id', current_time(), max_age=YEAR)

    return response

@app.route('/login/')
def auth_screen():
    response = make_response(render_template('auth.html'))

    if request.cookies.get('id') is None:
        return response # return the login screen. the client will later send their login credentials
    else:
        # redirect to the page that the user was at before they got redirected to the login screen
        # temporary code below
        return response

@app.route('/clicker/')
def clicker():
    tm = current_time()

    response = make_response(render_template('clicker.html', player_data=json.dumps(load_data(request.cookies.get('id') or tm))))

    if request.cookies.get('id') is None:
        response.set_cookie('id', tm, max_age=YEAR)

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

