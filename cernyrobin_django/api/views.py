from django.shortcuts import render
from django.http import HttpResponse, JsonResponse
from django.shortcuts import redirect
from api.models import System, Kafka, Job

from api.yt_transcriptor import main as yt_transcriptor
from api import get_video_info

import datetime, json, re, threading, dotenv, os

dotenv.load_dotenv()

GENERATE_RATE_LIMIT = 60 * 60 #60 * 60 * 24 * 7 - 60 * 60 * 6 # 7 days minus six hours to prevent it from shifting too far forward
KAFKA_CHANNEL = "https://www.youtube.com/@jankafka1535"
DESCRIPTION_FORMAT = r".*/s(?:\s+\d+.\s+.*?)+(?=\n\n|\Z)" #r"\d+\.\s(?:.+?\?)" # chatgpt

if os.getenv("NORATELIMIT") == "1":
    GENERATE_RATE_LIMIT = 0

def get_answers(video_url):
    try:
        kafka = Kafka.objects.get(video_url=video_url)

        return kafka.answers or "Unable to get answers"
    except Kafka.DoesNotExist:
        return "Unable to get answers"
    
def get_transcript(video_url):
    video_url = video_url.strip(" ")

    try:
        kafka = Kafka.objects.get(video_url=video_url)

        return kafka.transcript or "Unable to get transcript"
    except Kafka.DoesNotExist:
        return "Unable to get transcript"

def get_last_generated():
    try:
        system_data = System.objects.get_or_create(key="SYSTEM_DATA")

        return system_data[0].last_generated
    except System.DoesNotExist:
        return 0
    except Exception as e:
        print(e)
        return 0
    
def id_from_url(url):
    if url.find("watch?v=") != -1:
        id = url.split("watch?v=")[1]
        if id.find("&") != -1:
            id = id.split("&")[0]

        return id
    elif url.find("youtu.be/") != -1:
        id = url.split("youtu.be/")[1]
        if id.find("?") != -1:
            id = id.split("?")[0]

        return id
    
def is_json(js):
    try:
        json.loads(js)
    except:
        return False
    
    return True

def get_all_to_be_displayed():
    all_data = []

    for kafka in Kafka.objects.all():
        if kafka is None:
            continue

        if kafka.video_info is None:
            continue
        # elif not is_json(kafka.video_info):
        #     continue
        
        video_info = kafka.video_info
        
        all_data.append({
                    "video_id": id_from_url(kafka.video_url),
                    "description": video_info["description"],
                    "title": video_info["title"],
                })
    
    return all_data

