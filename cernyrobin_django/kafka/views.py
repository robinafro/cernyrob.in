from django.shortcuts import render, redirect
from django.http import HttpResponse, JsonResponse

from cernyrobin_app.models import UserProfile
from api.models import Kafka
from api import get_video_info
from api import views as api_views
from ads import views as ads_views
from kafka.history_quiz import quiz
import json
import re
from django.views.decorators.csrf import csrf_exempt

MAX_COMMENTS_PER_USER = 50

def get_user(request):
    try:
        user = UserProfile.objects.get_or_create(user=request.user)[0]
    except Exception as e:
        user = None

    return user or request.user

def strip_yapping(s):
    for i, char in enumerate(s):
        if char.isdigit():
            return s[i:]
    return s

def parse_numbered_text_old(text):
    segments = re.split(r'(\d+\.)', text)

    extracted_parts = []
    last_number = 0
    current_part = ''

    for segment in segments:
        if re.match(r'(\d+\.)', segment):
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

def parse_numbered_text(text):
    all_that_match = re.findall(r'(?:\A|\n)\d+\. [^\n]+', text)

    processed = []

    for i, match in enumerate(all_that_match):
        digit = int(match.split(".")[0])
        next_digit = int(all_that_match[i + 1].split(".")[0]) if i + 1 < len(all_that_match) else None

        if (next_digit or 999) > digit:
            processed.append(match)

    return processed

def index(request):
    filter = (request.GET.get("search") or "").lower()

    all_videos = api_views.get_all_to_be_displayed()

    context = ads_views.get_ads(length=len(all_videos))
    context["videos"] = []

    for video in all_videos:
        try:
            kafka_obj = Kafka.objects.get(video_url="https://www.youtube.com/watch?v=" + video["video_id"])
        except Kafka.DoesNotExist:
            kafka_obj = None

        if filter in video["title"].lower() or filter in video["description"].lower() or filter in kafka_obj.transcript.lower() or filter in kafka_obj.answers.lower() or filter == "":
            context["videos"].append(
                {
                    "title": video["title"],
                    "video_id": video["video_id"],
                    # "description": video["description"],
                    "questions" : parse_numbered_text(strip_yapping(video["description"])),
                }
            )

    context["videos"] = context["videos"][::-1]

    context["recent_video"] = api_views.get_recent_video()
    context["current_user"] = request.user
    context["cernyrobin_user"] = get_user(request)
    context["logged_in"] = request.user.is_authenticated

    return render(request, "kafka/index.html", context)


