from django.http import HttpResponse
from . import profile_operations

def add_click(request):
    user_profile, created = profile_operations.get_profile(request)
    print("Created" if created else "Not created")
    print(user_profile.robin_clicker["clicks"])
    clicker_data = user_profile.robin_clicker
    
    if clicker_data["clicks_mult"] == 0:
        clicker_data["clicks_mult"] = 1
    print("Adding clicks for user " + user_profile.user.username)
    clicker_data["clicks"] += clicker_data["clicks_mult"]

    user_profile.save()
    request.user.save()

    return HttpResponse(clicker_data["clicks"])