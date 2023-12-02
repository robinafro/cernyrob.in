from django.shortcuts import render
from django.http import HttpResponse

from api import get_video_info
from api import views as api_views
import json

def index(request):
    return render(request, "kafka/index.html", context={})

def view(request):
    id = request.GET.get("id")

    if id is None:
        return HttpResponse("Invalid video ID")
    
    video_url = "https://www.youtube.com/watch?v=" + id

    video_info = json.loads(get_video_info.get_video_info(video_url))
    
    answers = api_views.get_answers(video_url).strip()
    
    return render(request, "kafka/view.html", context={
        "title": video_info["title"],
        "video_url": video_url,
        "questions": video_info["description"],
        "answers": answers
    })

def submit(request):
    if request.method == "GET":
        return render(request, "kafka/submit.html", context={
            "last_generated": api_views.get_last_generated().timestamp(),
            "generate_rate_limit": api_views.GENERATE_RATE_LIMIT,
        })
    elif request.method == "POST":
        video_url = request.POST.get("video_url")
        
        if video_url is None:
            return HttpResponse("Invalid video URL")
        
        video_id = None
        if video_url.find("watch?v=") != -1:
            video_id = video_url.split("v=")[1]
        elif video_url.find("youtu.be/") != -1:
            video_id = video_url.split("youtu.be/")[1]
        else:
            video_id = video_url

        video_url = "https://www.youtube.com/watch?v=" + video_id
        
        response = api_views.generate_answers(video_url, "cs-CZ")

        return response