# BusSys
BusSys is a collaborative bus route designer

# Authors 
2465813 : Moustafa Ismail Hamed Mohamed Ismail

2455566: Hana Elboghdady


# Running phase 4
**To run the busSys server itself do the following** 

- Change directory to phase 2 `cd phase2` 

- Enter the following command to run the server `python3 web_server.py --port 1445`

**To run Djnago server do the following**

- Change directory to phase 4 `cd phase4` 

- Enter the following command to start the django server `python3 manage.py runserver`


# Implementaion Phase 4

## Web_server 

The interface of bussys server is changed from a normal tcp server to a server using web sockets

## DJango

Django is used to only serve static files of the system such as JS, HTML, and CSS files

## Javascript

There are several front end scripts used to authenticate user and communicate with bussys server through a websocket interface.

## requirements.txt 

File listing all the dependencies for the project.

# Running phase 3
First to run the busSys server itself, go to the first part of [Running phase 2](#running-phase-2) section 

Then to start the web server:

Change directory to phase 3 `cd phase3` 

Enter the following command to start the django server `python3 manage.py runserver`

A window will be opened and the Home-page will be displayed where several functionalities can be accessed.

Login must be done first to authorize access to the rest of the functionalities.


# Implementaion Phase 3

## Server Class

Some changes to the Server in phase 2 to incorprate a communication protocol between both web and busSys servers.

## busSys Directory

Contains views and urls. 

Views is where the server connects to busSys server and handles authorization, the user requests sent through the forms
and displaying results from busSys server.

Urls is where the linking of html and view functions happens.

## templates Directory 

Contains all the HTML pages that are displayed to users. 

## requirements.txt 

File listing all the dependencies for the project.

# Running phase 2

Change directory to phase 2 `cd phase2` 

Enter the following command to run the server `python3 Server.py --port <port number>`

Enter the following command to run clients `nc -v localhost <port number>`

After running the client login to be able to user all functions of the system


# Implementaion Phase 2

## User Class
It is used to store infomation about the users and hanldle authorization 

It is also used to notify user in case of updates

It also keeps a list of maps and scheduels that belongs to a specific user

## BusSys Class
It's a singiliton class that uses reader\writer sync approach to control the access of all user threads to various objects in the system

It contains all the API of the system and calls various classes and objects

## MapProxy
It is used as a proxy for map class that handles sync. 

It also implements observer sync approach that keeps track of all changes in the map and notify registered users


## ScheduleProxy
It is used as a proxy for schedule class that handles sync. 

It also implements observer sync approach that keeps track of all changes in the scheduel and notify registered users

## Simulator Class
It is the main class that is responsible for running and tracking the simulation

## Passenger Class
It is used by passenger threads to imitate a real passenger in the simulation

## Server Class
It is used to run the server and create threads for each connection request


# Implementaion Phase 1


## User class
It is used to store infomation about the users and hanldle authorization 

## BusSys class
It is used to control the access to the schedule class 

## Map class
It loads the map json file and parses the data. It also offers several functionalities on the data such as shortest path between node or stops

## schedules class
It takes map as input and allow user to access various functionalities such as:
* Adding, modifying, and deleting lines
* Adding, modifying, and deleting routes
* Adding, modifying, and deleting stops
* Getting information about various entities in the system

## Stop class
It stores information about stop entities 

## Route class
Allows user to create routes and edit them

## Line class 
Allows user to create line and edit them

## Demo class
Allowss users to interact with the system via cli


## Running the demo
use the follownig commands
`cd phase1` 
`python3 demo.py`
After running the demo you need to run the `login` command to be able to access all the functionalities of the systems.




