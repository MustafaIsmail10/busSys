from User import User
from Scheduale import Schedule
from Map import Map
from threading import RLock
from Exceptions import *


def auth(method):
    def f(self, user, token, *args, **kwargs):
        if user.is_authenticated(token):
            return method(self, *args, **kwargs)
        else:
            raise UserNotAuthenticated(
                "Invalid Access. User is not authenticated")
    return f


class Singleton:
    def __new__(cls, *a, **b):
        if hasattr(cls, '_inst'):
            return cls._inst
        else:
            cls._inst = super().__new__(cls, *a, **b)
            return cls._inst


class BusSys(Singleton):
    """
    This class shall be the main controller of the system 
    """

    def __init__(self):
        self.schedules = {}
        self.maps = {}
        self.users = {}
        self.mutex = RLock()
        self.ids = 0

    @auth
    def add_map(self, **kwargs):
        new_id = self.ids
        self.ids += 1
        new_map = Map(**kwargs)
        self.maps[new_id] = new_map
        return new_id

    @auth
    def get_map(self, map_id):
        return self.maps[map_id]

    @auth
    def add_schedule(self, map_id, name):
        new_id = self.ids
        self.ids += 1
        new_schedule = Schedule(self.maps[map_id], name, new_id)
        self.schedules[new_id] = new_schedule
        return new_id

    @auth
    def get_schedule(self, schdule_id):
        """
        Returns a specific schedule
        """
        return self.schedules[schdule_id]

    ################################### STOPS START #############################
    @auth
    def get_stops(self, schdule_id):
        """
        This function is used to get all stops in the system
        """
        stops = self.schedules[schdule_id].get_stops()
        return stops

    @auth
    def add_stop(self, sch_id, edgeid, directoin, percentage, description):
        """
        This command is used to add a new stop
        """
        stop_id = self.schedules[sch_id].add_stop(
            int(edgeid), bool(directoin), int(percentage), description)
        return stop_id

    @auth
    def del_stop(self, sch_id, stop_id):
        """
        This command is used to delete a stop
        """
        return self.schedules[sch_id].del_stop(int(stop_id))

    ############################## STOPS END #####################

    ############################# ROUTES START #########################

    @auth
    def add_route(self, sch_id):
        """
        This command is used to add a new empty route to the system
        """
        new_route_id = self.schedules[sch_id].add_route()
        return new_route_id

    @auth
    def get_route(self, sch_id, routeid):
        """
        This command is used to get route with route id from schedule with sch_id
        """
        route = self.schedules[sch_id].get_route(int(routeid))
        return route

    @auth
    def get_routes(self, sch_id):
        """
        This command is used to get all routes of the system in a schedule
        """
        routes = self.schedules[sch_id].get_routes()
        return routes

    @auth
    def add_stop_to_route(self, sch_id, routeid, stop_id, wait_time):
        """
        This command is used to a stop to a specific route
        """
        status = self.schedules[sch_id].add_stop_to_route(
            int(routeid), int(stop_id), int(wait_time))
        return status

    @auth
    def del_stop_from_route(self, sch_id, routeid, stop_id):
        """
        This command is used to remove a stop from a specific route
        """
        self.schedules[sch_id].del_stop_from_route(int(routeid), int(stop_id))
        return True

    @auth
    def change_stop_wait(self, sch_id, routeid, stopid, wait_time):
        """
        This command is used to change the wait time of a stop insied a route
        """
        self.schedules[sch_id].change_stop_wait(
            int(routeid), int(stopid), int(wait_time))

    @auth
    def del_stop(self, sch_id, stop_id):
        """
        This command is used to remove a stop from the system
        """
        self.schedules[sch_id].del_stop(int(stop_id))

    ############################# Routes END #########################

    ############################# LINES START ################################

    @auth
    def add_line(self, sch_id, name, start_time, end_time, time_between_trips, routeid, description):
        """
        This command is used to add a line to the system
        """
        self.schedules[sch_id].addline(
            name, int(start_time), int(end_time), int(
                time_between_trips), int(routeid), int(description)
        )

    @auth
    def get_lines(self, sch_id):
        """
        This command is used to print all line of the system
        """
        lines = self.schedules[sch_id].get_lines()
        return lines

    @auth
    def del_line(self, sch_id,  lineid):
        """
        This command is used to delete line from the system
        """
        self.schedules[sch_id].del_line(int(lineid))

    @auth
    def update_line_name(self, sch_id, lineid, new_name):
        """
        This command is used to update line name
        """
        self.schedules[sch_id].update_line_name(int(lineid), new_name)

    @auth
    def update_line_start_time(self, sch_id,  lineid, new_start_time):
        """
        This command is used to update line start time
        """
        self.schedules[sch_id].update_line_start_time(
            int(lineid), int(new_start_time))

    @auth
    def update_line_end_time(self, sch_id, lineid, new_end_time):
        """
        This command is used to update line end time
        ex
        update_line_end_time lineid new_end_time
        """
        self.schedules[sch_id].update_line_end_time(
            int(lineid), int(new_end_time))

    @auth
    def update_line_time_between_trips(self, sch_id, lineid, time_between_trips):
        """
        This command is used to update line start time
        """
        self.schedules[sch_id].update_line_time_between_trips(
            int(lineid), int(time_between_trips))

    @auth
    def update_line_description(self, sch_id, lineid, description):
        """
        This command is used to update line start time
        """
        self.schedules[sch_id].update_line_start_time(int(lineid), description)

    @auth
    def get_stop_info(self, sch_id, stopid):
        """
        This commnand return infomation about a stop
        """
        data = self.schedules[sch_id].stopinfo(int(stopid))
        return data

    @auth
    def get_line_info(self, sch_id, lineid):
        """
        This commnand return infomation about a line
        ex
        get_line_info lineid
        """
        data = self.schedules[sch_id].lineinfo(int(lineid))
        return data

    ############################# LINES END ################################
