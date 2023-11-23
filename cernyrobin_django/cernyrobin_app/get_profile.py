from .models import UserProfile, AnonymousUserProfile

def get_profile(request):
    if request.user.is_authenticated:
        return UserProfile.objects.get_or_create(user=request.user)
    else:
        session_key = request.session.session_key

        if not session_key:
            request.session.save()
            session_key = request.session.session_key

        return AnonymousUserProfile.objects.get_or_create(session_key=session_key)
