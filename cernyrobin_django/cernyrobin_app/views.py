from django.shortcuts import render
from . import clicker
from . import profile_operations
from django.shortcuts import render, redirect
from django.http import HttpResponse
from django.http import JsonResponse
from django.db.models import Q
from django.contrib.auth.decorators import login_required
from django.contrib.auth.forms import UserCreationForm
from cernyrobin_app.models import UserProfile
from django.contrib.auth.models import User
from django.contrib.auth.models import AnonymousUser
from django.contrib import messages
from django.contrib.auth import authenticate, login, logout
from django.core.serializers import serialize
from django.db.models import IntegerField
from django.db.models.fields.related import ForeignKey
from api import captcha
from api import send_mail

import json, re, shortuuid, datetime

# Utils
def go_back(request):
    next_url = request.POST.get("next", request.GET.get("next", ""))
    response_data = {"redirect_url": next_url}

    return JsonResponse(response_data) if next_url else HttpResponse("200 OK")

def get_user(request):
    try:
        user = UserProfile.objects.get_or_create(user=request.user)[0]
    except Exception as e:
        user = None

    return user or request.user

# Pages

def home(request):
    context = {
        "current_user" : request.user,
        "cernyrobin_user": get_user(request),
    }

    return render(request, "cernyrobin/home.html", context)


def clicker_page(request):
    context = {
        "current_user" : request.user,
        "cernyrobin_user": get_user(request),
    }

    return render(request, "cernyrobin/clicker.html", context)


def login_page(request):
    context = {
        "current_user" : request.user,
        "cernyrobin_user": get_user(request),
    }

    return render(request, "cernyrobin/login.html", context)
def account(request):
    if request.user.is_authenticated:

        context = {
            "current_user" : request.user,
            "cernyrobin_user": get_user(request),
        }
        return render(request, "cernyrobin/account.html", context)
    return redirect("login")

# API
def login_submit(request):
    if request.method == "POST":
        username = request.POST.get("username")
        password = request.POST.get("password")

        # add checks for username and password format
        if not username or not password:
            return HttpResponse("400 Bad Request")
        elif len(username) > 30 or len(password) > 30:
            return HttpResponse("400 Bad Request")
        elif len(username) < 3 or len(password) < 3:
            return HttpResponse("400 Bad Request")
        elif not username.isalnum() or not password.isalnum():
            return HttpResponse("400 Bad Request")

        try:
            user = User.objects.get(username=username.lower())
        except User.DoesNotExist:
            prevData = None
            if request.user.is_authenticated or request.user.is_anonymous:
                if request.user.is_anonymous:
                    current_profile, created = profile_operations.get_profile(request)
                    prevData = current_profile.get_robin_clicker()

                logout(request)

            user = User.objects.create_user(username=username, password=password)
            user_profile = UserProfile.objects.create(user=user)

            if prevData:
                user_profile.robin_clicker = json.dumps(prevData)

            user_profile.save()
            user.save()

            login(request, user)

            return go_back(request)

        if user.check_password(password):
            user = authenticate(request, username=username, password=password)

            if user is not None:
                login(request, user)

                return go_back(request)
            else:
                return HttpResponse("401 Unauthorized")
        else:
            return HttpResponse("401 Unauthorized")
    else:
        return HttpResponse("405 Method Not Allowed")


def add_click(request):
    if request.method == "POST":
        return clicker.add_click(request)
    else:
        return HttpResponse("405 Method Not Allowed")


def get_user_data(request):
    if request.method == "GET":
        scope = request.GET.get("scope")

        user_profile, created = profile_operations.get_profile(request)

        data = profile_operations.get_data(user_profile, scope)

        if data:
            return JsonResponse(data=data, safe=False)
        else:
            return HttpResponse("400 Bad Request")
    else:
        return HttpResponse("405 Method Not Allowed")


def get_all_data(request):
    if request.method == "GET":
        scope = request.GET.get("scope")

        if not scope:
            return HttpResponse("400 Bad Request")

        all_user_profiles = profile_operations.get_all_profiles()

        all_users_data = []

        for user_profile in all_user_profiles:
            user_data = profile_operations.get_data(user_profile, scope)

            if not user_data:
                continue

            all_users_data.append(user_data)

        return JsonResponse(data=all_users_data, safe=False)
    else:
        return HttpResponse("405 Method Not Allowed")
