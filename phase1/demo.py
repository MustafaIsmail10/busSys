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

        # Adding push of routes and stops to test with
        Sys.schedule.add_stop(1, True, 50, "Hola")
        Sys.schedule.add_stop(2, True, 50, "Hola")
        Sys.schedule.add_stop(3, True, 50, "Hola")
        Sys.schedule.add_stop(4, True, 50, "Hola")
        Sys.schedule.add_stop(5, True, 50, "Hola")
        Sys.schedule.add_stop(6, True, 50, "Hola")


        Sys.schedule.add_route()
        Sys.schedule.add_route()
        Sys.schedule.add_route()

        Sys.schedule.add_stop_to_route(1, 1, 5)
        Sys.schedule.add_stop_to_route(1, 2, 5)
        Sys.schedule.add_stop_to_route(1, 4, 5)
        Sys.schedule.add_stop_to_route(1, 5, 5)

        Sys.schedule.add_stop_to_route(2, 1, 5)
        Sys.schedule.add_stop_to_route(2, 5, 5)
        Sys.schedule.add_stop_to_route(2, 4, 5)
        Sys.schedule.add_stop_to_route(2, 2, 5)

        Sys.schedule.add_stop_to_route(3, 2, 5)
        Sys.schedule.add_stop_to_route(3, 4, 5)
        Sys.schedule.add_stop_to_route(3, 3, 5)


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

    def do_add_route(self, args):
        new_route_id = Sys.schedule.add_route()
        print(f"The new route id is {new_route_id}")

    def do_print_route_info(self, args):
        route = Sys.schedule.get_route(int(args))
        print(route)

    def do_print_all_routes(self, args):
        routes = Sys.schedule.get_routes()
        for route in routes:
            print(routes[route])

    def do_add_stop_to_route (self, args):
        ar = args.split(" ")
        Sys.schedule.add_stop_to_route(int(ar[0]),int(ar[1]), int(ar[2]))

    def do_remove_stop(self, args):
        Sys.schedule.remove_stop(int(args))



if __name__ == "__main__":
    map_path = "./test/test_map.json"
    my_map = Map(path=map_path)
    busSys = BusSys(my_map)
    Sys().cmdloop()
