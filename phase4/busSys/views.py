from django.shortcuts import render, redirect
from django.http import HttpResponse
from django.views.generic import TemplateView
from socket import *
from re import *

# Create your views here.


def home(request):
    """
    Handling main page requests
    """
    return render(request, "home.html")


def simulate(request):
    """
    Handling simualtion page requests
    """
    
    return render(request, "simulation.html")


def login(request):
    """
    Handling login page requests
    """
    # if request.method == 'POST':
    #     return login_post(request)

    context = {}
    return render(request, "login.html", context)


def signup(request):
    """
    Handling login page requests
    """
    # if request.method == 'POST':
    #     return login_post(request)

    context = {}
    return render(request, "signup.html", context)




def signout(request):
    """
    Handling signout requests
    """
    request.session["token"] = None
    request.session["username"] = None
    return redirect("home")


def display_result(request):
    
    return render(request, "result.html")


def design(request):
    """
    Handling requests for design page
    """
    

    return render(request, "design.html")


def stopOp(request):
    """
    Handling stop page
    """
  
    return render(request, "stopOp.html")


def route(request):
    """
    Handling route page
    """
    
    return render(request, "route.html")


def schedule(request):
    """
    Handling schedule page
    """
   
    return render(request, "schedule.html")


def map(request):
    """
    Handling map page
    """
  
    return render(request, "map.html")


def line(request):
    """
    Handling line page
    """
    
    return render(request, "line.html")
