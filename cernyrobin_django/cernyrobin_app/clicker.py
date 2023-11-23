from django.http import HttpResponse
from . import get_profile

def add_click(request):
    user_profile, created = get_profile.get_profile(request)
    print(user_profile.clicks_mult)

    if user_profile.clicks_mult == 0:
        user_profile.clicks_mult = 1

    user_profile.clicks += user_profile.clicks_mult

    user_profile.save()

    return HttpResponse(user_profile.clicks)