import time
import database
from flask import request, redirect, make_response, render_template
from urllib.parse import urlparse, urlunparse

def init(app):
    @app.route('/', subdomain="callme")
    def callme_home():
        return "Head over to callme.cernyrob.in/create to create a new phone number link" # Will display a button (href /create), or a button to share or edit (href /share) if already created
        
    @app.route('/create/', subdomain="callme", methods=['GET', 'POST'])
    def callme_create():
        if request.cookies.get('id') is None:
            return redirect("http://" + app.config['SERVER_NAME'] + "/login/callme.create/")

        if request.method == 'POST':
            data = database.load_data(request.cookies.get('id'))
            callme_data = data["callme"]

            callme_data["phone_number"] = request.form["phone_number"]
            callme_data["theme"] = request.form["theme"]

            database.save_data(request.cookies.get('id'), data)

            return "OK"
        else:
            return "TEST/CREATE" # Will display a menu where you can create a new link (acts as Share if already created)
    
    @app.route('/edit/', subdomain="callme", methods=['GET', 'POST']) # Just for the URL to look good
    def callme_edit():
        callme_create()

    @app.route('/share/', subdomain="callme")
    def callme_share():
        return "TEST/SHARE" # Will display a QR code and a link to share
    
    @app.route('/view/<username>/', subdomain="callme")
    def callme_view(username):
        data = database.load_data(database.get_cookie_from_user(username))
        callme_data = data["callme"]

        if callme_data["phone_number"] is None:
            return "NO PHONE NUMBER FOR THIS USERNAME"
        
        return "TEST/VIEW: " + callme_data["phone_number"]