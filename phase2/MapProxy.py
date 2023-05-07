from threading  import RLock
from Map import Map
from User import User

class MapProxy():
    def __init__(self, user, map_id ,**kwargs):
        self._map = Map(map_id, **kwargs)
        self.lock = RLock()
        self.users = [user]

    def synched( func):
        def synchronize(self, *args, **kwargs):
            with self.lock:
                return func(self, *args, **kwargs)
        return synchronize
    

    def notify(func):
        def notification(self, *args, **kwargs):
                res = func(self, *args, **kwargs)
                for user in self.users:
                    user.notify(res)
                return res
        return notification


    @synched
    def compute_edge_length(self, edge):
        return self._map.compute_edge_length(edge)

    @synched
    def get_users(self):
        return self.uesrs

    @synched
    @notify
    def register(self, user):
        self.users.append(user)

    @synched
    @notify
    def unregister(self, user):
        self.users.remove(user)

    @synched
    def shortest(self, node1, node2):
        return self._map.shortest(node1,node2)

    @synched
    def closestedge(self, loc):
        return self._map.closestedge(loc)

    @synched
    @notify
    def addstop(self, edgeid, direction, percentage, description):
        return self._map.addstop(edgeid,direction,percentage, description)
    
    @synched
    @notify
    def delstop(self, stopid):
        return self._map.delstop(stopid)

    @synched
    def getstop(self, stopid):
        return self._map.getstop(stopid)
    
    @synched
    def get_stops(self):
        return self._map.get_stops()
    
    @synched
    def stoptimeDistance(self, stop1: int, stop2: int):
        return self._map.stoptimeDistance(stop1,stop2)

    @synched 
    def shorteststop(self, location):
        return self._map.shorteststop(location)
    
    @synched
    def stops_within_r(self, location, radius):
        return self._map.stops_within_r(location,radius)
    
    @synched
    def __str__(self):
        return str(self._map)