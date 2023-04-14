import json
from math import sqrt
from uuid import uuid4
import heapq
import utilities


class Map:
    def __init__(self, **kwargs):
        """
        Map class constructor which takes a json file
        or json string containing the data of the map as input
        """

        # Loading the data and parsing it into a python dictionary
        data = None
        self.uids = 0  # is here for debugging purposes
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

        # Intializing bus stops
        self.busStops = {}

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
            p_length = self.compute_edge_length(self.edges[p]) /100
            p_time = path_length / self.edges[p]["speed"]
            path_length += p_length
            path_time += p_time
        return (path, path_length * 1000, path_time * 60)

    def shortest(self, node1, node2):
        """
        Implementing dijkstra algorithm

        """
        notVisited = [key for key in self.nodes]
        parent_link = {}
        time_list = {}
        for n in notVisited:
            if n == node1:
                time_list[n] = 0
                parent_link[n] = None
            else:
                time_list[n] = 1e30
        for i in range(len(notVisited)):
            node = self.__get_min_node(notVisited, time_list)
            for edge_id in self.nodes[node]["edges"]:
                edge = self.edges[edge_id]
                edge_length = self.compute_edge_length(edge) /100 
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

    def closestedge(self, loc):
        pass

    def addstop(self, edgeid, direction, percentage, description):
        pass

    def delstop(self, stopid):
        pass

    def getstop(self, stopid):
        pass

    def stoptimeListance(stop1, stop2):
        pass

    def shorteststop(self, location):
        for stop in self.busStops:
            pass


def main():
    map = Map(path="../map.json")
    path = map.shortest(7, 19)
    print(path)
    l = map.compute_edge_length(edge=map.edges[1])
    print(l)


if __name__ == "__main__":
    main()


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
#     }
# }
