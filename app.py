import os
import json
import time

from flask import Flask, render_template, request, jsonify, make_response, session
from flask_session import Session
from gunicorn.app.base import Application

app = Flask(__name__)
app.config['SESSION_TYPE'] = 'filesystem'
Session(app)

data_dir = os.path.join(os.path.dirname(__file__), "Database")

data_template = {
    "clicks": 0,
    "clickmult": 1,
    "upgrades": [],
}

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
        response.set_cookie('id', time.time())

    return response

@app.route('/clicker/')
def clicker():
    player_id = request.cookies.get('id') 
    player_data = json.dumps(load_data(player_id))

    return render_template('clicker.html', player_data=player_data)

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

