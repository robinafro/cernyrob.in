from django.shortcuts import render
from django.http import HttpResponse, JsonResponse
from django.shortcuts import redirect
from api.models import System, Kafka, Job

from api.yt_transcriptor import main as yt_transcriptor
from api import get_video_info
from api.paraphraser import main as paraphraser
from cernyrobin_app.models import UserProfile
import api.send_mail as send_mail

import datetime, json, re, threading, dotenv, os, docx, shortuuid

try:
    dotenv.load_dotenv()
except Exception as e:
    print("Failed to load dotenv file. This should only happen in a docker container!")
    print(e)

GENERATE_RATE_LIMIT = 60 * 60 #60 * 60 * 24 * 7 - 60 * 60 * 6 # 7 days minus six hours to prevent it from shifting too far forward
KAFKA_CHANNEL = "https://www.youtube.com/@jankafka1535"
DESCRIPTION_FORMAT = r".*/s(?:\s+\d+.\s+.*?)+(?=\n\n|\Z)" #r"\d+\.\s(?:.+?\?)" # chatgpt

if os.getenv("NORATELIMIT") == "1":
    GENERATE_RATE_LIMIT = 0

def strip_yapping(s):
    for i, char in enumerate(s):
        if char.isdigit():
            return s[i:]
    return s

def parse_numbered_text(text):
    all_that_match = re.findall(r'(?:\A|\n)\d+\. [^\n]+', text)

    processed = []

    for i, match in enumerate(all_that_match):
        digit = int(match.split(".")[0])
        next_digit = int(all_that_match[i + 1].split(".")[0]) if i + 1 < len(all_that_match) else None

        if (next_digit or 999) > digit:
            processed.append(match)

    return processed

def strip_number(arr):
    new_arr = []

    for line in arr:
        digit_count = 0
        for char in line:
            if char.isdigit(): 
                digit_count += 1
            else:
                break

        new_line = line[(digit_count + 2):]

        new_arr.append(new_line)

    return new_arr

def modify_questions(video_url, questions):
#    print(video_url)
    kafka = Kafka.objects.get(video_url=video_url)
#    print(kafka)
    kafka.answers = questions
#    print(kafka.answers)
    kafka.save()

    return "Success"

def get_answers(video_url, user, is_custom):
    try:
        kafka = Kafka.objects.get(video_url=video_url)

        if user.is_anonymous or kafka.custom_answers == "":
            return kafka.answers or "Unable to get answers"
        else:
            try:
                custom_answers = json.loads(kafka.custom_answers)

                if is_custom:
                    return custom_answers.get(user.username) or "Unable to get answers"
                else:
                    return kafka.answers or "Unable to get answers"
            except Exception as e:
                print("-"*60)
                print(e)
                print("-"*60)
                print("The error above is not fatal, but custom generated answers will not be used (either an error or there aren't any yet).") # At se vitek neboji tracebacku lol
                print("-"*60)

                return kafka.answers or "Unable to get answers"
            
    except Kafka.DoesNotExist:
        return "Unable to get answers"


def get_color(video_url):
    try:
        kafka = Kafka.objects.get(video_url=video_url)

        return kafka.color or "#000000"
    except Kafka.DoesNotExist:
        return "Unable to get color"
    
def get_summary(video_url):
    try:
        kafka = Kafka.objects.get(video_url=video_url)

        return kafka.summary or "Unable to get summary"
    except Kafka.DoesNotExist:
        return "Unable to get summary"
    
def get_recent_video():
    try:
        return Kafka.objects.filter(video_info__isnull=False).latest("timestamp").video_url
    except Kafka.DoesNotExist:
        return ""
    
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

