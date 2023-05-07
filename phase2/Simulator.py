from threading import Thread, RLock, Condition
from time import sleep
from Passenger import Passenger
import random


class Simulator:
    def __init__(self, user, schedule, start_time, end_time):
        self.start_time = start_time
        self.end_time = end_time
        self.curr_time = start_time
        self.user = user
        self.schedule = schedule
        self.waiting = {}
        self.in_bus = {}
        self.mutex = RLock()
        lines = self.schedule.get_lines()
        for lineid in lines:
            self.waiting[lineid] = []
            self.in_bus[lineid] = []
        self.passengers = []
        self.gurdian = RLock()
        self.ids = 1

    def run(self):
        pg = Thread(target=self.passenger_generator, args=())
        pg.start()

        while self.curr_time < self.end_time:
            with self.gurdian:
                self.curr_time += 1
                self.update_passengers()
            sleep(0.2)

            if self.curr_time % 5 == 0:
                self.print_updates()
        
        for passenger in self.passengers:
            passenger.exit_signel()

    def print_updates(self):
        msg = f"The current time is {self.curr_time} in minutes since mid-night"
        self.user.notify(msg)
        for passenger in self.passengers:
            # passenger.print_status()
            passenger_status = passenger.get_status()
            self.user.notify(passenger_status)

    def update_passengers(self):
        with self.mutex:
            for lineid in self.schedule.get_lines():
                # print(f"line {lineid}'s wait {self.waiting[lineid]}")
                for passenger in self.waiting[lineid]:
                    # print("Processign passenger")
                    # print(lineid, passenger[1])
                    if self.schedule.is_bus_at_stop(lineid, passenger[1], self.curr_time):
                        # print("Entering the buss")
                        # print("THE CUREEEEEENT TIME IS ", self.curr_time)
                        in_bus_time = passenger[0].bus_came()

                        self.waiting[lineid].remove(passenger)
                        self.in_bus[lineid].append(
                            (passenger[0], in_bus_time + self.curr_time)
                        )

                        # print("The current state of waiting is ", self.waiting)
                        # print("The current state of in bus is ", self.in_bus)

                for passenger in self.in_bus[lineid]:
                    if self.curr_time > passenger[1]:
                        passenger[0].bus_arrived()
                        self.in_bus[lineid].remove(passenger)



    def add_to_waiting(self, passenger, line, start_stop):
        with self.mutex:
            self.waiting[line.lineid].append((passenger, start_stop))

    def passenger_generator(self):
        for i in range(20):
            passenger_id = self.ids
            self.ids += 1
            loc = {"x": random.randint(0, 85), "y": random.randint(20, 75)}

            target = {"x": random.randint(0, 85), "y": random.randint(20, 75)}

            # loc = {"x": 13, "y": 47}

            # target = {"x": 80, "y": 54}

            new_passenger = Passenger(
                passenger_id, loc, target, 20, self.schedule, self
            )
            p_thread = Thread(target=new_passenger.run, args=())
            self.passengers.append(new_passenger)
            # self.waiting[?] = (new_passenger,?)
            p_thread.start()


    def remove_passenger(self, passenger):
        with self.mutex:
            self.passengers.remove(passenger)

    def get_statistics(self):
        pass

# lines {
#     lineid: [(passenger, stopid)]
# }
