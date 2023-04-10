class Map:
    def __init__(self, **kwargs):
        # jason file 
        nodes = {
            0: {
                "location": 55, 
                "edges": [1,4,8,36]
            }
        }

        edges = {
            0: {
                "fromNode": 55, 
                "toNode": 54, 
                "speed": 55, 
                "ways": 50,
                "stops": [55]
            },
        }


        ways = {
            0: {
                "cordiantes": [], 
                "edge": 54, 
                "length":[],
            },
            }


        stops = {
            0:{
                "edge":55, 
                "cordinates": 50, 
                "direction": True,
                "percnetage":50,
                "description":50

            }
        }
        
        pass