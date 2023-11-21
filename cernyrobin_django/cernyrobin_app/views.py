from django.shortcuts import render

def home(request):
    return render(request, "cernyrobin/home.html", {})

def clicker(request):
    return render(request, "cernyrobin/clicker.html", {})
   
