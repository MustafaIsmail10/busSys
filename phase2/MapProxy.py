from threading  import RLock, Thread
from Map import Map
import random as rand
from time import sleep

class MapProxy():
    def __init__(self,map_id, **kwargs):
        self.lock = RLock()
        self._map = Map(map_id,**kwargs)

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
    
    @synched
    def stops_within_r(self, location, radius):
        return self._map.stops_within_r(location,radius)
    
    @synched
    def testing_sync(self):
        i = 0
        while True:
            i += 1
    @synched
    def Testing_sync2(self):
        print("OMGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGG")


def test1(map:MapProxy):
    # while True:
    #     edge = rand.random()*10
    #     percent = rand.random()*100
    #     map.add_stop(edge, True, percent,"kofta")
    #     print(f"added to {edge} with True direction at {percent}%")
    sleep(2)
    map.testing_sync()

def test2(map:MapProxy):
    sleep(1)
    map.Testing_sync2()
    sleep(2)
    map.Testing_sync2()

kwargs = {"path": "./test/test_map.json"}
m = MapProxy(0,**kwargs)
t1 = Thread(target=test1,  args=(m,))
t2 = Thread(target=test2,  args=(m,))
t1.start()
t2.start()