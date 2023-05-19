from django.urls import path
from .views import Home, login

urlpatterns = [
    path("", Home.as_view(), name="home"),
    path("login", login, name="login"),
    path("signup", login, name="signup"),
    path("design", login, name="design"),
    path("simulate", login, name="simulate"),
    path("signout", login, name="signout"),
]