import cmd
from Map import Map
from Scheduale import Schedule
from BusSys import BusSys
from User import User


class Sys(cmd.Cmd):
    intro = "Welcome to busSys. The power of bus simulation is here\n"
    prompt = "(busSys)$: "
    schedule = None

    def do_wtf(self, args):
        print("wtf is a word used be people for expressing internail feelings of wtf")

    def do_login(self, args):
        global sechedule
        user = User("test", "test", "test")
        user.login()
        Sys.schedule = busSys.get_schedule(user)

    def do_map_test(self, args):
        print("Tesing map Functionalities")
        temp = my_map.shortest(1, 2)
        if temp[0] == [1]:
            print("Shortest is fine")
        else:
            print("Shortest has a problem")
            print(temp)

    def do_print_stops(self, args):
        stops = Sys.schedule.get_stops()
        for stop in stops:
            print(str(stops[stop]))

    def do_add_stop(self, args):
        ar = args.split(" ")
        Sys.schedule.add_stop(int(ar[0]), bool(ar[1]), int(ar[2]), ar[3])


if __name__ == "__main__":
    map_path = "./test/test_map.json"
    my_map = Map(path=map_path)
    busSys = BusSys(my_map)
    Sys().cmdloop()
