import cernyrobin_app.get_profile

def add_click(request):
    user_profile = get_profile(request.user)
    
    user_profile.clicks += user_profile.clicks_mult

    user_profile.save()

    return HttpResponse("user_profile.clicks")