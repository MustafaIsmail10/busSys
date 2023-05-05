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
    def print_hello(self, message):
        print("hello", message)

    @auth
    def get_schedule(self, schdule_id):
        """
        Returns a specific schedule
        """
        return self.schedules[schdule_id]

    @auth
    def get_stops(self, schdule_id):
        """
        This function is used to get all stops in the system
        ex
        print_stops
        """
        stops = self.schedules[schdule_id].get_stops()
        return stops

    @auth
    def add_schedule(self, map_id, name):
        with self.mutex:
            new_id = self.ids
            self.ids += 1
            new_schedule = Schedule(self.maps[map_id], name, new_id)
            self.schedules[new_id] = new_schedule
            return new_id

    @auth
    def add_map(self, **kwargs):
        with self.mutex:
            new_id = self.ids
            self.ids += 1
            new_map = Map(**kwargs)
            self.maps[new_id] = new_map
            return new_id

    def add_stop(self, sch_id , edgeid, directoin, percentage, description):
        """
        This command is used to add a new stop
        ex
        add_stop edgeid directoin percentage "description"
        """
        stop_id = self.schedules[sch_id].add_stop(int(edgeid), bool(directoin), int(percentage), description)
        return stop_id


    # def do_del_stop(self, args):
    #     """
    #     This command is used to delete a stop
    #     ex
    #     del_stop stopid
    #     """
    #     Sys.schedule.remove_stop(int(args))

    # def do_add_route(self, args):
    #     """
    #     This command is used to add a new empty route to the system
    #     ex
    #     add_route
    #     """
    #     new_route_id = Sys.schedule.add_route()
    #     print(f"The new route id is {new_route_id}")

    # def do_print_route_info(self, args):
    #     """
    #     This command is used to print route info taking the routeid as input
    #     ex
    #     print_route_info routeid
    #     """
    #     route = Sys.schedule.get_route(int(args))
    #     print(route)

    # def do_print_routes(self, args):
    #     """
    #     This command is used to print all routes of the system
    #     ex
    #     print_routes
    #     """
    #     routes = Sys.schedule.get_routes()
    #     for route in routes:
    #         print(routes[route])

    # def do_add_stop_to_route(self, args):
    #     """
    #     This command is used to a stop to a specific route
    #     ex
    #     add_stop_to_route routeid stop_id wait_time
    #     """
    #     ar = args.split(" ")
    #     Sys.schedule.add_stop_to_route(int(ar[0]), int(ar[1]), int(ar[2]))

    # def do_del_stop_from_route(self, args):
    #     """
    #     This command is used to remove a stop from a specific route
    #     ex
    #     del_stop_from_route routeid stop_id
    #     """
    #     ar = args.split(" ")
    #     Sys.schedule.del_stop_from_route(int(ar[0]), int(ar[1]))

    # def do_change_stop_wait(self, args):
    #     """
    #     This command is used to change the wait time of a stop insied a route
    #     ex
    #     change_stop_time routeid stopid wait_time
    #     """
    #     ar = args.split(" ")
    #     Sys.schedule.change_stop_wait(int([ar[0]]), int(ar[1]), int(ar[2]))

    # def do_del_stop(self, args):
    #     """
    #     This command is used to remove a stop from the system
    #     ex
    #     del_stop stop_id
    #     """
    #     Sys.schedule.del_stop(int(args))

    # def do_add_line(self, args):
    #     """
    #     This command is used to add a line to the system
    #     ex
    #     add_line name start_time end_time time_between_trips routeid "description"
    #     """
    #     ar = args.split(" ")
    #     Sys.schedule.addline(
    #         ar[0], int(ar[1]), int(ar[2]), int(ar[3]), int(ar[4]), int(ar[5])
    #     )

    # def do_print_lines(self, args):
    #     """
    #     This command is used to print all line of the system
    #     ex
    #     print_lines
    #     """
    #     lines = Sys.schedule.get_lines()
    #     for line in lines:
    #         print(str(lines[line]))

    # def do_del_line(self, args):
    #     """
    #     This command is used to delete line from the system
    #     ex
    #     del_line lineid
    #     """
    #     Sys.schedule.del_line(int(args))

    # def do_update_line_name(self, args):
    #     """
    #     This command is used to update line name
    #     ex
    #     update_line_name lineid new_name
    #     """
    #     ar = args.split(" ")
    #     Sys.schedule.update_line_name(int(ar[0]), ar[1])

    # def do_update_line_start_time(self, args):
    #     """
    #     This command is used to update line start time
    #     ex
    #     update_line_start_time lineid new_start_time
    #     """
    #     ar = args.split(" ")
    #     Sys.schedule.update_line_start_time(int(ar[0]), int(ar[1]))

    # def do_update_line_end_time(self, args):
    #     """
    #     This command is used to update line end time
    #     ex
    #     update_line_end_time lineid new_end_time
    #     """
    #     ar = args.split(" ")
    #     Sys.schedule.update_line_end_time(int(ar[0]), int(ar[1]))

    # def do_update_line_time_between_trips(self, args):
    #     """
    #     This command is used to update line start time
    #     ex
    #     update_line_time_between_trip lineid time_between_trips
    #     """
    #     ar = args.split(" ")
    #     Sys.schedule.update_line_time_between_trips(int(ar[0]), int(ar[1]))

    # def do_update_line_description(self, args):
    #     """
    #     This command is used to update line start time
    #     ex
    #     update_line_description lineid "description"
    #     """
    #     ar = args.split(" ")
    #     Sys.schedule.update_line_start_time(int(ar[0]), ar[1])

    # def do_get_stop_info(self, args):
    #     """
    #     This commnand return infomation about a stop
    #     ex
    #     get_stop_info stopid
    #     """
    #     data = Sys.schedule.stopinfo(int(args))
    #     print(str(data[0]))
    #     print(data[1])

    # def do_get_line_info(self, args):
    #     """
    #     This commnand return infomation about a line
    #     ex
    #     get_line_info lineid
    #     """
    #     data = Sys.schedule.lineinfo(int(args))
    #     print(data)


u = User()
t = u.login()
sysBus = BusSys()
sysBus.print_hello(u, t, "Hello from the outer")


# sysBus.print_hello(u, t ,"Hello from the outer")