def generate_answers(video_url, language, runbackground=False):
    video_url = video_url.strip(" ")
    
    response = {"code": 200, "message": "OK"}

    video_info = get_video_info.get_video_info(video_url)

    if video_info is None:
        return JsonResponse(data={"code": 400, "message": "Video not found"})
    
    if json.loads(video_info)["author_url"] != KAFKA_CHANNEL:
        return JsonResponse(data={"code": 400, "message": "Invalid video channel"})
    
    regexp = re.compile(r'\n|^\d. ?[\w,?\s\??.?]+')
    
    if regexp.search(json.loads(video_info)["description"]) is None:
        return JsonResponse(data={"code": 400, "message": "Invalid video description"})

    try:
        # Always use a rate limit when dealing with OpenAI API requests!
        print("Creating system data")
        system_data = System.objects.get_or_create(key="SYSTEM_DATA")
        print("Created system data")
        
        if not system_data[0].last_generated:
            print("B")
            system_data[0].last_generated = datetime.datetime.now().replace(tzinfo=None).timestamp()
            system_data[0].save()
            print("C")
        
        try:
            print("Getting kafak object")
            print("video_url", video_url)
            print(type(video_url))
            kafka = Kafka.objects.get(video_url=video_url) 
            print("done")
            if kafka.video_info is None or kafka.video_info == {} or kafka.video_info is {}:
                print("A") 
                kafka.video_info = json.loads(video_info)
            print(kafka.video_info)
            response["code"] = 201
            response["message"] = id_from_url(video_url)
            # response["data"] = {
            #     "answers": kafka.answers,
            #     "transcript": kafka.transcript,
            #     "language": language,
            #     "video_info": (kafka.video_info),
            #     "video_url": video_url,
            # }

            return JsonResponse(data=response)
        except Exception as e:
            print(e)
            kafka = None
        
        rate_limited = False
        if (datetime.datetime.now().replace(tzinfo=None).timestamp() - system_data[0].last_generated) < GENERATE_RATE_LIMIT:
            rate_limited = True

        job_already_exists = False
        job = None
        try:
            print("Finding job")
            job = Job.objects.get(job_id=id_from_url(video_url).strip(" "))
            
            job_already_exists = True
        except Exception as e:
            print(e)
            job = None

        # Make the job expire
        if job_already_exists and (datetime.datetime.now().replace(tzinfo=None).timestamp() - job.created >= 60 * 45 or job.video_url == ""): # Reset old jobs
            job.delete()

            job_already_exists = False
            
        if job_already_exists:
            return JsonResponse(data={"code": 200, "message": id_from_url(video_url)})
        else:
            if rate_limited:
                return JsonResponse(data={"code": 400, "message": "Rate limit exceeded"})
            
            print("Setting last generated")
            system_data[0].last_generated = datetime.datetime.now().replace(tzinfo=None).timestamp()
            system_data[0].save()
            print("Set last generated")
            print("Creating job with id " + id_from_url(video_url))
            job = Job.objects.create(
                job_id = id_from_url(video_url).strip(" "),
                video_url=video_url,
                created = datetime.datetime.now().replace(tzinfo=None).timestamp()
            )
            print("Created job")
            print("Saving job")
            job.save() # The script will continue running below
            print("Done")

        # job, created = Job.objects.get_or_create(id=id_from_url(video_url))  
        
        # if (not created) and (datetime.datetime.now().replace(tzinfo=None).timestamp() - job.created.replace(tzinfo=None).timestamp() >= 60 * 60) or job.video_url == "": # Reset old jobs
        #     job.delete()
        #     job, created = Job.objects.get_or_create(id=id_from_url(video_url))

        # if created:
        #     if rate_limited:
        #         return JsonResponse(data={"code": 400, "message": "Rate limit exceeded"})
            
        #     system_data[0].last_generated = datetime.datetime.now().replace(tzinfo=None).timestamp()
        #     system_data[0].save()

        #     job.video_url = video_url
        #     job.percent_completed = 0
        #     job.finished = False
        #     job.created = datetime.datetime.now()
        #     job.save()
        # else:
        #     return JsonResponse(data={"code": 200, "message": id_from_url(video_url)})

        def run():
            def progress_callback(chunk, max_chunks):
                job.percent_completed = round(chunk / max_chunks * 100)
                job.chunks_completed = chunk
                job.total_chunks = max_chunks
                job.save()
            
            answers, transcript = yt_transcriptor.run(video_url, language, callback=progress_callback)
            print(answers, transcript)
            # Save to database
            kafka, created = Kafka.objects.get_or_create(video_url=video_url)

            if created:
                kafka.timestamp=datetime.datetime.now().replace(tzinfo=None).timestamp()
            
            kafka.answers = answers
            kafka.transcript = transcript
            kafka.language = language
            kafka.video_info = json.loads(video_info)
            
            kafka.save()

            job.percent_completed = 100
            job.chunks_completed = job.total_chunks
            job.finished = True
            job.save()

            if not runbackground:
                response["code"] = 200
                response["message"] = "OK"
                response["data"] = {
                    "answers": answers,
                    "transcript": transcript,
                    "language": language,
                    "video_info": kafka.video_info,
                    "video_url": video_url,
                }

            
                return JsonResponse(data=response)
        
        if runbackground:
            daemon = threading.Thread(target=run, daemon=True)

            daemon.start()

            return JsonResponse(data={"code": 200, "message": id_from_url(video_url)})
        else:
            return run()
        
    except Exception as e:
        print(e)

        try:
            job.delete()
        except:
            pass

        response["code"] = 500
        response["message"] = "Internal server error"

        return JsonResponse(data=response)


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
            "video_info": kafka.video_info,
            "video_url": video_url,
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
    if request.method != "GET":
        return HttpResponse("Bad request")

    response = {"code": 200, "message": "OK", "list": {}}

    try:
        for kafka in Kafka.objects.all():
            response["list"][kafka.video_url] = {
                "answers": kafka.answers,
                "transcript": kafka.transcript,
                "language": kafka.language,
                "video_info": kafka.video_info,
                "video_url": kafka.video_url,
            }
    except Exception as e:
        print(e)
        response["code"] = 500
        response["list"] = {}
        response["message"] = "Internal server error"

    return JsonResponse(data=response)

def kafka_answer(request, subdomain):
    video_url = request.GET.get("video_url")
    language = request.GET.get("language")

    if not video_url:
        return HttpResponse("Bad request") # Not returning JSON to prevent bots
    
    if not language:
        language = "cs-CZ"

    video_url = video_url.replace("\"", "").strip(" ")

    return generate_answers(video_url, language)

def kafka_job(request, subdomain):
    if request.method == "GET":
        job_id = request.GET.get("id").strip(" ")

        if not job_id:
            return HttpResponse("Bad request")
        
        try:
            job = Job.objects.get(job_id=job_id.strip(" "))

            return JsonResponse(data={
                "video_url": job.video_url,
                "percent_completed": job.percent_completed,
                "chunks_completed": job.chunks_completed,
                "total_chunks": job.total_chunks,
                "finished": job.finished,
            })
        except Job.DoesNotExist:
            return HttpResponse("Job not found")
        except Exception as e:
            print("Error: " + e)
            return HttpResponse("Internal server error")
