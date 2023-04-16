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
        self.route_count += 1
        new_route_id = self.route_count
        new_route = Route(self.map, new_route_id)
        self.routes[new_route_id] = new_route
        return new_route_id
    
    def get_route(self, routeid):
        return self.routes[routeid]
    
    def get_route_info(self, route_id):
        return self.routes[route_id].get_stops()
    
    def get_routes(self):
        return self.routes

    def get_stops(self):
        return self.map.bus_stops

    def add_stop(self, edgeid,  direction, percentage,  description):
        stopid = self.map.addstop(edgeid,  direction, percentage,  description)
        return stopid

    def remove_stop(self, stop_id):
        self.map.delstop(stop_id)
        for r in self.routes:
            self.routes[r].del_stop(stop_id)

    def add_stop_to_route(self, route_id, stop_id, wait_time):
        self.routes[route_id].add_stop(stop_id, wait_time)    


    def change_stop_wait(self, route_id, stop_id, wait):
        self.routes[route_id].change_wait(stop_id, wait)

    def addline(self, name, start_time, end_time, time_between_trips, routeid, description):
        self.line_count += 1
        new_line = Line(self.line_count, name, start_time, end_time, time_between_trips, self.routes[routeid], description )
        self.lines[self.line_count] = new_line
        return self.line_count

    def removeline(self, line_id):
        del self.lines[line_id]

    def get_lines(self):
        return self.lines
        
    def lineinfo(self, lineid):
        line = self.lines[lineid]
        return line.get_info()
    
    def del_line(self, lineid):
        del self.lines[lineid]

    def update_line_name(self, lineid, name):
        self.lines[lineid].update_name(name)

    def stopinfo(self, stopid):  # which lines pass by it and when
        info = {}
        for line in self.lines:
            if self.lines[line].is_stop_included(stopid):
                info[line] =  self.lines[line].get_stop_pass_times(stopid)
        return info


# if __name__ == "__main__":
#     my_map = Map(path="./test/test_map.json")
#     my_schedule = Schedule(my_map)
#     stopid1 = my_schedule.add_stop(1, False, 50, "Nice stop")
#     stopid2 = my_schedule.add_stop(2, True, 50, "Nice stop")

#     print(my_schedule.map.stoptimeDistance(stopid1, stopid2))

#     routeid = my_schedule.add_route()
#     my_schedule.add_stop_to_route(routeid, stopid1, 2)
#     my_schedule.add_stop_to_route(routeid, stopid2, 2)

#     route = my_schedule.get_route_info(routeid)
#     print(route)

#     my_schedule.change_stop_wait(routeid, stopid1, 10)
#     route = my_schedule.get_route_info(routeid)
#     print(route)
#     my_schedule.map.print_stops()

    # self.routes = {
    #     id: Route
    # }

    # self.lines = {
    #     id: Line
    # }
