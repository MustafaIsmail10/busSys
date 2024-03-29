import json
from math import sqrt, sin, cos
from uuid import uuid4
import heapq
import utilities
from Stop import Stop


class Map:

    def __init__(self, **kwargs):
        """
        Map class constructor which takes a json file
        or json string containing the data of the map as input
        """
        self.uids = 0  # is here for debugging purposes
        self.stopIds = 0

        # Intializing bus stops
        self.bus_stops = {}

        # Loading the data and parsing it into a python dictionary
        data = None
        if "path" in kwargs.keys():
            with open(kwargs["path"], "r") as file:
                data = json.load(file)

        elif "json" in kwargs.keys():
            data = json.loads(kwargs["json"])
        else:
            raise Exception("omg man your data is not valide")

        # Parsing ways
        ws = data["ways"]
        self.ways = {}
        for key in ws:
            self.ways[int(key)] = ws[key]

        # Parsing nodes
        ns = data["nodes"]
        self.nodes = {}
        for key in ns:
            newKey = int(key)
            self.nodes[newKey] = {}
            self.nodes[newKey]["location"] = ns[key]
            self.nodes[newKey]["edges"] = []

        # Parsing edges
        eds = data["edges"]
        self.edges = {}
        for key in eds:
            ed = eds[key]
            newKey = int(key)
            for edge in ed:
                newEdge = {}
                newEdge["from"] = newKey
                newEdge["to"] = int(edge["to"])
                newEdge["way"] = edge["way"]
                newEdge["speed"] = float(edge["speed"])
                newEdge["stops"] = []
                edgeId = self.get_uid()
                newEdge["id"] = edgeId
                self.edges[edgeId] = newEdge
                self.nodes[newKey]["edges"].append(edgeId)
                self.nodes[newEdge["to"]]["edges"].append(edgeId)

    # Generating unique id for each new item
    def get_uid(self):
        # uuid4 should be used in the final verison
        self.uids += 1
        return self.uids

    def compute_edge_length(self, edge):
        """
        This funciton computes the length of a graph edge
        It takes the edge as input
        """
        way_id = edge["way"]
        way = self.ways[way_id]
        p0 = way[0]
        totaltimeList = 0
        for i in range(1, len(way)):
            p1 = way[i]
            totaltimeList += utilities.euclidean_distance(
                p0["x"], p0["y"], p1["x"], p1["y"]
            )
            p0 = p1
        return totaltimeList

    # Shotest path calculation start ******************************************
    # This fuction takes a list contaning nodes and gives the min node as a result
    def __get_min_node(self, notVisited, timeList):
        mintime = 1e31
        minNode = -1
        for n in notVisited:
            if timeList[n] < mintime:
                mintime = timeList[n]
                minNode = n
        return minNode

    def __get_path(self, parent_link, node):
        path = []
        while parent_link[node] != None:
            path.append(parent_link[node]["id"])
            if node == parent_link[node]["from"]:
                node = parent_link[node]["to"]
            else:
                node = parent_link[node]["from"]
        path.reverse()
        return path

    def __get_shortest_data(self, parent_link, node):
        path = self.__get_path(parent_link, node)
        path_length = 0
        path_time = 0
        for p in path:
            p_length = self.compute_edge_length(self.edges[p])
            p_time = p_length / self.edges[p]["speed"]
            path_length += p_length
            path_time += p_time
        return (path, path_length, path_time * 60)

    def shortest(self, node1, node2):
        """
        Implementing dijkstra algorithm
        It takes the id of 2 nodes as input
        It returns a tuple of 3 (edgeid, distace in kilometers, time in minutes)

        """
        # I'm using a list to store non visited nodes and getting and using a dictionary to store values for each edge
        notVisited = [key for key in self.nodes]
        parent_link = {}
        time_list = {}
        # Intializing the non visited list
        for n in notVisited:
            if n == node1:
                time_list[n] = 0
                parent_link[n] = None
            else:
                time_list[n] = 1e30

        # The real work is here
        # get the minimum node
        # process its edges and update their weight in time list
        # store the edges that let to the current node
        # until the wanted node is reached
        # find the edges that let to it to get the path to that node
        for i in range(len(notVisited)):
            node = self.__get_min_node(notVisited, time_list)
            for edge_id in self.nodes[node]["edges"]:
                edge = self.edges[edge_id]
                edge_length = self.compute_edge_length(edge)
                edge_time = edge_length / edge["speed"]
                toNode = edge["from"]
                if edge["from"] == node:
                    toNode = edge["to"]

                if time_list[node] + edge_time < time_list[toNode]:
                    time_list[toNode] = time_list[node] + edge_time
                    parent_link[toNode] = edge

            notVisited.remove(node)
            if node == node2:
                break

        return self.__get_shortest_data(parent_link, node2)

    # Shotest path calculation end ******************************************

    
    

    def dist(self, a, b):
        return sqrt((a["x"] - b["x"]) ** 2 + (a["y"] - b["y"]) ** 2)

    def closestedge(self, loc):
        '''
        Gets the closest edge to a location and returns it 
        along with, the closest point on that edge,
        and the percentage of the point from the edge start, in a triple.
        '''
        closest_point = None
        min_dist = 1e30  
        #by looping over all edges
        #then the ways of the edges to calculate the formula for 
        #point vs line segment which tells us where on the line is closest
        #to that point. then finds the distance between the loc and that point,
        #if it is the minimum, the minimum is set to it and the closest edge
        #is set to the current edge.
        
        for edge in self.edges:
            way = self.ways[self.edges[edge]["way"]]
            a = way[0]
            for i in range(1, len(way)):
                b = way[i]
                xa = utilities.subtract(loc, a)
                ba = utilities.subtract(b, a)
                d = utilities.dotprod(xa, ba) / utilities.dotprod(ba, ba)
                if d <= 0:
                    point = a
                elif d >= 1:
                    point = b
                else:
                    point = utilities.add(a, utilities.multiply(d, ba))
                distance = self.dist(point, loc)
                if distance < min_dist:
                    min_dist = distance
                    closest_point = point
                    closest_edge = edge
                    
                a = b
        #percentage is found using euclidean distance between closest point
        #and edge start, divided by the total edge length
        percentage = self.dist(
            self.nodes[self.edges[closest_edge]["from"]]["location"], closest_point
        ) / self.compute_edge_length(
            self.edges[closest_edge]
        )  
        return (closest_edge, closest_point, percentage)

    def addstop(self, edgeid, direction, percentage, description):
        '''
        adds a stop in the map on a given edge and at a given percentage
        with either a left or right poistion relative to the edge.
        Also stores the description of this stop.
        returns id of the stop.
        '''

        # use percentage to calculate how far into the edge the stop will be
        # if direction is reversed, percentage is also affected
        pe = percentage
        if not direction:
            pe = 100 - percentage

        factor = (pe * self.compute_edge_length(self.edges[edgeid])) / 100

        # loop over the edge way until the factor is less than
        # the distance between some 2 points in the way
        # then get the coordinate by getting percentage of stop on way
        # and adding it to start node
        way = self.ways[self.edges[edgeid]["way"]]
        node1 = way[0]
        for i in range(1, len(way)):
            node2 = way[i]
            way_distance = self.dist(node1, node2)
            if way_distance >= factor:
                temp = utilities.multiply(
                    (factor / way_distance), utilities.subtract(node2, node1)
                ) 
                coordinate = utilities.add(node1, temp)
                break
            node1 = node2
            factor -= way_distance

        self.stopIds += 1  # replace with uids()

        # create stop instance and add it to dict of bus stops
        stop = Stop(
            self.stopIds, edgeid, percentage, direction, description, coordinate
        )
        self.bus_stops[self.stopIds] = stop
        # self.bus_stops[self.stopIds] = {}
        # self.bus_stops[self.stopIds]["loc"] = coordinate
        # self.bus_stops[self.stopIds]["direction"] = direction
        # self.bus_stops[self.stopIds]["description"] = description
        # self.bus_stops[self.stopIds]["edge"] = edgeid
        # self.bus_stops[self.stopIds]["percent"] = percentage
        self.edges[edgeid]["stops"].append(self.stopIds) # updates edge's stops list
        return self.stopIds

    def delstop(self, stopid):
        '''
        removes a stop from the map given the id
        '''
        if self.stopIds == 0:
            raise Exception("no more stops to delete!")
        if stopid > self.stopIds or stopid not in self.bus_stops:
            raise Exception("no such stop to delete!")

        # removes stop from bus stops dict and from relevant edge's stop list
        edgeid = self.bus_stops[stopid].get_edgeid()
        del self.bus_stops[stopid]
        self.edges[edgeid]["stops"].remove(stopid)
        return "successful deletion"

    def getstop(self, stopid):
        '''
        returns a Stop object whose representation is in the overloaded __str__ method
        '''
        if self.stopIds == 0 or stopid > self.stopIds or stopid not in self.bus_stops:
            raise Exception("no such stop!")

        stop = self.bus_stops[stopid]
        # edge = self.edges[stop.get_edgeid()]  # frm and to depend on direction
        # ret = "This is {name} stop of id {id}. It connects nodes {frm} to {to} through edge {edgeid}".format(
        #     name=stop.description,
        #     id=stopid,
        #     frm=edge["from"],
        #     to=edge["to"],
        #     edgeid=stop["edge"],
        # )
        return stop  

    ## ******************************Review the following parts********************************########
    def stoptimeDistance(self, stop1: int, stop2: int):
        '''
        Gets the shortest distance and time between 2 stops, returns them in tuple
        If the direction of the stop is False the src and target are swapped. 
        
        '''
        if stop1 not in self.bus_stops:
            raise Exception("stop1 unavailable")
        if stop2 not in self.bus_stops:
            raise Exception("stop2 unavailable")

        s1 = self.bus_stops[stop1]
        s2 = self.bus_stops[stop2]
        
        if s1.direction:
            target_node = self.edges[s1.get_edgeid()]["to"]
            factor1 = (100 - s1.get_percent()) / 100
            dist_to_target = factor1 * self.compute_edge_length(
                self.edges[s1.get_edgeid()]
            )
        else:
            target_node = self.edges[s1.get_edgeid()]["from"]
            factor1 = (s1.get_percent()) / 100
            dist_to_target = factor1 * self.compute_edge_length(
                self.edges[s1.get_edgeid()]
            )

        if s2.direction:
            src_node = self.edges[s2.get_edgeid()]["from"]
            factor2 = (s2.get_percent()) / 100
            dist_from_src = factor2 * self.compute_edge_length(
                self.edges[s2.get_edgeid()]
            )

        else:
            src_node = self.edges[s2.get_edgeid()]["to"]
            factor2 = (100 - s2.get_percent()) / 100
            dist_from_src = factor2 * self.compute_edge_length(
                self.edges[s2.get_edgeid()]
            )


        # by using
        # the shortest() function to find the distance between 
        # the target node of stop1 and the src node of stop 2.
        # Adds to that the distance from stop to node using 
        # the percentage of the stop on the edge and
        # multiplying it with the length of the edge.

        shortest_between_nodes = self.shortest(target_node, src_node)

        path_length = shortest_between_nodes[1] + dist_from_src + dist_to_target
        time_to_target = dist_to_target / self.edges[s1.get_edgeid()]["speed"] # time found by dividing dist/speed of relevant edge
        time_form_src = dist_from_src / self.edges[s2.get_edgeid()]["speed"]
        path_time = shortest_between_nodes[2] + time_form_src + time_to_target
        return (path_length, path_time)

    def shorteststop(self, location):
        """
        Takes a location and returns the id of the closet stop to that location and returns None in case there is no stops
        """
        min_dist = 1e30
        min_stop = None
        for stop in self.bus_stops:
            temp_dist = self.dist(self.bus_stops[stop].get_location(), location)
            if temp_dist < min_dist:
                min_stop = stop
                min_dist = temp_dist # update min_dist
        return min_stop




# def main():
#     map = Map(path="./test/test_map.json")
#     path = map.shortest(1, 2)
#     # print(path)
#     print(map.edges)
#     # l = map.compute_edge_length(edge=map.edges[1])
#     # print(l)
#     print(map.shortest(1, 2))


# if __name__ == "__main__":
#     main()


# Date organization tempelete is here
#     nodes = {
#     0: {
#         "location": 55,
#         "edges": [1,4,8,36]
#     }
# }

# edges = {
#     0: {
#         "fromNode": 55,
#         "toNode": 54,
#         "speed": 55,
#         "ways": 50,
#         "stops": [55]
#     },
# }

#  "ways": {
#     "0": [
#       {
#         "x": 6.4144686,
#         "y": 269.23002
#       },
#       {
#         "x": 35.279578,
#         "y": 270.2991
#       }
#     ],
#  }


# stops = {
#     0:{
#         "edge":55,
#         "direction": True,
#         "percnetage":50,
#         "description":"Description of the bus stop"
#         "locatoin": {"x":1215, "y"=44}
#     }
# }
