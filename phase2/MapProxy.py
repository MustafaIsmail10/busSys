from threading  import RLock
from Map import Map
from User import User

class MapProxy():
    '''
    The main purpose of this class is to handle 
    the synchronization of the threads such that when 
    functions in the map are called, no 2 threads 
    can edit at the same time and no edit and read
    can happen at the same time.
    It is like a layer of protection for our data, to
    avoid corruption.
    During initialisation the arguments needed to 
    create a map are passed along with a map id and
    the user which is added to the list of users registered 
    to this map.
    Also a lock is created during initialisation.
    '''
    def __init__(self, user, map_id ,**kwargs):
        self._map = Map(map_id, **kwargs)
        self.lock = RLock()
        self.users = [user]


    def synched( func):
        '''
        This is the decorator that decorates all 
        the functions calling the map functions.
        It uses the lock to be able to call the 
        function
        '''
        def synchronize(self, *args, **kwargs):
            with self.lock:
                return func(self, *args, **kwargs)
        return synchronize
    

    def notify(func):
        '''
        This decorator is used to notify users
        when changes happen, including user registering
        to the map, adding stops in the map,
        deleting and such.
        '''
        def notification(self, *args, **kwargs):
                res = func(self, *args, **kwargs)
                for user in self.users:
                    user.notify(res)
                return res
        return notification


    
    @synched
    def compute_edge_length(self, edge):
        '''
        This function returns the computed 
        edge length of edge with given id
        by calling the implemented function in map
        '''
        return self._map.compute_edge_length(edge)

    @synched
    def get_users(self):
        '''
        This function returns current registered users
        '''
        return self.users

    @synched
    @notify
    def register(self, user):
        '''
        This function registers users to the map
        '''
        self.users.append(user)

    @synched
    @notify
    def unregister(self, user):
        '''
        This function unregisters user from map
        '''
        self.users.remove(user)

    @synched
    def shortest(self, node1, node2):
        '''
        This function returns the shortest path 
        It returns a tuple of 3 (edgeid, distace in kilometers, time in minutes)
        It calls the implemented function in map
        '''
        return self._map.shortest(node1,node2)

    @synched
    def closestedge(self, loc):
        '''
        This function returns the closest 
        edge to the given location
        by calling the implemented function in map
        '''
        return self._map.closestedge(loc)

    @synched
    @notify
    def addstop(self, edgeid, direction, percentage, description):
        '''
        This function adds a stop to the  
        edge with given id at percentage with direction and a description
        by calling the implemented function in map
        '''
        return self._map.addstop(edgeid,direction,percentage, description)
    
    @synched
    @notify
    def delstop(self, stopid):
        '''
        This function removes a stop with given stop id
        by calling the implemented function in map
        '''
        return self._map.delstop(stopid)

    @synched
    def getstop(self, stopid):
        '''
        This function gets a stop with given stop id
        by calling the implemented function in map
        '''
        return self._map.getstop(stopid)
    
    @synched
    def get_stops(self):
        '''
        This function gets all stops
        by calling the implemented function in map
        '''
        return self._map.get_stops()
    
    @synched
    def stoptimeDistance(self, stop1: int, stop2: int):
        '''
        Gets the shortest distance and time between 2 stops, returns them in tuple.
        Calls implementation in map
        '''
        return self._map.stoptimeDistance(stop1,stop2)

    @synched 
    def shorteststop(self, location):
        """
        Takes a location and returns the id of the closet stop to that location if any.
        Calls implementation in map
        """
        return self._map.shorteststop(location)
    
    @synched
    def stops_within_r(self, location, radius):
        '''
        This function finds all stop that are at a
        radius k away from the given location,
        by calling the implemented function in map
        '''
        return self._map.stops_within_r(location,radius)
    
    @synched
    def __str__(self):
        '''
        Representation of map
        '''
        return str(self._map)