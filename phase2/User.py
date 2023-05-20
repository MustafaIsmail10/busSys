from uuid import uuid4
from Exceptions import *
from threading import Condition
from threading import RLock


class User:

    """
    This class keeps information about a user of the system and provide various functionalities such as login and logout
    """

    def __init__(self):
        '''
        Creates the user and creates a mutex which is passed to a newly created Condition variable
        '''
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
        '''
        Checks if this user is authenticated
        '''
        return str(self.token) == str(token) and self.authorized
    
    def is_token(self, token):
        '''
        Checks if this user is authenticated
        '''
        return str(self.token) == str(token) 
    
    def login(self, password):
        '''
        Lets the already existing user log in and
        marks them as authorized to access our system.
        Also gives them a new token
        '''
        if self.passwd == password:
            self.authorized = True
            return str(self.token)
        else :
            raise Exception("Wrong Password")
    
    def change_id (self, userid):
        '''
        Changes user id
        '''
        self.id = userid
    
    def get_id(self):
        '''
        Returns user id
        '''
        return self.id

    def register(self, username, passwd):
        '''
        Registers a new user onto the system
        with a given username and password,
        generates a token for them
        and authorizes them
        '''
        self.username = username
        self.passwd = passwd
        self.token = uuid4()
        self.authorized = True
        return str(self.token)

    def get_username (self):
        return self.username

    def logout(self):
        '''
        User can logout of the system and is now unauthorised and token is invalid
        '''
        self.authorized = False
        self.token == None

    def add_map(self, map_id):
        '''
        Adds a map to the user's list of maps that they are subscribed to
        '''
        self.maps.append(map_id)

    def add_schedule(self, sch_id):
        '''
        Adds a schedule to the user's list of schedules that they are subscribed to
        
        '''
        self.schedules.append(sch_id)

    def get_notifications(self):
        '''
        Waits on the wait_notifcation condition and as soon as it can pass
        it returns messages the user should receive and that will be sent through the server
        '''
        with self.mutex:
            while len(self.messages) == 0:
                self.wait_notification.wait()
            
            new_messages = self.messages
            self.messages = []
            msg = ""
            for m in new_messages:
                new_msg = f"New Message \n"
                new_msg += str(m) + "\n"
                msg += new_msg
            return msg


    def notify(self, msg):
        '''
        Wakes up the thread waiting for notifcation after 
        adding message to the list of new messages of this user
        '''
        with self.mutex:
            self.messages.append(msg)
            self.wait_notification.notify()
