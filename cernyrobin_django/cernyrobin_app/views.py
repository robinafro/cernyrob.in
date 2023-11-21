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
   
def login(request):
    context = {}

    return render(request, "cernyrobin/login.html", context)

# Clicker

def add_click(request):
    if request.method == "POST":
        clicker.add_click(request)




def loginReg(request):
    page = "login"
    if request.user.is_authenticated:
        return redirect("home")
    else:
        if request.method == "POST":
            username = request.POST.get("username").lower()
            password = request.POST.get("password")
            try:
                user = User.objects.get(username=username)

            except:
                messages.error(request, "User doesnt exist")

            user = authenticate(request, username=username, password=password)
            if user is not None:
                login(request, user)
                return redirect("home")
            else:
                messages.error(request, "Password wrong")

    context = {
        "page": page,
    }
    return render(request, "cernyrobin/loginReg.html", context)
