from django.shortcuts import render, redirect
from django.http import HttpResponse, JsonResponse

from api import get_video_info
from api import views as api_views
from ads import views as ads_views
import json
import re


def parse_answers(text):


    segments = re.split(r'(\d+\.)', text)

    extracted_parts = []
    last_number = 0
    current_part = ''

    for segment in segments:
        if re.match(r'\d+\.', segment):
            current_number = int(segment.split('.')[0])
            if current_number == last_number + 1:
                if current_part:
                    extracted_parts.append(current_part.strip())
                current_part = segment
                last_number = current_number
            else:
                current_part += segment
        else:
            current_part += segment

    if current_part:
        extracted_parts.append(current_part.strip())

    return extracted_parts



def index(request):
    all_videos = api_views.get_all_to_be_displayed()

    context = ads_views.get_ads(length=len(all_videos))

    context["videos"] = []

    for video in all_videos:
        context["videos"].append(
    {
                "title": video["title"],
                "video_id": video["video_id"],
                "description": video["description"],
            }
        )

    return render(request, "kafka/index.html", context)


def view(request):
    if request.method == "GET":
        id = request.GET.get("id").strip(" ")

        if id is None:
            return HttpResponse("Invalid video ID")

        video_url = "https://www.youtube.com/watch?v=" + id

        video_info = json.loads(get_video_info.get_video_info(video_url))

        answers = api_views.get_answers(video_url).strip()
        transcript = api_views.get_transcript(video_url).strip()

        ads = ads_views.get_ads(length=2)

        return render(
            request,
            "kafka/view.html",
            context={
                "title": video_info["title"],
                "video_url": video_url,
                "video_id": id,
                "questions": video_info["description"],
                "answers": parse_answers(answers),
                "transcript": transcript,
                "ads_left": ads["ads_left"],
                "ads_right": ads["ads_right"],
                "is_staff" : request.user.is_staff
            },
        )
    elif request.method == "POST":
        if request.user.is_staff:
            questions = request.POST.get("edited_answers")
            video_url = "https://www.youtube.com/watch?v=" + request.POST.get("video_id").strip()

            print(questions)
            api_views.modify_questions(video_url, questions)
            
            return redirect("kafka_list")
        else:
            return HttpResponse("no lol")




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