def view(request, is_custom=False):
    if request.method == "GET":
        id = request.GET.get("id").strip(" ")

        if id is None:
            return HttpResponse("Invalid video ID")

        video_url = "https://www.youtube.com/watch?v=" + id

        video_info = json.loads(get_video_info.get_video_info(video_url))

        answers = api_views.get_answers(video_url, request.user, is_custom).strip()
        transcript = api_views.get_transcript(video_url).strip()

        ads = ads_views.get_ads(length=2)


        parsed_questions = parse_numbered_text(strip_yapping(video_info["description"]))
        parsed_answers = parse_numbered_text(strip_yapping(answers))
        qa_pairs = zip(parse_numbered_text(strip_yapping(video_info["description"])), parse_numbered_text(strip_yapping(answers)))

        i = 1
        qa_pairs_list_form = []
        for question, answer in qa_pairs:
            qa_pairs_list_form.append([i, question, answer])
            i=+1

        comments = []

        if not is_custom:
            comments = api_views.get_comments(video_url)
            comments.reverse()

        return render(
            request,
            "kafka/view.html",
            context={
                "title": video_info["title"],
                "video_url": video_url,
                "video_id": id,
                "video_title" :video_info["title"],
                "summary": api_views.get_summary(video_url),
                "qa_pairs" : qa_pairs,
                "answers_copy": answers,
                "transcript": transcript,
                "ads_left": ads["ads_left"],
                "ads_right": ads["ads_right"],
                "is_staff" : request.user.is_staff,
                "current_user" : request.user,
                "cernyrobin_user": get_user(request),
                "is_custom" : is_custom,
                "qa_pairs_indexed" : qa_pairs_list_form,
                "color": api_views.get_color(video_url),
                "comments": comments,
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

def view_custom(request):
    return view(request, is_custom=True)

def submit(request):
    if request.method == "GET":
        return render(
            request,
            "kafka/submit.html",
            context={
                "last_generated": api_views.get_last_generated(),
                "generate_rate_limit": api_views.GENERATE_RATE_LIMIT,
                "current_user" : request.user,
                "cernyrobin_user": get_user(request),
            },
        )
    elif request.method == "POST":
        if not get_user(request.user).email_verified:
            return JsonResponse({"code": 418, "message": "Nemáš verifikovaný email"})
        
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

        response = api_views.generate_answers(video_url, "cs-CZ", runbackground=True, submitter=request.user)

        return response

def regenerate(request):
    if request.method == "POST" and request.user.is_authenticated:
        # Check if the user has a verified email
        if not (UserProfile.objects.get(user=request.user)).email_verified:
            return HttpResponse("403 Forbidden")
        
        video_url = request.POST.get("video_url")

        if video_url is None:
            return JsonResponse({"code": 400, "message": "Invalid video URL"})

        video_id = None
        if video_url.find("watch?v=") != -1:
            video_id = video_url.split("v=")[1]
        elif video_url.find("youtu.be/") != -1:
            video_id = video_url.split("youtu.be/")[1]
        else:
            video_id = video_url

        if video_id is None:
            return JsonResponse({"code": 400, "message": "Invalid video URL"})
        
        if video_id.find("&") != -1:
            video_id = video_id.split("&")[0]
        elif video_id.find("?") != -1:
            video_id = video_id.split("?")[0]

        # video_url = "https://www.youtube.com/watch?v=" + video_id

        # response = api_views.generate_answers(video_url, "cs-CZ", runbackground=True, user=request.user)

        return api_views.regenerate_answers(request, video_id)
    
# def comment(request):
#     if request.method == "POST":
#         video_url = request.POST.get("video_url")
#         comment = request.POST.get("comment")

#         if video_url is None or comment is None:
#             return JsonResponse({"code": 400, "message": "Invalid video URL or comment"})

#         video_id = None
#         if video_url.find("watch?v=") != -1:
#             video_id = video_url.split("v=")[1]
#         elif video_url.find("youtu.be/") != -1:
#             video_id = video_url.split("youtu.be/")[1]
#         else:
#             video_id = video_url

#         if video_id is None:
#             return JsonResponse({"code": 400, "message": "Invalid video URL"})

#         if video_id.find("&") != -1:
#             video_id = video_id.split("&")[0]
#         elif video_id.find("?") != -1:
#             video_id = video_id.split("?")[0]

#         video_url = "https://www.youtube.com/watch?v=" + video_id

#         response = api_views.comment(video_url, comment, request.user, "kafka")

#         return response
    
def test_view_comments(request):
    if request.method == "GET":
        video_id = request.GET.get("video_url")
        video_url = ("https://www.youtube.com/watch?v=" + video_id).strip()

        comments = api_views.get_comments(video_url)

        print(video_url)
        print(comments)

        return render(
            request,
            "kafka/test_view_comments.html",
            context={
                "comments": comments,
                "current_user" : request.user,
                "cernyrobin_user": get_user(request),
            },
        )

def comment(request):
    if request.method == "POST":
        if request.user.is_anonymous:
            return JsonResponse({"code": 403, "message": "Forbidden"})
        
        cernyrobin_user = get_user(request)

        if not cernyrobin_user.email_verified:
            return JsonResponse({"code": 403, "message": "Forbidden"})
        
        video_url = request.POST.get("video_url")
        comment = request.POST.get("comment")

        if video_url is None or comment is None:
            return JsonResponse({"code": 400, "message": "Invalid video URL or comment"})

        video_id = None
        if video_url.find("watch?v=") != -1:
            video_id = video_url.split("v=")[1]
        elif video_url.find("youtu.be/") != -1:
            video_id = video_url.split("youtu.be/")[1]
        else:
            video_id = video_url

        if video_id is None:
            return JsonResponse({"code": 400, "message": "Invalid video URL"})

        if video_id.find("&") != -1:
            video_id = video_id.split("&")[0]
        elif video_id.find("?") != -1:
            video_id = video_id.split("?")[0]

        video_url = "https://www.youtube.com/watch?v=" + video_id
       
        comments_from_this_user = 0
        comments = api_views.get_comments(video_url)

        for _comment in comments:
            if _comment["user"] == request.user.username:
                comments_from_this_user += 1

        if comments_from_this_user >= MAX_COMMENTS_PER_USER:
            return JsonResponse({"code": 403, "message": "Forbidden"})
        
        anonymous = request.POST.get("anonymous", "off") == "on"

        response = api_views.comment(video_url, comment, request.user, anonymous, "kafka")

        return redirect("/kafka/view?id=" + video_id)
    else:
        # render template
        return render(
            request,
            "kafka/test_comment.html",
            context={
                "current_user" : request.user,
                "cernyrobin_user": get_user(request),
            },
        )
    
def subscribe(request):
    if request.method == "POST":
        if request.user.is_anonymous:
            return JsonResponse({"code": 403, "message": "Forbidden"})
        
        profile = get_user(request)

        if not profile.email_verified:
            return JsonResponse({"code": 403, "message": "Forbidden"})
        
        subscribed = request.POST.get("subscribed") == "on"

        # print(subscribed)

        profile.email_subscribed = subscribed
        profile.save()

        return redirect("/account/")
    
def quiz_info(request):
    topic = request.GET.get("topic")

    if topic:
        return JsonResponse({"course_name": quiz.get_courses(id=topic)})
    else:
        courses = quiz.get_courses()
        context = {"courses": courses}

        return render(request, "kafka/quiz_info.html", context)

def quiz_play(request):
    context = {"topic": request.GET.get("topic", "0")}
    return render(request, "kafka/quiz.html", context)

def quiz_get_questions(request):
    questions = quiz.get_questions(request.GET.get("topic", "0"))

    return JsonResponse({"questions": questions})

# @csrf_exempt
def quiz_evaluate(request):
    questions_answers = json.loads(request.POST.get("questions_answers"))

    id = request.POST.get("topic")

    course = quiz.get_courses(id=id)

    similarities = {}
    score = 0
    total = 0

    for question, answer in questions_answers.items():
        similarity = quiz.get_similarity(course, question, answer)

        similarities[question] = similarity
        
        if similarity > 0:
            score += similarity * 100
            total += similarity

    average = total / len(questions_answers)

    return JsonResponse({"similarities": similarities, "score": score, "result": average})
    
def quiz_dummy(request):
    return render(request, "kafka/quiz_dummy.html")
