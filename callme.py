import time
import database
from flask import request, redirect, make_response, render_template
from urllib.parse import urlparse, urlunparse

def init(app):
    @app.route('/', subdomain="callme")
    def callme_home():
        return render_template("callme-home.html")
        
    @app.route('/create/', subdomain="callme", methods=['GET', 'POST'])
    def callme_create():
        if request.cookies.get('id') is None:
            return redirect("http://" + app.config['SERVER_NAME'] + "/login/callme.create/")

        if request.method == 'POST':
            data = database.load_data(request.cookies.get('id'))
            callme_data = data["callme"]

            callme_data["phone_number"] = request.form["phone_number"]
            callme_data["name"] = request.form["name"]

            database.save_data(request.cookies.get('id'), data)

            return "OK"
        else:
            return render_template("callme-create.html")
    
    @app.route('/edit/', subdomain="callme", methods=['GET', 'POST']) # Just for the URL to look good
    def callme_edit():
        callme_create()

    @app.route('/share/', subdomain="callme")
    def callme_share():
        return render_template("callme-share.html")
    
    @app.route('/view/<username>/', subdomain="callme")
    def callme_view(username):
        data = database.load_data(database.get_cookie_from_user(username))
        callme_data = data["callme"]

        if callme_data["phone_number"] is None:
            return render_template("callme-error.html")
        
        return render_template("callme-view.html", phone_number=callme_data["phone_number"], name=callme_data["name"])