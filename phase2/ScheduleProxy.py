
from Map import Map
from Scheduale import Schedule
import threading as th


class ScheduleProxy():
    def __init__(self, sys_map: Map):
        self._schedule = Schedule.__init__(sys_map)
        self.lock = th.Rlock()

    def synched(self, func):
        def synchronize(*args, **kwargs):
            with self.lock:
                return func(*args, **kwargs)
        return synchronize

    @synched
    def add_route(self):  
        self.schedule.add_route()

    @synched
    def get_route(self, routeid):
        self.schedule.get_route(routeid)

    @synched
    def get_route_info(self, route_id):
        self.schedule.get_route_info(route_id)

    @synched
    def get_routes(self):
        self.schedule.get_routes()

    @synched
    def del_route(self, routeid):
        self.schedule.del_route(routeid)

    @synched
    def get_stops(self):     
        self.schedule.get_stops()
        
    @synched
    def add_stop(self, edgeid,  direction, percentage,  description):
        self.schedule.add_stop(
                edgeid,  direction, percentage,  description)

    def del_stop(self, stop_id):
        with self.lock:
            self.schedule.del_stop(stop_id)

    def add_stop_to_route(self, route_id, stop_id, wait_time):
        with self.lock:
            self.schedule.add_stop_to_route(route_id, stop_id, wait_time)

    def del_stop_from_route(self, route_id, stop_id):
        with self.lock:
            self.schedule.del_stop_from_route(route_id, stop_id)

    def change_stop_wait(self, route_id, stop_id, wait):
        with self.lock:
            self.schedule.change_stop_wait(route_id, stop_id, wait)

    def addline(self, name, start_time, end_time, time_between_trips, routeid, description):
        with self.lock:
            self.schedule.addline(name, start_time, end_time, time_between_trips, routeid, description)

    def get_lines(self):
        with self.lock:
            self.schedule.get_lines()

    def lineinfo(self, lineid):
        with self.lock:
            self.schedule.lineinfo(lineid)

    def del_line(self, lineid):
        with self.lock:
            self.schedule.del_line(lineid)

    def update_line_name(self, lineid, name):
        with self.lock:
            self.schedule.update_line_name(lineid, name)

    def update_line_start_time(self, lineid, start_time):
        with self.lock:
            self.schedule.update_line_start_time(lineid, start_time)

    def update_line_end_time(self, lineid, end_time):
        with self.lock:
            self.schedule.update_line_end_time(lineid, end_time)

    def update_line_time_between_trips(self, lineid, time_between_trips):
        with self.lock:
            self.schedule.update_line_time_between_trips(
                lineid, time_between_trips)

    def update_line_description(self, lineid, description):
        with self.lock:
            self.schedule.update_line_description(lineid, description)

    def stopinfo(self, stopid):  # which lines pass by it and when
        with self.lock:
            self.schedule.stopinfo(stopid)
