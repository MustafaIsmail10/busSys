from Route import Route
from Map import Map
from Line import Line

class Schedule:

    def __init__(self, sys_map: Map):
        self.map = sys_map
        self.routes = {}
        self.lines = {}
        self.route_count = 0
        self.line_count = 0

    def add_route(self):
        new_route = Route(self.map)
        self.route_count += 1
        new_route_id = self.route_count
        self.routes[new_route_id] = new_route
        return new_route_id

    def get_stops(self):
        return self.map.bus_stops

    def add_stop(self, edgeid,  direction, percentage,  description):
        stopid = self.map.addstop(edgeid,  direction, percentage,  description)
        return stopid

    def remove_stop(self, stop_id):
        self.map.delstop(stop_id)

    def add_stop_to_route(self, route_id, stop_id, wait_time):
        self.routes[route_id].add_stop(stop_id, wait_time)

    def get_route_info(self, route_id):
        return self.routes[route_id].get_route()

    def change_stop_wait(self, route_id, stop_id, wait):
        self.routes[route_id].change_wait(stop_id, wait)

    def addline(self, name, start_time, end_time, time_between_trips, route, description):
        new_line = Line(name, start_time, end_time, time_between_trips, route, description )
        self.line_count += 1
        self.lines[self.line_count] = new_line
        return self.line_count
        

    def removeline(self, line_id):
        del self.lines[line_id]
        

    def lineinfo(self):
        pass

    def stopinfo(self):  # which lines pass by it and when
        pass


if __name__ == "__main__":
    my_map = Map(path="./test/test_map.json")
    my_schedule = Schedule(my_map)
    stopid1 = my_schedule.add_stop(1, False, 50, "Nice stop")
    stopid2 = my_schedule.add_stop(2, True, 50, "Nice stop")

    print(my_schedule.map.stoptimeDistance(stopid1, stopid2))

    routeid = my_schedule.add_route()
    my_schedule.add_stop_to_route(routeid, stopid1, 2)
    my_schedule.add_stop_to_route(routeid, stopid2, 2)

    route = my_schedule.get_route_info(routeid)
    print(route)

    my_schedule.change_stop_wait(routeid, stopid1, 10)
    route = my_schedule.get_route_info(routeid)
    print(route)
    my_schedule.map.print_stops()

    # self.routes = {
    #     id: Route
    # }

    # self.lines = {
    #     id: Line
    # }
