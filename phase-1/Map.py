import json
from math import sqrt
from uuid import uuid4
import heapq

class Map:
    def __init__(self, **kwargs):
        data = None
        self.uids = 0
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
            singleEdges = eds[key]
            newKey = int(key)
            for edge in singleEdges:
                newEdge = {}
                newEdge["from"] = newKey
                newEdge["to"] = int(edge["to"])
                newEdge["way"] = edge["way"]
                newEdge["speed"] = edge["speed"]
                newEdge["stops"] = []
                edgeId = self.getUID()
                newEdge["id"] = edgeId
                self.edges[edgeId] = newEdge
                self.nodes[newKey]["edges"].append(edgeId)
                self.nodes[newEdge["to"]]["edges"].append(edgeId)

        # Intializing bus stops
        self.bus_stops = {}

    # Generating unique id for each new item
    def getUID(self):
        # uuid4 should be used in the final verison
        self.uids += 1
        return self.uids
    

    def computeEdgeLength(self, edge):
        '''
            This funciton computes the length of a graph edge 
        '''
        wayId = edge["way"]
        ways = self.ways[wayId]
        p0 = ways[0]
        totalDist = 0
        for i in range(1, len(ways)):
            p1 = ways[i]
            totalDist += sqrt((p0["x"] - p1["x"])**2 + (p0["y"] - p1["y"])**2)
            p0 = p1
        return totalDist



    # Shotest path calculation start ******************************************
    # This fuction takes a list contaning nodes and gives the min node as a result 
    def getMinNode(self, notVisited, dist):
        minDist = 1e31
        minNode = "-1"
        for n in notVisited:
            if (dist[n] < minDist):
                minDist = dist[n]
                minNode = n
 
        return minNode


    def getPath(self, parentLink, node):
        path = []
        while parentLink[node] != None:
            path.append(parentLink[node]["id"])
            if (node == parentLink[node]["from"]):
                node = parentLink[node]["to"]
            else : 
                node = parentLink[node]["from"]
        path.reverse()
        return path

    def shortest(self, node1, node2):
        notVisited = [key for key in self.nodes]
        parentLink = {}
        dist = {}
        for n in notVisited:
            if n == node1:
                dist[n] = 0
                parentLink [n] = None
            else : 
                dist[n] = 1e30
        for i in range(len(notVisited)):
            node = self.getMinNode(notVisited, dist)
            for edgeId in self.nodes[node]["edges"]:
                edge = self.edges[edgeId]
                edgeLength = self.computeEdgeLength(edge)
                toNode = edge["from"]
                if edge["from"] == node:
                    toNode = edge["to"]

                if dist[node] + edgeLength < dist[toNode]:
                        dist[toNode] = dist[node] + edgeLength 
                        parentLink[toNode] = edge

            notVisited.remove(node)
            if (node == node2):
                break
        return self.getPath(parentLink, node2)
    # Shotest path calculation end ******************************************

    def closestedge(loc):
        pass

    def addstop(edgeid, direction, percentage, description):
        pass

    def delstop(stopid):
        pass

    def getstop(stopid):
        pass

    def stopdistance(stop1, stop2):
        pass

    def shorteststop(location):
        pass


def main():
    map = Map(path="../map.json")
    path = map.shortest(7,19)
    print(path)


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


# ways = {
#     0: {
#         "cordiantes": [],
#         "edge": 54,
#         "length":[],
#     },
#     }


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
#         "cordinates": 50,
#         "direction": True,
#         "percnetage":50,
#         "description":50

#     }
# }
