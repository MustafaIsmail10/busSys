from django.urls import path
from .views import home, login,signout, simulate

urlpatterns = [
    path("", home, name="home"),
    path('login/', login, name='login'),
    path("signup", login, name="signup"),
    path("design", login, name="design"),
    path("simulate", simulate, name="simulate"),
    path("signout", signout, name="signout"),
]