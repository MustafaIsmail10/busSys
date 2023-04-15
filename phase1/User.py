from uuid import uuid4

class User:
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
        self.token == None


        