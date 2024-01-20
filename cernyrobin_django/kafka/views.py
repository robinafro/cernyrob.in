from django.shortcuts import render, redirect
from django.http import HttpResponse, JsonResponse

from api import get_video_info
from api import views as api_views
from ads import views as ads_views
import json
import re

def strip_yapping(s):
    for i, char in enumerate(s):
        if char.isdigit():
            return s[i:]
    return s

def parse_numbered_text(text):
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
                # "description": video["description"],
                "questions" : parse_numbered_text(strip_yapping(video["description"])),
            }
        )
    context["current_user"] = request.user
    context["logged_in"] = request.user.is_authenticated
    print(context)

    return render(request, "kafka/index.html", context)


def view(request):
    if request.method == "GET":
        id = request.GET.get("id").strip(" ")

        if id is None:
            return HttpResponse("Invalid video ID")

        video_url = "https://www.youtube.com/watch?v=" + id

        video_info = json.loads(get_video_info.get_video_info(video_url))

        answers = api_views.get_answers(video_url, request.user).strip()
        transcript = api_views.get_transcript(video_url).strip()

        ads = ads_views.get_ads(length=2)


        parsed_questions = parse_numbered_text(strip_yapping(video_info["description"]))

        parsed_answers = parse_numbered_text(strip_yapping(answers))
        # questions = ["otázka 1", "otázka 2"]
        # answers = ["odpověď 1", "odpověď 2"]

  #      qa_pairs = zip(parsed_questions, parsed_answers)
        

        # Bro stop waffling stupid ass shit
        # ˇˇˇˇ DO NOT EVER FUCKING TOUCH THIS GODDAMN LINE OR THE WHOLE THING FALLS APART
        qa_pairs = zip(parse_numbered_text(strip_yapping(video_info["description"])), parse_numbered_text(strip_yapping(answers)))
        # ^^^^ DO NOT EVER FUCKING TOUCH THIS GODDAMN LINE OR THE WHOLE THING FALLS APART

        # print(parsed_answers)
        # print(parsed_questions)
        # print(type(video_info["description"]))
        # print(type(strip_yapping(video_info["description"])))
        # print(type(parse_numbered_text(strip_yapping(video_info["description"]))))
        
        # print(type(answers))
        # print(type(parse_numbered_text(answers)))


        # for q, a in qa_pairs:
        #     print(q)
        #     print(a)
        #     print("---------------------")
        
#        print(video_info)
        # for question in answers:
        #     print("1111 " + question))
        return render(
            request,
            "kafka/view.html",
            context={
                "title": video_info["title"],
                "video_url": video_url,
                "video_id": id,
                "video_title" :video_info["title"],
#                "questions": parse_numbered_text(video_info["description"]),
#                "answers": parse_numbered_text(answers),
                "qa_pairs" : qa_pairs,
                "transcript": transcript,
                "ads_left": ads["ads_left"],
                "ads_right": ads["ads_right"],
                "is_staff" : request.user.is_staff,
                "current_user" : request.user,
            },
        )
    elif request.method == "POST":
        if request.user.is_staff:
            questions = request.POST.get("edited_answers")
            video_url = "https://www.youtube.com/watch?v=" + request.POST.get("video_id").strip()

#            print(questions)
            api_views.modify_questions(video_url, questions)
            
            return redirect("kafka_list")
        else:
            return HttpResponse("Nuh uh")

def submit(request):
    if request.method == "GET":
        return render(
            request,
            "kafka/submit.html",
            context={
                "last_generated": api_views.get_last_generated(),
                "generate_rate_limit": api_views.GENERATE_RATE_LIMIT,
                "current_user" : request.user,
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

def renegerate(request):
    if request.method == "POST":
        #! Check if the user has a verified email
        
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

        response = api_views.generate_answers(video_url, "cs-CZ", runbackground=True, user=request.user)

        return response