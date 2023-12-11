from django.shortcuts import render
from django.http import HttpResponse, JsonResponse

from api import get_video_info
from api import views as api_views
import json


def index(request):
    context = {"videos": []}

    for video in api_views.get_all_to_be_displayed():
        context["videos"].append(
            {
                "title": video["title"],
                "video_id": video["video_id"],
                "description": video["description"],
            }
        )

    return render(request, "kafka/index.html", context)


def view(request):
    id = request.GET.get("id").strip(" ")

    if id is None:
        return HttpResponse("Invalid video ID")

    video_url = "https://www.youtube.com/watch?v=" + id

    video_info = json.loads(get_video_info.get_video_info(video_url))

    answers = api_views.get_answers(video_url).strip()
    transcript = api_views.get_transcript(video_url).strip()

    return render(
        request,
        "kafka/view.html",
        context={
            "title": video_info["title"],
            "video_url": video_url,
            "video_id": id,
            "questions": video_info["description"],
            "answers": answers,
            "transcript": transcript,
        },
    )


def submit(request):
    if request.method == "GET":
        return render(
            request,
            "kafka/submit.html",
            context={
                "last_generated": api_views.get_last_generated(),
                "generate_rate_limit": api_views.GENERATE_RATE_LIMIT,
            },
        )
    elif request.method == "POST":
        video_url = request.POST.get("video_url")

        if video_url is None:
            return JsonResponse({"code": 400, "message": "Invalid video URL"})

        video_id = None
        if video_url.find("watch?v=") != -1:
            video_id = video_url.split("v=")[1]
        elif video_url.find("youtu.be/") != -1:
            video_id = video_url.split("youtu.be/")[1]

        if video_id is None:
            return JsonResponse({"code": 400, "message": "Invalid video URL"})
        
        if video_id.find("&") != -1:
            video_id = video_id.split("&")[0]
        elif video_id.find("?") != -1:
            video_id = video_id.split("?")[0]
 
        video_url = "https://www.youtube.com/watch?v=" + video_id

        response = api_views.generate_answers(video_url, "cs-CZ", runbackground=True)

        return response