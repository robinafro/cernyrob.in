from flask import Flask, render_template
from gunicorn.app.base import Application

app = Flask(__name__)


@app.route('/')

def index():
    return render_template('index.html')

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

    StandaloneApplication().run()

