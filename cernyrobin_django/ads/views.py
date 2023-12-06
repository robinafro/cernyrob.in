from django.shortcuts import render
from django.http import HttpResponse, JsonResponse
from django.shortcuts import redirect

from .models import Ad

def get_ad(id):
    try:
        return Ad.objects.get(ad_id=id)
    except Ad.DoesNotExist:
        return None
    
def get_ads_by_owner(owner_name):
    return Ad.objects.filter(owner_name=owner_name)

def get_random_ad():
    return Ad.objects.order_by('?').first()

def get_all_ads():
    return Ad.objects.all()

def get_ad_json(ad):
    return {
        "ad_id": ad.ad_id,
        "owner_name": ad.owner_name,
        "name": ad.name,
        "status": ad.status,
        "link": ad.link,
        "image_link": ad.image_link
    }

def create_ad(owner_name, name, image_link, link):
    ad = Ad(owner_name=owner_name, name=name, image_link=image_link, link=link)

    ad.save()

    return ad

def delete_ad(id):
    ad = get_ad(id)

    if ad is not None:
        ad.delete()

def get_owner_name(request):
    user = request.user.username

    if user is not None and user != "" and user != "AnonymousUser" and user != "anonymous":
        return user
    else:
        return None

def my_ads(request, subdomain):
    if request.method == "GET":
        owner_name = get_owner_name(request)

        if owner_name is not None:
            context = {
                "ads": get_ads_by_owner(owner_name),
            }

            return render(request, "ads/view.html", context)

        return JsonResponse({"error": "you must be logged in"}, status=400)

    return JsonResponse({"error": "GET method required"}, status=400)

def manage(request, subdomain):
    return render(request, "ads/manage.html")

def manage_submit(request, subdomain):
    if request.method == "POST":
        owner_name = get_owner_name(request)

        if owner_name is not None:
            name = request.POST.get("name")
            image_link = request.POST.get("image_link")
            link = request.POST.get("link")

            if name is not None and image_link is not None and link is not None:
                ad = create_ad(owner_name, name, image_link, link)

                return redirect("/me/")

            return JsonResponse({"error": "name, image_link and link required"}, status=400)

        return JsonResponse({"error": "you must be logged in"}, status=400)

def ad(request, subdomain):
    if request.method == "GET":
        id = request.GET.get("id")

        if id is not None:
            ad = get_ad(id)

            if ad is not None:
                return JsonResponse(get_ad_json(ad))

            return JsonResponse({"error": "ad not found"}, status=404)

        return JsonResponse({"error": "id required"}, status=400)