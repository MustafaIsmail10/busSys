# BusSys
BusSys is a collaborative bus route designer

# Authors 
2465813 : Moustafa Ismail Hamed Mohamed Ismail
2455566: Hana Elboghdady


# Implementaion

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




