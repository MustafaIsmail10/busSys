import math


class Line:

    def __init__(self, name, start_time, end_time, time_between_trips, route, description=""):
        """
        start_time and end_time are miniutes from starting from mid night
        a route of the Route class should be given
        """
        self.route = route
        self.name = name
        self.start_time = start_time
        self.end_time = end_time
        self.time_between_trips = time_between_trips
        self.id = None  # id must be generated for each line
        self.description = description

    def get_bus_num(self):
        trip_time = route.get_time()
        return math.ceil(trip_time/self.time_between_trips)

    def get_trips_num(self):
        """
        return the number of trips that will be conducted
        """
        total_time = (self.end_time - self.start_time) % 1440
        return total_time/self.time_between_trips
    