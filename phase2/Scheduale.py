from Route import Route
from Map import Map
from Line import Line

class Schedule:

    """
    This is the main class from which you can do everything in the system such as adding routes,stop, and lines
    """

    def __init__(self, sys_map: Map, name, sch_id):
        """
        The constructor which takes a map object as input 
        """
        self.map = sys_map
        self.routes = {}
        self.lines = {}
        self.route_count = 0
        self.line_count = 0
        self.name = name
        self.id = sch_id

    def add_route(self):
        """
        This function adds a new empty route and later stops and can be added to that route
        """
        self.route_count += 1
        new_route_id = self.route_count
        new_route = Route(self.map, new_route_id)
        self.routes[new_route_id] = new_route
        return new_route_id
    
    def get_route(self, routeid):
        """
        This function returns a route with its id as input
        """
        return self.routes[routeid]
    
    def get_route_info(self, route_id):
        """
        This function returns the stops of a route taking the route id as input 
        """
        return self.routes[route_id].get_stops()
    
    def get_routes(self):
        """
        This function returns all ruotes in the system
        """
        return self.routes
    

    def del_route(self, routeid):
        del self.routes[routeid]
        return True

    def get_stops(self):
        """
        This function returns all bus stops in the system
        """
        return self.map.bus_stops

    def add_stop(self, edgeid,  direction, percentage,  description):
        """
        This fucntion adds a bus stop to the system
        """
        stopid = self.map.addstop(edgeid,  direction, percentage,  description)
        return stopid

    def del_stop(self, stop_id):
        """
        This function removes a bus stop from the system
        """
        self.map.delstop(stop_id)
        for r in self.routes:
            self.routes[r].del_stop(stop_id)

    def add_stop_to_route(self, route_id, stop_id, wait_time):
        """
        This function adds existing bus stop to a route
        """
        self.routes[route_id].add_stop(stop_id, wait_time)    
        return True

    def del_stop_from_route(self, route_id, stop_id):
        """
        This function removes existing bus stop from a route
        """
        self.routes[route_id].del_stop(stop_id)  
          


    def change_stop_wait(self, route_id, stop_id, wait):
        """
        This fucntion changes the wait time of the bus in a specific stop in a specific route
        """
        self.routes[route_id].change_wait(stop_id, wait)

    def addline(self, name, start_time, end_time, time_between_trips, routeid, description):
        """
        This function adds a line to the system given the information of the line and the route that it will be assigned to. 
        """
        self.line_count += 1
        new_line = Line(self.line_count, name, start_time, end_time, time_between_trips, self.routes[routeid], description )
        self.lines[self.line_count] = new_line
        return self.line_count

    def get_lines(self):
        """
        This fucntion returns all the lines in the system
        """
        return self.lines
        
    def lineinfo(self, lineid):
        """
        This function returns line information
        """
        line = self.lines[lineid]
        return line.get_info()
    
    def del_line(self, lineid):
        """
        This fucntion deletes a line from the system
        """
        del self.lines[lineid]

    def update_line_name(self, lineid, name):
        """
        update line name
        """
        self.lines[lineid].update_name(name)

    def update_line_start_time(self, lineid, start_time):
        """
        update line start time
        """
        self.lines[lineid].update_start_time(start_time)


    def update_line_end_time(self, lineid, end_time):
        """
        update line end time
        """
        self.lines[lineid].update_end_time(end_time)



    def update_line_time_between_trips(self, lineid, time_between_trips):
        """
        update time between trips of a line
        """
        self.lines[lineid].update_time_between_trips(time_between_trips)
        

    def update_line_description(self, lineid, description):
        """
        update time between trips of a line
        """
        self.lines[lineid].update_description(description)



    def stopinfo(self, stopid):  # which lines pass by it and when
        info = {}
        for line in self.lines:
            if self.lines[line].is_stop_included(stopid):
                info[line] =  self.lines[line].get_stop_pass_times(stopid)
        return (self.map.getstop(stopid), info)


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
