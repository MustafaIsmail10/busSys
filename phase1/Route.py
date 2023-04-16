import Map


class Route:
    """
    Route represents a list of ordered stops based on user preference,
    along with the wait times at each stop stored with the stop id in a dict.
    Also keeps track of start node
    receives map in constructor to be able to form operations on stops
    """

    def __init__(self, mmap: Map, routeid):
        self.orderedStops = []
        self.stops = {}  # id and wait time
        self.start = -1
        self.map = mmap
        self.id = routeid

    def add_stop(self, stopid, wait):
        """
        Adds stops in order they come in with their wait times,
        tracks start for use in coming functions
        """
        if len(self.orderedStops) == 0:
            self.start = stopid
        self.orderedStops.append(stopid)
        self.stops[stopid] = wait

    def del_stop(self, stopid):
        """
        Delete a stop give the stopid and returns a boolean indication whether the operation is successful or not
        """
        if stopid in self.stops:
            del self.stops[stopid]
            self.orderedStops.remove(stopid)
            return True

        return False

    def change_stop_order(self, new_index, stopid):
        """
        Remove stop from old place in ordered list, then reinserts at desired location
        """
        if new_index == 0:
            self.set_start(stopid)
        else:
            old_index = self.orderedStops.index(stopid)
            del self.orderedStops[old_index]
            self.orderedStops.insert(new_index, stopid)

    def set_start(self, stopid):
        """
        Assumes stop is already in the list.
        removes old instance of the given stop
        then pushes it at the beginning of the list and updates start variable
        """
        self.start = stopid
        old_index = self.orderedStops.index(stopid)
        if self.orderedStops[0] == stopid:
            return
        del self.orderedStops[old_index]
        self.orderedStops.insert(0, stopid)

    def change_wait(self, stopid, new_wait):
        """
        edit the wait time of a stop
        """
        self.stops[stopid] = new_wait

    def get_stops_data(self):
        """
        Returns a list of triples which are (stop,arrival_time,leave_time)
        This function will be used in Line class functions.
        """
        # arrival time is the leave time of the previous stop + shortest time
        # from the previous stop and the current, found in Map class using stoptimeDistance().
        # For last element of list, only stop (which is start actually) and arrival time
        # are passed.
        first = self.orderedStops[0]
        route = []
        route.append((first, 0, self.stops[first]))  # stopid, starttime, leavetime
        for i in range(1, len(self.orderedStops)):
            second = self.orderedStops[i]
            result = self.map.stoptimeDistance(first, second)
            arrive = (
                result[1] + route[i - 1][2]
            )  # travel time + previous stop leave time
            leave = arrive + self.stops[second]  # add wait time
            route.append((second, arrive, leave))
            first = second
        last_trip = self.map.stoptimeDistance(
            self.orderedStops[-1], self.orderedStops[0]
        )
        arrive = last_trip[1] + route[-1][2]
        route.append((self.orderedStops[0], arrive))
        return route

    def get_time(self):
        """
        returns time it takes to finish the route
        (including wait time at stop and going back to start)
        """
        route = self.get_stops_data()
        #  the second element in result is that time when start is reached again
        return route[-1][1]

    def get_distance(self, map):
        """
        Takes in a map.
        Returns whole distance covered by route.

        """
        # goes over each 2 stops and gets the shortest distance between them.
        # Adds them all up and adds to them the time to go back to start
        # from the last stop in the list.
        # Shortest distance is found using first element of return object
        # of stoptimeDistance() from Map class
        stop1 = self.start
        dist = 0
        for i in range(1, len(self.orderedStops)):
            stop2 = self.orderedStops[i]
            dist += self.map.stoptimeDistance(stop1, stop2)[0]
            stop1 = stop2
        back = self.map.stoptimeDistance(self.orderedStops[-1], self.start)[
            0
        ]  # distance going back
        return dist + back

    def get_stops(self):
        """
        Returns dictionary of stops with stopid as key and wait time as value.
        """
        return self.orderedStops

    def __str__(self) -> str:
        return f"routeid: {self.id}, stops: {self.get_stops_data()}"
