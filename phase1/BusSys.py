from User import User
from Scheduale import Schedule

class BusSys:

    def __init__(self, mmap):
        self.schedule = Schedule(mmap)

    def get_schedule(self, user):
        if user.authorized == True:
            return self.schedule
        else :
            return None


    