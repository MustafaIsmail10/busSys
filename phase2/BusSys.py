from User import User
from ScheduleProxy import ScheduleProxy
from MapProxy import MapProxy
from threading import RLock, Semaphore, Thread
from Exceptions import *
from time import sleep
from Simulator import Simulator


def auth(method):
    """
    This decorator is used to handle authorization in the system by comparing the passed tokens and the user token
    """
    def f(self, user, token, *args, **kwargs):
        if user.is_authenticated(token):
            return method(self, user, *args, **kwargs)
        else:
            raise UserNotAuthenticated("Invalid Access. User is not authenticated")

    return f


class Singleton:
    def __new__(cls, *a, **b):
        if hasattr(cls, "_inst"):
            return cls._inst
        else:
            cls._inst = super().__new__(cls, *a, **b)
            return cls._inst


class BusSys(Singleton):
    """
    This class shall be the main controller of the system. It's a singiliton class and uses reader/writers kind of snyc
    """

    def __init__(self):
        self.schedules = {}
        self.maps = {}
        self.users = {}
        self.ids = 0
        self.sem = Semaphore(1)
        self.write = Semaphore(1)
        self.read_count = 0

    def reader(func):
        """
        This is a decorator used to mark functions that can be read by multiple threads in paralled
        """
        def synchronize(self, *args, **kwargs):
            self.sem.acquire()
            self.read_count += 1
            if self.read_count == 1:
                self.write.acquire()
            self.sem.release()
            res = func(self, *args, **kwargs)
            self.sem.acquire()
            self.read_count -= 1
            if self.read_count == 0:
                self.write.release()
            self.sem.release()
            return res

        return synchronize

    def writer(func):
        """
        This is a decorator used to mark functions that when accessed by a thread no more threads can access bussys 
        """
        def synchronize(self, *args, **kwargs):
            self.write.acquire()
            res = func(self, *args, **kwargs)
            self.write.release()
            return res

        return synchronize

    def add_user(self, user):
        """
        When adding new user. Since this manipulates a data structue that can accessed by many threads. When any thread is executing this method all other threads are suspended
        """
        if user.get_id():
            return
        else:
            new_id = self.ids
            self.ids += 1
            user.change_id(new_id)
            self.users[new_id] = user
    
    @writer
    def register(self, username, passwd):
        user = User()
        token = user.register(username, passwd)
        self.add_user(user)
        return (user, token)


    @reader
    def login(self, username, passwd):
        """
        This function is used to login a user with uesr_name and passwd
        """
        for user in self.users:
            if username == self.users[user].get_username():
                token =  self.users[user].login(passwd)
                return (self.users[user], token)

        return (None, None)
    

    @reader
    def login_with_token(self, token):
        """
        This function is used to login a user with uesr_name and passwd
        """
        for user in self.users:
            if self.users[user].is_token(token):
                print(self.users)
                return self.users[user]

        return None


    @reader
    @auth
    def get_username(self, user):
        return str(user.get_username()) + "\n"

    @writer
    @auth
    def add_map(self, user, type, mmap):
        """
        This function is used to add a map to the system. Type indicates the type of input
        type = 0 for path of the map on the server
        type = 1 for a map given as a json string 
        """
        new_id = self.ids
        self.ids += 1
        kwargs = None
        if int(type) == 1:
            kwargs = {"json": mmap}
        else:
            kwargs = {"path": mmap}

        new_map = MapProxy(user, new_id, **kwargs)
        self.maps[new_id] = new_map
        user.add_map(new_id)
        return str(new_map)

    @reader
    @auth
    def get_map(self, user, map_id):
        """
        This function is used to get a map with a specific id 
        """
        resutl = str(self.maps[int(map_id)])
        return resutl

    @reader
    @auth
    def get_maps(self, user):
        """
        This function is used to get all the maps in the system
        """
        result = ""
        for mapid in self.maps:
            result += f"{str(self.maps[mapid])}\n"
        return result

    @reader
    @auth
    def register_to_map(self, user, mapid):
        """
        This function is used by a user to register himself to a map in the system
        """
        self.maps[int(mapid)].register(user)
        return f"You are registered to map with id {mapid}\n"


    @writer
    @auth
    def add_schedule(self, user, map_id, name):
        """
        This function is used to add a new schedule to the system
        """
        new_id = self.ids
        self.ids += 1
        new_schedule = ScheduleProxy(user, self.maps[int(map_id)], name, new_id)
        self.schedules[new_id] = new_schedule
        user.add_schedule(new_id)
        return str(new_schedule)

    @reader
    @auth
    def get_schedule(self, user, schdule_id):
        """
        Returns a specific schedule
        """
        return str(self.schedules[int(schdule_id)])

    @reader
    @auth
    def get_schedules(self, user):
        """
        Returns all schedules in the system
        """
        result = ""
        for sch_id in self.schedules:
            result += f"({str(self.schedules[sch_id])})\n"
        return result

    @reader
    @auth
    def simulate(self, user, sch_id, start_time, end_time):
        """
        This fucntion is used to run the simulator. It takes schedule id ,start time,and end time as inputs
        """
        sim = Simulator(user, self.schedules[int(sch_id)], int(start_time), int(end_time))
        sim.run()
        stt = sim.get_statistics()
        print("OMG BUG IN HERE")
        return stt

    @reader
    @auth
    def register_to_schedule(self, user, sch_id):
        """
        This function is used by a user to register to a specific schedule
        """
        return self.schedules[int(sch_id)].register(user)

    ################################### STOPS START #############################
    @reader
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

    @reader
    @auth
    def add_stop(self, user, sch_id, edgeid, directoin, percentage, description):
        """
        This command is used to add a new stop
        """
        stop_id = self.schedules[int(sch_id)].add_stop(
            int(edgeid), bool(directoin), int(percentage), description
        )
        return f"A new stop with id {str(stop_id)} is added to the system\n"

    @reader
    @auth
    def del_stop(self, user, sch_id, stop_id):
        """
        This command is used to delete a stop
        """
        self.schedules[int(sch_id)].del_stop(int(stop_id))
        return f"The stop with {stop_id} that belongs to schadule with schaduel id {sch_id} is deleted\n"

    ############################## STOPS END #####################

    ############################# ROUTES START #########################

    @reader
    @auth
    def add_route(self, user, sch_id):
        """
        This command is used to add a new empty route to the system
        """
        new_route_id = self.schedules[int(sch_id)].add_route()
        return f"A new route with id {new_route_id} is added to schedule with id {sch_id}\n"

    @reader
    @auth
    def get_route(self, user, sch_id, routeid):
        """
        This command is used to get route with route id from schedule with sch_id
        """
        route = self.schedules[int(sch_id)].get_route(int(routeid))
        return str(route) + "\n"

    @reader
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

    @reader
    @auth
    def add_stop_to_route(self, user, sch_id, routeid, stop_id, wait_time):
        """
        This command is used to a stop to a specific route
        """
        status = self.schedules[int(sch_id)].add_stop_to_route(
            int(routeid), int(stop_id), int(wait_time)
        )
        return f"A stop with Stopid {stop_id} is added to route with id {routeid} in schedule {sch_id}\n"

    @reader
    @auth
    def del_stop_from_route(self, user, sch_id, routeid, stop_id):
        """
        This command is used to remove a stop from a specific route
        """
        self.schedules[int(sch_id)].del_stop_from_route(int(routeid), int(stop_id))
        return f"A stop with Stopid {stop_id} is deleted from route {routeid} in schedule {sch_id}\n"

    @reader
    @auth
    def change_stop_wait(self, user, sch_id, routeid, stop_id, wait_time):
        """
        This command is used to change the wait time of a stop insied a route
        """
        self.schedules[int(sch_id)].change_stop_wait(
            int(routeid), int(stop_id), int(wait_time)
        )
        return f"A stop with Stopid {stop_id} is in route with {routeid} in schedule {sch_id}, wait time is chaned to {wait_time}\n"

    ############################# Routes END #########################

    ############################# LINES START ################################
    @reader
    @auth
    def add_line(
        self,
        user,
        sch_id,
        name,
        start_time,
        end_time,
        time_between_trips,
        routeid,
        description,
    ):
        """
        This command is used to add a line to the system
        """
        lineid = self.schedules[int(sch_id)].addline(
            name,
            int(start_time),
            int(end_time),
            int(time_between_trips),
            int(routeid),
            description,
        )
        return f"A new line with lineid {lineid} is added to the system\n"

    @reader
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

    @reader
    @auth
    def del_line(self, user, sch_id, lineid):
        """
        This command is used to delete line from the system
        """
        self.schedules[int(sch_id)].del_line(int(lineid))
        return f"Line with lineid {lineid} in schedule with id {sch_id} is deleted from the system\n"

    @reader
    @auth
    def update_line_name(self, user, sch_id, lineid, new_name):
        """
        This command is used to update line name
        """
        self.schedules[int(sch_id)].update_line_name(int(lineid), new_name)
        return f"Line with lineid {lineid} in schedule with id {sch_id} is name is changed to {new_name}\n"

    @reader
    @auth
    def update_line_start_time(self, user, sch_id, lineid, new_start_time):
        """
        This command is used to update line start time
        """
        self.schedules[int(sch_id)].update_line_start_time(
            int(lineid), int(new_start_time)
        )
        return f"Line with lineid {lineid} in schedule with id {sch_id} is start time is changed to {new_start_time}\n"

    @reader
    @auth
    def update_line_end_time(self, user, sch_id, lineid, new_end_time):
        """
        This command is used to update line end time
        ex
        update_line_end_time lineid new_end_time
        """
        self.schedules[int(sch_id)].update_line_end_time(int(lineid), int(new_end_time))
        return f"Line with lineid {lineid} in schedule with id {sch_id} is end time is changed to {new_end_time}\n"

    @reader
    @auth
    def update_line_time_between_trips(self, user, sch_id, lineid, time_between_trips):
        """
        This command is used to update line start time
        """
        self.schedules[int(sch_id)].update_line_time_between_trips(
            int(lineid), int(time_between_trips)
        )
        return f"Line with lineid {lineid} in schedule with id {sch_id} is time between trips is changed to {time_between_trips}\n"

    @reader
    @auth
    def update_line_description(self, user, sch_id, lineid, description):
        """
        This command is used to update line start time
        """
        self.schedules[int(sch_id)].update_line_start_time(int(lineid), description)
        return f"Line with lineid {lineid} in schedule with id {sch_id} is description is changed to {description}\n"

    @reader
    @auth
    def get_stop_info(self, user, sch_id, stopid):
        """
        This commnand return infomation about a stop
        """
        stop, stop_lines = self.schedules[int(sch_id)].stopinfo(int(stopid))
        return str(stop) + str(stop_lines) + "\n"

    @reader
    @auth
    def get_line_info(self, user, sch_id, lineid):
        """
        This commnand return infomation about a line
        ex
        get_line_info lineid
        """
        data = self.schedules[int(sch_id)].lineinfo(int(lineid))
        return data + "\n"

    ############################# LINES END ################################

    ############################# TESTING ##################################


#     @writer
#     @auth
#     def test_1_bus(self,  user, ):
#         print("Writing")
#         i = 0
#         while True:
#             i += 1

#     @reader
#     @auth
#     def test_2_bus(self, user, rid):
#         print("reading ", rid)
#         i = 0
#         while True:
#             i += 1


# def test_1(bus, user, token):
#     bus.test_1_bus(user, token)


# def test_2(bus, rid, user, token):
#     bus.test_2_bus(user, token, rid)


# busSys = BusSys()
# user = User()
# token = user.login()

# th1 = Thread(target=test_1, args=(busSys, user, token))
# th6 = Thread(target=test_1, args=(busSys, user, token))

# th2 = Thread(target=test_2, args=(busSys, 1, user, token))
# th3 = Thread(target=test_2, args=(busSys, 2, user, token))
# th4 = Thread(target=test_2, args=(busSys, 3, user, token))
# th5 = Thread(target=test_2, args=(busSys, 4, user, token))

# th2.start()
# th1.start()

# th3.start()
# th4.start()
# th5.start()
# th6.start()
