from django.urls import path
from .views import Home, login

urlpatterns = [
    path("", Home.as_view(), name="home"),
    path("login", login, name="login"),
]