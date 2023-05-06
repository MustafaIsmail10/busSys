
from Map import Map
from Scheduale import Schedule
import threading as th
from User import User


class ScheduleProxy():
    def __init__(self, user, sys_map: Map, name, sch_id):
        self._schedule = Schedule(sys_map, name, sch_id)
        self.lock = th.RLock()
        self.users = [user]
        self.sch_id = sch_id

    def synched(func):
        def synchronize(self, *args, **kwargs):
            with self.lock:
                return func(self, *args, **kwargs)
        return synchronize

    def notify(func):
        def notification(self, *args, **kwargs):
                res = func(self, *args, **kwargs)
                for user in self.users:
                    user.notify(res)
                return res
        return notification

    @synched
    def test(self):
        print("using the lock")

    @synched
    @notify
    def register(self, user):
        self.users.append(user)
        return f"New User {user} is registered to schedule with id {self.sch_id}\n"

    @synched
    def unregister(self, user):
        self.users.remove(user)

    @synched
    def add_route(self):
        return self._schedule.add_route()

    @synched
    def get_route(self, routeid):
        return self._schedule.get_route(routeid)

    @synched
    def get_route_info(self, route_id):
        return self._schedule.get_route_info(route_id)

    @synched
    def get_routes(self):
        return self._schedule.get_routes()

    @synched
    def del_route(self, routeid):
        return self._schedule.del_route(routeid)

    @synched
    def get_stops(self):
        return self._schedule.get_stops()

    @synched
    def add_stop(self, edgeid,  direction, percentage,  description):
        return self._schedule.add_stop(
            edgeid,  direction, percentage,  description)

    @synched
    def del_stop(self, stop_id):
        return self._schedule.del_stop(stop_id)

    @synched
    def add_stop_to_route(self, route_id, stop_id, wait_time):
        return self._schedule.add_stop_to_route(route_id, stop_id, wait_time)

    @synched
    def del_stop_from_route(self, route_id, stop_id):
        return self._schedule.del_stop_from_route(route_id, stop_id)

    @synched
    def change_stop_wait(self, route_id, stop_id, wait):
        return self._schedule.change_stop_wait(route_id, stop_id, wait)

    @synched
    def addline(self, name, start_time, end_time, time_between_trips, routeid, description):
        return self._schedule.addline(name, start_time, end_time, time_between_trips, routeid, description)

    @synched
    def get_lines(self):
        return self._schedule.get_lines()

    @synched
    def lineinfo(self, lineid):
        return self._schedule.lineinfo(lineid)

    @synched
    def del_line(self, lineid):
        return self._schedule.del_line(lineid)

    @synched
    def update_line_name(self, lineid, name):
        return self._schedule.update_line_name(lineid, name)

    @synched
    def update_line_start_time(self, lineid, start_time):
        return self._schedule.update_line_start_time(lineid, start_time)

    @synched
    def update_line_end_time(self, lineid, end_time):
        return self._schedule.update_line_end_time(lineid, end_time)

    @synched
    def update_line_time_between_trips(self, lineid, time_between_trips):
        return self._schedule.update_line_time_between_trips(
            lineid, time_between_trips)

    @synched
    def update_line_description(self, lineid, description):
        return self._schedule.update_line_description(lineid, description)

    @synched
    def stopinfo(self, stopid):  # which lines pass by it and when
        return self._schedule.stopinfo(stopid)


    @synched
    def is_bus_at_stop(self,  lineid, stopid, curr_time):  
        return self._schedule.is_bus_at_stop(lineid, stopid, curr_time)
    

    @synched
    def get_line_stops_data(self, lineid):
        return self._schedule.get_line_stops_data(lineid)

# kwargs = {"path": "./test/test_map.json"}
# t = ScheduleProxy(Map( 1, **kwargs),"toto",0)
# t.test()
