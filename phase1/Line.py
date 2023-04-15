import math
from Route import Route

class Line:

    def __init__(self, lineid ,name, start_time, end_time, time_between_trips, route, description=""):
        """
        start_time and end_time are miniutes from starting from mid night
        a route of the Route class should be given
        """
        self.route:Route = route
        self.name = name
        self.start_time = start_time
        self.end_time = end_time
        self.time_between_trips = time_between_trips
        self.id = lineid  # id must be generated for each line
        self.description = description

    def get_bus_num(self):
        trip_time = self.route.get_time()
        return math.ceil(trip_time/self.time_between_trips)

    def get_trips_num(self):
        """
        return the number of trips that will be conducted
        """
        total_time = (self.end_time - self.start_time) % 1440
        return total_time/self.time_between_trips
    

    def get_stop_pass_times(self, stopid):
        stops = self.route.get_stops()
        passing_time_from_start = None
        passing_times = []
        for stop in stops:
            if stop[0] == stopid:
                passing_time_from_start = stop[1]
                break
        if not passing_time_from_start:
            raise Exception("Stop was not found in the route of this line")
        
        time = self.start_time + passing_time_from_start
        while time <= self.end_time + self.time_between_trips:
            passing_times.append(time)
            time += self.time_between_trips



