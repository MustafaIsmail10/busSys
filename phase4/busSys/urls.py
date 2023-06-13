from django.urls import path
from .views import home, login,signout, simulate,design,stopOp,schedule,line,map,route,display_result, signup


urlpatterns = [
    path("", home, name="home"),
    path('login/', login, name='login'),
    path("signup/", signup, name="signup"),
    path("simulate/", simulate, name="simulate"),
    path("signout/", signout, name="signout"),
    path("design/", design, name="design"),
    path("design/StopOp/", stopOp, name="StopOp"),
    path("design/route/", route, name="route"),
    path("design/schedule/", schedule, name="schedule"),
    path("design/map/", map, name="map"),
    path("design/line/", line, name="line"),
    path("result/",display_result,name="result"),
    
]