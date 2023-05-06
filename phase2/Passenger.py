from threading import Condition
from time import sleep
from MapProxy import MapProxy
from ScheduleProxy import ScheduleProxy
import utilities as ut

class Passenger:
    def __init__(self,pid, start_loc,target,radius, map: MapProxy, schedule:ScheduleProxy, simul) -> None:
        self.current_location = start_loc
        self.target =  target
        self.start =  start_loc #location dictionary
        self.radius =  radius
        self.map = map
        self.status = "Searching"
        self.schedule = schedule
        self.cond = Condition()
        self.arriveStop = Condition()
        self.time_waited = 0
        self.start_stop = None
        self.end_stop = None
        self.id = pid
    
    #wait for bus
    def wait_bus(self):
        #must add to waiting list in bus sys?
        #return wait_time
        self.status =  "Waiting"
        with self.cond:
            self.cond.wait()
            print("hala from wait_bus in passenger class ")
        #self.time_waited = ?

    def wait_travel(self):
        with self.arriveStop:
            self.arriveStop.wait()

    def bus_came(self):
        print("bus is here")
        with self.cond:
            self.cond.notify()
    
    def bus_arrived(self):
        with self.arriveStop:
            self.arriveStop.notify()


    def walk(self,loc1, loc2):
        self.status = "Walking"
        walking_time =  3/60 * ut.dist(loc2,loc1)
        sleep(walking_time)

    def time_between_stops(self, route,stopid1, stopid2):
        all_times = route.get_stops_data()
        # print("times",all_times)
        # print("s1 s2",stopid1,stopid2)
        for i in all_times:
            if i[0] == stopid1 and len(i)==3:
                val1=i[2]
        for i in all_times:
            if i[0] == stopid2:
                val2=i[1]    
        return val2-val1 #arrival of second - leave of first
        
    #takes 2 lists
    def shortest_route(self,stops1, stops2):
        if stops1 ==[] or stops2==[]:
            return (None,None)
        selected_routes = []
        routes =  self.schedule.get_routes()
        
        for routeid in routes:
            stops  = routes[routeid].get_stops()
            for s1 in stops1:
                if s1 in stops:
                    for s2 in stops2:
                        if  s2 in stops and stops.index(s1)<stops.index(s2):
                            selected_routes.append((routeid, s1, s2))

        min_route = None
        min_time = 1e30      
        for routeid,s1,s2 in selected_routes:
            t = self.time_between_stops(routes[routeid],s1,s2)
            if t<min_time:
                min_time = t
                min_route = routes[routeid]  
                self.start_stop = s1
                self.end_stop = s2
        print("start end",self.start_stop,self.end_stop)

        if self.start_stop==None or self.end_stop==None: #might be a bug , why would start and end stop be empty?
           return (None,None)
        stop1_loc = self.map.get_stops()[self.start_stop].get_location()
        stop2_loc = self.map.get_stops()[self.end_stop].get_location()
        

        return (stop1_loc,stop2_loc)  #returns stop 1 and 2 locations in a tuple


    def run(self):
        stops_around_start = self.map.stops_within_r(self.start, self.radius)
        stops_around_target = self.map.stops_within_r(self.target, self.radius)
        # print("closest to start",stops_around_start)
        # print("closest to end",stops_around_target)
        shortest = self.shortest_route(stops_around_start,stops_around_target)
        if(shortest == (None,None)):
            return 
        self.walk(self.current_location, shortest[0])
        self.wait_bus() 
        print("on bus")
        self.wait_travel()
        self.walk(shortest[1],self.target)
        self.status = "Arrived" # reset to Searching?

    def print_status(self):
        print(f"current staus: {self.status}")