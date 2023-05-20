from django.shortcuts import render, redirect
from django.http import HttpResponse
from django.views.generic import TemplateView
from socket import *
# Create your views here.

def home(request):
    token = request.session.get('token')
    context = {}
    if token:
        context['auth'] = True
        context['username'] = request.session.get("username")
       
    return render(request, 'home.html', context)

def simulate(request):
    token = request.session.get('token')
    context = {}
    if token:
        context['auth'] = True
        context['username'] = request.session.get("username")
    if request.method == "POST":
        return do_simulation(request, token, context)
    return render(request, 'simulation.html', context)

def do_simulation(request, token, context):
    simulation_data = request.POST
    sch_num = simulation_data["sch_num"]
    start_time = simulation_data["start_time"]
    end_time = simulation_data["end_time"]
    sock = socket(AF_INET, SOCK_STREAM)
    sock.connect( ('127.0.0.1', 1445))
    
    result = sock.recv(1000)
    sock.send(f'auToken {token}'.encode())
    result = sock.recv(1000).decode().split("\n")[0]
    print(result)
    if result == "Authentication Error":
        request.session['token'] = None
        request.session['username'] = None 
        return redirect('login')
    print(result)
    while(result):
        print(result)
        result = sock.recv(1000).decode().split("\n")[0]
    sock.send(b'close')

    return render(request, 'simulation.html', context)



def login(request):
    if request.method == 'POST':
        return login_post(request)  

    context = {}
    context['auth'] = False
    context['username'] = None    
    return render(request, 'login.html', context)

def login_post(request):
    login_data = request.POST
    username = login_data["username"]
    password = login_data["password"]
    sock = socket(AF_INET, SOCK_STREAM)
    sock.connect( ('127.0.0.1', 1445))
    sock.recv(1000)
    sock.send(f'login {username} {password}'.encode())
    token = sock.recv(1000).decode().split("\n")[0]
    print(token)
    sock.send('close'.encode())

    result = sock.recv(1000).decode().split("\n")
    while True and result[0]:
        if (len(result)>1 and result[1] == "closed"):
            break
        print(result)
        result = sock.recv(1000).decode().split("\n")
        
    sock.close()
    request.session['token'] = token
    request.session['username'] = login_data["username"]
    return redirect('home')


def signout(request):
    request.session['token'] = None
    request.session['username'] = None 
    return redirect('home')

def handle_form(request):
    token = request.session.get('token')
    context = {}
    print(token)
    if token:
        context['auth'] = True
        context['username'] = request.session.get("username")
    if request.method == 'POST':
        toserver = ""
        for key, value in request.POST.items():
            if key=="csrfmiddlewaretoken": 
                continue
            toserver+= f' {value}'  
        print(toserver)
        sock = socket(AF_INET, SOCK_STREAM)
        sock.connect(('127.0.0.1', 1445))
        sock.recv(1000)
        print(f'auToken {token}')
        sock.send(f'auToken {token}'.encode())        
        auth = sock.recv(1000).decode().split("\n")[0]
        print(auth)
        sock.send(toserver.encode())
        result = sock.recv(1000).decode().split("\n")
        print(result)

        sock.send('close'.encode())
        result = sock.recv(1000).decode().split("\n")
        print(result)
        while(True):
            if (len(result)> 1 and result[1] == "closed"):
                break
            print(result)
            result = sock.recv(1000).decode().split("\n")
        sock.close()
    return render(request,'home.html',context)        
            
def design(request):
    token = request.session.get('token')
    context = {}
    if token:
        context['auth'] = True
        context['username'] = request.session.get("username")
       
    return render(request, 'design.html', context)
    
def stopOp(request):
    token = request.session.get('token')
    print(token)
    context = {}
    if token:
        context['auth'] = True
        context['username'] = request.session.get("username")
       
    return render(request, 'stopOp.html', context)
   
    
def route(request):
    token = request.session.get('token')
    context = {}
    if token:
        context['auth'] = True
        context['username'] = request.session.get("username")
       
    return render(request, 'route.html', context)
        
def schedule(request):
    token = request.session.get('token')
    context = {}
    if token:
        context['auth'] = True
        context['username'] = request.session.get("username")
       
    return render(request, 'schedule.html', context)
    
    
def Map(request):
    token = request.session.get('token')
    context = {}
    if token:
        context['auth'] = True
        context['username'] = request.session.get("username")
       
    return render(request, 'map.html', context)
    
    
def line(request):
    token = request.session.get('token')
    context = {}
    if token:
        context['auth'] = True
        context['username'] = request.session.get("username")
       
    return render(request, 'line.html', context)
 