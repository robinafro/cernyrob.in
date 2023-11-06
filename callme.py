import time
import database
from flask import request, redirect, make_response, render_template
from urllib.parse import urlparse, urlunparse

def init(app):
    @app.route('/home/', subdomain="callme")
    def callme_home():
        return "Head over to callme.cernyrob.in/create to create a new phone number link" # Will display a button (href /create), or a button to share or edit (href /share) if already created
    
    # @app.before_request
    # def callme_create_redirect():
    #     urlparts = urlparse(request.url)
    #     print(urlparts.netloc)
    #     if urlparts.netloc == ('callme.' + app.config['SERVER_NAME'] + "/create/") or urlparts.netloc == ('callme.' + app.config['SERVER_NAME'] + "/create"):
    #         urlparts_list = list(urlparts)
    #         urlparts_list[1] = app.config['SERVER_NAME'] + "/login/callme.create/"
    #         print(urlunparse(urlparts_list))
    #         if request.cookies.get('id') is None:
    #             return redirect(urlunparse(urlparts_list), code=301)
        
    @app.route('/create/', subdomain="callme")
    def callme_create():
        print(request.cookies.get('id'))
        if request.cookies.get('id') is None:
            return redirect("http://" + app.config['SERVER_NAME'] + "/login/callme.create/")

        return "TEST/CREATE" # Will display a menu where you can create a new link (acts as Share if already created)
    
    @app.route('/share/', subdomain="callme")
    def callme_share():
        return "TEST/SHARE" # Will display a QR code and a link to share
    
    @app.route('/view/<username>/', subdomain="callme")
    def callme_view(username):
        data = database.load_data(username)
        callme_data = data["callme"]

        if callme_data["phone_number"] is None:
            return "NO PHONE NUMBER FOR THIS USERNAME"
        
        return "TEST/VIEW: " + callme_data["phone_number"]