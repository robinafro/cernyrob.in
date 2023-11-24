from .models import UserProfile, AnonymousUserProfile

def get_profile(request):
    if request.user.is_authenticated:
        return UserProfile.objects.get_or_create(user=request.user)
    else:
        #TODO: fix this being called even when the user seems to be authenticated
        session_key = request.session.session_key

        if not session_key:
            request.session.save()
            session_key = request.session.session_key

        return AnonymousUserProfile.objects.get_or_create(session_key=session_key)

def get_all_profiles():
    return UserProfile.objects.all()

def get_data(user_profile, scope):
    if scope:
        try:
            data = {
                "data": getattr(user_profile, scope),
                "username": user_profile.user.username,
            }

            return data
        except AttributeError:
            return None
    else:
        return user_profile.user.username