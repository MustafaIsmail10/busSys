import cmd
from Map import Map
from Scheduale import Schedule
from BusSys import BusSys
from User import User
from Route import Route


class Sys(cmd.Cmd):
    intro = "Welcome to busSys. The power of bus simulation is here\n"
    prompt = "(busSys)$: "
    schedule = None

    def do_login(self, args):
        """
        This funcion is used to log you into the system and loads the map and add some stops, routes, and lines
        ex
        login
        """
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

        Sys.schedule.addline("Blue Line", 50, 1000, 20, 1, "a Ring")
        Sys.schedule.addline("Green Line", 100, 1300, 30, 3, "a Ring")
        Sys.schedule.addline("Red Line", 50, 1200, 15, 2, "a Ring")

    def do_map_test(self, args):
        print("Tesing map Functionalities")
        temp = my_map.shortest(1, 2)
        if temp[0] == [1]:
            print("Shortest is fine")
        else:
            print("Shortest has a problem")
            print(temp)

        loc1 = {"x": 34, "y": 44}
        closest_edge = my_map.closestedge(loc1)
        if closest_edge[0] == 5:
            print("correct edge")
        else:
            print("incorrect edge")
            print(closest_edge)

        loc2 = {"x": 20, "y": 35}
        closest_edge = my_map.closestedge(loc2)
        if closest_edge[0] == 3:
            print("correct edge")
        else:
            print("incorrect edge")
            print(closest_edge)

        loc3 = {"x": 70, "y": 40}
        closest_edge = my_map.closestedge(loc3)
        if closest_edge[0] == 7:
            print("correct edge")
        else:
            print("incorrect edge")
            print(closest_edge)

        stop1 = my_map.addstop(1, True, 20, "cafe")
        print(stop1)
        stop2 = my_map.addstop(4, False, 50, "isbank")
        print(stop2)
        stop3 = my_map.addstop(6, True, 20, "park")
        print(stop3)
        stop4 = my_map.addstop(9, False, 80, "pluto")
        print(stop4)
        my_map.delstop(1)
        # my_map.delstop(3)
        # my_map.delstop(5) # raises exception
        print(my_map.getstop(2))
        # print(my_map.getstop(1)) raises exception
        print(my_map.stoptimeDistance(2, 3))
        print(my_map.stoptimeDistance(2, 4))
        # print(my_map.stoptimeDistance(1,3)) #raises error
        # print(my_map.bus_stops[1]) #key error
        print(my_map.bus_stops[2])
        print(my_map.bus_stops[3])
        print(my_map.bus_stops[4])
        print(my_map.shorteststop(loc1))
        print(my_map.shorteststop(loc2))
        print(my_map.shorteststop(loc3))

    def do_route_test(self, args):
        print("Tesing route Functionalities")
        route = Route(my_map)
        # without the following stops, route's get_stop_data wont work.
        # stops should be already in map given this implementation
        stop1 = my_map.addstop(1, True, 20, "cafe")
        print(stop1)
        stop2 = my_map.addstop(4, False, 50, "isbank")
        print(stop2)
        stop3 = my_map.addstop(6, True, 20, "park")
        print(stop3)
        stop4 = my_map.addstop(9, False, 80, "pluto")
        print(stop4)
        stop5 = my_map.addstop(3, False, 40, "civil eng")
        print(stop5)
        print("------")
        route.add_stop(1, 2)
        route.add_stop(2, 2)
        route.add_stop(3, 4)
        route.add_stop(4, 4)
        route.add_stop(5, 1)
        print(route.start)
        print(route.get_stops())
        print(route.get_stops_data())
        route.change_stop_order(1, 5)
        print("changed stop 5")
        print(route.get_stops())
        print(route.get_stops_data())
        route.set_start(5)
        print(route.start)
        route.set_start(4)
        print(route.start)
        route.change_wait(3, 1)
        print(route.get_stops())
        print(route.get_stops_data())
        print(route.get_time())
        print(route.get_distance(my_map))

    def do_print_stops(self, args):
        """
        This command is used to print all stops
        ex
        print_stops
        """
        stops = Sys.schedule.get_stops()
        for stop in stops:
            print(str(stops[stop]))

    def do_add_stop(self, args):
        """
        This command is used to add a new stop 
        ex
        add_stop edgeid directoin percentage "description"
        """
        ar = args.split(" ")
        Sys.schedule.add_stop(int(ar[0]), bool(ar[1]), int(ar[2]), ar[3])

    def do_del_stop(self, args):
        """
        This command is used to delete a stop
        ex
        del_stop stopid
        """
        Sys.schedule.remove_stop(int(args))

    def do_add_route(self, args):
        """
        This command is used to add a new empty route to the system
        ex
        add_route
        """
        new_route_id = Sys.schedule.add_route()
        print(f"The new route id is {new_route_id}")

    def do_print_route_info(self, args):
        """
        This command is used to print route info taking the routeid as input
        ex
        print_route_info routeid
        """
        route = Sys.schedule.get_route(int(args))
        print(route)

    def do_print_routes(self, args):
        """
        This command is used to print all routes of the system
        ex
        print_routes
        """
        routes = Sys.schedule.get_routes()
        for route in routes:
            print(routes[route])

    def do_add_stop_to_route(self, args):
        """
        This command is used to a stop to a specific route
        ex
        add_stop_to_route routeid stop_id wait_time
        """
        ar = args.split(" ")
        Sys.schedule.add_stop_to_route(int(ar[0]), int(ar[1]), int(ar[2]))

    def do_del_stop_from_route(self, args):
        """
        This command is used to remove a stop from a specific route
        ex
        del_stop_from_route routeid stop_id 
        """
        ar = args.split(" ")
        Sys.schedule.del_stop_from_route(int(ar[0]), int(ar[1]))

    def do_change_stop_wait(self, args):
        """
        This command is used to change the wait time of a stop insied a route
        ex
        change_stop_time routeid stopid wait_time
        """
        ar = args.split(" ")
        Sys.schedule.change_stop_wait(int([ar[0]]), int(ar[1]), int(ar[2]))

    def do_del_stop(self, args):
        """
        This command is used to remove a stop from the system
        ex
        del_stop stop_id 
        """
        Sys.schedule.del_stop(int(args))


    def do_add_line(self, args):
        """
        This command is used to add a line to the system
        ex
        add_line name start_time end_time time_between_trips routeid "description"
        """
        ar = args.split(" ")
        Sys.schedule.addline(
            ar[0], int(ar[1]), int(ar[2]), int(ar[3]), int(ar[4]), int(ar[5])
        )

    def do_print_lines(self, args):
        """
        This command is used to print all line of the system
        ex
        print_lines
        """
        lines = Sys.schedule.get_lines()
        for line in lines:
            print(str(lines[line]))


    def do_del_line(self, args):
        """
        This command is used to delete line from the system
        ex
        del_line lineid
        """
        Sys.schedule.del_line(int(args))

    def do_update_line_name(self, args):
        """
        This command is used to update line name
        ex 
        update_line_name lineid new_name
        """
        ar = args.split(" ")
        Sys.schedule.update_line_name(int(ar[0]), ar[1])

    def do_update_line_start_time(self, args):
        """
        This command is used to update line start time
        ex 
        update_line_start_time lineid new_start_time
        """
        ar = args.split(" ")
        Sys.schedule.update_line_start_time(int(ar[0]), int(ar[1]))



    def do_update_line_end_time(self, args):
        """
        This command is used to update line end time
        ex 
        update_line_end_time lineid new_end_time
        """
        ar = args.split(" ")
        Sys.schedule.update_line_end_time(int(ar[0]), int(ar[1]))


    def do_update_line_time_between_trips(self, args):
        """
        This command is used to update line start time
        ex 
        update_line_time_between_trip lineid time_between_trips
        """
        ar = args.split(" ")
        Sys.schedule.update_line_time_between_trips(int(ar[0]), int(ar[1]))


    def do_update_line_description(self, args):
        """
        This command is used to update line start time
        ex 
        update_line_description lineid "description"
        """
        ar = args.split(" ")
        Sys.schedule.update_line_start_time(int(ar[0]), ar[1])


    def do_get_stop_info(self, args):
        """
        This commnand return infomation about a stop
        ex
        get_stop_info stopid
        """
        data = Sys.schedule.stopinfo(int(args))
        print(str(data[0]))
        print(data[1])


    def do_get_line_info(self, args):
        """
        This commnand return infomation about a line
        ex
        get_line_info lineid
        """
        data = Sys.schedule.lineinfo(int(args))
        print(data)


if __name__ == "__main__":
    map_path = "./test/test_map.json"
    my_map = Map(path=map_path)
    busSys = BusSys(my_map)
    Sys().cmdloop()
