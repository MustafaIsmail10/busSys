from Route import Route
from Map import Map


class Schedule:


    def __init__(self, map: Map):
        self.map
        self.stops = map.busStops
        self.routes = {}
        self.lines = {}
        self.route_count = 0
        pass

    def add_route(self):
        new_route = Route(self.map)
        Schedule.route_count += 1
        new_route_id = Schedule.route_count
        self.routes[new_route_id] = new_route

    def addline():
        pass

    def removeline():
        pass

    def lineinfo():
        pass

    def stopinfo():  # which lines pass by it and when
        pass

    # self.routes = {
    #     id: Route
    # }

    # self.lines = {
    #     id: Line
    # }
