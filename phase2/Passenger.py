from threading import Condition, Lock
from time import sleep
from MapProxy import MapProxy
from ScheduleProxy import ScheduleProxy
import utilities as ut


class Passenger:
    """
    This class is used by the passenger thread to imitaite a real passnger in the simulation
    The main function that passenger simulation threads run is run method
    """
    def __init__(
        self,
        pid,
        start_loc,
        target,
        radius,
        schedule: ScheduleProxy,
        simul,
    ) -> None:
        self.id = pid
        self.current_location = start_loc
        self.target = target
        self.start = start_loc  # location dictionary
        self.radius = radius
        self.status = "Searching"
        self.schedule = schedule
        self.mutex = Lock()
        self.cond = Condition(self.mutex)
        self.arriveStop = Condition(self.mutex)
        self.time_waited = 0
        self.start_stop = None
        self.end_stop = None
        self.in_bus_time = None
        self.selected_line = None
        self.simul = simul
        self.is_exit = False
        self.start_waiting_time = 0

    # wait for bus
    def wait_bus(self):
        """
        This method is used by passenger to wait until buss arrives at source station
        """
        with self.mutex:
            # must add to waiting list in bus sys?
            # return wait_time
            self.status = "Waiting bus"
            self.start_waiting_time = self.simul.add_to_waiting(self, self.selected_line, self.start_stop)
            self.cond.wait()
            # self.time_waited = ?

    def wait_travel(self):
        """
        This method is used by passenger to wait till bus arrived target station
        """
        with self.mutex:
            self.status = "In bus"
            self.arriveStop.wait()


    def bus_came(self):
        """
        This method is used by simulator to notify passenger that the bus has arrived to start station
        """
        with self.mutex:
            self.cond.notify()
            return (self.in_bus_time, self.start_waiting_time)

    def bus_arrived(self):
        """
        The method is used by simulator class to notify passenger that the bus has arrived its targer station
        """
        with self.mutex:
            self.arriveStop.notify()

    def walk(self, loc1, loc2, status):
        """
        This fucntion is used to handle the walking of a passenger, It calcuates walking time and sleep for that time
        """
        self.status = status
        walking_time = abs(ut.dist(loc2, loc1)) / (30 / 60)
        #### TESTING #######################
        sleep(walking_time *.2)

    def time_between_stops(self, line, stopid1, stopid2):
        """
        This function is used to calculate the time between start and target stops using a specific line 
        """
        all_times = line.get_stops_data()
        # print(all_times)
        # print("times",all_times)
        # print("s1 s2",stopid1,stopid2)
        for i in all_times:
            if i[0] == stopid1 and len(i) == 3:
                val1 = i[2]
        for i in all_times:
            if i[0] == stopid2 and len(i) == 3:
                val2 = i[2]
        if val1 == None or val2 == None:
            return 1e30
        return val2 - val1  # arrival of second - leave of first

    # takes 2 lists
    def shortest_route(self, stops1, stops2):
        """
        This function finds the shortest line to be taken by the passenger 
        It searches all combination of source and target stops to find the most suitable route
        It then compares selected lines and finds the one with minimum time and returns that one
        """
        if stops1 == [] or stops2 == []:
            return (None, None)
        selected_lines = []
        # Finding the line that contains one of the starting or ending stops
        lines = self.schedule.get_lines()
        # print(lines)
        for lineid in lines:
            stops = lines[lineid].get_line_stops()
            for s1 in stops1:
                if s1 in stops:
                    for s2 in stops2:
                        if s2 in stops and stops.index(s1) < stops.index(s2):
                            selected_lines.append((lineid, s1, s2))

        
        # print(selected_lines)
        min_line = None
        min_time = 1e30
        for lineid, s1, s2 in selected_lines:
            t = self.time_between_stops(lines[lineid], s1, s2)
            if t < min_time:
                min_time = t
                min_line = lines[lineid]
                self.selected_line = min_line
                self.start_stop = s1
                self.end_stop = s2
                self.in_bus_time = t
        
        # print("start end", self.start_stop, self.end_stop)
        if (
            self.start_stop == None or self.end_stop == None
        ):  # might be a bug , why would start and end stop be empty?
            return (None, None)  # There maybe no selected lines at all....
        
        stop1_loc = self.schedule.get_stops()[self.start_stop].get_location()
        stop2_loc = self.schedule.get_stops()[self.end_stop].get_location()
        return (stop1_loc, stop2_loc)  # returns stop 1 and 2 locations in a tuple

    def run(self):
        """
        This is the main method of passenger threads 
        The passenger first searches for the nearest stops 
        Passnger the walks to the stop with min route time
        Passneger waits for the bus to come
        After the bus comes passenger enters the bus
        After that passenger waits until the bus arrives the target station
        Passenger leaves the bus and walks to the tagret location
        """
        
        # getting bus stops near start and target locations
        stops_around_start = self.schedule.stops_within_r(self.start, self.radius)
        stops_around_target = self.schedule.stops_within_r(self.target, self.radius)
        
        # print(stops_around_start)
        # print(stops_around_target)
        
        # print("closest to start",stops_around_start)
        # print("closest to end",stops_around_target)
        # Finding the shortest line to take
        shortest = self.shortest_route(stops_around_start, stops_around_target)
        
        
        if shortest == (None, None):
            self.simul.remove_passenger(self)
            return
        sleep(.5)
        # Walking to the target bus station
        self.walk(self.current_location, shortest[0], f"Walking to Bus Station with id {self.start_stop}")
        
        if (self.is_exit):
            return
        # waiting for the bus to come
        self.wait_bus()
        if (self.is_exit):
            return
        # wating to arrive at target station
        self.wait_travel()
        self.current_location = shortest[1]
        # walking from target station to target location
        self.walk(shortest[1], self.target, f"Walking from Bus Station with id {self.start_stop} to target location")
        
        if (self.is_exit):
            return
        self.status = "Arrived"  # reset to Searching?
        sleep(1)
        self.simul.remove_passenger(self)
        return

    def print_status(self):
        """
        This function is used by simulator class to print the current status of passnger thread
        """
        with self.mutex:
            print(f"Passenger with id {self.id} has staus: {self.status}")

    def exit_signel(self):
        """
        This function is used by simulator class to notify passnger that the simulation has ended
        """
        with self.mutex:
            self.is_exit = True
            self.arriveStop.notify()
            self.cond.notify()

    def get_status(self):
        """
        This function is used by simulator class to get the status of passneger
        """
        with self.mutex:
            return f"Passenger with id {self.id} has staus: {self.status}"