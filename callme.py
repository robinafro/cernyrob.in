import time
import platform;
import database
import re
from flask import request, redirect, make_response, render_template, jsonify, Response
from urllib.parse import urlparse, urlunparse

def validate_phone_number(phone_number):
    # Check if the phone number matches the pattern
    if re.match("^\\+?[1-9][0-9]{7,14}$", phone_number):
        return True
    else:
        return False
    
def init(app):
    @app.route('/', subdomain="callme")
    def callme_home():
        return render_template("callme-home.html")
        
    @app.route('/create/', subdomain="callme", methods=['GET', 'POST'])
    def callme_create():
        if request.cookies.get('id') is None and platform.system() == "Linux":
            return redirect("http://" + app.config['SERVER_NAME'] + "/login/callme.create/")

        if request.method == 'POST':
            name = request.form.get("name")
            phone_number = request.form.get("phone_number")
            
            # Validate phone number
            if phone_number is None or phone_number == "":
                return Response("Phone number not specified", status=400)
            
            phone_number = phone_number.replace(" ", "")

            if not validate_phone_number(phone_number):
                return Response("Invalid phone number", status=400)

            # Validate name
            if name is None or name == "":
                return Response("Name not specified", status=400)
            
            if re.match("^[a-zA-Z0-9_ ]*$", name) is None:
                return Response("Invalid name", status=400)
            
            if len(name) > 20:
                return Response("Name too long", status=400)

            data = database.load_data(request.cookies.get('id'))
            callme_data = data["callme"]

            callme_data["phone_number"] = phone_number
            callme_data["name"] = name

            database.save_data(request.cookies.get('id'), data)

            return Response("OK", status=200)
        else:
            return render_template("callme-create.html")
    
    @app.route('/edit/', subdomain="callme", methods=['GET', 'POST']) # Just for the URL to look good
    def callme_edit():
        return callme_create()

    @app.route('/share/', subdomain="callme")
    def callme_share():
        if request.cookies.get('id') is None and platform.system() == "Linux":
            return redirect("http://" + app.config['SERVER_NAME'] + "/login/callme.share/")
        
        data = database.load_data(request.cookies.get('id'))

        if data["callme"]["phone_number"] is None:
            return render_template("callme-error.html")
        
        link = "http://callme." + app.config['SERVER_NAME'] + "/view/" + database.get_userid_from_username(data["user_data"]["username"])

        return render_template("callme-share.html", link=link)
    
    @app.route('/view/<userid>/', subdomain="callme")
    def callme_view(userid):
        data = database.load_data(database.get_cookie_from_user(database.get_user_from_user_id(userid)))
        callme_data = data["callme"]

        if callme_data["phone_number"] is None:
            return render_template("callme-error.html")
        
        return render_template("callme-view.html", phone_number=callme_data["phone_number"], name=callme_data["name"])
    
    @app.route('/get_data/', subdomain="callme")
    def get_data():
        data = database.load_data(request.cookies.get('id'))

        return jsonify(callme_data=data["callme"])
    
    @app.route('/delete/', subdomain="callme")
    def delete():
        data = database.load_data(request.cookies.get('id'))
        callme_data = data["callme"]

        callme_data["phone_number"] = None
        callme_data["name"] = None

        database.save_data(request.cookies.get('id'), data)

        return redirect("http://callme." + app.config['SERVER_NAME'] + "/")