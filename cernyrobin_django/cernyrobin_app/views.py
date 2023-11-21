from django.shortcuts import render

def home(request):
    context = {}
    return render(request, "cernyrobin/home.html", context)

def clicker(request):
    context = {}

    return render(request, "cernyrobin/clicker.html", context)
   
def login(request):
    context = {}

    return render(request, "cernyrobin/login.html", context)