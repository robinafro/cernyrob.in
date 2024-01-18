"""
URL configuration for cernyrobin_django project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/4.2/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path
from django.conf import settings
from django.conf.urls.static import static

from cernyrobin_app import views as cernyrobin
from kafka import views as kafka
# from miskovsky import views as miskovsky
from api import views as api
from ads import views as ads

urlpatterns = [
    path("admin/", admin.site.urls),

    path("", cernyrobin.home, name="root"),
    path("home/", cernyrobin.home, name="home"),

    path("login/", cernyrobin.login_page, name="login"),
    path("register/", cernyrobin.login_page, name="register"),
    path("login/submit/", cernyrobin.login_submit, name="login_submit"),
    path("account/", cernyrobin.account, name="account"),

    path("clicker/", cernyrobin.clicker_page, name="clicker"),
    path("clicker/add_click", cernyrobin.add_click, name="add_click"),
    path("get_user_data/", cernyrobin.get_user_data, name="get_user_data"),
    path("get_all_data/", cernyrobin.get_all_data, name="get_all_data"),

    path("kafka/answer", api.kafka_answer, {"subdomain": "api"}, name="kafka_answer"),
    path("kafka/list", api.kafka_list, {"subdomain": "api"}, name="kafka_list"),
    path("kafka/get", api.kafka_get, {"subdomain": "api"}, name="kafka_get"),
    path("kafka/job", api.kafka_job, {"subdomain": "api"}, name="kafka_job"),
    path("kafka/", kafka.index, name="kafka_index"),
    path("kafka/view/", kafka.view, name="kafka_view"),
    path("kafka/submit/", kafka.submit, name="kafka_submit"),

    # path("miskovsky/", miskovsky.index, name="miskovsky_index"),
    # path("miskovsky/submit/", miskovsky.submit, name="miskovsky_submit"),
    # path("miskovsky/view/", miskovsky.view, name="miskovsky_view"),

    path("me/", ads.my_ads, {"subdomain": "reklamy"}, name="my_ads"),
    path("manage/", ads.manage, {"subdomain": "reklamy"}, name="manage"),
    path("manage/submit/", ads.manage_submit, {"subdomain": "reklamy"}, name="manage_submit"),
    path("manage/delete/", ads.manage_delete, {"subdomain": "reklamy"}, name="manage_delete"),
    path("a/", ads.ad, {"subdomain": "reklamy"}, name="ad"),
    path("pending/", ads.admin_pending, {"subdomain": "reklamy"}, name="admin_pending"),
    path("accept/", ads.admin_accept, {"subdomain": "reklamy"}, name="admin_accept"),
    path("reject/", ads.admin_reject, {"subdomain": "reklamy"}, name="admin_reject"),
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)