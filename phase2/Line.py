import math
from Route import Route


class Line:
    def __init__(
        self,
        lineid,
        name,
        start_time,
        end_time,
        time_between_trips,
        route,
        description="",
    ):
        """
        start_time and end_time are int miniutes from mid night
        a Route object of the Route class should be given
        """
        self.route: Route = route
        self.name = name
        self.start_time = start_time
        self.end_time = end_time
        self.time_between_trips = time_between_trips
        self.lineid = lineid  # id must be generated for each line
        self.description = description

    def get_bus_num(self):
        """
        return the number of busses needed to execute the route with the required time_between_trips
        """
        trip_time = self.route.get_time()
        return math.ceil(trip_time / self.time_between_trips)

    def get_trips_num(self):
        """
        return the number of trips that will be conducted
        """
        total_time = (self.end_time - self.start_time) % 1440
        return total_time / self.time_between_trips

    def get_stop_pass_times(self, stopid):
        """
        This function takes a stopid as input and returns the times that the busses following the line would pass this stop
        """
        stops = self.route.get_stops_data()
        passing_time_from_start = None
        passing_times = []
        for stop in stops:
            if stop[0] == stopid:
                passing_time_from_start = stop[1]

                break
        if passing_time_from_start == None:
            raise Exception("Stop was not found in the route of this line")

        time = self.start_time + passing_time_from_start
        while time <= self.end_time + self.time_between_trips:
            passing_times.append(time)
            time += self.time_between_trips

        # This passing_times list contains a list of times in minutes in which the line would pass the stop from the start of the pass
        return passing_times

    def is_stop_included(self, stopid):
        """
        Checks if a stop is included in a line
        """
        stops = self.route.get_stops()
        for stop in stops:
            if stop == stopid:
                return True
        return False

    def get_line_stops(self):
        """
        Returns a list of all stops in the line
        """
        return self.route.get_stops()

    def get_info(self):
        """
        Returns various info about the line
        """
        return (
            self.lineid,
            self.name,
            self.start_time,
            self.end_time,
            self.time_between_trips,
            self.description,
            self.get_line_stops(),
        )

    def update_name(self, name):
        """
        Updates the name of the line
        """
        self.name = name

    def update_start_time(self, start_time):
        """
        Updates the start_time of the line
        """
        self.start_time = start_time

    def update_end_time(self, end_time):
        """
        Updates the end time of the line
        """
        self.end_time = end_time

    def update_time_between_trips(self, time):
        """
        Updates the time between trips for a line
        """
        self.time_between_trips = time

    def update_description(self, description):
        """
        Updates the desciption of the line
        """
        self.description = description

    def __str__(self) -> str:
        return str(self.get_info())

    def is_bus_at_stop(self, stopid, curr_time):
        '''
        Checks if bus is at the stop, returns a tuple containing bus number and a boolean value
        '''
        stop_pass_times = self.get_stop_pass_times(stopid)
        for i in range(len(stop_pass_times)):
            if curr_time < stop_pass_times[i]+ self.route.get_stop_wait(stopid) and curr_time > stop_pass_times[i]:
                return (i +1, True)     
        return (None, False)
    
    def get_journey_times(self):
        start_times = []
        curr_time = self.start_time
        while curr_time < self.end_time:
            start_times.append(curr_time)
            curr_time += self.time_between_trips
        return start_times

    def get_stops_data(self):
        return self.route.get_stops_data()
    

    def get_line_distance(self):
        """
        Returns whole distance covered by route of Line.
        """
        return self.route.get_distance()
    

    def get_distance_until_stop(self, stopid):
        '''
        Finds the distance to a stop with given stop id
        '''
        return self.route.get_distance_until_stop(stopid)