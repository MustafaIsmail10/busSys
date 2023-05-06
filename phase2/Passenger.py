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
        self.cond.wait()
        #self.time_waited = ?

    def wait_travel(self):
        self.arriveStop.wait()

    def walk(self,loc1, loc2):
        self.status = "Walking"
        walking_time =  3/60 * ut.dist(loc2,loc1)
        sleep(walking_time)

    def time_between_stops(self, route,stopid1, stopid2):
        all_times = route.get_stops_data()
        return all_times[stopid2][1]-all_times[stopid1][2] #arrival of second - leave of first
        
    #takes 2 lists
    def shortest_route(self,stops1, stops2):
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
        for route in selected_routes:
            t = self.time_between_stops(*routes[route[0]])
            if t<min_time:
                min_time = t
                min_route = routes[route]  
        stop1_loc = routes[min_route[0]].getstops()[min_route[1]].get_location()
        stop2_loc = routes[min_route[0]].getstops()[min_route[2]].get_location()
        self.start_stop = min_route[1]
        self.end_stop = min_route[2]

        return (stop1_loc,stop2_loc)  #returns stop 1 and 2 locations in a tuple

    def run(self):
        stops_around_start = self.map.stops_within_r(self.start, self.radius)
        stops_around_target = self.map.stops_within_r(self.target, self.radius)

        shortest = self.shortest_route(stops_around_start,stops_around_target)
        self.walk(self.current_location, shortest[0])
        self.wait_bus() #wait for bus
        self.wait_travel()
        self.walk(shortest[1],self.target)
        self.status = "Arrived" # reset to Searching?

    def print_status(self):
        print(f"current staus: {self.status}")