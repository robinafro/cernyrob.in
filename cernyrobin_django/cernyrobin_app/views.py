from django.shortcuts import render
from . import clicker
from django.shortcuts import render, redirect
from django.http import HttpResponse
from django.db.models import Q
from django.contrib.auth.decorators import login_required
from django.contrib.auth.forms import UserCreationForm
""" from .models import Room, Topic
from .forms import RoomForm """
from django.contrib.auth.models import User
from django.contrib import messages
from django.contrib.auth import authenticate, login, logout

# Pages

def home(request):
    context = {}
    return render(request, "cernyrobin/home.html", context)

def clicker(request):
    context = {}

    return render(request, "cernyrobin/clicker.html", context)
   
def login_page(request):
    if request.user.is_authenticated:
        return redirect("home") #!
    else:
        context = {
            "page": "login",
        }

        return render(request, "cernyrobin/login.html", context)

def login_submit(request):
    if request.user.is_authenticated:
        return HttpResponse("400 Bad Request")

    if request.method == "POST":
        username = request.POST.get("username").lower()
        password = request.POST.get("password")

        try:
            user = User.objects.get(username=username)
        except User.DoesNotExist:
            user = User.objects.create_user(username=username, password=password)
            user.save()
            return HttpResponse("200 OK")

        if user.check_password(password):
            user = authenticate(request, username=username, password=password)
            
            if user is not None:
                login(request, user)
                return HttpResponse("200 OK")
            else:
                return HttpResponse("401 Unauthorized")
        else:
            return HttpResponse("401 Unauthorized")

    return HttpResponse("405 Method Not Allowed")
        
# Clicker

def add_click(request):
    if request.method == "POST":
        clicker.add_click(request)
