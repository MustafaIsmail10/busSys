from User import User
from Scheduale import Schedule
from Map import Map
from threading import RLock
from Exceptions import *


def auth(method):
    def f(self, user, token, *args, **kwargs):
        if user.is_authenticated(token):
            return method(self, user, *args, **kwargs)
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

    def add_user(self, user):
        if user.get_id():
            return
        else:
            new_id = self.ids
            self.ids += 1
            user.change_id(new_id)
            self.users[new_id] = user

    @auth
    def add_map(self, user, type, mmap):
        new_id = self.ids
        self.ids += 1
        kwargs = None
        if int(type) == 1:
            kwargs = {"json": mmap}
        else:
            kwargs = {"path": mmap}

        new_map = Map(new_id, **kwargs)
        self.maps[new_id] = new_map
        user.add_map(new_id)
        return str(new_map)

    @auth
    def get_map(self, user, map_id):
        return str(self.maps[int(map_id)])

    @auth
    def add_schedule(self, user, map_id, name):
        new_id = self.ids
        self.ids += 1
        new_schedule = Schedule(self.maps[int(map_id)], name, new_id)
        self.schedules[new_id] = new_schedule
        user.add_schedule(new_id)
        return str(new_schedule)

    @auth
    def get_schedule(self, user,  schdule_id):
        """
        Returns a specific schedule
        """
        return str(self.schedules[int(schdule_id)])

    ################################### STOPS START #############################
    @auth
    def get_stops(self, user, schdule_id):
        """
        This function is used to get all stops in the system
        """
        stops = self.schedules[int(schdule_id)].get_stops()
        result = "{"
        for s in stops:
            result += str(s) + ": "
            result += str(stops[s]) + ","
        result += "}\n"
        return result

    @auth
    def add_stop(self, user, sch_id, edgeid, directoin, percentage, description):
        """
        This command is used to add a new stop
        """
        stop_id = self.schedules[int(sch_id)].add_stop(
            int(edgeid), bool(directoin), int(percentage), description)
        return f"The id of the new stop is {str(stop_id)} is added to the system\n"

    @auth
    def del_stop(self, user, sch_id, stop_id):
        """
        This command is used to delete a stop
        """
        self.schedules[int(sch_id)].del_stop(int(stop_id))
        return f"The stop with {stop_id} that belongs to schadule with schaduel id {sch_id} is deleted\n"

    ############################## STOPS END #####################

    ############################# ROUTES START #########################

    @auth
    def add_route(self, user, sch_id):
        """
        This command is used to add a new empty route to the system
        """
        new_route_id = self.schedules[int(sch_id)].add_route()
        return f"A new route with id {new_route_id} is added to schedule with id {sch_id}\n"

    @auth
    def get_route(self, user, sch_id, routeid):
        """
        This command is used to get route with route id from schedule with sch_id
        """
        route = self.schedules[int(sch_id)].get_route(int(routeid))
        return str(route) + "\n"

    @auth
    def get_routes(self, user, sch_id):
        """
        This command is used to get all routes of the system in a schedule
        """
        routes = self.schedules[int(sch_id)].get_routes()
        result = "{"
        for s in routes:
            result += str(s) + ": "
            result += str(routes[s]) + ","
        result += "}\n"
        return result

    @auth
    def add_stop_to_route(self, user, sch_id, routeid, stop_id, wait_time):
        """
        This command is used to a stop to a specific route
        """
        status = self.schedules[int(sch_id)].add_stop_to_route(
            int(routeid), int(stop_id), int(wait_time))
        return f"A stop with Stopid {stop_id} is added to route with id {routeid} in schedule {sch_id}\n"

    @auth
    def del_stop_from_route(self, user, sch_id, routeid, stop_id):
        """
        This command is used to remove a stop from a specific route
        """
        self.schedules[int(sch_id)].del_stop_from_route(
            int(routeid), int(stop_id))
        return f"A stop with Stopid {stop_id} is deleted from route {routeid} in schedule {sch_id}\n"

    @auth
    def change_stop_wait(self, user, sch_id, routeid, stop_id, wait_time):
        """
        This command is used to change the wait time of a stop insied a route
        """
        self.schedules[int(sch_id)].change_stop_wait(
            int(routeid), int(stop_id), int(wait_time))
        return f"A stop with Stopid {stop_id} is in route with {routeid} in schedule {sch_id}, wait time is chaned to {wait_time}\n"

    ############################# Routes END #########################

    ############################# LINES START ################################

    @auth
    def add_line(self, user, sch_id, name, start_time, end_time, time_between_trips, routeid, description):
        """
        This command is used to add a line to the system
        """
        lineid = self.schedules[int(sch_id)].addline(
            name, int(start_time), int(end_time), int(
                time_between_trips), int(routeid), description
        )
        return f"A new line with lineid {lineid} is added to the system"

    @auth
    def get_lines(self, user, sch_id):
        """
        This command is used to print all line of the system
        """
        lines = self.schedules[int(sch_id)].get_lines()
        result = "{"
        for s in lines:
            result += str(s) + ": "
            result += str(lines[s]) + ","
        result += "}\n"
        return result

    @auth
    def del_line(self, user, sch_id,  lineid):
        """
        This command is used to delete line from the system
        """
        self.schedules[int(sch_id)].del_line(int(lineid))
        return f"Line with lineid {lineid} in schedule with id {sch_id} is deleted from the system\n"

    @auth
    def update_line_name(self, user, sch_id, lineid, new_name):
        """
        This command is used to update line name
        """
        self.schedules[int(sch_id)].update_line_name(int(lineid), new_name)
        return f"Line with lineid {lineid} in schedule with id {sch_id} is name is changed to {new_name}\n"



    @auth
    def update_line_start_time(self, user, sch_id,  lineid, new_start_time):
        """
        This command is used to update line start time
        """
        self.schedules[int(sch_id)].update_line_start_time(
            int(lineid), int(new_start_time))
        return 

    @auth
    def update_line_end_time(self, user, sch_id, lineid, new_end_time):
        """
        This command is used to update line end time
        ex
        update_line_end_time lineid new_end_time
        """
        self.schedules[int(sch_id)].update_line_end_time(
            int(lineid), int(new_end_time))

    @auth
    def update_line_time_between_trips(self, user, sch_id, lineid, time_between_trips):
        """
        This command is used to update line start time
        """
        self.schedules[int(sch_id)].update_line_time_between_trips(
            int(lineid), int(time_between_trips))

    @auth
    def update_line_description(self, user, sch_id, lineid, description):
        """
        This command is used to update line start time
        """
        self.schedules[int(sch_id)].update_line_start_time(
            int(lineid), description)

    @auth
    def get_stop_info(self, user, sch_id, stopid):
        """
        This commnand return infomation about a stop
        """
        data = self.schedules[int(sch_id)].stopinfo(int(stopid))
        return data

    @auth
    def get_line_info(self, user, sch_id, lineid):
        """
        This commnand return infomation about a line
        ex
        get_line_info lineid
        """
        data = self.schedules[int(sch_id)].lineinfo(int(lineid))
        return data

    ############################# LINES END ################################
