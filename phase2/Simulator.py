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
        self.busses = {} # to keep track of busses for each route
        self.mutex = RLock()
        lines = self.schedule.get_lines()
        for lineid in lines:
            self.waiting[lineid] = []
            self.in_bus[lineid] = []
            self.busses[lineid] = {}
        self.passengers = []
        self.gurdian = RLock()
        self.ids = 1
        self.trips_num  = 0
        self.wait_times = []


    def run(self):
        pg = Thread(target=self.passenger_generator, args=())
        pg.start()

        self.initalize_busses()
        while self.curr_time < self.end_time:
            with self.gurdian:
                self.curr_time += 1
                self.update_busses()
                self.update_passengers()
            sleep(0.2)

            if self.curr_time % 10 == 0:
                self.print_updates()
        
        for passenger in self.passengers:
            passenger.exit_signel()

        return 


    def print_updates(self):
        msg = f"The current time is {self.curr_time} in minutes since mid-night"
        self.user.notify(msg)
        # for passenger in self.passengers:
        #     # passenger.print_status()
        #     passenger_status = passenger.get_status()
        #     self.user.notify(passenger_status)

        for lineid in self.busses:
            for busid in self.busses[lineid]:
                bus_status = self.busses[lineid][busid]
                if bus_status[1] :
                    msg = f"The bus number {busid} that belongs to line with id {lineid}"
                    msg += f" has currently {bus_status[3]} passengers. "
                    msg += f"The number of passengers that got out of the bus is {bus_status[5]}. "
                    msg += f"The number of passengers that got into the bus is {bus_status[4]}\n"
                    bus_status[4] = 0
                    bus_status[5] = 0
                    self.user.notify(msg)

    def initalize_busses(self):
        for lineid in self.busses:
            stops_data = self.schedule.get_line_stops_data(lineid)
            trips_times = self.schedule.get_journey_times(lineid)
            for tripid in range(len(trips_times)):
                self.busses[lineid][tripid+1] = [trips_times[tripid],False, 0, 0, 0, 0, stops_data]
                

    def update_busses(self):
        for lineid in self.busses:
            for busid in self.busses[lineid]:
                if self.busses[lineid][busid][0] == self.curr_time:
                    self.busses[lineid][busid][1] = True
                    msg = f"Bus number {busid} that belongs to line with id {lineid} has depatured at {self.curr_time}\n"
                    self.user.notify(msg)
                    self.trips_num += 1

                if self.busses[lineid][busid][6][-2][2] + self.busses[lineid][busid][0] < self.curr_time and self.busses[lineid][busid][1] == True:
                    print(self.busses[lineid][busid][6])
                    self.busses[lineid][busid][1] = None
                    msg = f"Bus number {busid} that belongs to line with id {lineid} has arrived its final stop at {self.curr_time}\n"
                    self.user.notify(msg)                    

    def update_passengers(self):
        with self.mutex:
            for lineid in self.schedule.get_lines():
                # print(f"line {lineid}'s wait {self.waiting[lineid]}")
                for passenger in self.waiting[lineid]:
                    # print("Processign passenger")
                    # print(lineid, passenger[1])
                    bus_at_stop = self.schedule.is_bus_at_stop(lineid, passenger[1], self.curr_time)
                    if bus_at_stop[1] and self.busses[lineid][bus_at_stop[0]][1]:
                        # print("Entering the buss")
                        # print("THE CUREEEEEENT TIME IS ", self.curr_time)
                        self.busses[lineid][bus_at_stop[0]][2] += 1
                        self.busses[lineid][bus_at_stop[0]][3] += 1
                        self.busses[lineid][bus_at_stop[0]][4] += 1

                        in_bus_time , start_waiting_time= passenger[0].bus_came()
                        self.wait_times.append(self.curr_time - start_waiting_time)

                        self.waiting[lineid].remove(passenger)
                        self.in_bus[lineid].append(
                            (passenger[0], in_bus_time + self.curr_time, bus_at_stop[0])
                        )

                        # print("The current state of waiting is ", self.waiting)
                        # print("The current state of in bus is ", self.in_bus)

                for passenger in self.in_bus[lineid]:
                    if self.curr_time > passenger[1]:
                        self.busses[lineid][passenger[2]][3] -= 1
                        self.busses[lineid][passenger[2]][5] += 1
                        passenger[0].bus_arrived()
                        self.in_bus[lineid].remove(passenger)



    def add_to_waiting(self, passenger, line, start_stop):
        with self.mutex:
            self.waiting[line.lineid].append((passenger, start_stop))
            return self.curr_time

    def passenger_generator(self):
        for i in range(3000):
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
        avg_time = 0
        for t in self.wait_times:
            avg_time += t

        avg_time = avg_time / len(self.wait_times)

        avg_passengers = 0
        for lineid in self.busses:
            for busid in self.busses[lineid]:
                avg_passengers += self.busses[lineid][busid][2]
        avg_passengers = avg_passengers / self.trips_num

        total_distance = 0
        for lineid in self.busses:
            for busid in self.busses[lineid]:
                bus = self.busses[lineid][busid]
                if bus[1] == None:
                    total_distance += self.schedule.get_line_distance(lineid)
                elif bus[1] == True:
                    curr_stop = None
                    for stop in bus[6]:
                        if bus[0] + stop[1] > self.curr_time:
                            curr_stop = stop[0]
                            break

                    total_distance += self.schedule.get_line_distance_until_stop(lineid, curr_stop)

        
        return f"The average wait time of passengers is {avg_time}. The average number of passengers is {avg_passengers}. The total distance covered by busses is {total_distance}\n"



# lines {
#     lineid: [(passenger, stopid)]
# }
