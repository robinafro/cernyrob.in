from django.shortcuts import render
from django.http import HttpResponse, JsonResponse

from api.yt_transcriptor import main as yt_transcriptor

def kafka(request, subdomain):
    return HttpResponse("Hello, world. You're at the api index.")

def kafka_answer(request, subdomain):
    response = {"code": 200, "message": "OK"}

    video_url = request.GET.get("video_url")
    language = request.GET.get("language")

    if not video_url:
        response["code"] = 400
        response["message"] = "Bad request"

        return JsonResponse(response)
    
    if not language:
        language = "cs-CZ"

    video_url = video_url.replace("\"", "")

    try:
        answers = yt_transcriptor.run(video_url, language)

        response["code"] = 200
        response["message"] = "OK"
        response["answers"] = answers

        return JsonResponse(response)
    except Exception as e:
        response["code"] = 500
        response["message"] = "Internal server error"

        return JsonResponse(response)

