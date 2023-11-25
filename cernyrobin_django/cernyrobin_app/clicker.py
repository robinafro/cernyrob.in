from django.http import HttpResponse
from . import profile_operations
import json

def add_click(request):
    user_profile, created = profile_operations.get_profile(request)
    
    clicker_data = user_profile.get_robin_clicker()
    
    if clicker_data["clicks_mult"] == 0:
        clicker_data["clicks_mult"] = 1

    clicker_data["clicks"] += clicker_data["clicks_mult"]

    user_profile.set_robin_clicker(clicker_data)

    user_profile.save()

    return HttpResponse(clicker_data["clicks"])