from django.shortcuts import render
from django.http import HttpResponse, JsonResponse
from api.models import System, Kafka

from api.yt_transcriptor import main as yt_transcriptor

import datetime, json

GENERATE_RATE_LIMIT = 60 * 60 * 24 * 7 - 60 * 60 * 6 # 7 days minus six hours to prevent it from shifting too far forward
KAFKA_CHANNEL = "https://www.youtube.com/channel/@jankafka1535"

def kafka(request, subdomain):
    return HttpResponse("Hello, world. You're at the api index.")

def kafka_get(request, subdomain):
    response = {"code": 200, "message": "OK"}

    video_url = request.GET.get("video_url")

    if not video_url:
        response["code"] = 400
        response["message"] = "Bad request"

        return JsonResponse(response)

    video_url = video_url.replace("\"", "")

    try:
        kafka = Kafka.objects.get(video_url=video_url)

        response["code"] = 200
        response["message"] = "OK"
        response["data"] = {
            "answers": kafka.answers,
            "transcript": kafka.transcript,
            "language": kafka.language,
            "video_info": json.loads(kafka.video_info),
        }

        return JsonResponse(data=response)
    except Kafka.DoesNotExist:
        response["code"] = 404
        response["message"] = "Not found"

        return JsonResponse(data=response)
    except Exception as e:
        print(e)
        response["code"] = 500
        response["message"] = "Internal server error"

        return JsonResponse(data=response)

def kafka_list(request, subdomain):
    response = {"code": 200, "message": "OK", "list": {}}

    try:
        for kafka in Kafka.objects.all():
            response["list"][kafka.video_url] = {
                "answers": kafka.answers,
                "transcript": kafka.transcript,
                "language": kafka.language,
                "video_info": json.loads(kafka.video_info),
            }
    except Exception as e:
        print(e)
        response["code"] = 500
        response["list"] = {}
        response["message"] = "Internal server error"

    return JsonResponse(data=response)

def kafka_answer(request, subdomain):
    response = {"code": 200, "message": "OK"}

    video_url = request.GET.get("video_url")
    language = request.GET.get("language")

    if not video_url:
        return HttpResponse("Bad request") # Not returning JSON to prevent bots
    
    if not language:
        language = "cs-CZ"

    video_url = video_url.replace("\"", "")

    video_info = yt_transcriptor.get_video_info(video_url)

    if not video_info:
        return HttpResponse("Video not found")
    
    if json.loads(video_info)["author_url"] != KAFKA_CHANNEL:
        return HttpResponse("Invalid video channel")

    try:
        # Always use a rate limit when dealing with OpenAI API requests!

        system_data = System.objects.get_or_create(key="SYSTEM_DATA")
        
        if False and (datetime.datetime.now().replace(tzinfo=None) - system_data[0].last_generated.replace(tzinfo=None)).total_seconds() < GENERATE_RATE_LIMIT:
            return HttpResponse("Rate limit exceeded")
        
        system_data[0].last_generated = datetime.datetime.now().replace(tzinfo=None)
        system_data[0].save()

        answers, transcript = yt_transcriptor.run(video_url, language)

        # Save to database
        kafka, created = Kafka.objects.get_or_create(video_url=video_url)

        kafka.answers = answers
        kafka.transcript = transcript
        kafka.language = language
        kafka.video_info = video_info
        kafka.save()

        response["code"] = 200
        response["message"] = "OK"
        response["data"] = {
            "answers": answers,
            "transcript": transcript,
            "language": language,
            "video_info": json.loads(kafka.video_info),
        }

        return JsonResponse(data=response)
    except Exception as e:
        print(e)
        response["code"] = 500
        response["message"] = "Internal server error"

        return JsonResponse(data=response)

