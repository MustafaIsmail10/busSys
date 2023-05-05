class Stop:
    """
    This class keeps information about a bus stops
    A bus stop shall not be modified after creation since modifing a bus stop may have a great effect on other parts of the system
    """
    def __init__(self, stopid, edgeid, percent, direction, description, loc):
        self.stopid = stopid
        self.edgeid = edgeid  # integer or another represention of the id
        self.percent = percent  # integer
        self.direction = direction  # boolean value
        self.description = description  # string description of the stop
        self.loc = loc  # dictionary representing location of the stop
        self.lines = []  # list of lines in which the stop exist

    def get_stopid(self):
        return self.stopid

    def get_edgeid(self):
        return self.edgeid

    def get_percent(self):
        return self.percent

    def get_direction(self):
        return self.direction

    def get_description(self):
        return self.description

    def get_location(self):
        return self.loc

    def add_line(self, line_id):
        self.lines.append(line_id)

    def __str__(self):
        return f"Id: {self.stopid}, edgeid: {self.edgeid}, percent: {self.percent}, direction: {self.direction}, description: {self.description}, location: {self.loc}"
