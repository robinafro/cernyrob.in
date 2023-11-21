from django.urls import path
from . import views

urlpatterns = [
        path('', views.home, name="root"),
        path('home/', views.home, name="home"),
]
