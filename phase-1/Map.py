import json
from math import sqrt

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
        
        self.ways = data["ways"]
        # Parsing nodes 
        ns = data["nodes"]
        self.nodes = {}
        for key in ns:
            self.nodes[key] = {}
            self.nodes[key]["location"] = ns[key]
            self.nodes[key]["edges"] = []
        
        # Parsing edges 
        eds = data["edges"]
        self.edges = {}
        for key in eds:
            singleEdges = eds[key]
            for edge in singleEdges:
                newEdge = {}
                newEdge["from"] = key
                newEdge["to"] = edge["to"]
                newEdge["way"] = str(edge["way"])
                newEdge["speed"] = edge["speed"]
                newEdge["stops"] = []
                edgeId = self.getUID()
                self.edges[edgeId] = newEdge
                self.nodes[key]["edges"].append(edgeId)
                self.nodes[edge["to"]]["edges"].append(edgeId)       

        print(self.edges[1])
        weight = self.computeEdgeLength(self.edges[1])
        print(weight)
        # Intializing bus stops
        self.bus_stops = None


    def getUID(self):
        self.uids += 1
        return self.uids

    def getMinNode(self, lst):
        minimum = min(lst)
        minIndex = lst.index(minimum)
        return minIndex

    def computeEdgeLength(self, edge):
        wayId = edge["way"]
        
        ways = self.ways[wayId]
        p0 = ways[0]
        totalDist = 0
        for i in range(1, len(ways)):
            p1 = ways[i]
            totalDist += sqrt((p0["x"] - p1["x"] )**2 + (p0["y"] - p1["y"] )**2 )
            p0 = p1
        return totalDist



    def pathFinder(self, node1, node2, visited, path, dist):
        visited[node1] = True
        path.apped(node1)
        if (node1 == node2): return
        minNodeId = self.getMinNode(dist)
        node = self.nodes[minNodeId]
        for edgeId in node["edges"]:
            edge = self.edges[edgeId]
            edgeLength = self.computeEdgeLength(edge)
            if edge["from"] == node1:
                toNode = edge["to"]
                dist[toNode] = dist[node1] + edgeLength if dist[node1] + edgeLength < dist[toNode] else dist[toNode] 
                pass
            else:
                pass
        



    def shortest(self, node1: int, node2: int):
        visited = [False for i in range(len(self.nodes))]
        dist = [1e30 for i in range(len(self.nodes))]
        dist[node1] = 0
        path = []
        self.pathFinder(node1, node2, visited, path, dist)
        pass

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