def new_login(request):
    page = "login"
    if request.user.is_authenticated:
        return redirect("home")
    else:
        if request.method == "POST":
            username = request.POST.get("username")
            password = request.POST.get("password")

            if username == "" or password == "":
                messages.error(request, "Username or password is empty")
                return redirect("new_login")
        
            username = username.lower()

            next_page = request.POST.get("next")

            try:
                user = User.objects.get(username=username)

            except:
                return  HttpResponse("username not found")

            user = authenticate(request, username=username, password=password)
            if user is not None:
                login(request, user)
                return redirect(next_page or "home")
            else:
                messages.error(request, "Password wrong")

    context = {
        "page": page,
    }
    return render(request, "cernyrobin/new_login.html", context)
def new_register(request):
    if request.method == "POST":
        form = UserCreationForm(request.POST)
        if form.is_valid():
            user = form.save(commit=False)
            user.username = user.username.lower()
            user.save()

            #! Create UserProfile
            user_profile = UserProfile.objects.create(user=user)

            if re.match(r"\w+\.[\w]{2,4}\.2[\d]{3}@skola\.ssps\.cz", request.POST.get("email") or "") or request.POST.get("email") or "" == "actulurus@gmail.com":
                user_profile.email = request.POST.get("email") or ""

            user_profile.save()

            login(request, user)

            if (request.POST.get("email") or "") == "":
                return redirect("home")
            else:
                return redirect("verify_page")
        else:
            messages.error(request, "error happened")
    page = "register"
    form = UserCreationForm()
    context = {"page": page, "form": form}
    return render(request, "cernyrobin/new_register.html", context)

user_captchas = {}
user_captcha_images = {}
verification_codes = {}

def get_current_school_year():
    now = datetime.datetime.now()

    if now.month >= 9:
        return now.year
    else:
        return now.year - 1
    
def email_sent(request):
    return render(request, "cernyrobin/email_sent.html")

def verify_submit(request):
    if not request.user.is_authenticated:
        return HttpResponse("401 Unauthorized")
    
    entered_captcha = request.POST.get("captcha")

    if entered_captcha.strip() == user_captchas[request.user.username]:
        password = request.POST.get("password")

        if not request.user.check_password(password):
            return HttpResponse("401 Unauthorized")
        
        email = request.POST.get("email")

        if not email:
            return HttpResponse("400 Bad Request")
        
        if not re.match(r"\w+\.[\w]{2,4}\.2[\d]{3}@skola\.ssps\.cz", email) and email != "actulurus@gmail.com": # There might be an issue with the escape characters near the dots. Look into this first if the verification seems to be broken.
            return HttpResponse("400 Bad Request")
    
        #! Check if the email is already being used
        for user in UserProfile.objects.all():
            if user.email == email and user.email_verified:
                return HttpResponse("Email is already being used")
        
        cernyrobin_user, created = UserProfile.objects.get_or_create(user=request.user)

        cernyrobin_user.email = email

        cernyrobin_user.save()

        code = shortuuid.uuid()
        
        verification_codes[code] = request.user.username

        user_captchas.pop(request.user.username)
        user_captcha_images.pop(request.user.username)

        #! Send email with code
        send_mail.verify_mail(email, request.user.username, code)

        return redirect("email_sent")
    else:
        return HttpResponse("Invalid captcha")

def verify_code(request):
    if request.method == "GET" and request.user.is_authenticated:
        cernyrobin_user, created = UserProfile.objects.get_or_create(user=request.user)
        code = request.GET.get("code")

        print(cernyrobin_user.email_verified)

        if not code:
            return HttpResponse("400 Bad Request")
        
        if code not in verification_codes:
            return HttpResponse("Invalid code")
        
        username = verification_codes[code]

        if request.user.username != username:
            return HttpResponse("401 Unauthorized")

        cernyrobin_user.email_verified = True

        cernyrobin_user.save()

        print(cernyrobin_user.email_verified)

        del verification_codes[code]

        return HttpResponse("200 OK")
    elif not request.user.is_authenticated:
        return HttpResponse("401 Unauthorized")
    
    return HttpResponse("What?")

def verify_account_page(request):
    context = {
        "current_user" : request.user,
        "cernyrobin_user": get_user(request),
    }

    # if request.user.email_verified:
    #     return HttpResponse("Already verified")

    if request.method == 'POST':
        if not request.user.is_authenticated:
            return HttpResponse("401 Unauthorized")
        
        return verify_submit(request)
    else:
        image, correct = captcha.gen_captcha()

        user_captchas[request.user.username] = correct
        user_captcha_images[request.user.username] = image

        return render(request, "cernyrobin/verify-page.html", context)
    
def get_captcha_image(request):
    return HttpResponse(user_captcha_images[request.user.username], content_type="image/png")

def simulate_redirect(request):
    context = {
        "target_url" : "https://status.stuckinvim.com"
    }
    return render(request, "global/redirecting.html", context)
def manifest(request):
    context = {}
    return render(request, 'global/manifest.json', context, content_type='application/json')