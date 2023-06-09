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
    token = request.session.get('token')
    context = {}
    if token:
        context['auth'] = True
        context['username'] = request.session.get("username")
    return render(request, 'home.html', context)

def simulate(request):
    """
    Handling simualtion page requests
    """
    token = request.session.get('token')
    context = {}
    if token:
        context['auth'] = True
        context['username'] = request.session.get("username")
    return render(request, 'simulation.html', context)




def login(request):
    """
    Handling login page requests
    """
    # if request.method == 'POST':
    #     return login_post(request)  

    context = {}
    context['auth'] = False
    context['username'] = None    
    return render(request, 'login.html', context)

def login_post(request):
    """
    Handling login form requests
    """
    login_data = request.POST
    username = login_data["username"]
    password = login_data["password"]
    sock = socket(AF_INET, SOCK_STREAM)
    sock.connect( ('127.0.0.1', 1445))
    sock.recv(1000)
    sock.send(f'login {username} {password}'.encode())
    token = sock.recv(1000).decode().split("\n")[0]
    sock.send('close'.encode())

    result = sock.recv(1000).decode().split("\n")
    while result[0]:
        if (len(result)>1 and result[1] == "closed"):
            break
        result = sock.recv(1000).decode().split("\n")
        
    sock.close()
    request.session['token'] = token
    request.session['username'] = login_data["username"]
    return redirect('home')


def signout(request):
    """
    Handling signout requests
    """
    request.session['token'] = None
    request.session['username'] = None 
    return redirect('home')

def handle_form(request):
    """
    Handling form requests for all functionalities. Getting the requests from the web page and sending them to bussys server
    """    
    token = request.session.get('token')
    context = {}
    if token:
        context['auth'] = True
        context['username'] = request.session.get("username")
    if request.method == 'POST':
        toserver = ""
        for key, value in request.POST.items():
            if key=="csrfmiddlewaretoken": 
                continue
            toserver+= f' {value}'  
        # The following is a holy piece of code. 
        # It establishes a connection with the bussys server for getting the required functionalities
        # It gets the response from the server and sends it to the display function for formatting
        sock = socket(AF_INET, SOCK_STREAM)
        sock.connect(('127.0.0.1', 1445))
        sock.recv(1000)
        sock.send(f'auToken {token}'.encode())        
        auth = sock.recv(1000).decode().split("\n")[0]
        sock.send(toserver.encode())
        response_list = []
        result = sock.recv(1000).decode().split("\n")
        response_list.append(result)
        sock.send('close'.encode())
        result = sock.recv(1000).decode().split("\n")
        while result[0]:
            if (len(result)> 1 and result[1] == "closed"):
                break
            response_list.append(result)
            result = sock.recv(1000).decode().split("\n")
        sock.close()
        context['result_list'] = response_list
    return display_result(request,context)        

def display_result(request,context):
    """
    Handling diplay of the results for all functionalities
    """  
    result_str =""
    for lst in context['result_list']:
        for elem in lst:
            result_str+=elem
    result_str = result_str.replace("New Message", "\nNew Message: ")
    result_str = result_str.replace(" The", "$")
    result_str = result_str.replace("The", "\nThe")
    result_str = result_str.replace("$", " The")
    result_str = sub(r"},", "}\n ",result_str)
    result_str = result_str.replace("A", "\nA").split("\n")
    # indices = [index for index in range(len(result_str)) if result_str.startswith('New', index)]
    # print(indices)
    # indices= indices.reverse()
    # for i in indices:
        
    context['result_list'] = result_str
    return render(request,'result.html',context)

def design(request):
    """
    Handling requests for design page
    """  
    token = request.session.get('token')
    context = {}
    if token:
        context['auth'] = True
        context['username'] = request.session.get("username")
       
    return render(request, 'design.html', context)
    
def stopOp(request):
    """
    Handling stop page 
    """  
    token = request.session.get('token')
    context = {}
    if token:
        context['auth'] = True
        context['username'] = request.session.get("username")
       
    return render(request, 'stopOp.html', context)
   
    
def route(request):
    """
    Handling route page 
    """  
    token = request.session.get('token')
    context = {}
    if token:
        context['auth'] = True
        context['username'] = request.session.get("username")
       
    return render(request, 'route.html', context)
        
def schedule(request):
    """
    Handling schedule page 
    """  
    token = request.session.get('token')
    context = {}
    if token:
        context['auth'] = True
        context['username'] = request.session.get("username")
       
    return render(request, 'schedule.html', context)
    
    
def Map(request):
    """
    Handling map page 
    """  
    token = request.session.get('token')
    context = {}
    if token:
        context['auth'] = True
        context['username'] = request.session.get("username")
       
    return render(request, 'map.html', context)
    
    
def line(request):
    """
    Handling line page 
    """  
    token = request.session.get('token')
    context = {}
    if token:
        context['auth'] = True
        context['username'] = request.session.get("username")
       
    return render(request, 'line.html', context)
 