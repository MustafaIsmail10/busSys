from django.urls import path
from .views import homePageView

urlpatterns = [
    path("", home, name="home"),
]