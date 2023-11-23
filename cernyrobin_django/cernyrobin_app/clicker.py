from cernyrobin_app.models import UserProfile

# todo:
# for the temporary login system, make it so that temporary accounts start with !temp_ followed by a UUID
# temporary accounts will be created when a user accesses a page that would normally require a login
# when a user tries to login/register, if they are on a temporary account, the account will be renamed to the username they enter

def add_click(request):
    user_profile = UserProfile.objects.get(user=request.user)

    user_profile.clicks += user_profile.clicks_mult

    user_profile.save()