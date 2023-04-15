from User import User
class BusSys:

    def __init__(self):
        self.auth = False

    def login_user(self, user:User):
        if user.login():
            self.auth = True


    