import os
import json

from flask import Flask, render_template, request
from gunicorn.app.base import Application

app = Flask(__name__)

data_dir = os.path.join(script_dir, os.path.dirname(__file__))

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

@app.route('/add_click/')
def add_click(ip_address):
    data = load_data(ip_address)

    data.clicks = data.clicks + data.clickmult

    save_data(ip_address, data)

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/clicker/')
def clicker():
    player_ip = request.remote_addr
    player_data = load_data(player_ip)

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

