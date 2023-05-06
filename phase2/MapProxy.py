from phase1.Map import *
from threading  import RLock
from Map import Map

class MapProxy():
    def __init__(self, **kwargs):
        self.guardian = RLock()
        self._map = Map(kwargs)

    def synched( func):
        def synchronize(self,**kwargs):
            with self.lock:
                return func(self,**kwargs)
        return synchronize
    
    @synched
    def compute_edge_length(self, edge):
        return self._map.compute_edge_length(edge)

    @synched
    def shortest(self, node1, node2):
        return self._map.shortest(node1,node2)

    @synched
    def closestedge(self, loc):
        return self._map.closestedge(loc)

    @synched
    def addstop(self, edgeid, direction, percentage, description):
        return self._map.addstop(edgeid,direction,percentage, description)
    
    @synched
    def delstop(self, stopid):
        return self._map.delstop(stopid)

    @synched
    def getstop(self, stopid):
        return self._map.getstop(stopid)
    
    @synched
    def stoptimeDistance(self, stop1: int, stop2: int):
        return self._map.stoptimeDistance(stop1,stop2)

    @synched 
    def shorteststop(self, location):
        return self._map.shorteststop(location)