import Map

class Route:
    def __init__(self,mmap:Map):
        self.orderedStops = [] 
        self.stops = {} #id and wait time
        self.start = -1
        self.map = mmap
    
    def add_stop(self,stopid,wait):
        if len(self.orderedStops)==0:
            self.start = stopid
        self.orderedStops.append(stopid)    
        self.stops[stopid] = wait
    

    def change_stop_order(self,new_index,stopid): 
        if new_index==0:
            self.set_start(self,stopid)
        else:
            old_index = self.orderedStops.index(stopid)
            del self.orderedStops[old_index]
            self.orderedStops.insert(new_index,stopid)  
           
    def set_start(self,stopid): # assumes stop is already in the list
        self.start = stopid
        old_index = self.orderedStops.index(stopid)
        del self.orderedStops[old_index]
        self.orderedStops.insert(0,stopid)

    def change_wait(self,stopid, new_wait):
        self.stops[stopid] =  new_wait
 
    def get_stops(self):
        first = self.orderedStops[0]
        route = []
        route.append((first,0,self.stops[first])) # stopid, starttime, leavetime
        for i in range(1,len(self.orderedStops)): 
            second = self.orderedStops[i]
            result = self.map.stoptimeDistance(first,second)
            arrive = result[1] + route[i-1][2] # travel time + previous stop leave time
            leave = arrive +  self.stops[second] #add wait time
            route.append((second,arrive,leave))
            first = second
        last_trip = self.map.stoptimeDistance(self.orderedStops[-1],self.orderedStops[0])
        arrive = last_trip[1] + route[-1][2]
        route.append((self.orderedStops[0],arrive))
        return route
    


    # time it takes to finish the route (including wait time at stop)
    def get_time(self):
        route = self.get_route()
        return route[-1][1] # back to start arrive time
        

    def get_distance(self, map): # whole distance covered by route
        stop1 = self.start
        dist = 0
        for i in range(1,len(self.orderedStops)): 
            stop2 = self.orderedStops[i]
            dist += map.stoptimeDistance(stop1,stop2)[0]
            stop1 = stop2
        back = map.stoptimeDistance(self.orderedStops[-1],self.start)[0] # distance going back
        return dist+back

