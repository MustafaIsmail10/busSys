from threading import Thread, RLock, Condition
from time import sleep
from Passenger import Passenger
import random

class Simulator:
    def __init__(self, user, schedule, mmap, start_time, end_time):
        self.start_time = start_time
        self.end_time = end_time
        self.curr_time = start_time
        self.user = user
        self.schedule = schedule
        self.waiting = {}
        self.in_bus = {}
        lines = self.schedule.get_lines()
        for lineid in lines:
            self.waiting[lineid] = []
            self.in_bus[lineid] = []
        self.passengers = []
        self.gurdian = RLock()
        self.ids = 1
        self.map = mmap
        

    def run(self):
        pg = Thread(target=self.passenger_generator, args=())
        pg.start()
        print("Bl7aaaa")

        while self.curr_time < self.end_time:
            with self.gurdian:
                self.curr_time += 1
                self.update_passengers()
            sleep(.2)

            if self.curr_time % 5 == 0:
                self.print_updates()


    def print_updates(self):
        print(f"The current time is {self.curr_time} in minutes since mid-night")
        for passenger in self.passengers:
            passenger.print_status()
    


    def update_passengers(self):
        for lineid in self.waiting:
            for passenger in self.waiting[lineid]:
                if self.schedule.is_bus_at_stop(lineid, passenger[1], self.curr_time):
                    in_bus_time = passenger[0].bus_came()
                    self.waiting[lineid].remove(passenger)
                    self.in_bus[lineid].append((passenger, in_bus_time + self.curr_time))
                    
            for passenger in self.in_bus[lineid]:
                if self.curr_time > passenger[1]:
                    passenger[0].bus_arrived()
                    self.in_bus[lineid].remove(passenger)
                    


    def passenger_generator(self):
        for i in range(20):
            passenger_id = self.ids
            self.ids += 1
            loc = {
                "x": random.randint(0, 85), 
                "y":random.randint(20, 75)
            }

            target = {
                "x": random.randint(0, 85), 
                "y":random.randint(20, 75)
            }

            new_passenger = Passenger(passenger_id,loc, target, 10, self.map, self.schedule, self)
            p_thread = Thread(target=new_passenger.run, args=())
            self.passengers.append(new_passenger)
            p_thread.start()


# lines {
#     lineid: [(passenger, stopid)]
# }