def generate_answers(video_url, language, user=None, runbackground=False, submitter=None):
    video_url = video_url.strip(" ")
    
    response = {"code": 200, "message": "OK"}

    video_info = get_video_info.get_video_info(video_url)

    if video_info is None:
        return JsonResponse(data={"code": 400, "message": "Video not found"})
    
    if json.loads(video_info)["author_url"] != KAFKA_CHANNEL:
        return JsonResponse(data={"code": 400, "message": "Invalid video channel"})
    
    regexp = re.compile(r'\n|^\d. ?[\w,?\s\?]+')
    
    if regexp.search(json.loads(video_info)["description"]) is None:
        return JsonResponse(data={"code": 400, "message": "Invalid video description"})

    try:
        # Always use a rate limit when dealing with OpenAI API requests!
        print("Creating system data")
        system_data = System.objects.get_or_create(key="SYSTEM_DATA")
        print("Created system data")
        
        if not system_data[0].last_generated:
            system_data[0].last_generated = datetime.datetime.now().replace(tzinfo=None).timestamp()
            system_data[0].save()
        
        job_id = id_from_url(video_url)

        if user is not None:
            job_id += user.username

        try:
            print("Getting kafka object")
            print("video_url", video_url)
            kafka = Kafka.objects.get(video_url=video_url)

            if kafka is not None:
                print("Would redirect user to the page now")
                # return redirect(f"/kafka/view/?id={id_from_url(video_url)}")

            custom_answers = json.loads(kafka.custom_answers) if kafka.custom_answers else None

            if custom_answers is not None and user is not None and custom_answers.get(user.username):
                response["code"] = 429
                response["message"] = "Already generated for user"

                return JsonResponse(data=response)

            # if custom_answers is None or custom_answers.get(user.username):
            #     if kafka.video_info is None or kafka.video_info == {} or kafka.video_info is {}:
            #         kafka.video_info = json.loads(video_info)

            #     response["code"] = 201
            #     response["message"] = job_id
            #     # response["data"] = {
            #     #     "answers": kafka.answers,
            #     #     "transcript": kafka.transcript,
            #     #     "language": language,
            #     #     "video_info": (kafka.video_info),
            #     #     "video_url": video_url,
            #     # }

            #     return JsonResponse(data=response)
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
            job = Job.objects.get(job_id=job_id.strip(" "))
            
            job_already_exists = True
        except Exception as e:
            print(e)
            job = None

        # Make the job expire
        if job_already_exists and (datetime.datetime.now().replace(tzinfo=None).timestamp() - job.created >= 60 * 45 or job.video_url == ""): # Reset old jobs
            job.delete()

            job_already_exists = False
            
        if job_already_exists:
            print("already exists")
            return JsonResponse(data={"code": 200, "message": job_id})
        else:
            if rate_limited:
                return JsonResponse(data={"code": 400, "message": "Rate limit exceeded"})
            
            print("Setting last generated")
            system_data[0].last_generated = datetime.datetime.now().replace(tzinfo=None).timestamp()
            system_data[0].save()
            print("Set last generated")
            print("Creating job with id " + job_id)
            job = Job.objects.create(
                job_id = job_id.strip(" "),
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
            
            is_regen = user is not None

            kafka = None
            try:
                kafka = Kafka.objects.get(video_url=video_url)
            except Kafka.DoesNotExist:
                kafka = None

            if kafka is not None and not is_regen:
                job.percent_completed = 100
                job.chunks_completed = job.total_chunks
                job.finished = True
                job.save()

                return

            answers, transcript, summary, color = yt_transcriptor.run(video_url, language, callback=progress_callback, ignore_existing=True, is_regen=is_regen)
            
            # Save to database
            kafka, created = Kafka.objects.get_or_create(video_url=video_url)

            if created:
                kafka.timestamp=datetime.datetime.now().replace(tzinfo=None).timestamp()
            
            if user is None:
                kafka.answers = answers
                kafka.transcript = transcript
                kafka.summary = summary
                kafka.language = language
                kafka.video_info = json.loads(video_info)

                if color is not None:
                    kafka.color = color
                else:
                    kafka.color = "#221fc7"
            else:
                try:
                    custom_answers = json.loads(kafka.custom_answers)
                except:
                    custom_answers = {}

                custom_answers[user.username] = answers

                kafka.custom_answers = json.dumps(custom_answers)
            
            kafka.save()

            job.percent_completed = 100
            job.chunks_completed = job.total_chunks
            job.finished = True
            job.save()

            # Broadcast to mailing list
            if not is_regen:
                print("&&Would send mail now")

            # if not is_regen:
            #     try:
            #         email = UserProfile.objects.get(user=submitter).email
                    
            #         year = email.split("@")[0].split(".")[-1]
                    
            #         all_users = UserProfile.objects.filter(email_verified=True)

            #         send_to = []

            #         for usr in all_users:
            #             if year in usr.email and usr.email_subscribed == True:
            #                 send_to.append(usr.email)

            #         if len(send_to) > 0:
            #             filename = "odpovedi.docx"
            #             dirname = shortuuid.uuid()[:8]

            #             os.makedirs(f"/tmp/{dirname}", exist_ok=True)

            #             doc = docx.Document()
            #             doc.add_paragraph(answers)
            #             doc.save(f"/tmp/{dirname}/" + filename)

            #             send_mail.broadcast_mail(send_to, file_path=f"/tmp/{dirname}/" + filename)

            #             # os.remove(f"/tmp/{dirname}/" + filename)
            #             # os.rmdir(f"/tmp/{dirname}")
                            
            #     except Exception as e:
            #         print(e)
            #         pass


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

            return JsonResponse(data={"code": 200, "message": job_id})
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

def regenerate_answers(request, video_id):
    if not request.user.is_authenticated or not UserProfile.objects.get(user=request.user).email_verified:
        return JsonResponse({"code": 403, "message": "Forbidden"})
    
    video_url = "https://www.youtube.com/watch?v=" + video_id
    job_id = video_id + request.user.username

    kafka = None

    if Kafka.objects.filter(video_url=video_url).exists():
        kafka = Kafka.objects.get(video_url=video_url)
    else:
        return JsonResponse({"code": 404, "message": "Not found"})

    if Job.objects.filter(job_id=job_id).exists():
        # Expire if its too old
        job = Job.objects.get(job_id=job_id)

        if (datetime.datetime.now().replace(tzinfo=None).timestamp() - job.created >= 60 * 0.1 or job.video_url == ""):
            job.delete()
        else:
            return JsonResponse({"code": 400, "message": "Job already exists"})
    
    job = Job.objects.create(
        job_id = job_id.strip(" "),
        video_url=video_url,
        created = datetime.datetime.now().replace(tzinfo=None).timestamp()
    )

    def run():
        current_answers = kafka.answers

        custom_answers = paraphraser.get_paraphrase(current_answers)

        try:
            kafka_custom_answers = json.loads(kafka.custom_answers)
        except:
            kafka_custom_answers = {}

        kafka_custom_answers[request.user.username] = custom_answers

        kafka.custom_answers = json.dumps(kafka_custom_answers)

        kafka.save()

        job.percent_completed = 100
        job.finished = True

        job.save()

    daemon = threading.Thread(target=run, daemon=True)

    daemon.start()

    return JsonResponse(data={"code": 200, "message": job_id})

def kafka(request, subdomain):
    return HttpResponse("Hello, world. You're at the api index.")

def kafka_get(request, subdomain):
    response = {"code": 200, "message": "OK"}

    video_url = request.GET.get("video_url")

    if not "=" in video_url or not "/" in video_url: # Lmao
        video_url = "https://www.youtube.com/watch?v=" + video_url

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
            "list_answers": strip_number(parse_numbered_text(strip_yapping(kafka.answers))),
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

    if not "=" in video_url or not "/" in video_url: # Lmao
        video_url = "https://www.youtube.com/watch?v=" + video_url

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
                "status": "OK",
                "video_url": job.video_url,
                "percent_completed": job.percent_completed,
                "chunks_completed": job.chunks_completed,
                "total_chunks": job.total_chunks,
                "finished": job.finished,
            })
        except Job.DoesNotExist:
            return JsonResponse(data={"status": "Error", "message": "Job not found"})
        except Exception as e:
            print("Error: " + e)
            return JsonResponse(data={"status": "Error", "message": "Internal server error"})

def get_comments(video_url):
    # print(video_url)
    try:    
        kafka = Kafka.objects.get(video_url=video_url)
        # print(kafka.comments)
        return json.loads(kafka.comments) if kafka.comments else []
    except Exception as e:
        print(e)
        return []

def comment(video_url, comment, user, anonymous, type):
    # print(type)
    if type == "kafka":
        try:
            kafka = Kafka.objects.get(video_url=video_url)

            comments = json.loads(kafka.comments) if kafka.comments else []

            comments.append({
                "user": "Anonymous" if anonymous else user.username,
                "message": comment,
                "timestamp": datetime.datetime.now().replace(tzinfo=None).timestamp()
            })

            kafka.comments = json.dumps(comments)

            kafka.save()

            return JsonResponse({"code": 200, "message": "OK"})
        except Kafka.DoesNotExist:
            return JsonResponse({"code": 404, "message": "Not found"})
        except Exception as e:
            print(e)
            return JsonResponse({"code": 500, "message": "Internal server error"})