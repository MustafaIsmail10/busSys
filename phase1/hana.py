import json
from math import sqrt
from uuid import uuid4
import heapq


class Map:
    def __init__(self, **kwargs):
        data = None
        self.uids = 0
        self.stopIds = 0
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
        self.busStops = {}

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
        totaltimeList = 0
        for i in range(1, len(ways)):
            p1 = ways[i]
            totaltimeList += sqrt((p0["x"] - p1["x"])
                                  ** 2 + (p0["y"] - p1["y"])**2)
            p0 = p1
        return totaltimeList

    # Shotest path calculation start ******************************************
    # This fuction takes a list contaning nodes and gives the min node as a result

    def getMinNode(self, notVisited, timeList):
        mintime = 1e31
        minNode = "-1"
        for n in notVisited:
            if (timeList[n] < mintime):
                mintime = timeList[n]
                minNode = n

        return minNode

    def getPath(self, parentLink, node):
        path = []
        while parentLink[node] != None:
            path.append(parentLink[node]["id"])
            if (node == parentLink[node]["from"]):
                node = parentLink[node]["to"]
            else:
                node = parentLink[node]["from"]
        path.reverse()
        return path

    def shortest(self, node1, node2):
        notVisited = [key for key in self.nodes]
        parentLink = {}
        timeList = {}
        for n in notVisited:
            if n == node1:
                timeList[n] = 0
                parentLink[n] = None
            else:
                timeList[n] = 1e30
        for i in range(len(notVisited)):
            node = self.getMinNode(notVisited, timeList)
            for edgeId in self.nodes[node]["edges"]:
                edge = self.edges[edgeId]
                edgeLength = self.computeEdgeLength(edge)
                edgeTime = edgeLength/edge["speed"]
                toNode = edge["from"]
                if edge["from"] == node:
                    toNode = edge["to"]

                if timeList[node] + edgeTime < timeList[toNode]:
                    timeList[toNode] = timeList[node] + edgeTime
                    parentLink[toNode] = edge

            notVisited.remove(node)
            if (node == node2):
                break
        return self.getPath(parentLink, node2)
    # Shotest path calculation end ******************************************

    def dotprod(self,a,b):
        product = a["x"]*b["x"]
        product += a["y"]*b["y"]
        return product

    def subtract(self,a,b):
        c = {}
        c["x"]=a["x"]-b["x"]
        c["y"]=a["y"]-b["y"]
        return c

    def add(self,a,b):
        c = {}
        c["x"]=a["x"]+b["x"]
        c["y"]=a["y"]+b["y"]
        return c

    def multiply(self,cons,a):
        c = {}
        c["x"]=cons*a["x"]
        c["y"]=cons*a["y"]
        return c

    def dist(self,a,b):
        return sqrt((a["x"] - b["x"] )**2 + (a["y"] - b["y"] )**2 )


    def closestedge(self,loc): # instead of storing all these can we set a min and calculate on the fly
        allpoints = {}
        distances = {}
        points =[]
        closest_point = None
        min_dist = 10000 #change later to inf
        for edge in self.edges:

            way = self.ways[self.edges[edge]["way"]]
            a = way[0]
            for i in range(1, len(way)):
                b = way[i]
                xa = self.subtract(loc,a)
                ba = self.subtract(b,a)
                d = self.dotprod(xa,ba)/self.dotprod(ba,ba)
                if d<=0:
                    point = a
                elif d>=1:
                    point = b
                else:
                    point = self.add(a,self.multiply(d,ba))
                distance = self.dist(point , loc)
                if distance<min_dist:
                    min_dist = distance
                    closest_point = point
                    closest_edge = edge
                    closest_way = way
                a = b


        percentage = self.dist(self.nodes[self.edges[closest_edge]["from"]]["location"],closest_point)/self.computeEdgeLength(self.edges[closest_edge])
        return (closest_edge,closest_point,percentage)


    def addstop(self,edgeid, direction, percentage, description):
        factor = (percentage*self.computeEdgeLength(self.edges[edgeid]))/100

        way = self.ways[self.edges[edgeid]["way"]]
        if not direction:
            way = self.ways[self.edges[edgeid]["way"]].copy().reverse()
        node1 = way[0]
        for i in range(1,len(way)):
            node2 = way[i]
            way_distance = self.dist(node1,node2)
            if way_distance > factor:
                coordinate = self.mult(1+(factor/way_distance), node1) #are there edge cases such as node1 coord bigger than node2
                between = (node1,node2)
                break
            node1 = node2
            factor-=way_distance


        self.stopIds+=1 #replace with uids()
        self.busStops[self.stopIds] = {}
        self.busStops[self.stopIds]["loc"] = coordinate
        self.busStops[self.stopIds]["direction"] = direction
        self.busStops[self.stopIds]["description"] = description
        self.busStops[self.stopIds]["edge"] = edgeid
        self.busStops[self.stopIds]["percent"] = percentage
        self.edges[edgeid]["stops"].append(self.stopIds)

        return self.busStops[self.stopIds]

    def delstop(self,stopid):
        if self.stopIds==0:
            raise Exception("no more stops to delete!")
        if stopid>self.stopIds:
            raise Exception("no such stop to delete!")
        edgeid = self.busStops[stopid]["edge"]
        del self.busStops[stopid]

        self.edges[edgeid]["stops"].remove(self.stopIds)
        self.stopIds-=1
        return "successful deletion"

    def getstop(self,stopid):
        if self.stopIds==0 or stopid>self.stopIds:
            raise Exception("no such stop!")
        stop = self.busStops[stopid]
        edge =self.edges[stop["edge"]] # frm and to depend on direction
        ret = "This is {name} stop of id {id}. It connects nodes {frm} to {to} through edge {edgeid}".format(name=stop["description"],id=stopid,frm=edge["from"],to=edge["to"],edgeid=stop["edge"])
        return ret  # format or just return the stop dictionary?


    def stoptimeDistance(self, stop1, stop2):

        s1 = self.busStops[stop1]
        s2 = self.busStops[stop2]
        if s1["direction"]:
            target_node = self.edges[s1["edge"]]["to"]
            way1 = self.ways[self.edges[s1["edge"]]["way"]]

        else:
            target_node = self.edges[s1["edge"]]["from"]
            way1 = self.ways[self.edges[s1["edge"]]["way"]].copy().reverse()

        if s2["direction"]:
            src_node = self.edges[s2["edge"]]["from"]
            way2 = self.ways[self.edges[s2["edge"]]["way"]]

        else:
            src_node = self.edges[s2["edge"]]["to"]
            way2 = self.ways[self.edges[s2["edge"]]["way"]].copy().reverse()

        factor1 = s1["percent"]*self.computeEdgeLength(s1["edge"])
        factor2 = s2["percent"]*self.computeEdgeLength(s2["edge"])
        node1 = way1[0]
        dist1 = dist2 = 0
        for i in range(1,len(way1)):
            node2 = way1[i]
            if self.dist(node1,node2)>factor1:
                dist1+= self.dist(s1["loc"],node1)
                break
            dist1+=self.dist(node1,node2)

        node1 = way2[0]
        for i in range(1,len(way1)):
            node2 = way2[i]
            if self.dist(node1,node2)>factor2:
                dist2+= self.dist(s2["loc"],node1)
                break
            dist2+=self.dist(node1,node2)

        shortestDist = self.shortest(target_node,src_node)
        fullDistance = shortestDist[0]+dist1+dist2
        time = shortestDist[1] + dist1/s1["edge"]["speed"] + dist2/s2["edge"]["speed"]
        return (fullDistance,time)


    def shorteststop(self, location):
        for stop in self.busStops:
            pass


def main():
    map = Map(path="../map.json")
    loc ={}
    loc["x"] = 220.0
    loc["y"] = 106.5
    answer = map.closestedge(loc)
    print(answer)
    print(map.edges[answer[0]])

    #path = map.shortest(7, 19)
    #print(path)
    print(map.addstop(2,True,20,"civil eng"))


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