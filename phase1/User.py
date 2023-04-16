from uuid import uuid4

class User:

    """
    This class keeps information about a user of the system and provide various functionalities such as login and logout
    """
    def __init__(self, username, email, passwd):
        self.username = username
        self.email = email 
        self.passwd = passwd 
        self.authorized = False

    def auth (self, plainpass):
        return plainpass == self.passwd
    
    def login(self): 
        self.token = uuid4()
        self.authorized = True
        return self.token
    
    def checksession(self, token):
        return self.token == token
    
    def logout(self):
        self.authorized = False
        self.token == None


        