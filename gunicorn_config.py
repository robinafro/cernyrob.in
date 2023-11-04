import os

workers = int(os.environ.get('GUNICORN_PROCESSES', '2'))

threads = int(os.environ.get('GUNICORN_THREADS', '4'))

# timeout = int(os.environ.get('GUNICORN_TIMEOUT', '120'))

bind = os.environ.get('GUNICORN_BIND', '0.0.0.0:443')

forwarded_allow_ips = '*'

secure_scheme_headers = { 'X-Forwarded-Proto': 'https' }

keyfile = '/etc/letsencrypt/live/cernyrob.in-0001/privkey.pem'
certfile = '/etc/letsencrypt/live/cernyrob.in-0001/fullchain.pem'
