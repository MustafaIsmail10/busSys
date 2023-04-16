from User import User
from Scheduale import Schedule

class BusSys:
    """
    This class shall be the main controller of the system return schedule object to authorized users
    """
    def __init__(self, mmap):
        self.schedule = Schedule(mmap)

    def get_schedule(self, user):
        """
        This fucntion takes a user object as input and checks if the user is authorized
        In case the user is authorized it returns a schedule object
        """
        if user.authorized == True:
            return self.schedule
        else :
            return None


    