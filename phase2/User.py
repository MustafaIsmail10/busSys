from uuid import uuid4
from Exceptions import *
from threading import Condition
from threading import RLock


class User:

    """
    This class keeps information about a user of the system and provide various functionalities such as login and logout
    """

    def __init__(self):
        self.username = None
        self.passwd = None
        self.token = None
        self.authorized = False
        self.mutex = RLock()
        self.wait_notification = Condition(self.mutex)
        self.messages = []
        self.maps = []
        self.schedules = []
        self.id = None

    def is_authenticated(self, token):
        return self.token == token and self.authorized

    def login(self):
        self.token = uuid4()
        self.authorized = True
        return self.token
    
    def change_id (self, userid):
        self.id = userid
    
    def get_id(self):
        return self.id

    def register(self, username, passwd):
        self.username = username
        self.passwd = passwd
        self.token = uuid4()
        self.authorized = True
        return self.token

    def logout(self):
        self.authorized = False
        self.token == None

    def add_map(self, map_id):
        self.maps.append(map_id)

    def add_schedule(self, sch_id):
        self.schedules.append(sch_id)

    def get_notifications(self):
        with self.mutex:
            if len(self.messages) == 0:
                self.wait_notification.wait()
            else :
                new_messages = self.messages
                self.messages = []
                return new_messages
