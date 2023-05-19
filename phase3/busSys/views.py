from django.shortcuts import render
from django.http import HttpResponse
from django.views.generic import TemplateView
# Create your views here.

class Home(TemplateView):
    template_name = "home.html"

def Simulation(reqest):
    pass

def login(request):
    return render(request, 'login.html')