
from Map import Map
from Scheduale import Schedule
import threading as th
from User import User


class ScheduleProxy():
    '''
    The main purpose of this class is to handle 
    the synchronization of the threads such that when 
    functions in the Schedule are called, no 2 threads 
    can edit at the same time and no edit and read
    can happen at the same time.
    It is like a layer of protection for our data, to
    avoid corruption.
    During initialisation a map is passed along with a schedule id
    and the user which is added to the list of users registered 
    to this Schedule.
    Schedule object created using the map, name and schedule id
    Also a lock is created during initialisation.
    '''
    def __init__(self, user, sys_map: Map, name, sch_id):
        self._schedule = Schedule(sys_map, name, sch_id)
        self.lock = th.RLock()
        self.users = [user]
        self.sch_id = sch_id

    def synched(func):
        '''
        This is the decorator that decorates all 
        the functions calling the Schedule functions.
        It uses the lock to be able to call the 
        function
        '''
        def synchronize(self, *args, **kwargs):
            with self.lock:
                return func(self, *args, **kwargs)
        return synchronize

    def notify(func):
        '''
        This decorator is used to notify users
        when changes happen, including a new user
        registering to the Schedule, adding stops
        in the map, deleting and such.
        '''
        def notification(self, *args, **kwargs):
                res = func(self, *args, **kwargs)
                for user in self.users:
                    user.notify(res)
                return res
        return notification

    def get_map(self):
        '''
        Returns the map associated with this schedule
        '''
        return self._schedule.map

    @synched
    def test(self):
        print("using the lock")

    @synched
    @notify
    def register(self, user):
        '''
        This function registers users to the Schedule
        '''
        self.users.append(user)
        return f"New User {user} is registered to schedule with id {self.sch_id}\n"

    @synched
    @notify
    def unregister(self, user):
        '''
        This function unregisters users from the Schedule
        '''
        self.users.remove(user)

    @synched
    @notify
    def add_route(self):
        """
        This function adds a new empty route and later stops
        and can be added to that route by calling implementation in schedule
        
        """
        return self._schedule.add_route()

    @synched
    def get_route(self, routeid):
        """
        This function returns a route with its id as input,
        calls the implemented function in schedule
        """
        return self._schedule.get_route(routeid)

    @synched
    def get_route_info(self, route_id):
        """
        This function returns the stops of a route taking the route id as input 
        """
        return self._schedule.get_route_info(route_id)

    @synched
    def get_routes(self):
        """
        This function returns all ruotes in the system
        """
        return self._schedule.get_routes()

    @synched
    @notify
    def del_route(self, routeid):
        '''
        This function deletes a route from our schedule
        '''
        return self._schedule.del_route(routeid)

    @synched
    def get_stops(self):
        """
        This function returns all bus stops in the system, 
        calling the original function in schedule.
        """
        return self._schedule.get_stops()

    @synched
    @notify
    def add_stop(self, edgeid,  direction, percentage,  description):
        """
        This fucntion adds a bus stop to the system.
        It calls the implemented version in schedule
        """
        return self._schedule.add_stop(
            edgeid,  direction, percentage,  description)

    @synched
    @notify
    def del_stop(self, stop_id):
        """
        This function removes a bus stop from the system.
        It calls the implemented version in schedule
        """
        return self._schedule.del_stop(stop_id)

    @synched
    @notify
    def add_stop_to_route(self, route_id, stop_id, wait_time):
        """
        This function adds existing bus stop to a route
        It calls the implemented version in schedule
        """
        return self._schedule.add_stop_to_route(route_id, stop_id, wait_time)

    @synched
    @notify
    def del_stop_from_route(self, route_id, stop_id):
        """
        This function removes existing bus stop from a route
        It calls the implemented version in schedule
        """
        return self._schedule.del_stop_from_route(route_id, stop_id)

    @synched
    @notify
    def change_stop_wait(self, route_id, stop_id, wait):
        """
        This fucntion changes the wait time of the bus in a specific stop in a specific route
        It calls the implemented version in schedule
        """
        return self._schedule.change_stop_wait(route_id, stop_id, wait)

    @synched
    @notify
    def addline(self, name, start_time, end_time, time_between_trips, routeid, description):
        """
        This function adds a line to the system given the information of the line and the route that it will be assigned to. 
        Calls implemented version in schedule
        """
        return self._schedule.addline(name, start_time, end_time, time_between_trips, routeid, description)

    @synched
    def get_lines(self):
        """
        This fucntion returns all the lines in the system
        Calls implemented version in schedule
        """
        return self._schedule.get_lines()

    @synched
    def lineinfo(self, lineid):
        """
        This function returns line information
        Calls implemented version in schedule
        """
        return self._schedule.lineinfo(lineid)

    @synched
    @notify
    def del_line(self, lineid):
        """
        This fucntion deletes a line from the system
        Calls implemented version in schedule
        """
        return self._schedule.del_line(lineid)

    @synched
    @notify
    def update_line_name(self, lineid, name):
        """
        Update line name
        Calls implemented version in schedule
        """
        return self._schedule.update_line_name(lineid, name)

    @synched
    @notify
    def update_line_start_time(self, lineid, start_time):
        """
        Update line start time
        Calls implemented version in schedule
        """
        return self._schedule.update_line_start_time(lineid, start_time)

    @synched
    @notify
    def update_line_end_time(self, lineid, end_time):
        """
        Update line end time.
        Calls implemented version in schedule
        """
        return self._schedule.update_line_end_time(lineid, end_time)

    @synched
    @notify
    def update_line_time_between_trips(self, lineid, time_between_trips):
        """
        Update time between trips of a line.
        Calls implemented version in schedule
        """
        return self._schedule.update_line_time_between_trips(
            lineid, time_between_trips)

    @synched
    @notify
    def update_line_description(self, lineid, description):
        """
        Update line description.
        Calls implemented version in schedule
        """
        return self._schedule.update_line_description(lineid, description)

    @synched
    def stopinfo(self, stopid):  
        '''
        Returns which lines pass by it and when
        Calls implemented version in schedule
        '''
        return self._schedule.stopinfo(stopid)


    @synched
    def is_bus_at_stop(self,  lineid, stopid, curr_time):  
        '''
        Checks if bus is at the stop, returns a tuple containing bus number and a boolean value
        Calls implemented version in schedule
        '''
        return self._schedule.is_bus_at_stop(lineid, stopid, curr_time)
    

    @synched
    def get_line_stops_data(self, lineid):
        
        return self._schedule.get_line_stops_data(lineid)
    
    @synched
    def stops_within_r(self, stopid, radius):
        '''
        Returns list of all stop that are at a
        radius k away from the given location, if they exist
        Calls implemented version in schedule
        '''
        return self._schedule.stops_within_r(stopid, radius)
    
    @synched
    def __str__(self):
        '''
        Representation of Schedule
        '''
        return str(self._schedule)

    @synched
    def get_journey_times(self, lineid):
        '''
        Returns times of the journey 
        Calls implemented version in schedule
        '''
        return self._schedule.get_journey_times(lineid)
    
    @synched
    def get_line_distance(self, lineid):
        """
        Returns whole distance covered by route of Line with given line id.
        Adds a map to the user's list of maps that they are subscribed to
        """
        return self._schedule.get_line_distance(lineid)
    
    @synched
    def get_line_distance_until_stop(self, lineid, stopid):
        '''
        Finds the distance to a stop with given stop id of the line with given line id
        c
        '''
        return self._schedule.get_line_distance_until_stop(lineid, stopid)

# kwargs = {"path": "./test/test_map.json"}
# t = ScheduleProxy(Map( 1, **kwargs),"toto",0)
# t.test()
