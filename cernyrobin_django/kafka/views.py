from django.shortcuts import render

def index(request):
    return render(request, "kafka/index.html")

def view(request):
    return render(request, "kafka/view.html")